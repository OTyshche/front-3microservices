const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Proxy to User Service
app.use('/api/user', createProxyMiddleware({
  target: 'http://user-service-service.default.svc.cluster.local',
  changeOrigin: true,
  pathRewrite: { '^/api/user': '/api/user' },
}));

// Proxy to Time Service
app.use('/api/time', createProxyMiddleware({
  target: 'http://time-service-service.default.svc.cluster.local',
  changeOrigin: true,
  pathRewrite: { '^/api/time': '/api/time' },
}));

// Proxy to Random Number Service
app.use('/api/random', createProxyMiddleware({
  target: 'http://random-service-service.default.svc.cluster.local',
  changeOrigin: true,
  pathRewrite: { '^/api/random': '/api/random' },
}));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`API Gateway listening on port ${PORT}`);
});
