import requests

# 1. Update with your NEW ngrok URL
URL = "http://localhost/v1/chat/completions"

payload = {
    "messages": [{"role": "user", "content": "Hi! Are you ready?"}],
    "max_tokens": 10
}

print(f"Pinging vLLM at: {URL}")
try:
    response = requests.post(URL, json=payload, timeout=60)
    if response.status_code == 200:
        print("SUCCESS!")
        print("Model Response:", response.json()['choices'][0]['message']['content'])
        print(response)
    else:
        print(f"ERROR {response.status_code}: {response.text}")
except Exception as e:
    print(f"Connection Failed: {e}")