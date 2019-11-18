"""
Title: heartbeat_analyzer.py
By: M5DS1
Date: 09/23/19
Description: Parses JSON for heartbeat packets. Returns timing frequency information and computes average time between heartbeats. Outputs to spreadsheet (wip).
"""

import json
import random
import matplotlib.pyplot as plt
import statistics
import xlsxwriter
import numpy as np
import pandas as pd

''' Location of Data for Parsing '''

# json_location = '../Data/decrypted/Viper/Viper_1.json'
json_location = '../Data/decrypted/Intel/Intel_3.json'
#json_location = '../Data/decrypted/Intel/Intel_1_1of16.json'

''' Initialize Relevant Fields '''
frame_reltime = []
data_data = []
count = 0
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    for packet in src_loader:
        try:
            packet_array = packet['_source']['layers']['data']['data.data'].split(':')
            if packet_array[0] == 'fd':
                ''' Relevant Fields '''
                frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
                data_data.append(packet['_source']['layers']['data']['data.data'])
                count += 1
        except KeyError:
            print("Failed to append Data, KeyError")

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
payloads = []
payloads_id = []

for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':')) # array of packets; packet is split into bytes
    payloads.append(' '.join(split_data[dat][10:-2]))
    payloads_id.append(' '.join(split_data[dat][7:10]))

print("DEBUG: Length of data_data is {}".format(len(data_data)))

'''
Get counts of all IDs in data
'''

id_rep_count = []
unique_id = list(dict.fromkeys(payloads_id) )
for item in unique_id:
    id_rep_count.append(payloads_id.count(item))
    print(f"id: {item} count: {payloads_id.count(item)}")

fig = plt.figure()
plt.bar(unique_id, id_rep_count)
plt.xlabel('MsgID')
plt.ylabel('ID count')
plt.xticks(rotation=90)
plt.yticks(np.arange(100, max(id_rep_count), 200))
ax = plt.gca()
ax.grid(True)
plt.show()
fig.savefig('results/plot.png')