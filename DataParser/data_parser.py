import json
import pandas as pd
import numpy as np


''' Location of Data for Parsing '''
json_location = 'decrypted/Viper/100p-udp-viper-trial1.json'
# json_location = 'decrypted/Intel_4_json.json'

''' Initialize Relevant Fields '''
frame_reltime = []
data_len = []
data_data = []

with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    for packet in src_loader:
        try:
            # Relevant Fields
            frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
            data_len.append(packet['_source']['layers']['data']['data.len'])
            data_data.append(packet['_source']['layers']['data']['data.data'])
        except KeyError:
            print("Failed to append Data, KeyError")

    # for n in range(len(src_loader)):
    #     print("DEBUG src_loader:  {}\t{}".format(data_len[n], data_data[n]))

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':'))
    # print(split_data[dat])

# print("Length of split_data is {}".format(split_data))
print("DEBUG: Length of data_data is {}".format(len(data_data)))


'''
First, lets make our data really nice.. using [0][1][2][3][4][5][6][7:10][10:-3][-3:] or something like that
use pandas or csv to present the data in a nice table split by fields

Serialization format: https://mavlink.io/en/guide/serialization.html
'''

'''
Serialization Values for Mavlink 2.0 (magic is always 0xFD)
if only i can find out what the payload checksum and signature are...
for now I'll just assume there are no signatures and the checksum is the last 3 bytes 
'''
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
    # signature.append(split_data[n])

# print("DEBUG: \n magic \t\t{}\n length \t\t{}\n incompat \t{}\n compat \t{}\n seq \t\t{}\n sysid \t\t{}\n"
#       "compid \t{}\n msgid \t\t{}\n {}\n {}\n {}\n".format(magic, length, incompat_flags, compat_flags, seq, sysid,
#                                                            compid, msgid, payload, checksum, signature))

clean = pd.DataFrame(np.column_stack([magic, length, incompat_flags, compat_flags, seq, sysid, compid, msgid,
                                      payload, checksum, frame_reltime]),
                     columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'seq [4]',
                              'sysid [5]', 'compid [6]', 'msgid [7:10]', 'payload [10:-2]', 'checksum [-2:]', 'frame_reltime'])


'''
Next, I want it to display random statistical information.
How about it parses through split_data and returns an occurance count of data within each field?
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


'''
I can't autofit columns through the script but here's how to do it manually
https://support.office.com/en-us/article/change-the-column-width-and-row-height-72f5e3cc-994d-43e8-ae58-9774a0905f46
'''
occurances = pd.DataFrame(np.column_stack([fieldcounter(magic), fieldcounter(length), fieldcounter(incompat_flags),
                                           fieldcounter(compat_flags), fieldcounter(sysid),
                                           fieldcounter(compid), fieldcounter(msgid)]),
                          columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'sysid [5]',
                                   'compid [6]', 'msgid [7:10]']).T


# with pd.ExcelWriter('results/udp-100-viper-trial1.xlsx') as writer:
with pd.ExcelWriter('results/udp-7k-viper-trial5-json.xlsx') as writer:
    clean.to_excel(writer, sheet_name='Parsed')
    occurances.to_excel(writer, sheet_name='Occurances')
