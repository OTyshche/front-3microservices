import unittest
import requests
import json
from urllib.parse import urljoin

# Base URLs for the services
# These should match the URLs your services are running on.
# If running via Docker Compose, these might be service names like 'http://user-service:5001'
# For local testing, localhost is usually fine.
USER_SERVICE_BASE_URL = 'http://localhost:5001/'
TIME_SERVICE_BASE_URL = 'http://localhost:3001/'
RANDOM_NUMBER_SERVICE_BASE_URL = 'http://localhost:8081/'

# API Endpoints
USER_API_ENDPOINT = 'api/user'
TIME_API_ENDPOINT = 'api/time'
RANDOM_API_ENDPOINT = 'api/random'

class TestMicroservices(unittest.TestCase):

    def _make_request(self, base_url, endpoint, service_name):
        """Helper function to make a GET request and handle common errors."""
        url = urljoin(base_url, endpoint)
        try:
            response = requests.get(url, timeout=5) # 5 second timeout
            response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
            return response.json()
        except requests.exceptions.ConnectionError:
            self.fail(f"{service_name} is not reachable at {url}. Ensure the service is running.")
        except requests.exceptions.Timeout:
            self.fail(f"Request to {service_name} at {url} timed out.")
        except requests.exceptions.HTTPError as e:
            self.fail(f"HTTP error for {service_name} at {url}: {e}")
        except requests.exceptions.JSONDecodeError:
            self.fail(f"Failed to decode JSON response from {service_name} at {url}. Response text: {response.text}")
        except Exception as e:
            self.fail(f"An unexpected error occurred while testing {service_name} at {url}: {e}")

    def test_user_service(self):
        """Test the User Service (Python/Flask)."""
        service_name = "User Service"
        print(f"\nTesting {service_name}...")
        data = self._make_request(USER_SERVICE_BASE_URL, USER_API_ENDPOINT, service_name)

        self.assertIn("message", data, f"'message' key not found in {service_name} response.")
        self.assertIsInstance(data["message"], str, f"'message' in {service_name} should be a string.")
        self.assertEqual(data["message"], "Hello from the Python User Service!", f"Unexpected message from {service_name}.")
        print(f"{service_name} test passed. Response: {data}")

    def test_time_service(self):
        """Test the Time Service (Node.js/Express)."""
        service_name = "Time Service"
        print(f"\nTesting {service_name}...")
        data = self._make_request(TIME_SERVICE_BASE_URL, TIME_API_ENDPOINT, service_name)

        self.assertIn("time", data, f"'time' key not found in {service_name} response.")
        self.assertIsInstance(data["time"], str, f"'time' in {service_name} should be a string.")
        # Basic check for ISO-like format (YYYY-MM-DDTHH:MM:SS.sssZ)
        # A more robust validation could use datetime.fromisoformat in Python 3.7+
        self.assertRegex(data["time"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$", f"Time format from {service_name} is not as expected.")
        print(f"{service_name} test passed. Response: {data}")

    def test_random_number_service(self):
        """Test the Random Number Service (Go)."""
        service_name = "Random Number Service"
        print(f"\nTesting {service_name}...")
        data = self._make_request(RANDOM_NUMBER_SERVICE_BASE_URL, RANDOM_API_ENDPOINT, service_name)

        self.assertIn("randomNumber", data, f"'randomNumber' key not found in {service_name} response.")
        self.assertIsInstance(data["randomNumber"], int, f"'randomNumber' in {service_name} should be an integer.")
        self.assertTrue(0 <= data["randomNumber"] < 1000, f"Random number from {service_name} is out of expected range (0-999).")
        print(f"{service_name} test passed. Response: {data}")

if __name__ == '__main__':
    print("Starting microservice tests...")
    print("Ensure all microservices (User, Time, Random Number) are running on their respective ports.")
    print(f"User Service expected at: {urljoin(USER_SERVICE_BASE_URL, USER_API_ENDPOINT)}")
    print(f"Time Service expected at: {urljoin(TIME_SERVICE_BASE_URL, TIME_API_ENDPOINT)}")
    print(f"Random Number Service expected at: {urljoin(RANDOM_NUMBER_SERVICE_BASE_URL, RANDOM_API_ENDPOINT)}")
    print("-" * 70)

    unittest.main(verbosity=2)
