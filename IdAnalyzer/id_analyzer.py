"""
Title: id_analyzer.py
By: M5DS1
Date: 10/24/19
Description: Parses JSON for heartbeat packets. Returns timing frequency information and computes average time between heartbeats. Outputs to spreadsheet (wip).
"""

import json
import random
import statistics
import xlsxwriter
import numpy as np
import pandas as pd

''' Location of Data for Parsing '''
# json_location = 'decrypted/Viper/udp-7k-viper-trial5-json.json'
# json_location = 'decrypted/Viper/100p-udp-viper-trial1.json'
# json_location = 'decrypted/Viper/json-07272019-viper-trial3-01.json'
json_location = 'decrypted/Viper/Viper_1.json'


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
payloads =[]
payloads_id = []
vipIDs = ['7d 00 00', '00 00 00', '93 00 00', '98 00 00', 'a5 00 00', 'a2 00 00', '2a 00 00']

for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':')) # array of packets; packet is split into bytes
    payloads.append(' '.join(split_data[dat][10:-2]))
    payloads_id.append(' '.join(split_data[dat][7:10]))

print("DEBUG: Length of data_data is {}".format(len(data_data)))

'''
Timing for each message ID
'''
idTiming = []

for target in vipIDs:
    idIndexes = []
    idReltimes = []
    idDeltas = []
    avgIDdelta = 0
    avgIDstdDev = 0

    for x in range(len(data_data)):

        if payloads_id[x] == target:
            idIndexes.append(x)
            idReltimes.append(frame_reltime[x])

    for i in range(len(idReltimes) - 1):
        delta = float(idReltimes[i + 1]) - float(idReltimes[i])
        idDeltas.append(delta)

    if len(idDeltas) > 1:
        avgIDdelta = statistics.mean(idDeltas)
        avgIDstdDev = statistics.stdev(idDeltas)
    stats = [avgIDdelta, avgIDstdDev]
    stats.append(target)
    stats.extend(idReltimes)
    idTiming.append(stats)
for element in idTiming:
        print("Debug ID Timing: ", element)

# heartbeats = pd.DataFrame(idTiming)
#
#
# with pd.ExcelWriter('results/Viper1-stats.xlsx') as writer:
#     heartbeats.to_excel(writer, sheet_name='heartbeat')
#
workbook = xlsxwriter.Workbook('results/Viper1-array.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for col, data in enumerate(idTiming):
    worksheet.write_column(row, col, data)

workbook.close()
