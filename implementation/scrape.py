import requests
from convert import valid
import sys
from os import listdir
from os.path import isfile, join
import urllib.request
from bs4 import BeautifulSoup

storage_path = "../data/faa_registrations/"
cache = [f[:-5] for f in listdir(storage_path) if isfile(join(storage_path, f))]

fields = [  ('Registration', 'ctl00_content_lbNNumberTitle'),
            ('Type Reservation', 'ctl00_content_lbResTypeReg'),
            ('Mode S Code', 'ctl00_content_lbResACReserveDate'),
            ('Reserved Date', 'ctl00_content_lbResACReserveDate'),
            ('Renewal Date', 'ctl00_content_lbResACRenewalDate'),
            ('Purge Date', 'ctl00_content_lbResACPurgeDate'),
            ('Pending Number Change', 'ctl00_content_lbResNNumForChange'),
            ('Date Change Authorized', 'ctl00_content_lbResDateChange'),
            ('Reserving Party Name', 'ctl00_content_lbResACOwnerName'),
            ('Street', 'ctl00_content_lbResACOwnerStreet'),
            ('City', 'ctl00_content_lbResACOwnerCity'),
            ('State', 'ctl00_content_lbResACOwnerState'),
            ('Zip Code', 'ctl00_content_lbResACOwnerZip'),
            ('County', 'ctl00_content_lbResACOwnerCounty'),
            ('Country', 'ctl00_content_lbResACOwnerCountry'),
            ('Serial Number', 'ctl00_content_lbSerialNo'),
            ('Status', 'ctl00_content_lbStatus'),
            ('Manufacturer', 'ctl00_content_lbMfrName'),
            ('Certificate Issue Date', 'ctl00_content_lbCertDate'),
            ('Model', 'ctl00_content_Label7'),
            ('Expiration Date', 'ctl00_content_Label9'),
            ('Type Aircraft', 'ctl00_content_Label11'),
            ('Type Engine', 'ctl00_content_lbTypeEng'),
            ('Pending Number Change', 'ctl00_content_Label13'),
            ('Dealer', 'ctl00_content_lbDealer'),
            ('Mode S Code (base 8 / oct)', 'ctl00_content_lbModeSCode'),
            ('MFR Year', 'ctl00_content_Label17'),
            ('Type Registration', 'ctl00_content_lbTypeReg'),
            ('Fractional Owner', 'ctl00_content_lbFacOwner'),
            ('Name', 'ctl00_content_lbOwnerName'),
            ('Street', 'ctl00_content_lbOwnerStreet'),
            ('City', 'ctl00_content_lbOwnerCity'),
            ('State', 'ctl00_content_lbOwnerState'),
            ('County', 'ctl00_content_lbOwnerCounty'),
            ('Zip Code', 'ctl00_content_lbOwnerZip'),
            ('Country', 'ctl00_content_lbOwnerCountry'),
            ('Engine Manufacturer', 'ctl00_content_lbEngMfr'),
            ('Classification', 'ctl00_content_lbClassification'),
            ('Engine Model', 'ctl00_content_lbEngModel'),
            ('Category', 'ctl00_content_lbCategory1'),
            ('A/W Date', 'ctl00_content_lbAWDate'),
            ('Exception Code', 'ctl00_content_Label26'),
        ]

nnumber = 'N628CI'

if not valid(nnumber):
    print('Invalid N-Number')
    sys.exit()

if nnumber in cache:
    f = open(storage_path+nnumber+'.html', 'r')
    response = f.read()
    f.close()
else:
    url = 'http://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?NNumbertxt='+nnumber
    response = requests.get(url).text
    f = open(storage_path+nnumber+'.html', 'w')
    f.write(response)
    f.close()

soup = BeautifulSoup(response, "html.parser")

# Record type
data = dict()
for (entry, id_) in fields:
    t = soup.find(id=id_)
    if t is not None:
        data[entry]=t.text.strip()

"""
data['Registration'] = soup.find(id='ctl00_content_lbNNumberTitle').text.strip()
data['Type Reservation'] = soup.find(id='ctl00_content_lbResTypeReg').text.strip()
data['Mode S Code'] = soup.find(id='ctl00_content_lbResModeSCode').text.strip()
data['Reserved Date'] = soup.find(id='ctl00_content_lbResACReserveDate').text.strip()
data['Renewal Date'] = soup.find(id='ctl00_content_lbResACRenewalDate').text.strip()
data['Purge Date'] = soup.find(id='ctl00_content_lbResACPurgeDate').text.strip()
data['Pending Number Change'] = soup.find(id='ctl00_content_lbResNNumForChange').text.strip()
data['Date Change Authorized'] = soup.find(id='ctl00_content_lbResDateChange').text.strip()
data['Reserving Party Name'] = soup.find(id='ctl00_content_lbResACOwnerName').text.strip()
data['Street'] = soup.find(id='ctl00_content_lbResACOwnerStreet').text.strip()
data['City'] = soup.find(id='ctl00_content_lbResACOwnerCity').text.strip()
data['State'] = soup.find(id='ctl00_content_lbResACOwnerState').text.strip()
data['ZIP Code'] = soup.find(id='ctl00_content_lbResACOwnerZip').text.strip()
data['County'] = soup.find(id='ctl00_content_lbResACOwnerCounty').text.strip()
data['Country'] = soup.find(id='ctl00_content_lbResACOwnerCountry').text.strip()
"""
"""
for e in soup.find_all('span'):
    print(e)
    print()
"""

# minimal lateral position for dictionary value
pos = 0

# get longest key
maxi = 0
for e in data:
    if len(e)>maxi:
        maxi=len(e)

# if longest key lenght is shorter than pos, use pos as value position
if maxi < pos:
    maxi = pos

# print dictionary
for e in data:
    print(e+' : '+' '*(maxi-len(e))+data[e])