const express = require('express');
const request = require('request'); // HTTPS Requests

const app = express();
const PORT  = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`>> http://localhost:${PORT}`);
});

var Base64Img = ""
var isDetected = false;
var object = ""


// POST (Send) Image
// -- Note: Body JSON Request = ["imgString"]
app.post('/image', (req, res) => {
    console.log(`>> Recieved Image`);
    Base64Img = req.body[0];
    res.status(200).send({
        "image" : Base64Img,
        "status" : "Success"
    });
});

// GET (Retrieve) Image
app.get('/image', (req, res) => {
    console.log(">> Requested: Sent")
    res.status(200).send({
        "image" : Base64Img,
        "status" : "Success"
    });
});


// Detection trigger
// -- After image is sent to the detection python script, it will send a reuqest to the API to let the front end know that detection is completed
app.post('/detect', (req, res) => {
    console.log(`>> Detection Completed`);
    isDetected = true;
    object = req.body["object"];

    res.status(200).send({
        "status" : isDetected,
        "object" : object
    });
});


app.get('/detect', (req, res) => {
    console.log(`>> Detection Requested`);

    if (isDetected) {
        res.status(200).send({
            "isDetected" : isDetected,
            "object" : object
        });
        isDetected = false;
    }
    else {
        res.status(200).send({
            "isDetected" : isDetected
        });
    }
});