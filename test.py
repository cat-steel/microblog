import requests

url = 'https://mail.qq.com/'
response = requests.get(url)
text = response.text
code = response.status_code
print(code)
print(text)