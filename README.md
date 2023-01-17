# ml-skribbl

This repository contains the source code for Overflow's ML Skribbl game, presented during Ngee Ann Polytechnic's 2023 Open House. This project was made using Svelte for the front-end, Flask for the back-end, and Keras (TensorFlow) for the model training.

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
