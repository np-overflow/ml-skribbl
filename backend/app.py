from flask import Flask, request, send_file
import os
import datetime
import base64
from PIL import Image
from model import DrawModel
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

category = "test"


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/transform", methods=["POST"])
@cross_origin()
def transform():
    if not os.path.exists("drawings/"):
        os.mkdir("drawings")

    image_data = request.get_data(
        "image_data").removeprefix(b"data:image/png;base64,")

    current_timestring = datetime.datetime.now().strftime("%d%m%y%H%M%S")
    image_name = f"{current_timestring}-{category}.png"

    image_path = os.path.join("drawings", image_name)

    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_data))

    image = Image.open(image_path).resize((28, 28))
    image.save(image_path)

    return send_file(image_path)


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    image_data = request.get_data(
        "image_data")
    print(image_data)
    model = DrawModel("models/fruits.h5")
    model.predict(image_data)
    return "OK!"


@app.route("/purge")
@cross_origin()
def purge():
    for file in os.listdir("drawings/"):
        os.remove(f"drawings/{file}")
    return "Purged"


if __name__ == '__main__':
    app.run(debug=True)
