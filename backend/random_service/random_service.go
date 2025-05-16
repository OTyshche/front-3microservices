// random_service.go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"
)

// Response structure for the JSON
type RandomResponse struct {
	RandomNumber int `json:"randomNumber"`
}

func randomNumberHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
    // Allow requests from any origin. For production, you might want to restrict this.
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

    // Handle preflight OPTIONS requests
    if r.Method == "OPTIONS" {
        w.WriteHeader(http.StatusOK)
        return
    }

	// Generate a random number
	s := rand.NewSource(time.Now().UnixNano())
	rng := rand.New(s)
	randomNumber := rng.Intn(1000) // Random number between 0 and 999

	response := RandomResponse{RandomNumber: randomNumber}

	// Set content type to JSON
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// Encode and send the JSON response
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
		http.Error(w, "Error creating response", http.StatusInternalServerError)
	}
}

func main() {
	http.HandleFunc("/api/random", randomNumberHandler)

	port := "8081"
	fmt.Printf("Random Number Service (Go) listening on port %s\n", port)
    // Listen on 0.0.0.0 to be accessible from outside the container if running in Docker
	log.Fatal(http.ListenAndServe("0.0.0.0:"+port, nil))
}
