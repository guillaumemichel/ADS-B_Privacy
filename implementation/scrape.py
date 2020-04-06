import requests
from os import listdir
from os.path import isfile, join
import urllib.request
from bs4 import BeautifulSoup

storage_path = "../data/faa_registrations/"
cache = [f[:-5] for f in listdir(storage_path) if isfile(join(storage_path, f))]
print(cache)

nnumber = 'N628CC'

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
for e in soup.find_all('span'):
    print(e)
    print()
"""

print(data)