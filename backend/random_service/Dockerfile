FROM golang:1.24.3-alpine3.21

WORKDIR /app

COPY . .

# Expose the port the app runs on
EXPOSE 8081

# Start the app
CMD ["go", "run", "random_service.go"]