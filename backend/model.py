import tensorflow as tf
import matplotlib.pyplot as plt
import PIL
import io
import base64

from keras.models import *
from PIL import Image
import numpy as np


def normalize(data):
    # takes a list ot a list of lists and returns its normalized form
    return np.interp(data, [0, 255], [-1, 1])


class DrawModel:

    def __init__(self, path) -> None:
        self.path = path
        self.model = tf.keras.models.load_model(self.path)
        self.categories = {0: "Apple", 1: "Banana", 2: "Grape", 3: "Pineapple"}

    def predict(self, image_data):
        image = PIL.Image.open(io.BytesIO(base64.b64decode(
            image_data.removeprefix(b"data:image/png;base64,"))))

        # Create a white rgba background
        new_image = Image.new("RGBA", image.size, "WHITE")
        # Paste the image on the background. Go to the links given below for details.
        new_image.paste(image, (0, 0), image)
        new_image.convert('RGB').save('test.jpg', "JPEG")  # Save as JPEG

        image = new_image.convert("L")
        image = image.resize((28, 28))
        image = np.array(image)

        print(type(image))

        # Transform the image
        image = np.expand_dims(image, axis=0)
        image = np.invert(image)

        # Get Dimensions
        # print(f"(RAW) Image Input Dimensions: {image_raw.shape}")
        # print(f"Image Input Dimensions: {image.shape}")
        # print(f"Model Input Dimensions: {self.model.input_shape}")

        # # image = normalize(list(image))
        # # plt.imshow(image)
        # # plt.show()
        # print(image)
        # print(image.shape)
        # # image = image.reshape(1, 28, 28, 1)
        # # plt.imshow(image)
        # # plt.show()

        # Make Prediction
        predictions = self.model.predict(image)
        print(f">> Confidence Scores: {predictions}")
        predictions_raw = predictions[0]
        predictions = self.categories[np.argmax(predictions)]
        print(predictions)
        print("\n"*10)
        predictions_data = {}
        for i in range(len(self.categories) - 1):
            predictions_data[self.categories[i]] = predictions_raw[i]
        return predictions
