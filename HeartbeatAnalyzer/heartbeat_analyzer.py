"""
Title: heartbeat_analyzer.py
By: M5DS1
Date: 09/23/19
Description: Parses JSON for heartbeat packets. Returns timing frequency information. Outputs to spreadsheet.
"""

import json
import numpy as np
import pandas as pd

''' Location of Data for Parsing '''
json_location = 'decrypted/Viper/100p-udp-viper-trial1.json'
# json_location = 'decrypted/Viper/json-07272019-viper-trial3-01.json'


''' Initialize Relevant Fields '''
frame_reltime = []
data_data = []
count = 0
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    print(src_loader)

    for packet in src_loader:
        try:
            ''' Relevant Fields '''
            frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
            data_data.append(packet['_source']['layers']['data']['data.data'])
            # print(count)
            count += 1
        except KeyError:
            print("Failed to append Data, KeyError")

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':'))
    # print(split_data[dat])

# print("Length of split_data is {}".format(split_data))
print("DEBUG: Length of data_data is {}".format(len(data_data)))

'''
Timing Data for Each packet
'''
hb_count = []
hb_payload = []
hb_reltime = []

for n in range(len(data_data)):
    # print(''.join(split_data[n][7:10]))
    if ''.join(split_data[n][7:10]) == "000000":
        hb_count.append(n)
        hb_payload.append(' '.join(split_data[n][10:-2]))
        hb_reltime.append(frame_reltime[n])
        n += 1

print("DEBUG: hb_count:", hb_count)
print("DEBUG: hb_payload:", hb_payload)
print("DEBUG: hb_reltime:", hb_reltime)


# heartbeats = pd.DataFrame(np.column_stack([count, hb_payload, hb_reltime]), columns=['count', 'payload [10:-2]',
#                                                                                      'relative_time'])
#
#
# with pd.ExcelWriter('results/hb-test-100-pkts.xlsx') as writer:
#     heartbeats.to_excel(writer, sheet_name='heartbeat')



'''
Compute average relative time for heartbeat
'''
tsum = 0
for i in range(len(hb_reltime)-1):
    tsum += float(hb_reltime[i+1]) - float(hb_reltime[i])
    print("count:", i, "value is:", hb_reltime[i])
av_time = tsum / (len(hb_reltime) - 1)
print("The average relative time is:", av_time)
