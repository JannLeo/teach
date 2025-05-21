// Visible server for COMP30023 2025 Project 2
// Copyright (c) 2025 University of Melbourne
package main

import (
	"fmt"
	"io"
	"math/rand"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("usage: server <port>")
		return
	}
	port := os.Args[1]

	server := &http.Server{
		Addr: ":" + port,
	}

	// Hello world
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		fmt.Fprintln(w, "Hello, World!")
	})

	// Echos the param
	http.HandleFunc("/echo/{message}", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		message := r.PathValue("message")
		if len(message) > 10000 {
			http.Error(w, "Message too long", http.StatusBadRequest)
			return
		}

		w.Header().Set("Transfer-Encoding", "identity")
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Content-Length", strconv.Itoa(len(message)))
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(message))
	})

	// Flip
	var flipMap sync.Map
	http.HandleFunc("/flip", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet && r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		ip := transformIPToKey(r)
		if r.Method == http.MethodPost {
			if r.Body == nil {
				flipAny, ok := flipMap.Load(ip)
				if !ok {
					flipMap.Store(ip, true)
				} else {
					flipMap.Store(ip, !bool(flipAny.(bool)))
				}
			} else {
				// Read the first byte
				buffer := make([]byte, 1)
				n, err := r.Body.Read(buffer)
				if err != io.EOF || n != 1 {
					http.Error(w, "Failed to read body", http.StatusBadRequest)
					return
				}

				switch buffer[0] {
				case '1':
					flipMap.Store(ip, true)
				case '0':
					flipMap.Store(ip, false)
				default:
					http.Error(w, "Expected 0/1", http.StatusBadRequest)
					return
				}
			}
			w.WriteHeader(http.StatusNoContent)
		}

		if r.Method == http.MethodGet {
			cacheControlQueryValue := r.URL.Query().Get("cache-control")
			if cacheControlQueryValue != "" && len(cacheControlQueryValue) < 10000 {
				w.Header().Set("Cache-Control", cacheControlQueryValue)
			}

			flip, ok := flipMap.Load(ip)
			if ok && bool(flip.(bool)) {
				fmt.Fprintln(w, "true")
			} else {
				fmt.Fprintln(w, "false")
			}
		}
	})

	// Produce length number of 'a' characters
	var lengthMap sync.Map
	http.HandleFunc("/a", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet && r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		ip := transformIPToKey(r)
		if r.Method == http.MethodPost {
			var newLength int
			if _, err := fmt.Fscanf(r.Body, "%d", &newLength); err != nil {
				http.Error(w, "Cannot parse new length", http.StatusBadRequest)
				return
			}

			if newLength < 0 || newLength > 200*1024 {
				http.Error(w, "Invalid length", http.StatusBadRequest)
				return
			}

			lengthMap.Store(ip, newLength)
			w.WriteHeader(http.StatusNoContent)
		}

		if r.Method == http.MethodGet {
			cacheControlQueryValue := r.URL.Query().Get("cache-control")
			if cacheControlQueryValue != "" && len(cacheControlQueryValue) < 10000 {
				w.Header().Set("Cache-Control", cacheControlQueryValue)
			}

			lengthAny, ok := lengthMap.Load(ip)
			var length int
			if !ok {
				length = 1
			} else {
				length = int(lengthAny.(int))
			}

			w.Header().Set("Transfer-Encoding", "identity")
			w.Header().Set("Content-Type", "text/plain")
			w.Header().Set("Content-Length", strconv.Itoa(length))
			w.WriteHeader(http.StatusOK)

			buffer := make([]byte, length)
			for i := range buffer {
				buffer[i] = 'a'
			}
			w.Write(buffer)
		}
	})

	// Set seed
	var seedMap sync.Map
	http.HandleFunc("/seed", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var newSeed int
		if _, err := fmt.Fscanf(r.Body, "%d", &newSeed); err != nil {
			http.Error(w, "Cannot parse new seed", http.StatusBadRequest)
			return
		}

		ip := transformIPToKey(r)
		seedMap.Store(ip, int64(newSeed))
		w.WriteHeader(http.StatusNoContent)
	})

	// Random bytes
	http.HandleFunc("/gen/{n}", func(w http.ResponseWriter, r *http.Request) {
		randomResponseHelper(&seedMap, w, r, "application/octet-stream", nil)
	})

	// Random string
	const alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	http.HandleFunc("/gen-plain/{n}", func(w http.ResponseWriter, r *http.Request) {
		randomResponseHelper(&seedMap, w, r, "text/plain", func(buffer []byte, rnd *rand.Rand) {
			// Map bytes to characters in alphabet
			for i := range buffer {
				buffer[i] = alphabet[rnd.Intn(len(alphabet))]
			}
		})
	})

	fmt.Printf("Starting on port %s...\n", port)
	if err := server.ListenAndServe(); err != nil {
		fmt.Println("Error:", err)
	}
}

// Helper function for random response
func randomResponseHelper(seedMap *sync.Map, w http.ResponseWriter, r *http.Request, contentType string, transform func([]byte, *rand.Rand)) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	nStr := r.PathValue("n")
	n, err := strconv.Atoi(nStr)
	if err != nil || n < 0 {
		http.Error(w, "Invalid size", http.StatusBadRequest)
		return
	}

	w.Header().Set("Transfer-Encoding", "identity")
	w.Header().Set("Content-Type", contentType)
	w.Header().Set("Content-Length", strconv.Itoa(n))
	w.WriteHeader(http.StatusOK)

	ip := transformIPToKey(r)

	seedAny, ok := seedMap.Load(ip)
	var seed int64
	if !ok {
		seed = int64(30023)
	} else {
		seed = int64(seedAny.(int64))
	}
	rnd := rand.New(rand.NewSource(seed))

	left := n
	for left > 0 {
		current := min(left, 16384)

		buffer := make([]byte, current)
		if _, err := rnd.Read(buffer); err != nil {
			http.Error(w, "Error generating random bytes", http.StatusInternalServerError)
			return
		}

		if transform != nil {
			transform(buffer, rnd)
		}

		w.Write(buffer)
		left -= current
	}
}

// Transforms the IP address to a key
// The key is used to track state for each IP
func transformIPToKey(r *http.Request) string {
	ip := r.Header.Get("X-Forwarded-For")

	// Do not bother with multiple values
	if ip == "" || strings.Contains(ip, ",") {
		ip = r.RemoteAddr
	}

	// Try to parse form without port
	parsed := net.ParseIP(ip)
	// Map 127.0.0.0/8 and ::1 for testing framework
	if parsed.IsLoopback() {
		return "loopback"
	}

	// Try to parse form with port
	if host, _, err := net.SplitHostPort(ip); err == nil {
		parsed := net.ParseIP(host)
		if parsed.IsLoopback() {
			return "loopback"
		}
		return host
	}

	return ip
}
