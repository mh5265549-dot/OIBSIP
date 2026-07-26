require('dotenv').config();
const dns = require('dns');
dns.setServers(['8.8.8.8', '1.1.1.1']);

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

const inventorySchema = new mongoose.Schema({
    name: String,
    quantity: Number,
    category: String,
    price: Number
});
const Inventory = mongoose.model('Inventory', inventorySchema);

app.get('/api/inventory', async (req, res) => {
    try {
        const items = await Inventory.find();
        res.json(items);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 5000;

console.log("Loaded URI:", process.env.MONGO_URI);

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('Connected to MongoDB successfully!'))
  .catch(err => console.error('DATABASE CONNECTION ERROR:', err.message));
