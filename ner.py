import re
import os
import sys

LOCATIONS = []
entries = os.listdir('locations/')

for entry in entries:

    file = "locations/" + entry
    f = open(file, mode='r')
    for line in f:
        if line != "\n":
            line = line.rstrip("\n")
            LOCATIONS.append(line)
    f.close()

ORGANIZATIONS = []
entries = os.listdir('organizations/')

for entry in entries:
    if entry != 'kurumlar':

        file = "organizations/" + entry
        f = open(file, mode='r')
        for line in f:
            if line != "\n":
                line = line.rstrip("\n")
                ORGANIZATIONS.append(line)
        f.close()

file = "organizations/kurumlar"
f = open(file, mode='r')
for line in f:
    if line != "\n":
        words = line.split(' ', maxsplit=1)
        for word in words:
            word = word.rstrip("\n")
            ORGANIZATIONS.append(word)
f.close()

inda= ORGANIZATIONS.index('TÜRKİYE')
ORGANIZATIONS.__delitem__(inda)

PERSON = []
entries = os.listdir('person/')

for entry in entries:

    file = "person/" + entry
    f = open(file, mode='r')
    for line in f:
        if line != "\n":
            line = line.rstrip("\n")
            for word in line.split():
                PERSON.append(word)
                break

    f.close()
el_No = 0
for element in PERSON:
    element = element.rstrip(":")
    PERSON[el_No] = element
    el_No += 1

inFile = sys.argv[1]
with open(inFile,'r') as i:
    lines = i.readlines()


months = ['Aralık', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım']


def date(line, lineNo):
    printd = []
    if 'yıl' in line:
        str = re.findall(r'\d{4}(?=\syıl[a-zçğıöşü]+)', line)
        for index in str:
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "TIME", index)
    if 'ay' in line:
        str = re.findall(r'\d{0,2} [A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?=\say[a-zçğıöşü]+)', line)
        for index in str:
            if index in months:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "TIME", index)
    if 'tarih' in line:
        str = re.findall(r'\d{1,2}\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s\d{4}(?=\starih[a-zçğıöşü]*)*', line)
        for index in str:
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "TIME", index)
    if re.search(r'\d{1,2}\/+\d{1,2}\/+\d{4}', line):
        str = re.findall(r'\d{1,2}\/+\d{1,2}\/+\d{4}', line)
        for index in str:
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "TIME", index)
    if re.search(r'\d{1,2}\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s\d{4}', line):
        str = re.findall(r'\d{1,2}\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s\d{4}', line)
        for index in str:
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "TIME", index)
    if re.search(r'(?<!\d\s)[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[0-9]{4}', line):
        str = re.findall(r'(?<!\d\s)[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[0-9]{4}', line)
        for index in str:
            if index.split()[0] in months:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "TIME", index)
    if re.search(r'\d{4}\'\w+', line):
        str = re.findall(r'\d{4}\'\w+', line)
        for index in str:
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "TIME", index)


lineNo = 0
for line in lines:
    lineNo += 1


    printd = []
    if 'Üniversite' in line:
        # 1 word uni
        str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* Üniversite\w+', line)
        for index in str:
            if index in ORGANIZATIONS:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)
        # 2 word uni
        str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* Üniversite\w+', line)
        for index in str:
            if index in ORGANIZATIONS:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)

        # 3 word uni
        str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* Üniversite\w+', line)
        for index in str:
            if index in ORGANIZATIONS:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)

    # KISALTMA KURUMLAR
    if re.search(r'[A-ZÇĞİÖŞÜ]{2,}', line):
        str = re.findall(r'[A-ZÇĞİÖŞÜ]{2,}', line)
        for index in str:
            if index in ORGANIZATIONS:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)

    # TARİH
    date(line, lineNo)

    # Holding, Vakfı, Federasyonu
    organization_list = ['Holding', 'Vakfı', 'Federasyonu', 'Bankası', 'Örgütü',
                         'Teşkilatı', 'Birliği', 'Başkanlığı', 'Müdürlüğü', 'Komisyonu', 'Kurumu',
                         'Merkezi', 'Meclisi', 'Kurulu', 'Enstitüsü', 'Konfederasyonu', 'Partisi', 'Bürosu', 'Müsteşarlığı']

    for word in organization_list:
        if word in line:
            # 1 word uni
            str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* ' + word,
                             line)
            for index in str:
                if index in ORGANIZATIONS:
                    if index not in printd:
                        printd.append(index)
                        print("Line ",lineNo,": ", "ORGANIZATION", index)
                        break
            str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* [A-ZÇĞİÖŞÜ][a-zçğıöşü]* ' + word, line)
            for index in str:
                index = index.rstrip()
                if index in ORGANIZATIONS:
                    if index not in printd:
                        printd.append(index)
                        print("Line ",lineNo,": ", "ORGANIZATION", index)
                        break

            str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* '+word, line)
            for index in str:
                if index in ORGANIZATIONS:
                    if index not in printd:
                        printd.append(index)
                        print("Line ",lineNo,": ", "ORGANIZATION", index)
                        break



            # 3 word uni


    # BEY; HANIM
    unvans = ['Bey', 'Hanım', 'Abi', 'Hoca', 'Baba', 'Abla', 'Amca', 'Nine', 'Ana', 'Anne']
    line = line.rstrip("\n")
    for un in unvans:
        if re.search(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?= ' + un + ')', line):
            str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?= ' + un + ')', line)
            for index in str:
                if index in PERSON:
                    if index not in printd:
                        printd.append(index)
                        print("Line ", lineNo,": ", "PERSON", index)
                elif index not in PERSON:
                    index_format = index.upper()
                    if index_format in PERSON:
                        if index not in printd:
                            printd.append(index)
                            print("Line ",lineNo,": ", "PERSON", index)

    # Cumhurbaşkanı,  Sevgili
    baskans = ['Cumhurbaşkanı', 'Belediye Başkanı', 'Vali', 'Kaymakam', 'Başkanı', 'Müdür[a-zçğıöşü]',
               'Müdür Yardımcısı',
               'Müdiresi', 'Bakanı', 'Prof\. Dr\.', 'Dr\.', 'Av\.', 'Bşk\.', 'Dt\.', 'Uzm\.', 'Yard\. Doç\.', 'Sayın',
               'Sevgili', 'Değerli']
    line = line.rstrip("\n")

    for baskan in baskans:
        if re.search(r'(?<=' + baskan + ' )([A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)+', line):
            threebool = False
            # 3 name
            str = re.findall(
                r'(?<=' + baskan + ' )([A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)+',
                line)
            for index in str:
                threebool = True
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "PERSON", index)

            # 2 name
            if threebool is False:
                str = re.findall(
                    r'(?<=' + baskan + ' )([A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*)+', line)
                for index in str:
                    if index not in printd:
                        printd.append(index)
                        print("Line ",lineNo,": ", "PERSON", index)

    lokasyon = ['Köyü', 'Dağı', 'Gölü', 'Mahallesi', 'Sokağı', 'Sok.', 'Caddesi', 'Cad.', 'Bulvarı', 'Bulv.',
                'Stadyumu', 'Stadı', 'Arena', 'Sokak', 'Sitesi']
    for loc in lokasyon:
        if re.search(r'[A-ZÇĞİÇŞÜ][a-zçğıöşü]* ' + loc + '\W', line):
            str = re.findall(r'[A-ZÇĞİÇŞÜ][a-zçğıöşü]* ' + loc + '\W', line)
            for index in str:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "LOCATION", index)

    sehir = ['il', 'ilçe', 'Cumhuriyeti', 'Devleti', 'Prensliği', 'Krallığı', 'bölgesi']
    for s in sehir:
        if re.search(r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]*){1,3}(?= ' + s + '[a-zçğıöşü]+)', line):
            str = re.findall(r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]*){1,3}(?= ' + s + '[a-zçğıöşü]+)', line)
            for index in str:
                if index in LOCATIONS:
                    if index not in printd:
                        printd.append(index)
                        print("Line ",lineNo,": ", "LOCATION", index)
                elif index not in LOCATIONS:
                    index = index.upper()
                    if index in LOCATIONS:
                        if index not in printd:
                            printd.append(index)
                            print("Line ",lineNo,": ", "LOCATION", index)
                    else:
                        if index not in printd:
                            printd.append(index)
                            print("Line ",lineNo,": ", "LOCATION", index)

    bridge = ['Saray', 'köprü', 'Mezarlığı', 'Köprü', 'Cumhuriyeti', 'Devleti', 'Prensliği', 'Krallığı', 'Havalimanı']
    for b in bridge:
        if re.search(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* ' + b + '[a-zçğıöşü]*', line):
            str = re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* ' + b + '[a-zçğıöşü]*', line)
            for index in str:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "LOCATION", index)

    if re.search(r'(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* ){1,3}(A\.Ş\.|LTD\.|Ltd\. Şti\.))+', line):
        thebool=False
        str = re.findall(r'([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* [A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* [A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* )+(A\.Ş\.|LTD\.|Ltd\. Şti\.)', line)
        for index in str:
            thebool=True
            if index not in printd:
                printd.append(index)
                print("Line ",lineNo,": ", "ORGANIZATION", index)

        if thebool is False:
            str = re.findall(
                r'([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* [A-ZÇĞİÖŞÜ]+[a-zçğıöşü]* )+(A\.Ş\.|LTD\.|Ltd\. Şti\.)',line)
            for index in str:
                if index not in printd:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)

    #2 word özel isim
    if re.search(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ [A-ZÇĞİÖŞÜ][a-zçğıöşü]+',line):
        str=re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ [A-ZÇĞİÖŞÜ][a-zçğıöşü]+',line)
        for index in str:
            indexo = index.split()
            if index not in printd:
                if index in LOCATIONS:
                    printd.append(index)
                    print("Line ",lineNo,": ", "LOCATION", index)
                elif index in ORGANIZATIONS:
                    printd.append(index)
                    print("Line ",lineNo,": ", "ORGANIZATION", index)

                elif indexo[0] in PERSON and indexo[1] not in baskans:
                    print("Line ",lineNo,": ", "PERSON", index)
                    printd.append(index)

    if re.search(r'[A-ZÇĞİÖŞÜ][a-zçığöşü]*(?= \'[a-zçğiöşü]+)',line):
        str= re.findall(r'[A-ZÇĞİÖŞÜ][a-zçığöşü]*(?= \'[a-zçğiöşü]+)',line)
        for index in str:
            if index not in printd:
                if index in LOCATIONS:
                    print("Line ",lineNo,": ", "LOCATION", index)
                    printd.append(index)






