import requests

# Register Test
print("REGISTER TEST")
res = requests.post("http://127.0.0.1:5000/api/auth/register", json={
    "name": "Test User",
    "email": "test1@gmail.com",
    "password": "123456"
})
print(res.status_code, res.text)


# Login Test
print("\nLOGIN TEST")
res = requests.post("http://127.0.0.1:5000/api/auth/login", json={
    "email": "test1@gmail.com",
    "password": "123456"
})
print(res.status_code, res.text)


# Create Deal Test
print("\nCREATE DEAL TEST")
res = requests.post("http://127.0.0.1:5000/api/deals", json={
    "title": "Test Deal",
    "amount": 10000
})
print(res.status_code, res.text)