import React, { useState, useEffect } from 'react';
import './App.css';

const API = "http://localhost:5000/api";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [isAdmin, setIsAdmin] = useState(localStorage.getItem('isAdmin') === 'true');
  const [view, setView] = useState('login'); // login, register, user-dash, admin-dash, builder

  // Builder States
  const [base, setBase] = useState('Thin Crust');
  const [sauce, setSauce] = useState('Classic Tomato');
  const [cheese, setCheese] = useState('Mozzarella');
  const [veggies, setVeggies] = useState([]);
  const [orders, setOrders] = useState([]);
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    if (token) {
      fetchOrders();
      if (isAdmin) fetchInventory();
    }
  }, [token]);

  const fetchOrders = async () => {
    const res = await fetch(`${API}/orders`);
    const data = await res.json();
    setOrders(data);
  };

  const fetchInventory = async () => {
    const res = await fetch(`${API}/inventory`);
    const data = await res.json();
    setInventory(data);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    const res = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      localStorage.setItem('isAdmin', data.isAdmin);
      setToken(data.token);
      setIsAdmin(data.isAdmin);
      setView(data.isAdmin ? 'admin-dash' : 'user-dash');
    } else {
      alert(data.error);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    const adminSecret = e.target.adminSecret.value;
    const res = await fetch(`${API}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, adminSecret })
    });
    const data = await res.json();
    if (res.ok) {
      alert('Registration successful! Please login.');
      setView('login');
    } else {
      alert(data.error);
    }
  };

  const handleCheckout = async () => {
    const amount = 450; // Fixed custom pizza test price
    const orderRes = await fetch(`${API}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userEmail: localStorage.getItem('email') || 'user@test.com',
        pizzaDetails: { base, sauce, cheese, veggies },
        amount
      })
    });
    if (orderRes.ok) {
      alert('Order placed successfully!');
      fetchOrders();
      setView('user-dash');
    }
  };

  const updateOrderStatus = async (id, status) => {
    await fetch(`${API}/orders/${id}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    fetchOrders();
  };

  if (!token) {
    return (
      <div className="auth-wrapper">
        <div className="auth-card">
          <h1>🍕 Pizza Platform</h1>
          {view === 'login' ? (
            <form onSubmit={handleLogin}>
              <h3>Login</h3>
              <input name="email" type="email" placeholder="Email" required />
              <input name="password" type="password" placeholder="Password" required />
              <button type="submit">Login</button>
              <p onClick={() => setView('register')} className="link">Need an account? Register</p>
            </form>
          ) : (
            <form onSubmit={handleRegister}>
              <h3>Register</h3>
              <input name="email" type="email" placeholder="Email" required />
              <input name="password" type="password" placeholder="Password (min 8 chars)" required />
              <input name="adminSecret" type="password" placeholder="Admin Secret (optional)" />
              <button type="submit">Register</button>
              <p onClick={() => setView('login')} className="link">Existing user? Login</p>
            </form>
          )}
        </div>
        <Watermark />
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <nav className="navbar">
        <h2>🍕 Full-Stack Pizza Platform</h2>
        <button onClick={() => { localStorage.clear(); window.location.reload(); }}>Logout</button>
      </nav>

      <div className="content">
        {isAdmin ? (
          <div>
            <h2>Admin Inventory & Order Panel</h2>
            <div className="admin-grid">
              <div className="card">
                <h3>Live Inventory Stock</h3>
                <ul>
                  {inventory.map(item => (
                    <li key={item._id}>{item.itemName} ({item.category}): <b>{item.stock}</b> (Alert &lt; {item.threshold})</li>
                  ))}
                </ul>
              </div>
              <div className="card">
                <h3>Incoming Customer Orders</h3>
                {orders.map(o => (
                  <div key={o._id} className="order-item">
                    <p><b>User:</b> {o.userEmail}</p>
                    <p><b>Pizza:</b> {o.pizzaDetails.base}, {o.pizzaDetails.sauce}, {o.pizzaDetails.cheese}</p>
                    <p><b>Status:</b> {o.status}</p>
                    <select value={o.status} onChange={(e) => updateOrderStatus(o._id, e.target.value)}>
                      <option value="Order Received">Order Received</option>
                      <option value="In Kitchen">In Kitchen</option>
                      <option value="Sent to Delivery">Sent to Delivery</option>
                    </select>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div>
            <div className="user-header">
              <h2>Welcome to Your Dashboard</h2>
              <button className="primary-btn" onClick={() => setView('builder')}>+ Build Custom Pizza</button>
            </div>

            {view === 'builder' ? (
              <div className="card builder-card">
                <h3>Custom Pizza Builder</h3>
                <label>1. Choose Base:</label>
                <select value={base} onChange={e => setBase(e.target.value)}>
                  <option>Thin Crust</option><option>Hand Tossed</option><option>Cheese Burst</option><option>Wheat Crust</option><option>Gluten Free</option>
                </select>

                <label>2. Choose Sauce:</label>
                <select value={sauce} onChange={e => setSauce(e.target.value)}>
                  <option>Classic Tomato</option><option>Spicy Barbeque</option><option>Garlic Ranch</option><option>Pesto Sauce</option><option>White Alfredo</option>
                </select>

                <label>3. Choose Cheese:</label>
                <select value={cheese} onChange={e => setCheese(e.target.value)}>
                  <option>Mozzarella</option><option>Cheddar</option><option>Parmesan</option>
                </select>

                <label>4. Vegetables (Multiple):</label>
                <div className="checkbox-group">
                  {['Mushrooms', 'Jalapenos', 'Bell Peppers', 'Olives'].map(v => (
                    <label key={v}><input type="checkbox" onChange={e => {
                      if(e.target.checked) setVeggies([...veggies, v]);
                      else setVeggies(veggies.filter(item => item !== v));
                    }} /> {v}</label>
                  ))}
                </div>

                <button className="success-btn" onClick={handleCheckout}>Proceed to Checkout (₹450)</button>
              </div>
            ) : (
              <div>
                <h3>Your Active Orders & Tracking</h3>
                <div className="orders-grid">
                  {orders.map(o => (
                    <div key={o._id} className="card">
                      <p><b>Base:</b> {o.pizzaDetails.base}</p>
                      <p><b>Sauce:</b> {o.pizzaDetails.sauce}</p>
                      <p><b>Status Tracker:</b> <span className="badge">{o.status}</span></p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      <Watermark />
    </div>
  );
}

function Watermark() {
  return (
    <div className="watermark-banner">
      <span className="banner-name">MUHAMMAD HASHIR</span>
      <span className="banner-task">Web Development & Designing</span>
      <span className="banner-sub">LEVEL 3 · PIZZA DELIVERY APP</span>
    </div>
  );
}
