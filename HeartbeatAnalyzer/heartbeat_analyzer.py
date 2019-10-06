"""
Title: heartbeat_analyzer.py
By: M5DS1
Date: 09/23/19
Description: Parses JSON for heartbeat packets. Returns timing frequency information and computes average time between heartbeats. Outputs to spreadsheet (wip).
"""

import json
import numpy as np
import pandas as pd

''' Location of Data for Parsing '''
json_location = 'decrypted/Viper/udp-7k-viper-trial5-json.json'
# json_location = 'decrypted/Viper/100p-udp-viper-trial1.json'
# json_location = 'decrypted/Viper/json-07272019-viper-trial3-01.json'


''' Initialize Relevant Fields '''
frame_reltime = []
data_data = []
count = 0
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    for packet in src_loader:
        try:
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

for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':')) # array of packets; packet is split into bytes
    payloads.append(' '.join(split_data[dat][10:-2]))
    payloads_id.append(split_data[dat][7:10])

print("DEBUG: Length of data_data is {}".format(len(data_data)))

'''
Sample 300 consecutive payloads'''

start = 6250
end = start + 300
sample = payloads[start:end]
print("Sample size: 300 starting at ", start)


'''
Get counts of all payloads in sample
'''

rep_count = []
for item in sample:
    rep_count.append(payloads.count(item))
print("DEBUG: Sample counts", rep_count)


#most_repeated = sample[rep_count.index(max(rep_count))]
#print("DEBUG: Most repeated payload", most_repeated)

'''
Save top 5 counts in the sample
'''

rep_set = set(rep_count)
uniq_reps = list(rep_set)
top1 = 0
top2 = 0
top3 = 0
top4 = 0
top5 = 0

for j in range(len(uniq_reps)):
    cnt = uniq_reps[j]
    if cnt > top1:
      top5 = top4
      top4 = top3
      top3 = top2
      top2 = top1
      top1 = cnt
    elif cnt > top2:
        top5 = top4
        top4 = top3
        top3 = top2
        top2 = cnt
    elif cnt > top3:
        top5 = top4
        top4 = top3
        top3 = cnt
    elif cnt > top4:
        top5 = top4
        top4 = cnt
    elif cnt > top4:
        top5 = cnt

top_repeats = [] # for storing relevant information
top_repeats.append([payloads_id[start + rep_count.index(top1)], payloads[start + rep_count.index(top1)]])
top_repeats.append([payloads_id[start + rep_count.index(top2)], payloads[start + rep_count.index(top2)]])
top_repeats.append([payloads_id[start + rep_count.index(top3)], payloads[start + rep_count.index(top3)]])
top_repeats.append([payloads_id[start + rep_count.index(top4)], payloads[start + rep_count.index(top4)]])
top_repeats.append([payloads_id[start + rep_count.index(top5)], payloads[start + rep_count.index(top5)]])

'''
Timing Data for Each Packet
'''
for j in range(0, 5):
    hb_indexes = []
    hb_reltimes = []
    hb_deltas = []
    avg_delta = 0

    for n in range(start, end):
        if payloads[n] == top_repeats[j][1]:
            hb_indexes.append(n)
            hb_reltimes.append(frame_reltime[n])

    for i in range(len(hb_reltimes) - 1):
        delta = float(hb_reltimes[i + 1]) - float(hb_reltimes[i])
        hb_deltas.append(delta)
        avg_delta = 0
    if( len(hb_deltas) > 0):
        sum = 0
        for k in hb_deltas:
            sum += k
        avg_delta = sum / len(hb_deltas)
    top_repeats[j].append(avg_delta)
    print("Debug: Top Repeats", top_repeats[j])

'''
Print probable heartbeat in sample
'''
for m in range(0, 5):
    if top_repeats[m][2] >.8 and top_repeats[m][2] <1.2:
        print("Probable Heartbeat: ", top_repeats[m])

# heartbeats = pd.DataFrame(np.column_stack([count, hb_payload, hb_reltime]), columns=['count', 'payload [10:-2]',
#                                                                                      'relative_time'])
#
#
# with pd.ExcelWriter('results/hb-test-100-pkts.xlsx') as writer:
#     heartbeats.to_excel(writer, sheet_name='heartbeat')


