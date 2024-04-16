const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

// MongoDB connection URI
const mongoURI = 'mongodb+srv://hekiga1032:nEU@n$Nz94frw6H@cluster0.lhyfsaa.mongodb.net/';

// Connect to MongoDB
mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true });

// Define location schema
const locationSchema = new mongoose.Schema({
    latitude: Number,
    longitude: Number
});
const Location = mongoose.model('Location', locationSchema);

const app = express();
app.use(bodyParser.json());

// Endpoint to save location
app.post('/saveLocation', (req, res) => {
    const latitude = req.body.latitude;
    const longitude = req.body.longitude;

    const newLocation = new Location({
        latitude: latitude,
        longitude: longitude
    });

    newLocation.save()
        .then(() => res.status(200).send('Location saved successfully'))
        .catch(err => res.status(500).send('Error saving location: ' + err));
});

// Endpoint to fetch all locations
app.get('/getLocations', (req, res) => {
    Location.find()
        .then(locations => res.status(200).json(locations))
        .catch(err => res.status(500).send('Error fetching locations: ' + err));
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));
