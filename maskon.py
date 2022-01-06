import subprocess as sub
import argparse 
import re
import random
import platform
import uuid

def get_args():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--interface', type=str, required=True)
    # Parse the argument
    args = parser.parse_args()
    return args.interface

#"Windows", "Linux", "Mac?"
def os_detection():
    my_os = platform.system()
    return my_os
    
#Randomize new mac address
def new_mac():
    new_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))
    return new_mac

#Get Current mac to compare
def get_current_mac_unix(interface: str):
  output = sub.check_output(['ifconfig', interface], universal_newlines = True)
  search_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
  if search_mac:
    print('Old MAC: ' + search_mac.group(0))
    old_mac = search_mac.group(0)

  else:
    print('[-] Could not read the MAC Address')

def get_current_mac_windows():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def maskon_unix(interface, new_mac):
    print("\n Putting Mask On \n")
    sub.call(['sudo', 'ifconfig', interface, 'ether', new_mac])

if __name__ == "__main__":
    interface = get_args()
    os = os_detection()
    if os == "Windows":
        print("Windows OS Not Supported")
        
    else:
        mac = get_current_mac_unix(interface)
        new_mac = new_mac(mac)
        maskon_unix(interface, new_mac)

        if mac != new_mac:
            print('MAC has been changed')
            print('New mac is ' + new_mac)
        else:
            print('Could not change MAC')
