import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

APIC_URL = "https://sandboxapicdc.cisco.com/"

def apic_login():
    """ Login to APIC """

    token = ""
    err = ""

    try:
        response = requests.post(
            url=APIC_URL+"/api/aaaLogin.json",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(
                {
                    "aaaUser": {
                        "attributes": {
                            "name": "admin",
                            "pwd": "ciscopsdt"
                        }
                    }
                }
            ),
            verify=False
        )

        json_response = json.loads(response.content)
        token = json_response['imdata'][0]['aaaLogin']['attributes']['token']
        print('Authentication token:', token)

        print('Authentication Response Status: {status_code} \n'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException as err:
        print("HTTP Request failed")
        print(err)

    return token


def get_tenants():
    """ Get Tenants """

    token = apic_login()
    url=APIC_URL+"/api/node/class/fvTenant.json"
    print('GET request resource: ',url)

    try:
        response = requests.get(
            url,
            headers={
                "Cookie": "APIC-cookie=" + token,
                "Content-Type": "application/json; charset=utf-8",
            },
            verify=False
        )
        
        print('Response HTTP Status Code: {status_code}'.format(
           status_code=response.status_code))
        # print('Response HTTP Response Body:', json.dumps(response.json(), indent=4))  # uncomment to get full json print out
        json_response = json.loads(response.content)
        print("\nTotal Count of Tenants: "+json_response['totalCount']+"\n")
        for tenant in json_response['imdata']:
            print(tenant['fvTenant']['attributes']['dn'])

    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def get_devices():
    """ Get Devices """

    token = apic_login()
    url=APIC_URL+"/api/node/class/fabricNode.json?order-by=fabricNode.role|asc"
    print('GET request resource: ',url)

    try:
        response = requests.get(
                  url,
                  headers={
                    "Cookie": "APIC-cookie=" + token,
                    "Content-Type": "application/json; charset=utf-8"
                          },
                  verify=False)

        print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
        # print('Response HTTP Response Body:', json.dumps(response.json(), indent=4)) # uncomment to get full json print out
        json_response = json.loads(response.content)
        print("\nTotal Count Fabric Devices : "+json_response['totalCount']+"\n")
        for fabricdevices in json_response['imdata']:
            # print(mac['fvCEp']['attributes']['dn'])
            role = fabricdevices['fabricNode']['attributes']['role']
            name = fabricdevices['fabricNode']['attributes']['name']
            fabricSt = fabricdevices['fabricNode']['attributes']['fabricSt']
            AdSt = fabricdevices['fabricNode']['attributes']['adSt']
            print(role+" "+name+" "+"FabricState = "+fabricSt+" AdSt = "+AdSt+"\n")

    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def get_mac():
    """ Get the mac tables from the APIC and display neatly"""
    token = apic_login()
    url=APIC_URL+"/api/node/class/fvCEp.json?rsp-subtree=children&order-by=fvCEp.mac"
    print('GET request resource: ',url)

    try:
        response = requests.get(
                  url,
                  headers={
                    "Cookie": "APIC-cookie=" + token,
                    "Content-Type": "application/json; charset=utf-8"
                          },
                  verify=False)

        print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
        # print('Response HTTP Response Body:', json.dumps(response.json(), indent=4)) # uncomment to get full json print out
        json_response = json.loads(response.content)
        print("\nTotal Count of MAC addrs : "+json_response['totalCount']+"\n")
        print("~"*10+" List of all MACs "+"~"*10)
        for mac in json_response['imdata']:
            # print(mac['fvCEp']['attributes']['dn'])
            print(mac['fvCEp']['attributes']['mac'])
        
        print("\n"*2+"~"*10+" List of all MACs with vLAN , DN & Path "+"~"*10+"\n")

        for maclist in json_response['imdata']:
            # print(mac['fvCEp']['attributes']['dn'])
            mac = maclist['fvCEp']['attributes']['mac']
            vlan = maclist['fvCEp']['attributes']['encap']
            dn = maclist['fvCEp']['attributes']['dn']
            pathep = maclist['fvCEp']['children'][0]['fvRsCEpToPathEp']['attributes']['rn']
            print(mac+"  "+vlan+"  "+dn+"  "+pathep)

    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def get_rib():
    """ Get the IPv4 RIB from the APIC """
    token = apic_login()
    url=APIC_URL+"/api/class/uribv4Route.json?order-by=uribv4Route.prefix|asc"  # Gets the full RIB from all fabric Nodes
    print('GET request resource: ',url)

    try:
        response = requests.get(
                  url,
                  headers={
                    "Cookie": "APIC-cookie=" + token,
                    "Content-Type": "application/json; charset=utf-8"
                          },
                  verify=False)

        print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
        # print('Response HTTP Response Body:', json.dumps(response.json(), indent=4)) # uncomment to get full json print out
        json_response = json.loads(response.content)
        print("\nTotal Count of RIB entries : "+json_response['totalCount']+"\n")
        for mac in json_response['imdata']:
            # print(mac['fvCEp']['attributes']['dn'])
            print(mac['uribv4Route']['attributes']['prefix']+"  "+mac['uribv4Route']['attributes']['dn'])

    except requests.exceptions.RequestException:
        print("HTTP Request failed")




# Suppress credential warning for this exercise
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("\n"+40*'='+' GET TENANTS '+'='*40+"\n")
get_tenants()
print("\n"+40*'='+' GET FABRIC '+'='*40+"\n")
get_devices()
print("\n"+40*'='+' GET MAC TABLE '+'='*40+"\n")
get_mac()
print("\n"+40*'='+' GET RIB TABLE '+'='*40+"\n")
get_rib()
