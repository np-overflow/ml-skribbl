from flask import Flask, request, send_file
import os
import datetime
import base64
from PIL import Image
from model import DrawModel

app = Flask(__name__)
category = "test"


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/transform", methods=["POST"])
def transform():
    if not os.path.exists("drawings/"):
        os.mkdir("drawings")

    image_data = request.get_data(
        "image_data").removeprefix(b"data:image/png;base64,")

    current_timestring = datetime.datetime.now().strftime("%d%m%y%H%M%S")
    image_name = f"{current_timestring}-{category}.png"

    with open(f"drawings/{image_name}", "wb") as f:
        f.write(base64.b64decode(image_data))

    image = Image.open(f"drawings/{image_name}").resize((28, 28))
    image.save(f"drawings/{image_name}")

    return send_file(f"drawings/{image_name}")


@app.route("/predict", methods=["POST"])
def predict():
    image_data = request.get_data(
        "image_data")
    print(image_data)
    model = DrawModel("models/fruits.h5")
    model.predict(image_data)
    return "OK!"


@app.route("/purge")
def purge():
    for file in os.listdir("drawings/"):
        os.remove(f"drawings/{file}")
    return "Purged"


if __name__ == '__main__':
    app.run(debug=True)
