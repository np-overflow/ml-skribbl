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
        self.categories = {
            0: "Calculator",
            1: "Camera",
            2: "Computer",
            3: "Headphones",
            4: "Mouse",
            5: "Telephone",
        }

    def predict(self, image_data):
        image = PIL.Image.open(io.BytesIO(base64.b64decode(
            image_data.removeprefix(b"data:image/png;base64,"))))

        # Creates a new image with a white background using the RGBA mode.
        new_image = Image.new("RGBA", image.size, "WHITE")
        # Pastes the user-drawn image on the background. Go to the links given below for details.
        new_image.paste(image, (0, 0), image)

        image = new_image.convert("L")
        image = image.resize((28, 28))
        image = np.array(image)

        # Transforms the image to fit the model.
        image = np.expand_dims(image, axis=0)
        image = np.invert(image)

        # Makes a prediction using the model.
        predictions = self.model.predict(image)
        print(f">> Confidence Scores: {predictions}")
        predictions_raw = predictions[0]
        predictions = self.categories[np.argmax(predictions)]
        print(predictions)
        predictions_data = {}
        for i in range(len(self.categories) - 1):
            predictions_data[self.categories[i]] = predictions_raw[i]
        return predictions
