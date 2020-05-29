import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    dumy= []
    payload = {}
    headers = {
        'Authorization': 'Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU='
    }
    print("Do you want to delete a single interface or  range of interface?")
    select = input("Enter (Single or Range): ")
    if select.lower() == "single":
        try:
            number = int(input("Enter the Loopback number to be deleted: "))
            dumy.append(number)
        except:
            print("Invalid number.. Try again!")
            sys.exit(0)
    elif select.lower() == "range":
        number = (input("Enter Loopback interfaces to be deleted (start number, end number): "))
        number = number.split(",")
        for i in range(len(number)):
            try:
                number[i] = int(number[i])
                dumy.append(number[i])
            except:
                print(f"Please Enter an interger value. {number[i]} is not an integer. Try again!")
                sys.exit(0)
    else:
        print("Invalid Input, Try again!!")

    if len(dumy) == 1:
        dumy.append(int(dumy[0]))
    elif len(dumy) == 0:
        print("Please enter start and end value")
        sys.exit(0)
    elif len(dumy) > 2:
        print(f"Expected 2 values, start and end, got {len(dumy)}")
        sys.exit(0)
    for i in range(dumy[0], dumy[1]+1):
        url = "https://ios-xe-mgmt.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=Loopback" + str(i)
        response = requests.request("DELETE", url, headers=headers, data = payload, verify=False)
        if response.status_code == 204:
            print(f"Loopback{i} Deleted successfully")
        else:
            print(f"Loopback{i} not found.")

if __name__ == '__main__':
    main()
