# EE496-Drone-Traffic-Profiling-Protocol-Reverse-Engineering

## Setup
Using Wireshark,
1. decrypt packets with wpa-pwd
2. export udp packets as json


## data_parser.py
This script parses the packets .json file and delimits the Mavlink 2.0 message within the data frame. It then tabulates this data and exports it as a .xlsx file.
 
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


Developed in JetBrains PyCharm 2019.1.2
