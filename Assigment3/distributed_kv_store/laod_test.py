import requests
import concurrent.futures
import time

API_URL = "http://localhost:80/api/kv/"
GET_KEY_URL = API_URL + "user123/"

def post_request():
    payload = {"key": "user123", "value": "Alice"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.status_code

def get_request():
    response = requests.get(GET_KEY_URL)
    return response.status_code

def run_load_test(num_requests=100, max_workers=10):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(post_request if i % 2 == 0 else get_request) for i in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                status_code = future.result()
                print(f"Request completed with status: {status_code}")
            except Exception as e:
                print(f"Request generated an exception: {e}")

    end_time = time.time()
    print(f"Completed {num_requests} requests in {end_time - start_time} seconds")

if __name__ == "__main__":
    run_load_test(num_requests=100, max_workers=10)
