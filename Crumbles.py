import csv
import random
import rstr
import hashlib, binascii


##### source file is g.csv and the results shall be in results.csv #####
##### choose method #####

def crumble_string(s):
    sl = list(s)
    random.shuffle(sl)
    afterlist = []
    for i in sl:
        afterlist.append(i)
    afterstring = ''.join(afterlist)
    return afterstring

def generate_regex():
    regi = input("regex: ")
    gen = rstr.xeger(regi)
    return gen


f = open('g.csv')
csv_f = csv.reader(f, delimiter=',')
head = next(csv_f)


with open('results.csv', 'w', newline='') as output:
    output_data = csv.writer(output)
    output_data.writerow(head)
    columns = len(head)
    print(columns)


##### Get modes for each column and regex if needed. create modes list and regex list #####

    regexeslist = []
    modeslist=[]
    for column in range(columns):
        crumble = input("mode for column " + head[column] + " (string shuffle - s, generate regex - g, leave as is - l, last digits hash -h ): ")
        if crumble == 'g':
            regi = input("regex for column " + head[column] + ": ")
            regexeslist.append(regi)
        if crumble == 'h':
            digits = input("Number of last digits to change in " + head[column] + ": ")
            regexeslist.append(0)
        if crumble == 's':
            regexeslist.append(0)
        modeslist.append(crumble)

##### iterate rows, check for each column the requested mode, and create list for each row to wright in the resultset #####

    uu = []
    for row in csv_f:
        for column in range(columns):
            if modeslist[column] == 'g':
                regtodo = regexeslist[column]
                res = rstr.xeger(str(regtodo))
                uu.append(res)
            if modeslist[column] == 's':
                res = crumble_string(str(row[column]))
                uu.append(res)
            if modeslist[column] == 'c':
                uu.append(str(row[column]))
                #change --- uu[column], uu[column + 1] = uu[column+1], uu[column]
            if modeslist[column] == 'l':
                uu.append(str(row[column]))
            if modeslist[column] == 'h':
                ##### in order to keep the original statistics relations between items in the data, we hashed the last 4 digits and took the 4 digits of the results
                digits = int(digits)
                word = str(row[column])
                dighash = word[-digits:]
                rest = word[:-digits]
                t = bytes(str(dighash), encoding='utf8')
                dk = hashlib.pbkdf2_hmac('sha256', t, b'lolo', 100000)
                resi = binascii.hexlify(dk)
                resi2 = resi.decode("utf-8")
                digres = resi2[-digits:]
                hh = rest+digres
                uu.append(hh)
        output_data.writerow(uu)
        uu[:] = []


#regex for example:
#cve-\d{4}-\d{4} (CSV)
#((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?) (IP)
#(?:[a-zA-Z0-9]+)? (Sentence)