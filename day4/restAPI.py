import http.client
import json
conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

payload = json.dumps(REQUEST BODY :{ # pyright: ignore[reportUndefinedVariable]
  'UserId':1,
  'title':'Python Flask API Developement',
}
RESPONSE:
)

conn.request("GET", "/todos", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8")