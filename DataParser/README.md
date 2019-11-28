<<<<<<< HEAD
# EE-x96-Drone-Traffic-Profiling-Protocol-Reverse-Engineering


## Purpose
This script parses through this JSON file to extract the payload data for each packet.
  
This payload data is then parsed using the MAVLINK 2.0 Serialization

Outputs to Excel (.xlsx) Sheet in results/ directory


## Setup
From Team Drive,
  1) Download pcap from OFFICIAL DATA folder 

Using Wireshark,
   1) Decrypt Packets 
      1) Edit > Preferences > Protocols > IEEE 802.11 > Edit (Decryption Keys)
      2) Create new entry
      3) Add wpa-pwd type   
      4) Under key field, insert password of drone (passwords found in cmdlist.txt in Data folder of team drive)
   2) Filter UDP
   3) Export as JSON
      1) File > Export Packet Dissections > As JSON...

Note: the variable json_location specifies the path to this JSON file


## How to run
With Anaconda Prompt,

```
# perform update if prompted
    > python3 -m pip install --upgrade pip --user
# install required libraries
    > python3 -m pip install pandas --user
    > python3 -m pip install openpyxl --user
    > python3 -m pip install [LIBRARY] --user
# clone repo --> enter main directory containing data_parser.py --> execute script
    > git clone [LINK]
    > cd [DIRECTORY]
    > python3 .\data_parser.py
``` 

With Mac OS,

       idk just do it





Developed in JetBrains PyCharm 2019.1.2

=======
# EE-x96-Drone-Traffic-Profiling-Protocol-Reverse-Engineering


## Purpose
This script parses through this JSON file to extract the payload data for each packet.
  
This payload data is then parsed using the MAVLINK 2.0 Serialization

Outputs to Excel (.xlsx) Sheet in results/ directory


## Setup
From Team Drive,
  1) Download pcap from OFFICIAL DATA folder 

Using Wireshark,
   1) Decrypt Packets 
      1) Edit > Preferences > Protocols > IEEE 802.11 > Edit (Decryption Keys)
      2) Create new entry
      3) Add wpa-pwd type   
      4) Under key field, insert password of drone (passwords found in cmdlist.txt in Data folder of team drive)
   2) Filter UDP
   3) Export as JSON
      1) File > Export Packet Dissections > As JSON...

Note: the variable json_location specifies the path to this JSON file


## How to run
With Anaconda Prompt,

```
# perform update if prompted
    > python3 -m pip install --upgrade pip --user
# install required libraries
    > python3 -m pip install pandas --user
    > python3 -m pip install openpyxl --user
    > python3 -m pip install [LIBRARY] --user
# clone repo --> enter main directory containing data_parser.py --> execute script
    > git clone [LINK]
    > cd [DIRECTORY]
    > python3 .\data_parser.py
``` 

With Mac OS,

       idk just do it





Developed in JetBrains PyCharm 2019.1.2

>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244
