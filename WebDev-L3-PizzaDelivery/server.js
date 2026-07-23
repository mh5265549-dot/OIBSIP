const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cron = require('node-cron');
const nodemailer = require('nodemailer');
const Razorpay = require('razorpay');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('MongoDB Connected')).catch(err => console.log(err));

// --- SCHEMAS & MODELS ---
const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    isAdmin: { type: Boolean, default: false }
});
const User = mongoose.model('User', userSchema);

const inventorySchema = new mongoose.Schema({
    itemName: String,
    category: String, // base, sauce, cheese, vegetable
    stock: Number,
    threshold: Number
});
const Inventory = mongoose.model('Inventory', inventorySchema);

const orderSchema = new mongoose.Schema({
    userEmail: String,
    pizzaDetails: Object,
    amount: Number,
    status: { type: String, default: 'Order Received' }, // Order Received -> In Kitchen -> Sent to Delivery
    createdAt: { type: Date, default: Date.now }
});
const Order = mongoose.model('Order', orderSchema);

// Razorpay Setup
const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID || 'rzp_test_dummy',
    key_secret: process.env.RAZORPAY_KEY_SECRET || 'dummy_secret'
});

// Nodemailer Setup for Low Stock Alerts
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

// Cron Job: Check inventory thresholds every day at midnight (or test frequently)
cron.schedule('0 0 * * *', async () => {
    try {
        const lowItems = await Inventory.find({ $expr: { $lt: ["$stock", "$threshold"] } });
        if (lowItems.length > 0 && process.env.EMAIL_USER) {
            const report = lowItems.map(i => `${i.itemName}: ${i.stock} remaining (Threshold: ${i.threshold})`).join('\n');
            await transporter.sendMail({
                from: process.env.EMAIL_USER,
                to: process.env.ADMIN_EMAIL,
                subject: '⚠️ Urgent: Pizza Inventory Low Stock Alert',
                text: `The following items have dropped below their safety threshold:\n\n${report}`
            });
            console.log('Low stock alert email sent.');
        }
    } catch (err) {
        console.error('Cron job error:', err);
    }
});

// --- AUTH ROUTES ---
app.post('/api/register', async (req, res) => {
    try {
        const { email, password, adminSecret } = req.body;
        const existing = await User.findOne({ email });
        if (existing) return res.status(400).json({ error: 'User already exists' });

        const hashedPassword = await bcrypt.hash(password, 10);
        const isAdmin = adminSecret === 'HASHIR_ADMIN_2026';

        const user = new User({ email, password: hashedPassword, isAdmin });
        await user.save();
        res.json({ message: 'Registration successful' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user || !(await bcrypt.compare(password, user.password))) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }
        const token = jwt.sign({ id: user._id, email: user.email, isAdmin: user.isAdmin }, process.env.JWT_SECRET, { expiresIn: '1d' });
        res.json({ token, isAdmin: user.isAdmin, email: user.email });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// --- INVENTORY ROUTES ---
app.get('/api/inventory', async (req, res) => {
    const items = await Inventory.find();
    res.json(items);
});

app.post('/api/inventory/update', async (req, res) => {
    const { id, stock } = req.body;
    const updated = await Inventory.findByIdAndUpdate(id, { stock }, { new: true });
    res.json(updated);
});

// --- ORDER & PAYMENT ROUTES ---
app.post('/api/create-order-razorpay', async (req, res) => {
    try {
        const options = {
            amount: req.body.amount * 100, // amount in paisa/cents
            currency: "INR",
            receipt: "order_rcptid_" + Date.now()
        };
        const order = await razorpay.orders.create(options);
        res.json(order);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/orders', async (req, res) => {
    try {
        const { userEmail, pizzaDetails, amount } = req.body;
        
        // Automatically decrement inventory stocks
        await Inventory.findOneAndUpdate({ itemName: pizzaDetails.base }, { $inc: { stock: -1 } });
        await Inventory.findOneAndUpdate({ itemName: pizzaDetails.sauce }, { $inc: { stock: -1 } });
        await Inventory.findOneAndUpdate({ itemName: pizzaDetails.cheese }, { $inc: { stock: -1 } });

        const order = new Order({ userEmail, pizzaDetails, amount });
        await order.save();
        res.json({ message: 'Order placed successfully', orderId: order._id });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/orders', async (req, res) => {
    const orders = await Order.find().sort({ createdAt: -1 });
    res.json(orders);
});

app.put('/api/orders/:id/status', async (req, res) => {
    const { status } = req.body;
    const updated = await Order.findByIdAndUpdate(req.params.id, { status }, { new: true });
    res.json(updated);
});

// Seed initial inventory if empty
async function seedDB() {
    const count = await Inventory.countDocuments();
    if (count === 0) {
        await Inventory.insertMany([
            { itemName: 'Thin Crust', category: 'base', stock: 50, threshold: 10 },
            { itemName: 'Hand Tossed', category: 'base', stock: 40, threshold: 10 },
            { itemName: 'Cheese Burst', category: 'base', stock: 25, threshold: 10 },
            { itemName: 'Wheat Crust', category: 'base', stock: 30, threshold: 10 },
            { itemName: 'Gluten Free', category: 'base', stock: 15, threshold: 10 },
            { itemName: 'Classic Tomato', category: 'sauce', stock: 60, threshold: 15 },
            { itemName: 'Spicy Barbeque', category: 'sauce', stock: 50, threshold: 15 },
            { itemName: 'Garlic Ranch', category: 'sauce', stock: 45, threshold: 15 },
            { itemName: 'Pesto Sauce', category: 'sauce', stock: 20, threshold: 10 },
            { itemName: 'White Alfredo', category: 'sauce', stock: 35, threshold: 10 },
            { itemName: 'Mozzarella', category: 'cheese', stock: 100, threshold: 20 },
            { itemName: 'Cheddar', category: 'cheese', stock: 80, threshold: 20 },
            { itemName: 'Parmesan', category: 'cheese', stock: 50, threshold: 15 },
            { itemName: 'Mushrooms', category: 'vegetable', stock: 40, threshold: 10 },
            { itemName: 'Jalapenos', category: 'vegetable', stock: 45, threshold: 10 },
            { itemName: 'Bell Peppers', category: 'vegetable', stock: 60, threshold: 15 },
            { itemName: 'Olives', category: 'vegetable', stock: 50, threshold: 15 }
        ]);
        console.log('Inventory Seeded.');
    }
}
seedDB();

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
