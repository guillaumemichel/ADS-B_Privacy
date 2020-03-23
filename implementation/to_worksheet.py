from flights import Flights
from openpyxl.workbook import Workbook
from openpyxl.styles import Alignment

from os import listdir
from os.path import isfile, join

mypath = '../data/flight_lists/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

wb = Workbook()
wb.remove(wb.active)

for f in files:
    month = f.split('.')[0]

    allFlights = Flights()
    allFlights.from_file(mypath+f)

    ws = wb.create_sheet(month)
    ws.title = month

    row0 = 1
    row_title = row0
    row_desc = row_title + 1
    row_unit = row_desc + 1
    row_data = row_unit + 1

    col0 = 1
    col_icao = col0
    col_callsign = col_icao + 1
    col_nnumber = col_callsign + 1

    col_dep_ap = col_nnumber + 1
    col_dep_time = col_dep_ap + 1
    col_dep_ap_pos_lat = col_dep_time + 1
    col_dep_ap_pos_lon = col_dep_ap_pos_lat + 1
    col_dep_ap_pos_alt = col_dep_ap_pos_lon + 1
    col_dep_ac_pos_lat = col_dep_ap_pos_alt + 1
    col_dep_ac_pos_lon = col_dep_ac_pos_lat + 1
    col_dep_ac_pos_alt = col_dep_ac_pos_lon + 1

    col_arr_ap = col_dep_ac_pos_alt + 1
    col_arr_time = col_arr_ap + 1
    col_arr_ap_pos_lat = col_arr_time + 1
    col_arr_ap_pos_lon = col_arr_ap_pos_lat + 1
    col_arr_ap_pos_alt = col_arr_ap_pos_lon + 1
    col_arr_ac_pos_lat = col_arr_ap_pos_alt + 1
    col_arr_ac_pos_lon = col_arr_ac_pos_lat + 1
    col_arr_ac_pos_alt = col_arr_ac_pos_lon + 1

    col_last = col_arr_ac_pos_alt + 1

    ws.merge_cells(start_row=row_title, end_row=row_title, start_column=col_icao, end_column=col_nnumber)
    ws.cell(row=row_title, column=col_icao).value = 'Identification Numbers'
    ws.cell(row=row_title, column=col_icao).alignment = Alignment(horizontal='center')
    ws.cell(row=row_desc,column=col_icao).value = 'ICAO24'
    ws.cell(row=row_desc,column=col_callsign).value = 'Callsign'
    ws.cell(row=row_desc,column=col_nnumber).value = 'N-Number'

    ws.merge_cells(start_row=row_title, end_row=row_title, start_column=col_dep_ap, end_column=col_dep_ac_pos_alt)
    ws.cell(row=row_title, column=col_dep_ap).value = "Departure"
    ws.cell(row=row_title, column=col_dep_ap).alignment = Alignment(horizontal='center')
    ws.cell(row=row_desc,column=col_dep_ap).value = 'Departure Airport'
    ws.cell(row=row_unit,column=col_dep_ap).value = 'ICAO number'
    ws.cell(row=row_desc,column=col_dep_time).value = 'Departure Time'
    ws.cell(row=row_unit,column=col_dep_time).value = 'YYYY-MM-DD HH:MM:SS'

    ws.merge_cells(start_row=row_desc, end_row=row_desc, start_column=col_dep_ap_pos_lat, end_column=col_dep_ap_pos_alt)
    ws.cell(row=row_desc,column=col_dep_ap_pos_lat).value = 'Departure Airport Positon'
    ws.cell(row=row_desc,column=col_dep_ap_pos_lat).alignment = Alignment(horizontal='center')
    ws.cell(row=row_unit,column=col_dep_ap_pos_lat).value = 'Latitude'
    ws.cell(row=row_unit,column=col_dep_ap_pos_lon).value = 'Longitude'
    ws.cell(row=row_unit,column=col_dep_ap_pos_alt).value = 'Altitude'

    ws.merge_cells(start_row=row_desc, end_row=row_desc, start_column=col_dep_ac_pos_lat, end_column=col_dep_ac_pos_alt)
    ws.cell(row=row_desc,column=col_dep_ac_pos_lat).value = 'First Aircraft Positon'
    ws.cell(row=row_desc,column=col_dep_ac_pos_lat).alignment = Alignment(horizontal='center')
    ws.cell(row=row_unit,column=col_dep_ac_pos_lat).value = 'Latitude'
    ws.cell(row=row_unit,column=col_dep_ac_pos_lon).value = 'Longitude'
    ws.cell(row=row_unit,column=col_dep_ac_pos_alt).value = 'Altitude'

    ws.merge_cells(start_row=row_title, end_row=row_title, start_column=col_arr_ap, end_column=col_arr_ac_pos_alt)
    ws.cell(row=row_title, column=col_arr_ap).value = "Arrival"
    ws.cell(row=row_title, column=col_arr_ap).alignment = Alignment(horizontal='center')
    ws.cell(row=row_desc,column=col_arr_ap).value = 'Arrival Airport'
    ws.cell(row=row_unit,column=col_arr_ap).value = 'ICAO number'
    ws.cell(row=row_desc,column=col_arr_time).value = 'Departure Time'
    ws.cell(row=row_unit,column=col_arr_time).value = 'YYYY-MM-DD HH:MM:SS'

    ws.merge_cells(start_row=row_desc, end_row=row_desc, start_column=col_arr_ap_pos_lat, end_column=col_arr_ap_pos_alt)
    ws.cell(row=row_desc,column=col_arr_ap_pos_lat).value = 'Arrival Airport Positon'
    ws.cell(row=row_desc,column=col_arr_ap_pos_lat).alignment = Alignment(horizontal='center')
    ws.cell(row=row_unit,column=col_arr_ap_pos_lat).value = 'Latitude'
    ws.cell(row=row_unit,column=col_arr_ap_pos_lon).value = 'Longitude'
    ws.cell(row=row_unit,column=col_arr_ap_pos_alt).value = 'Altitude'

    ws.merge_cells(start_row=row_desc, end_row=row_desc, start_column=col_arr_ac_pos_lat, end_column=col_arr_ac_pos_alt)
    ws.cell(row=row_desc,column=col_arr_ac_pos_lat).value = 'Last Aircraft Positon'
    ws.cell(row=row_desc,column=col_arr_ac_pos_lat).alignment = Alignment(horizontal='center')
    ws.cell(row=row_unit,column=col_arr_ac_pos_lat).value = 'Latitude'
    ws.cell(row=row_unit,column=col_arr_ac_pos_lon).value = 'Longitude'
    ws.cell(row=row_unit,column=col_arr_ac_pos_alt).value = 'Altitude'

    for i in range(col0, col_last):
        ws.column_dimensions[chr(ord('A')-col0+i)].width = 15
    ws.column_dimensions[chr(ord('A')-col0+col_dep_time)].width = 19
    ws.column_dimensions[chr(ord('A')-col0+col_arr_time)].width = 19

    for f in allFlights.elements:
        ws.cell(row=row_data, column=col_icao).value = f.icao.strip()
        ws.cell(row=row_data, column=col_callsign).value = f.callsign.strip()
        if 'None' not in f.nnumber:
            ws.cell(row=row_data, column=col_nnumber).value = f.nnumber

        if 'None' not in f.departure.airport:
            ws.cell(row=row_data, column=col_dep_ap).value = f.departure.airport
        ws.cell(row=row_data, column=col_dep_time).value = f.departure.time[:19]
        if f.departure.airport_position is not None:
            ws.cell(row=row_data, column=col_dep_ap_pos_lat).value = f.departure.airport_position.latitude
            ws.cell(row=row_data, column=col_dep_ap_pos_lon).value = f.departure.airport_position.longitude
            ws.cell(row=row_data, column=col_dep_ap_pos_alt).value = f.departure.airport_position.altitude
        if f.departure.aircraft_position is not None:
            ws.cell(row=row_data, column=col_dep_ac_pos_lat).value = f.departure.aircraft_position.latitude
            ws.cell(row=row_data, column=col_dep_ac_pos_lon).value = f.departure.aircraft_position.longitude
            ws.cell(row=row_data, column=col_dep_ac_pos_alt).value = f.departure.aircraft_position.altitude


        if 'None' not in f.arrival.airport:
            ws.cell(row=row_data, column=col_arr_ap).value = f.arrival.airport
        ws.cell(row=row_data, column=col_arr_time).value = f.arrival.time[:19]
        if f.arrival.airport_position is not None:
            ws.cell(row=row_data, column=col_arr_ap_pos_lat).value = f.arrival.airport_position.latitude
            ws.cell(row=row_data, column=col_arr_ap_pos_lon).value = f.arrival.airport_position.longitude
            ws.cell(row=row_data, column=col_arr_ap_pos_alt).value = f.arrival.airport_position.altitude
        if f.arrival.aircraft_position is not None:
            ws.cell(row=row_data, column=col_arr_ac_pos_lat).value = f.arrival.aircraft_position.latitude
            ws.cell(row=row_data, column=col_arr_ac_pos_lon).value = f.arrival.aircraft_position.longitude
            ws.cell(row=row_data, column=col_arr_ac_pos_alt).value = f.arrival.aircraft_position.altitude

        row_data += 1

wb.save('../data/sheets/flights.xlsx')