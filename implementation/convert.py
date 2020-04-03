import sys

charset = "ABCDEFGHJKLMNPQRSTUVWXYZ"
digitset = "0123456789"
hexset = "0123456789ABCDEF"
allchars = charset+digitset

suffix_size = 1 + len(charset) + len(charset)*len(charset) # 601
bucket4_size = 1 + len(charset) + len(digitset) # 35
bucket3_size = len(digitset)*bucket4_size + suffix_size # 951
bucket2_size = len(digitset)*(bucket3_size) + suffix_size # 10111
bucket1_size = len(digitset)*(bucket2_size) + suffix_size # 101711

def get_suffix(i):
    if i==0:
        return ''
    char0 = charset[int((i-1)/(len(charset)+1))]
    rem = (i-1)%(len(charset)+1)
    if rem==0:
        return char0
    return char0+charset[rem-1]

def n_to_icao(nnumber):
    if nnumber[0] != 'N':
        return None
    
    return ''

def icao_to_n(icao):
    icao = icao.upper()
    valid = True
    if len(icao) != 6 or icao[0] != 'A':
        valid = False
    else:
        for c in icao:
            if c not in hexset:
                valid = False
            
    if not valid:
        return None

    output = 'N'

    i = int(icao[1:], base=16)-1 # parse icao to int
    if i < 0:
        return output

    dig1 = int(i/bucket1_size) + 1 # first digit
    rem1 = i%bucket1_size
    output += str(dig1)

    if rem1 < suffix_size:
        return output + get_suffix(rem1)

    rem1 -= suffix_size
    dig2 = int(rem1/bucket2_size)
    rem2 = rem1%bucket2_size
    output += str(dig2)

    if rem2 < suffix_size:
        return output + get_suffix(rem2)

    rem2 -= suffix_size
    dig3 = int(rem2/bucket3_size)
    rem3 = rem2%bucket3_size
    output += str(dig3)

    if rem3 < suffix_size:
        return output + get_suffix(rem3)

    rem3 -= suffix_size
    dig4 = int(rem3/bucket4_size)
    rem4 = rem3%bucket4_size
    output += str(dig4)

    if rem4 == 0:
        return output
    return output + allchars[rem4-1]

def print_help():
    print('Help:')

def invalid_parameter():
    print("Invalid parameter, N-Number should start with N..., Icao should start with a...")
    print_help()

if __name__ == "__main__":
    if len(sys.argv)-1 != 1:
        print("Please give me a N-Number or Icao to translate")
        print_help()
        sys.exit()

    val = sys.argv[1].upper()

    # debug
    if val[0] == 'I':
        val = 'A' + ('00000' + hex(int(val[1:]))[2:])[-5:]
        print(val)
    
    if val[0] == 'N': # N-Number
        pass
    elif val[0] == 'A': # icao
        nnumber = icao_to_n(val)
        if nnumber is None:
            invalid_parameter()
        print(nnumber)
    else:
        invalid_parameter()
