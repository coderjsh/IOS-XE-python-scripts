import requests
import ipaddress
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    dumy = (input("Enter Loopback interfaces to be created (start number, end number): "))
    dumy = dumy.split(",")
    for i in range(len(dumy)):
        try:
            dumy[i] = int(dumy[i])
        except:
            print(f"Please Enter an interger value. Try again!")
            sys.exit(0)
    url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/ietf-interfaces:interfaces"
    headers = {
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json',
        'Authorization': 'Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU='
    }

    if len(dumy) == 1:
        a = int(dumy[0])+1
        dumy.append(a)
    elif len(dumy) == 0:
        print("Please enter start and end value")
        sys.exit(0)
    elif len(dumy) > 2:
        print(f"Expected 2 values, start and end, got {len(dumy)}")
        sys.exit(0)
    if int(dumy[0]) >= int(dumy[1]):
        print("Start value should be smaller than End value")
        sys.exit(0)
    difference = int(dumy[1])+1 - int(dumy[0])
    if difference > 254:
        print("please enter difference of less than 254")
        sys.exit(0)
    ip = input("Enter a subnet to configure the loopbacks (xx.xx.xx.xx/xx): ")
    net4 = ipaddress.ip_network(ip)
    ip = [i for i in net4.hosts()]

    dumy = [i for i in range(int(dumy[0]), int(dumy[1])+1)]
    if len(dumy) > len(ip):
        print("Enter correct subnet, number of interfaces are more than subnet alloted!")
        sys.exit(0)
    new_ip = [str(net4[i]) for i in range(1,len(dumy)+1)]
    res = dict(zip(dumy,new_ip))


    for x,y in res.items():
        payload = '\
        {\
            "ietf-interfaces:interface": {\
                "name": "Loopback' + str(x) + '",\
                "description": "Added with RESTCONF",\
                "type": "iana-if-type:softwareLoopback",\
                "enabled": true,\
                "ietf-ip:ipv4": {\
                    "address": [\
                        {\
                            "ip": "' + str(y) + '",\
                            "netmask": "255.255.255.255"\
                        }\
                    ]\
                }\
            }\
        }'
        data = json.loads(payload)
        data = data["ietf-interfaces:interface"]["name"]
        print(f"Creating {data} ... ")
        response = requests.request("POST", url, headers=headers, data = payload, verify=False)
        if response.status_code == 201:
            print(f"Interface created successfully")
        elif response.status_code == 409:
            print("Interface already present")
        else:
            print("Could not create interface...")
        print("*** --- *** --- ***")

if __name__ == '__main__':
    main()
