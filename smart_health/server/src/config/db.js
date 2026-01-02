// server/src/config/db.js
const mongoose = require('mongoose');

module.exports = () => {
  const url = process.env.MONGO_URL;
  if (!url) {
    console.error('MONGO_URL not set in .env');
    process.exit(1);
  }
  mongoose.set('strictQuery', false);
  mongoose.connect(url, { dbName: 'smarthealth' })
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => {
      console.error('❌ MongoDB connection error:', err.message);
      console.log('💡 Make sure MongoDB is running locally or check your connection string');
      // Don't exit, let the server run without database for now
    });
};
