# Machine Learning Skribbl Game

This repository contains the source code for Overflow's ML Skribbl game, presented during Ngee Ann Polytechnic's 2023 Open House. This project was made using Svelte for the front-end, Flask for the back-end, and Keras (TensorFlow) for the model training.

## Convolutional Neural Network (CNN)

The model architecture used for this project is a Convolutional Neural Network (CNN), which is designed to process image data efficiently and effectively. The CNN architecture consists of several layers:

![image](https://github.com/np-overflow/ml-skribbl/assets/105436607/8565387a-67c8-4250-96e9-d881c5567d5d)

1. **Input Layer**: The input images are resized to 64x64 pixels and have a single channel (black and white).
2. **Convolutional Layers**: The CNN starts with two convolutional layers with 32 filters each, followed by max-pooling layers to downsample the feature maps.
3. **More Convolutional Layers**: Additional convolutional layers with 64 and 128 filters are added, each followed by max-pooling layers.
4. **Flattening Layer**: After the convolutional layers, the feature maps are flattened into a one-dimensional array.
5. **Dense Layers**: Fully connected dense layers are added with 128 units each, followed by a final dense layer with 256 units, and an output layer with softmax activation to predict the category of the input image.
6. **Dropout**: Although not included in the final architecture, dropout layers can be added to prevent overfitting during training.

The model is compiled using the categorical cross-entropy loss function and the Adam optimizer.

## Setting up

There are two components that need to be set up independently. They are located in two separate folders — `backend/` and `frontend/` respectively.

### Back end setup

0. Ensure that you have a version of Python installed.

1. Change your current working directory to `backend/`:
	```sh
	cd backend
	```

2. Install package dependencies using pip:
	```sh
	pip3 install -r requirements.txt
	```

3. Run and start the Flask server:
	```sh
	python3 app.py
	```

### Front end setup

0. Ensure that you have Node.js installed along with npm. Optionally, [enable Corepack and install pnpm](https://pnpm.io/installation).

1. Change your current working directory to `frontend/`:
	```sh
	cd frontend
	```

2. Install package dependencies using your Node package manager:
	```sh
	pnpm i
	# or
	npm install
	# or
	yarn
	```

3. Run and start the SvelteKit app:
	```sh
	pnpm start dev
	# or
	npm start dev
	# or 
	yarn start dev
	```

### Model training

We used a Jupyter Notebook to handle the training and creation of the machine learning model used in this project. The Notebook can be accessed under `backend/utils/model-gen.ipynb`. If you have a local installation of Jupyter, you can use that to open and view the contents of the Notebook. Otherwise, cloud installations like [Google Colaboratory](https://colab.research.google.com) can help, too!

## Acknowledgements

We've scouted a lot of resources when researching more about creating a machine learning model. We acknowledge and thank the following for their resources:

- [FreeBirdsCrew](https://github.com/FreeBirdsCrew/Google_QuickDraw_Implementation)
- [martinohanlon](https://github.com/martinohanlon/quickdraw_python)
- [nicknochnack](https://github.com/nicknochnack/ImageClassification)

## License

This project is made open source with the MIT License. View more details about the license at LICENSE.md.
