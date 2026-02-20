import requests
import time

# Wait for server to start
print("Waiting for server to start...")
time.sleep(5)

# Test login
url = "http://127.0.0.1:8000/auth/login"
data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✓ Login successful! Backend is working correctly.")
    else:
        print("\n✗ Login failed!")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the backend server is running on port 8000")
