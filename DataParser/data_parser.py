"""
Title: data_parser.py
By: M5DS1
Description:
    From Team Drive,
        1) Download pcap from OFFICIAL DATA folder
    Using Wireshark,
        1) decrypt pcap with wpa-pwd
        2) filter UDP
        3) File > Export Packet Dissections > As JSON...
    Note: the variable json_location specifies the path to this JSON file

    Purpose:
    This script parses through this JSON file to extract the payload data for each packet.
    This payload data is then parsed using the MAVLINK 2.0 Serialization
    Outputs to Excel (.xlsx) Sheet in results/ directory
"""

import json
import pandas as pd
import numpy as np


''' Location of Data for Parsing '''
# json_location = 'decrypted/Viper/Viper_1.json'
#json_location = '../Data/decrypted/Intel/Intel_3.json'
json_location = '../Data/decrypted/Intel/Intel_1_4of16.json'
''' Initialize Relevant Fields '''
frame_reltime = []
data_len = []
data_data = []

''' Load JSON file '''
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    ''' Parse through JSON file for specific information'''
    for packet in src_loader:
        try:
            ''' Relevant fields '''
            data_len.append(packet['_source']['layers']['data']['data.len'])
            data_data.append(packet['_source']['layers']['data']['data.data'])
            frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
        except KeyError:
            print("Failed to append Data, KeyError")

    # for n in range(len(src_loader)):
    #     print("DEBUG src_loader:  {}\t{}".format(data_len[n], data_data[n]))

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':'))
    # print(split_data[dat])

# print("DEBUG: Length of split_data is {}".format(split_data))
print("DEBUG: Length of data_data is {}".format(len(data_data)))
print("DEBUG: Length of frame_reltime is {}".format(len(frame_reltime)))


'''
First, lets split these data into MavLink fields.. [0][1][2][3][4][5][6][7:10][10:-3][-3:]

Serialization format: https://mavlink.io/en/guide/serialization.html
'''

''' Declare arrays for each field '''
magic = []
length = []
incompat_flags = []
compat_flags = []
seq = []
sysid = []
compid = []
msgid = []
payload = []
checksum = []
signature = []

''' Store data in these field arrays '''
for n in range(len(data_data)):
    magic.append(split_data[n][0])
    length.append(split_data[n][1])
    incompat_flags.append(split_data[n][2])
    compat_flags.append(split_data[n][3])
    seq.append(split_data[n][4])
    sysid.append(split_data[n][5])
    compid.append(split_data[n][6])
    msgid.append(' '.join(split_data[n][7:10]))
    payload.append(' '.join(split_data[n][10:-2]))
    checksum.append(' '.join(split_data[n][-2:]))


clean = pd.DataFrame(np.column_stack([frame_reltime, magic, length, incompat_flags, compat_flags, seq, sysid, compid, msgid, payload,
                                      checksum]),
                     columns=['frame_reltime', 'magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'seq [4]',
                              'sysid [5]', 'compid [6]', 'msgid [7:10]', 'payload [10:-2]', 'checksum [-2:]'])


'''
Next, I want it to display random statistical information.
How about it parses through each field and returns an occurance count of data within each field?
'''
def fieldcounter(data_field):
    count_arr = {}
    for d in data_field:
        if d in count_arr:
            # print("inside", d)
            count_arr[d] += 1
        else:
            # print("make new", d)
            count_arr[d] = 1

    return count_arr

# print(fieldcounter(length))

occurances = pd.DataFrame(np.column_stack([fieldcounter(magic), fieldcounter(length), fieldcounter(incompat_flags),
                                           fieldcounter(compat_flags), fieldcounter(sysid),
                                           fieldcounter(compid), fieldcounter(msgid)]),
                          columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'sysid [5]',
                                   'compid [6]', 'msgid [7:10]']).T



'''
Let's display parsed data and occurance count in an excel file (.xlsx)

NOTE: I can't autofit columns through the script but here's how to do it manually:
https://support.office.com/en-us/article/change-the-column-width-and-row-height-72f5e3cc-994d-43e8-ae58-9774a0905f46
'''
with pd.ExcelWriter('results/results_test.xlsx') as writer:
    clean.to_excel(writer, sheet_name='Parsed')
    occurances.to_excel(writer, sheet_name='Occurances')
