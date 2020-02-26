import dicttoxml    // serialization library
import requests     // http request library

auth = {            // Python dict, containing authentication info
  "user": {
    "username": "myemail@mydomain.com",
    "key": "90823ff08409408aebcf4320384"
  }
}

get_services_query = "https://myservice.com/status/services"

xmlstring = dicttoxml(auth)       // convert dict to XML in string form

myresponse = requests.get(get_services_query,auth=xmlstring)  // query service


'''
<services>
  <service>
    <name>Service A</name>
    <status>Running</status>
  </service>
  <service>
    <name>Service B</name>
    <status>Idle</status>
  </service>
</services>
'''

import untangle     // xml parser library

myreponse_python = untangle.parse(myresponse)

print myreponse_python.services.service[1].name.cdata,myreponse_python.services.service[1].status.cdata


###########################################################################################

import json
import yaml

with open('myfile.json','r') as json_file:
    ourjson = json.load(json_file) # from JSON to PY DICT

print(type(ourjson))
json_file.close()
print(ourjson)


print(ourjson['expires_in'])

print("The access token from JSON is: %s" % ourjson['access_token'])

print("\n\n---")

print(yaml.dump(ourjson))               # dump from py DICT to YAML DICT
print(json.dumps(ourjson, indent=4))    # dump from py DICt to JSON dict


###########################################################################################


import json
import yaml

yaml_file = open("myfile.yaml","r")

pythondata = yaml.safe_load(yaml_file)

print(pythondata['expires_in'])

print("The access token from YAML is: %s" % pythondata['access_token'])

print("\n\n")

print(json.dumps(pythondata))

## Functions defined within a class are known as class methods
