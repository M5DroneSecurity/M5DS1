
from xml.dom import minidom

'''
Function that parses through each field and returns an occurance count of data within each field
@input: 
@output: 
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

# print(list(fieldcounter(msgid).keys()))


'''
Function that compares the msgid to the common_messages.xml to find the msg_type
@input: msg_id
@output: msg_type
'''
def message_decoder(msgid):
    ''' grab msgid as str '''
    m = msgid.replace(" ", "")

    ''' str -> hex -> int -> str '''
    m = bytearray.fromhex(m)
    m.reverse()
    m = int.from_bytes(m, byteorder='big', signed=False)
    m = str(m).lstrip()

    ''' Compare to XML '''
    xml_source = './Includes/common_messages.xml'
    # print("Grabbing XML: " + xml_source)
    common = minidom.parse(xml_source).getElementsByTagName('message')
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