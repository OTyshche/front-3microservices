FROM node:alpine

WORKDIR /app

COPY *.json *.js ./

# Install dependencies
RUN npm install

# Expose the port the app runs on
EXPOSE 3001

# Start the app
CMD ["node", "time_service.js"]
