import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import PIL
import io
import base64


def normalize(data):
    # takes a list ot a list of lists and returns its normalized form
    return np.interp(data, [0, 255], [-1, 1])


class DrawModel:
    def __init__(self, path) -> None:
        self.path = path
        self.model = tf.keras.models.load_model(self.path)

    def predict(self, image_data):
        # Use PIL to convert the image to a grayscale 28x28 image
        image = PIL.Image.open(io.BytesIO(base64.b64decode(
            image_data.removeprefix(b"data:image/png;base64,"))))
        image = np.asarray(image)
        image = normalize(list(image))
        # plt.imshow(image)
        # plt.show()
        print(image)
        print(image.shape)
        # image = image.reshape(1, 28, 28, 1)
        # plt.imshow(image)
        # plt.show()
        predictions = self.model.predict(image)[0]
        print(predictions)
        return predictions
