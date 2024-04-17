function submitForm() {
    const data = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        house_address: document.getElementById('house_address').value,
        ip: getIP()
    };

    fetch('/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    alert('Your data has been logged.');
}

function getIP() {
    const response = fetch('https://api.ipify.org?format=json');
    return response.then(response => response.json()).then(json => json.ip);
}
