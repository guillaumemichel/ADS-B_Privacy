import requests
from convert import valid, n_to_icao, icao_to_n
import pickle
import sys
from os import listdir
from os.path import isfile, join
import urllib.request
from bs4 import BeautifulSoup

raw_storage_path = "../data/faa_registrations/raw/"
raw_cache = [f[:-5] for f in listdir(raw_storage_path) if isfile(join(raw_storage_path, f))]
filtered_storage_path = "../data/faa_registrations/filtered/"
filtered_cache = [f[:-4] for f in listdir(filtered_storage_path) if isfile(join(filtered_storage_path, f))]

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

def print_dict(data, pos=0):

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
        print(e+' : '+' '*(maxi-len(e))+str(data[e]))

def save_dict(obj, name ):
    with open(filtered_storage_path+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dict(name ):
    with open(filtered_storage_path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def scrape_individual(nnumber):

    # checking that the N-Number is correct
    if not valid(nnumber):
        print('Invalid N-Number: '+nnumber)
        sys.exit()

    if nnumber in filtered_cache:
        return load_dict(nnumber)
    elif nnumber in raw_cache:
        f = open(raw_storage_path+nnumber+'.html', 'r')
        response = f.read()
        f.close()
    else:
        url = 'http://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?NNumbertxt='+nnumber
        response = requests.get(url).text
        f = open(raw_storage_path+nnumber+'.html', 'w')
        f.write(response)
        f.close()

    soup = BeautifulSoup(response, "html.parser")

    # Record type
    data = dict()
    data['N-Number']=nnumber
    for (entry, id_) in fields:
        t = soup.find(id=id_)
        if t is not None and len(t.text.strip()) > 0:
            data[entry]=t.text.strip()

    save_dict(data, nnumber)
    return data

def scrape_range(initial, length):
    valid = True
    if initial is None:
        valid = False
    initial = initial.upper()
    if initial[0] == 'A': # icao
        icao = initial
    elif initial[0] == 'N': # nnumber
        icao = n_to_icao(initial)
    else:
        valid = False

    if icao is None:
        valid = False

    if not valid:
        print('Invalid parameter "initial" passed to scrape_range()')
        sys.exit()

    print('Starting to scrape from '+icao_to_n(icao)+' to '+icao_to_n(hex(int(icao, base=16)+length-1)[2:]))

    all_data = dict()
    reg_type = dict()
    for i in range(length):
        icao = hex(int(icao, base=16)+1)[2:]
        nnumber = icao_to_n(icao)
        data = scrape_individual(nnumber)
        all_data[nnumber] = data
        if 'Registration' in data:
            reg = data['Registration'][len(nnumber)+1:]
            if 'Not Assigned' in reg:
                reg = 'Not Assigned'
            elif 'Assigned' in reg:
                reg='Assigned'
            elif 'Reserved' in reg:
                reg = 'Reserved'
            elif 'Deregistered' in reg:
                reg = 'Deregistered'
        else:
            reg = 'Attention'

        if reg == 'Reserved':
            if reg not in reg_type:
                reg_type[reg] = dict()
            if data['Type Reservation'] not in reg_type[reg]:
                reg_type[reg][data['Type Reservation']]=list()
            if 'Reserving Party Name' in data:
                reg_type[reg][data['Type Reservation']].append((nnumber,data['Reserving Party Name']=='SBS PROGRAM OFFICE'))
            else:
                reg_type[reg][data['Type Reservation']].append((nnumber,False))
        else:
            if reg not in reg_type:                
                reg_type[reg] = list()
            reg_type[reg].append(nnumber)

        total = 60
        perc = int(total * i / length)
        print('|'+'█'*(perc)+' '*(total-perc-1)+'|'+' '+str(i+1)+'/'+str(length)+' '*5+nnumber,end='\r')

    print('|'+'█'*(total)+'|'+' '+str(i+1)+'/'+str(length)+' '*5+'Done!',end='\n')
    #print_dict(reg_type)

    # printing array
    counter = 0
    for r in reg_type:
        if r == 'Reserved':
            c = 0
            string = ""
            for d in reg_type[r]:
                string += "  " + d + " [" + str(len(reg_type[r][d])) + "] : "
                for (e1,e2) in reg_type[r][d]:
                    if e2:
                        string += "\x1b[32m"+e1+"\x1b[0m"+ ", "
                        counter += 1
                    else:
                        string += e1+ ", "
                    c+=1
                string = string[:-2]+'\n'
            string = r + " ["+str(c)+"]:\n"+string[:-1]
            print(string)
        else:
            string = r + " [" + str(len(reg_type[r])) + "] : "
            for e in reg_type[r]:
                string += e + ", "
            string = string[:-2]
            print(string)

    print(counter)

if __name__ == "__main__":
    scrape_range('N4100', 9100)