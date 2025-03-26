# Example using the requests library
import requests

url = "http://127.0.0.1:5000/payload"

# payload = {
#     "data": {
#         "this": "is",
#         "a": "test"
#     }
# }

# response = requests.post(url, json=payload)
# print(f"Status Code: {response.status_code}")
# print(f"Response Headers: {dict(response.headers)}")
# print(f"Raw Response: {response.text}")

# try:
#     print(f"JSON Response: {response.json()}")
# except requests.exceptions.JSONDecodeError:
#     print("Could not decode response as JSON")

url = "http://127.0.0.1:5000/payloads"
response = requests.get(url)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Raw Response: {response.text}")

try:
    print(f"JSON Response: {response.json()}")
except requests.exceptions.JSONDecodeError:
    print("Could not decode response as JSON")