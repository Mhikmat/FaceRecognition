# Import kivy dependencies first
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

# Other dependencies
import cv2
import tensorflow as tf
from layers import L1Dist
import os
import numpy as np
import requests
from flask import Flask, request
import threading

# Setup Flask
flask_app = Flask(__name__)

class CamApp(App):

    def build(self):
        # Main layout
        self.web_cam = Image(size_hint=(1, .8))
        self.button = Button(text="Verify", on_press=self.verify, size_hint=(1, .1))
        self.verification_label = Label(text="Verification Uninitiated", size_hint=(1, .1))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification_label)

        # Load model
        self.model = tf.keras.models.load_model('model.keras', custom_objects={'L1Dist': L1Dist})

        # Video capture
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 33.0)

        return layout

    def update(self, *args):
        ret, frame = self.capture.read()
        frame = frame[120:120+250, 200:200+250, :]

        buf = cv2.flip(frame, 0).tobytes()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.web_cam.texture = img_texture

    def preprocess(self, file_path):
        byte_img = tf.io.read_file(file_path)
        img = tf.io.decode_jpeg(byte_img)
        img = tf.image.resize(img, (100, 100))
        img = img / 255.0
        return img

    def verify(self, *args):
        detection_threshold = 0.99
        verification_threshold = 0.8

        SAVE_PATH = os.path.join('application_data', 'input_image', 'input_image.jpg')
        ret, frame = self.capture.read()
        frame = frame[120:120+250, 200:200+250, :]
        cv2.imwrite(SAVE_PATH, frame)

        results = []
        for image in os.listdir(os.path.join('application_data', 'verification_images')):
            input_img = self.preprocess(SAVE_PATH)
            validation_img = self.preprocess(os.path.join('application_data', 'verification_images', image))
            result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
            results.append(result)

        detection = np.sum(np.array(results) > detection_threshold)
        verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images')))
        verified = verification > verification_threshold

        self.verification_label.text = 'Verified' if verified else 'Unverified'

        Logger.info(f"Results: {results}")
        Logger.info(f"Detection count: {detection}")
        Logger.info(f"Verification score: {verification}")
        Logger.info(f"Verified: {verified}")

        # Send webhook to Home Assistant
        try:
            if verified:
                url = 'http://homeassistant.local:8123/api/webhook/faceid_verified'
                Logger.info("Sending 'Verified' webhook to Home Assistant.")
            else:
                url = 'http://homeassistant.local:8123/api/webhook/faceid_unverified'
                Logger.info("Sending 'Unverified' webhook to Home Assistant.")

            response = requests.post(url)
            if response.status_code == 200:
                Logger.info("Webhook sent successfully.")
            else:
                Logger.warning(f"Webhook failed. Status code: {response.status_code}")
        except Exception as e:
            Logger.error(f"Error sending webhook: {e}")

        return results, verified

# Now define the Flask webhook to trigger the verify
@flask_app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("Received webhook data:", data)
    if data and data.get('status') == 'scan':
        print("Triggering verification from webhook...")
        app_instance = App.get_running_app()
        app_instance.verify()
    return 'OK', 200

def start_flask():
    flask_app.run(port=5000)

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()  # Start Flask in background
    CamApp().run()
