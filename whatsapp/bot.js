const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();

app.use(express.json());

const client = new Client({
    puppeteer: {
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
    webVersionCache: {
        type: 'remote',
        remotePath: 'https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/2.2412.54.html',
    },
});

let qrCode = '';

client.on('qr', (qr) => {
    qrCode = qr;
    qrcode.generate(qr, { small: true });
    console.log('QR code received, scan please!');
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', msg => {
    console.log(`Message from ${msg.from}: ${msg.body}`);
});

client.initialize().catch(error => {
    console.error('Failed to initialize the client:', error);
});

// Endpoint to get QR code
app.get('/qr', (req, res) => {
    if (qrCode) {
        res.status(200).send(`<img src="https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(qrCode)}&size=200x200" alt="QR Code" />`);
    } else {
        res.status(200).send('QR code not generated yet. Please wait.');
    }
});

// Home page endpoint
app.get('/', (req, res) => {
    res.status(200).send('This is the Node API');
});

app.post('/send', (req, res) => {
    const { number, message } = req.body;
    client.sendMessage(number, message).then(response => {
        res.status(200).json({ status: 'success', response });
    }).catch(err => {
        res.status(500).json({ status: 'error', error: err });
    });
});

app.get('/messages', (req, res) => {
    // Implement fetching messages from the client
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
