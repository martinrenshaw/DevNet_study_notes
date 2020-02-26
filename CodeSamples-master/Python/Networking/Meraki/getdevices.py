import requests
import json

url = "https://dashboard.meraki.com/api/v0/organizations"

headers = {
    'X-Cisco-Meraki-API-Key': "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
}

response = requests.get(url, headers=headers).json()

print(json.dumps(response, indent=2, sort_keys=True))

for response_org in response:
    if response_org['name'] == 'DevNet Sandbox':
        orgId = response_org['id']

#net_url = f'{url}/{orgId}/networks'
net_url = '{url}/{orgId}/networks'.format(url, orgId)

networks = requests.get(net_url, headers=headers).json()
for network in networks:
    if network['name'] == 'DNSMB2':
        netId = network['id']

#dev_url = f'https://dashboard.meraki.com/api/v0/networks/{netId}/devices'
dev_url = 'https://dashboard.meraki.com/api/v0/networks/{netId}/devices'.format(netId)
devices = requests.get(dev_url, headers=headers).json()
print(json.dumps(devices, indent=2, sort_keys=True))
