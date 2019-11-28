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
<<<<<<< HEAD
from xml.dom import minidom

''' Only Change This!! '''
json_filename = 'Viper_1'
''' Only Change This!! '''


''' Location of Data for Parsing '''
json_location = 'decrypted/'+json_filename+'.json'

''' Initialize Relevant Fields '''
ip_src = []
ip_dst = []
frame_reltime = []
payload_len = []
=======


''' Location of Data for Parsing '''
# json_location = 'decrypted/Viper/100p-udp-viper-trial1.json'
json_location = 'decrypted/Viper_1'
# json_location = 'decrypted/Intel_4'
# json_location = 'decrypted/Intel_4_json.json'

''' Initialize Relevant Fields '''
frame_reltime = []
>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244
data_len = []
data_data = []
count = 0
dead = 0

''' Load JSON file '''
<<<<<<< HEAD
print("Grabbing JSON: ", json_location)
=======
>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    ''' Parse through JSON file for specific information'''
    for packet in src_loader:
        try:
<<<<<<< HEAD
            packet_array = packet['_source']['layers']['data']['data.data'].split(':')
            ''' Filter for MavLink 2.0 '''
            if packet_array[0] == 'fd':
                ''' Relevant fields '''
                ip_src.append(packet['_source']['layers']['ip']['ip.src'])
                ip_dst.append(packet['_source']['layers']['ip']['ip.dst'])
                frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
                payload_len.append(int(packet['_source']['layers']['data']['data.len']) - 12)
                data_len.append(packet['_source']['layers']['data']['data.len'])
                data_data.append(packet['_source']['layers']['data']['data.data'])
                count += 1
=======
            ''' Relevant fields '''
            # frame_reltime.append(packet['_source']['layers']['frame']['frame.time_relative'])
            data_len.append(packet['_source']['layers']['data']['data.len'])
            data_data.append(packet['_source']['layers']['data']['data.data'])
            count += 1
>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244
        except KeyError:
            print("Failed to append Data, KeyError. Packet " + str(count))
            count += 1
            dead += 1
    print("Lost Packets ", dead)
    # for n in range(len(src_loader)):
    #     print("DEBUG src_loader:  {}\t{}".format(data_len[n], data_data[n]))

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':'))
    # print(split_data[dat])

# print("DEBUG: Length of split_data is {}".format(split_data))
print("DEBUG: Length of data_data is {}".format(len(data_data)))


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
<<<<<<< HEAD
=======
signature = []
>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244

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

<<<<<<< HEAD
clean = pd.DataFrame(np.column_stack([magic, length, incompat_flags, compat_flags, seq, sysid, compid, msgid, payload,
                                      checksum, payload_len, ip_src, ip_dst, frame_reltime]),
                     columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'seq [4]',
                              'sysid [5]', 'compid [6]', 'msgid [7:10]', 'payload [10:-2]', 'checksum [-2:]',
                              'PAYLOAD_LENGTH', 'ip_src', 'ip_dst','FRAME_RELTIME'])

''' Convert some fields to numeric '''
clean['FRAME_RELTIME'] = pd.to_numeric(clean['FRAME_RELTIME'])
clean['PAYLOAD_LENGTH'] = pd.to_numeric(clean['PAYLOAD_LENGTH'])
=======

clean = pd.DataFrame(np.column_stack([magic, length, incompat_flags, compat_flags, seq, sysid, compid, msgid, payload,
                                      checksum]),
                     columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'seq [4]',
                              'sysid [5]', 'compid [6]', 'msgid [7:10]', 'payload [10:-2]', 'checksum [-2:]'])

>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244

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

<<<<<<< HEAD
# print(list(fieldcounter(msgid).keys()))


occurrences = pd.DataFrame(np.column_stack([fieldcounter(magic), fieldcounter(length), fieldcounter(incompat_flags),
                                           fieldcounter(compat_flags), fieldcounter(sysid),
                                           fieldcounter(compid), fieldcounter(msgid)]),
                          columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'sysid [5]',
                                   'compid [6]', 'msgid [7:10]'])

msg_ids = pd.DataFrame(np.column_stack([list(fieldcounter(msgid).keys()), list(fieldcounter(msgid).values())]),
                          columns=['Msg_ID', 'Occurrences'])

msg_ids['Occurrences'] = pd.to_numeric(msg_ids['Occurrences'])
msg_ids.sort_values(['Occurrences'], ascending=False, inplace=True)
# print(msg_ids)

'''
Function that graphs the payload lengths for a given msgid
@input: writer, sheet, data
@output: 
'''
def occur_grapher(writer_, sheet_, data_):
    ## Access the Xlswriter workbook and worksheets objects from the dataframe.
    workbook = writer_.book
    worksheet = writer_.sheets[sheet_]

    ## Create a chart object
    occur_chart = workbook.add_chart({'type': 'bar'})

    ## Configure the series of the chart from the dataframe data
    indexList = list(data_['Occurrences'])
    r1 = 2
    r2 = len(indexList) + 1
    occur_chart.add_series({
        'categories': [sheet_, r1, 1, r2, 1],
        'values': [sheet_, r1, 2, r2, 2]
    })

    ## Configure chart axis
    occur_chart.set_x_axis({'name': 'Number of Packets'})
    occur_chart.set_y_axis({'name': 'Message ID'})

    ## Title and Size
    occur_chart.set_title({'name': 'Occurrences by Msg_ID'})
    occur_chart.set_size({'width': 720, 'height': 800})

    ## Turn off default legend
    occur_chart.set_legend({'none': True})

    ## Insert chart into worksheet
    worksheet.insert_chart('E2', occur_chart)


'''
Function that graphs the payload lengths for a given msgid
@input: writer, sheet, data
@output: 
'''
def payload_grapher(writer_, sheet_, data_, msgid_):
    ## Access the Xlswriter workbook and worksheets objects from the dataframe.
    workbook = writer_.book
    worksheet = writer_.sheets[sheet_]

    ## Create a chart object
    plen_chart = workbook.add_chart({'type': 'scatter'})

    ## Configure the series of the chart from the dataframe data
    indexList = list(data_['PAYLOAD_LENGTH'])
    r1 = 2
    r2 = len(indexList) + 1
    plen_chart.add_series({
        'categories': [sheet_, r1, 1, r2, 1],
        'values': [sheet_, r1, 11, r2, 11]
    })

    ## Configure chart axis
    plen_chart.set_x_axis({'name': 'Number of Packets',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    plen_chart.set_y_axis({'name': 'Payload Length',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    plen_chart.set_title({'name': 'Payload Sizes fo Msg ID-' + msgid_})
    # chart.set_chartarea({'border': {'none': True}})

    ## Turn off default legend
    plen_chart.set_legend({'none': True})

    ## Insert chart into worksheet
    worksheet.insert_chart('S10', plen_chart)


'''
Function that graphs the payload lengths for a given msgid
@input: writer, sheet, data
@output: 
'''
def time_grapher(writer_, sheet_, data_, msgid_):
    ## Access the Xlswriter workbook and worksheets objects from the dataframe.
    workbook = writer_.book
    worksheet = writer_.sheets[sheet_]

    ## Create a chart object
    time_chart = workbook.add_chart({'type': 'scatter'})

    ## Configure the series of the chart from the dataframe data
    indexList = list(data_['FRAME_RELTIME'])
    r1 = 2
    r2 = len(indexList) + 1
    time_chart.add_series({
        'categories': [sheet_, r1, 1, r2, 1],
        'values': [sheet_, r1, 15, r2, 15]
    })

    ## Configure chart axis
    time_chart.set_x_axis({'name': 'Packet Number',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    time_chart.set_y_axis({'name': 'Relative Time',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    time_chart.set_title({'name': 'Time Delta for Msg ID-' + msgid_})
    # chart.set_chartarea({'border': {'none': True}})

    ## Turn off default legend
    time_chart.set_legend({'none': True})

    ## Insert chart into worksheet
    worksheet.insert_chart('S27', time_chart)


'''
Function that compares the msgid to the common_messages.xml to find the msg_type
@input: msg_id
@output: msg_type
'''
def message_decoder(msgid):
    # grab msgid as str
    m = msgid.replace(" ", "")

    # str -> hex -> int -> str
    m = bytearray.fromhex(m)
    m.reverse()
    m = int.from_bytes(m, byteorder='big', signed=False)
    m = str(m).lstrip()

    # Compare to XML
    common = minidom.parse('common_messages.xml').getElementsByTagName('message')
    for c in common:
        if c.attributes['id'].value == m:
            return c.attributes['name'].value

# print(message_decoder('00 00 00'))


'''
Function that creates a stat table w/ msg_type, count, ave_delta, delta_stddev, ave_plen
@input: writer, sheet,
@output: array with top 5 msgids as strings
'''
def stat_tabler(writer_, sheet_, data_, msg_):
    workbook = writer_.book
    worksheet = writer_.sheets[sheet_]
    cell_format = workbook.add_format({'bold': True, 'bg_color':'yellow'})
    cell_format2 = workbook.add_format({'bg_color':'yellow'})

    pList = list(data_['PAYLOAD_LENGTH'])
    r1 = 2
    r2 = len(pList) + 1

    worksheet.write('S2', 'Msg Type:', cell_format)
    worksheet.write('T2', message_decoder(msg_), cell_format2)

    worksheet.write('S3', 'Count:', cell_format)
    worksheet.write_formula('T3', '=COUNTA(B{0}:B{1})'.format(r1, r2), cell_format2)

    worksheet.write('S4', 'Ave Delta:', cell_format)
    worksheet.write_formula('T4', '=AVERAGE(P{0}:P{1})'.format(r1, r2), cell_format2)

    worksheet.write('S5', 'Delta Std Dev:', cell_format)
    worksheet.write_formula('T5', '=STDEV(P{0}:P{1})'.format(r1, r2), cell_format2)

    worksheet.write('S6', 'Ave Payload Length:', cell_format)
    worksheet.write_formula('T6', '=AVERAGE(L{0}:L{1})'.format(r1, r2), cell_format2)
=======
# print(fieldcounter(length))

occurances = pd.DataFrame(np.column_stack([fieldcounter(magic), fieldcounter(length), fieldcounter(incompat_flags),
                                           fieldcounter(compat_flags), fieldcounter(sysid),
                                           fieldcounter(compid), fieldcounter(msgid)]),
                          columns=['magic [0]', 'length [1]', 'incompat_flags [2]', 'compat_flags [3]', 'sysid [5]',
                                   'compid [6]', 'msgid [7:10]']).T

>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244


'''
Let's display parsed data and occurance count in an excel file (.xlsx)

NOTE: I can't autofit columns through the script but here's how to do it manually:
https://support.office.com/en-us/article/change-the-column-width-and-row-height-72f5e3cc-994d-43e8-ae58-9774a0905f46
'''
<<<<<<< HEAD
with pd.ExcelWriter('results/'+json_filename+'.xlsx', engine='xlsxwriter') as writer:
    clean.to_excel(writer, sheet_name='All Packets')
    occurrences.to_excel(writer, sheet_name='Occurrences')
    msg_ids.to_excel(writer, sheet_name='Msg_IDs')
    occur_grapher(writer, 'Msg_IDs', msg_ids)
    hb = clean.loc[clean['msgid [7:10]'] == '00 00 00']
    hb['TIME_DELTA'] = hb['FRAME_RELTIME'] - hb['FRAME_RELTIME'].shift(1)
    hb.to_excel(writer, sheet_name='msgID-'+'00 00 00')
    payload_grapher(writer, 'msgID-00 00 00', hb, '00 00 00')
    time_grapher(writer, 'msgID-00 00 00', hb, '00 00 00')
    stat_tabler(writer, 'msgID-00 00 00', hb, '00 00 00')
    for msg in list(msg_ids['Msg_ID'])[0:4]:
        data = clean.loc[clean['msgid [7:10]'] == msg]
        data['TIME_DELTA'] = data['FRAME_RELTIME'] - data['FRAME_RELTIME'].shift(1)
        data.to_excel(writer, sheet_name='msgID-'+msg)
        payload_grapher(writer, 'msgID-'+msg, data, msg)
        time_grapher(writer, 'msgID-'+msg, data, msg)
        stat_tabler(writer, 'msgID-'+msg, data, msg)


=======
with pd.ExcelWriter('results/intel_results_test.xlsx') as writer:
    clean.to_excel(writer, sheet_name='Parsed')
    occurances.to_excel(writer, sheet_name='Occurances')
>>>>>>> 23598fd066b78c745309480d9d18aaf5ea7d3244
