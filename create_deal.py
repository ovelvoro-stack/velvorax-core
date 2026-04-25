import requests

url = "http://127.0.0.1:5000/api/deals"

data = {
    "title": "Test Deal",
    "amount": 10000
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)