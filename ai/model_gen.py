from sklearn.model_selection import train_test_split as train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.utils import to_categorical
from random import randint
import numpy as np
import os
from PIL import Image

# Creates a dictionary with all the categories.
CATEGORIES = {
    0: "Calculator",
    1: "Camera",
    2: "Computer",
    3: "Headphones",
    4: "Mouse",
    5: "Telephone",
}
N_CATEGORIES = len(CATEGORIES)

# Defines the number of drawings per category to take in.
N = 7500

# Defines the number of epochs (iterations of training) the model will undergo.
N_EPOCHS = 10

# The files to learn from. They MUST match the information in CATEGORIES for proper classification.
files = ["calculator.npy", "camera.npy", "computer.npy",
         "headphones.npy", "mouse.npy", "telephone.npy"]


def load(dir, reshaped, files):
    # Takes the .npy files and return them as arrays.
    data = []
    for file in files:
        f = np.load(dir + file)
        if reshaped:
            new_f = []
            for i in range(len(f)):
                x = np.reshape(f[i], (28, 28))
                x = np.expand_dims(x, axis=0)
                x = np.reshape(f[i], (28, 28, 1))
                new_f.append(x)
            f = new_f
        data.append(f)
    return data


def normalize(data):
    # Takes a list ot a list of lists and returns its normalized form.
    return np.interp(data, [0, 255], [-1, 1])


def denormalize(data):
    # Takes a list ot a list of lists and returns its denormalized form.
    return np.interp(data, [-1, 1], [0, 255])


def visualize(array):
    # Visualizes a 2D array as an Image.
    array = np.reshape(array, (28, 28))
    img = Image.fromarray(array)
    return img


def set_limit(arrays, n):
    # Limits the elements from each array up to the nth element and returns a single list.
    new = []
    for array in arrays:
        i = 0
        for item in array:
            if i == n:
                break
            new.append(item)
            i += 1
    return new


def make_labels(N1, N2):
    # Make labels from 0 to N1, each repeated N2 times.
    labels = []
    for i in range(N1):
        labels += [i] * N2
    return labels


# Loads the content into /content/data/ while reshaping images to 28 x 28 (second True argument). A ConvNet expects this format.
images = load("data/", True, files)

images = set_limit(images, N)
# Normalizes the values and makes the values -1 to 1. This ensures better performance of the model.
images = list(map(normalize, images))

labels = make_labels(N_CATEGORIES, N)

# Reserves 5 percent of the dataset for training purposes only (test_size) and splits the data into training and testing datasets.
x_train, x_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.05)

# Performs one-hot encoding.
Y_train = to_categorical(y_train, N_CATEGORIES)
Y_test = to_categorical(y_test, N_CATEGORIES)

# Creating the ConvNet, adding a process each step of the way.
model = Sequential()

# The input shape is 28 x 28 because of the image size, and 1 is due to it being black and white image (1 channel instead of 3 channels for RGB).
model.add(Conv2D(32, kernel_size=(3, 3),
          activation="relu", input_shape=(28, 28, 1)))
model.add(Conv2D(64, (3, 3), activation="relu"))

# A resizing kind of error. Simplified image.
model.add(MaxPooling2D(pool_size=(2, 2)))

# Dropout layers ensure that we are not overfitting the model.
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))

# The N_CATEGORIES is present because we want the number of nodes to be the same as the number of categories.
model.add(Dense(N_CATEGORIES, activation="softmax"))

# Compiles and trains the model; the fit() function is the most important in actually creating the model.
model.compile(loss="categorical_crossentropy",
              optimizer="adam", metrics=["accuracy"])
model.fit(np.array(x_train), np.array(Y_train), batch_size=32, epochs=N_EPOCHS)
print("Training complete")

# Evaluates the performance of the model by passing a test image into it.
print("Evaluating model")
preds = model.predict(np.array(x_test))

# Calculates an accuracy score and displays it.
score = 0
for i in range(len(preds)):
    if np.argmax(preds[i]) == y_test[i]:
        score += 1
print("Accuracy:", ((score + 0.0) / len(preds)) * 100)

# Saves the model as a Keras H5 (.h5) file.
model.save("out/temp.keras")
print("Model saved")
