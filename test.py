from requests import Session
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import smtplib


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def writefile(filename, txt):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(txt)
    f.close()

def readfile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        rez = f.read()
    f.close()
    return rez

def getinfo():
    session = Session()
    session.head('https://www.aviaperm.ru/passengers/information/timetable/')

    response = session.post(
        url='https://www.aviaperm.ru/ajax/ttable.php',
        data={
        "day": "tomorrow",
        "items_count": "0",
        "rel": "departure"
        },
        headers={
            'Referer': 'https://www.aviaperm.ru/passengers/information/timetable/'
        }
    )
    return response.text

def findtomorrow():
    txt=getinfo()
    # print(txt)
    # writefile('avia.html',txt)
    # txt=readfile('avia.html')
    soup = BeautifulSoup(txt, 'lxml')
    spans=soup.find_all('span',{'class':"tth-destination"})
    dest = set([span.get_text().strip('\n').strip().lower() for span in spans][1:])
    dest.add('шарм-эльшейх')
    print(dest)
    fnd=[]
    for s in ['[хургада','шарм-эль-шейх','марса-алам']:
        for l in dest:
            if similar(s,l)>0.75:
                fnd=fnd+[l]
            # print(s,l,similar(s,l))
    return ','.join(fnd)



city=findtomorrow()
print('-----',city)
