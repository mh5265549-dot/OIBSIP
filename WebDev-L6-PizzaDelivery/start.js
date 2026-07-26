const dns = require('dns');
// Use Google Public DNS to reliably resolve MongoDB Atlas SRV records
dns.setServers(['8.8.8.8', '8.8.4.4']);

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

// Define Schema & Model safely
const inventorySchema = new mongoose.Schema({
    name: String,
    quantity: Number,
    category: String,
    price: Number
});
const Inventory = mongoose.model('Inventory', inventorySchema);

// Test Route
app.get('/api/inventory', async (req, res) => {
    try {
        const items = await Inventory.find();
        res.json(items);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 5000;

// Connect to DB FIRST, using IPv4 family setting
mongoose.connect(process.env.MONGO_URI, {
    family: 4,
    serverSelectionTimeoutMS: 10000
})
    .then(() => {
        console.log('SUCCESS: Connected to MongoDB Atlas!');
        app.listen(PORT, () => {
            console.log(`Server is running smoothly on port ${PORT}`);
        });
    })
    .catch((err) => {
        console.error('DATABASE CONNECTION ERROR:', err.message);
        if (err.message.includes('querySrv ECONNREFUSED')) {
            console.error('DNS SRV Resolution Failed. Ensure your network allows DNS queries to port 53 or check MongoDB Atlas IP access list.');
        }
    });
