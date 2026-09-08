import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';
import db from './db.js';

dotenv.config();
console.log(
  "Gemini key loaded:",
  process.env.GEMINI_API_KEY ? "YES" : "NO"
);

const app = express();

app.use(cors());
app.use(express.json());

// Initialize Gemini API
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Custom system instruction for your agricultural bot
const systemInstruction = `
You are AgriBot, an expert AI agricultural assistant for Maha Crop Guard.
Your goal is to answer queries related to crop health, plant disease identification, soil conditions, and general farming advice.
Be concise, helpful, and clear. If asked non-agricultural questions, politely redirect the conversation back to farming.
`;

const model = genAI.getGenerativeModel({
  model: 'gemini-2.5-flash',
  systemInstruction: systemInstruction,
});

// Root Route
app.get('/', (req, res) => {
  res.json({
    message: 'Maha Crop Guard Backend Running',
  });
});

// User Login Route
app.post('/api/login', (req, res) => {
  const { email, password, role } = req.body;

  const sql = `
    SELECT *
    FROM users
    WHERE email = ?
    AND password = ?
    AND role = ?
  `;

  db.query(sql, [email, password, role], (err, results) => {
    if (err) {
      console.error('Login database error:', err);
      return res.status(500).json({
        success: false,
        message: 'Database error',
      });
    }

    if (results.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email, password, or role',
      });
    }

    const user = results[0];

    res.json({
      success: true,
      message: 'Login successful',
      user: user,
    });
  });
});

// Gemini Chatbot Route
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const result = await model.generateContent(message);
    const reply = result.response.text();

    res.json({ reply });
  } catch (error) {
    console.error('Gemini API Error:', error);
    res.status(500).json({ error: 'Failed to generate response' });
  }
});

// Single Server Listen
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});


// Officer Data
app.get('/api/officers', (req, res) => {
  const sql = 'SELECT * FROM officers';

  db.query(sql, (err, results) => {
    if (err) {
      console.error('Officer data error:', err);

      return res.status(500).json({
        success: false,
        message: 'Database error'
      });
    }

    res.json({
      success: true,
      officers: results
    });
  });
});


// Weather API
app.get('/api/weather', async (req, res) => {
  try {
    const latitude = req.query.latitude || 19.9975;
    const longitude = req.query.longitude || 73.7898;

    const url =
      `https://api.open-meteo.com/v1/forecast` +
      `?latitude=${latitude}` +
      `&longitude=${longitude}` +
      `&current=temperature_2m,relative_humidity_2m,rain` +
      `&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain` +
      `&forecast_days=2`;

    const response = await fetch(url);

    if (!response.ok) {
      return res.status(500).json({
        success: false,
        message: 'Unable to fetch weather data'
      });
    }

    const data = await response.json();

    res.json({
      success: true,

      temperature: data.current.temperature_2m,
      humidity: data.current.relative_humidity_2m,
      rainfall: data.current.rain,

      rain_probability:
        data.hourly.precipitation_probability[0],

      forecast: {
        time: data.hourly.time.slice(0, 24),
        temperature: data.hourly.temperature_2m.slice(0, 24),
        humidity: data.hourly.relative_humidity_2m.slice(0, 24),
        rain_probability:
          data.hourly.precipitation_probability.slice(0, 24),
        rainfall: data.hourly.rain.slice(0, 24)
      }
    });

  } catch (error) {
    console.error('Weather API Error:', error);

    res.status(500).json({
      success: false,
      message: 'Weather service unavailable'
    });
  }
});