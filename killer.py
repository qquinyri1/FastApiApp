import requests

for _ in range(10):
    response = requests.get("http://localhost:8000/")
    print(f"Status Code: {response.status_code}, Response Text: {response.text}")
