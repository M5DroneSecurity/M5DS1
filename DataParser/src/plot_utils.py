"""
Title: plot_utils.py
By: M5DS1
Description:
    Contains functions for graphing in excel
"""


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
    occur_chart = workbook.add_chart({'type': 'column'})

    ## Configure the series of the chart from the dataframe data
    indexList = list(data_['Occurrences'])
    r1 = 1
    r2 = len(indexList)
    occur_chart.add_series({
        'categories': [sheet_, r1, 1, r2, 1],
        'values': [sheet_, r1, 2, r2, 2],
        'data_labels': {'value': True}
    })

    ## Configure chart axis
    occur_chart.set_y_axis({'name': 'Number of Packets','major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }})
    occur_chart.set_x_axis({'name': 'Message ID', 'reverse':False})

    ## Title and Size
    occur_chart.set_title({'name': 'Occurrences by Msg_ID'})
    occur_chart.set_size({'width': 2400, 'height': 1000})

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
    r1 = 1
    r2 = len(indexList)
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
    r1 = 1
    r2 = len(indexList)
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
Function that graphs the normal distribution of time_delta for a given msgid
@input: writer, sheet, data
@output: 
'''
def density_grapher(writer_, sheet_, data_, msgid_):
    ## Access the Xlswriter workbook and worksheets objects from the dataframe.
    workbook = writer_.book
    worksheet = writer_.sheets[sheet_]

    ## Create a chart object
    density_chart = workbook.add_chart({'type': 'line'})

    ## Configure the series of the chart from the dataframe data
    indexList = list(data_['FRAME_RELTIME'])
    r1 = 1
    r2 = len(indexList)
    density_chart.add_series({
        'categories': [sheet_, r1, 1, r2, 1],
        'values': [sheet_, r1, 15, r2, 15]
    })

    ## Configure chart axis
    density_chart.set_x_axis({'name': 'time_delta (sec)',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    density_chart.set_y_axis({'name': 'Density',
                      'major_gridlines': {
                          'visible': True,
                          'line': {'width': 1, 'dash_type': 'dash'}
                      }
                      })
    density_chart.set_title({'name': 'Distribution for Msg ID-' + msgid_})
    # chart.set_chartarea({'border': {'none': True}})

    ## Turn off default legend
    density_chart.set_legend({'none': True})

    ## Insert chart into worksheet
    worksheet.insert_chart('S44', density_chart)


