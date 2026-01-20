import httpx


login_payload = {
  "email": "che@example.com",
  "password": "12345"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

print("Login response: ", login_response_data)
print("Status Code: ", login_response.status_code)

access_token = login_response_data['token']['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}

get_user_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
get_user_response_data = get_user_response.json()

print("Get user response: ", get_user_response)
print("Status Code: ", get_user_response.status_code)