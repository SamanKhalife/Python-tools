import requests
import time
import threading
import logging
import argparse

logging.basicConfig(
    filename='url_visit_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def visit_url(url):
    """Visit the specified URL and log the response status."""
    try:
        with requests.Session() as session:
            response = session.get(url)
            logging.info(f'Opened {url} with status code: {response.status_code}')
    except requests.ConnectionError:
        logging.error(f'Failed to connect to {url}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

def main(url, num_visits, interval):
    """Visit a URL multiple times using threads."""
    threads = []
    for _ in range(num_visits):
        thread = threading.Thread(target=visit_url, args=(url,))
        threads.append(thread)
        thread.start()
        time.sleep(interval)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visit a URL multiple times.")
    parser.add_argument('url', type=str, help='The URL to visit.')
    parser.add_argument('num_visits', type=int, help='Number of times to visit the URL.')
    parser.add_argument('interval', type=int, help='Time interval between visits in seconds.')

    args = parser.parse_args()

    if args.num_visits <= 0:
        print("Error: Number of visits must be a positive integer.")
        exit(1)
    if args.interval < 0:
        print("Error: Interval must be a non-negative integer.")
        exit(1)

    main(args.url, args.num_visits, args.interval)
