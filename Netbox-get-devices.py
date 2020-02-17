import requests
import pprint
import json

url = "https://netboxdemo.com/api/dcim/devices/"

payload = {}
headers = {
    'Authorization': 'Token 72830d67beff4ae178b94d8f781842408df8069d'
}

response = requests.get(
    url, headers=headers, data=payload, verify=False).json()

print(type(response))

for response_dn in response['results']:
    pprint.pprint(response_dn)
    for device in response_dn['name']:
        pprint.pprint(device)
    # print(type(response_dn))
    # print(response_dn[0])

# print(json.dumps(response, indent=2, sort_keys=True))

# for key, values in response.items():
#     print(key, 'some str', response[key])
#     for value in values:
#         print('poop' + value)
