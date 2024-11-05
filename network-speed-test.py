import speedtest
import json
import time

def test_speed(num_tests=1):
    st = speedtest.Speedtest()

    print("Finding the best server...")
    best_server = st.get_best_server()
    print(f"Best server found: {best_server['sponsor']} in {best_server['name']} ({best_server['country']})")

    results = []

    for i in range(num_tests):
        print(f"\nRunning speed test {i + 1}/{num_tests}...")
        try:
            print("Testing download speed...")
            download_speed = st.download() / 1_000_000
            print("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000
            ping = st.results.ping

            result = {
                "test_number": i + 1,
                "download_speed_mbps": download_speed,
                "upload_speed_mbps": upload_speed,
                "ping_ms": ping,
                "server": best_server['sponsor'],
                "server_location": f"{best_server['name']}, {best_server['country']}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            results.append(result)
            print(f"Test {i + 1} completed.")
        except Exception as e:
            print(f"An error occurred during the speed test: {e}")

    print("\nSpeed Test Results:")
    for result in results:
        print(json.dumps(result, indent=4))

    with open('speed_test_results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print("Results saved to speed_test_results.json")

if __name__ == "__main__":
    number_of_tests = int(input("Enter the number of tests to run: "))
    test_speed(num_tests=number_of_tests)
