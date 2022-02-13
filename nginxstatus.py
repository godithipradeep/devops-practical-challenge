import requests

url = "http://nginx-ip"

request_response = requests.head(url)
status_code = request_response.status_code
print(status_code)
