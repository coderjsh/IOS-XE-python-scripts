import requests
import sys
from ipaddress import IPv4Network
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/ietf-interfaces:interfaces"

    payload = {}
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json',
        'Authorization': 'Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU='
    }

    response = requests.request("GET", url, headers=headers, data = payload, verify=False)

    if response.status_code !=  200:
        print('Login Failed ')
        sys.exit(0)

    data = response.json()['ietf-interfaces:interfaces']['interface']

    for x in data:
        try:
            netmask = IPv4Network("0.0.0.0/" + str(x["ietf-ip:ipv4"]["address"][0]["netmask"])).prefixlen
        except:
            pass

        if "description" in x.keys():
            if x["ietf-ip:ipv4"] != {}:
                print(x["name"] + " : " + x["description"] + " : " + x["ietf-ip:ipv4"]["address"][0]['ip'] + "/" + str(netmask))
                continue
            print(x["name"] + " : " + x["description"] + " : " + "No IP")
            continue
        elif x["ietf-ip:ipv4"] != {}:
            print(x["name"] + " : " + "No Description" + " : " + x["ietf-ip:ipv4"]["address"][0]['ip'] + "/" + str(netmask))
            continue
        print(x["name"] + " : " + "No Description" + " : " + "No IP")


if __name__ == '__main__':
    main()
