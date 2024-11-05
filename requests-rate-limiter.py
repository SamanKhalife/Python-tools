import requests
import time
import logging

class RateLimiter:
    def __init__(self, rate):
        self.rate = rate
        self.last_called = 0

    def wait(self):
        elapsed = time.time() - self.last_called
        if elapsed < self.rate:
            time.sleep(self.rate - elapsed)
        self.last_called = time.time()

def send_request(url, method='GET', payload=None):
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=payload)
        else:
            print(f"Unsupported method: {method}")
            return None

        logging.info(f"Response from {url}: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    url = input("Enter the URL to send requests to: ")
    rate = float(input("Enter the rate limit in seconds: "))
    method = input("Enter the HTTP method (GET or POST): ").strip().upper()
    payload = None

    if method == 'POST':
        payload = input("Enter the JSON payload for the POST request (as a string): ")
        try:
            payload = eval(payload)
        except Exception as e:
            logging.error(f"Failed to parse JSON payload: {e}")
            payload = None

    limiter = RateLimiter(rate)

    while True:
        limiter.wait()
        response = send_request(url, method, payload)
        if response:
            print(f"Response Code: {response.status_code}, Response Body: {response.text}")
