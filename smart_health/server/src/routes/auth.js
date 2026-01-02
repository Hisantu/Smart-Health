const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const memoryStore = require('../config/memoryStore');
const router = express.Router();

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Try MongoDB first
    try {
      const user = await User.findOne({ username });
      
      if (user && (await user.comparePassword(password))) {
        const token = jwt.sign(
          { userId: user._id, role: user.role },
          process.env.JWT_SECRET,
          { expiresIn: '24h' }
        );
        return res.json({ token, user: { id: user._id, username: user.username, role: user.role, name: user.name } });
      }
    } catch (dbError) {
      console.log('MongoDB error, trying fallback auth');
    }
    
    // Fallback: Simple credential check for testing
    const testCredentials = {
      'admin': { password: 'admin123', role: 'admin', name: 'Admin User' },
      'receptionist': { password: 'recep123', role: 'receptionist', name: 'Receptionist User' },
      'doctor1': { password: 'doc123', role: 'doctor', name: 'Dr. Sarah Johnson' }
    };
    
    if (testCredentials[username] && testCredentials[username].password === password) {
      const token = jwt.sign(
        { userId: username, role: testCredentials[username].role },
        process.env.JWT_SECRET,
        { expiresIn: '24h' }
      );
      return res.json({ 
        token, 
        user: { 
          id: username, 
          username, 
          role: testCredentials[username].role, 
          name: testCredentials[username].name 
        } 
      });
    }

    return res.status(401).json({ error: 'Invalid credentials' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/register', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.status(201).json({ message: 'User created successfully' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;
