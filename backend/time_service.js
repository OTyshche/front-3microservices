// time_service.js
const express = require('express');
const cors = require('cors'); // Import CORS package
const app = express();
const port = 3001;

app.use(cors()); // Enable CORS for all routes and origins

app.get('/api/time', (req, res) => {
  /**
   * Returns the current server time.
   */
  const currentTime = new Date().toISOString();
  res.json({ time: currentTime });
});

app.listen(port, '0.0.0.0', () => {
  // Listening on 0.0.0.0 makes it accessible externally (e.g. from other Docker containers)
  console.log(`Time Service listening at http://0.0.0.0:${port}`);
});
