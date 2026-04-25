import requests

def test_register():
    url = "http://127.0.0.1:5000/api/auth/register"

    data = {
        "name": "Test User",
        "email": "test@gmail.com",
        "password": "123456"
    }

    try:
        response = requests.post(url, json=data)

        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Server not running on 127.0.0.1:5000")
        print("👉 First run: python run.py")

if __name__ == "__main__":
    test_register()