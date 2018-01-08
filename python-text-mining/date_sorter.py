import re
import sys
from pprint import pprint
import pandas as pd

import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)

"""
doc = []
for line in sys.stdin:
    doc.append(line)
"""



def date_sorter():
    all_months = {'jan': '01',
              'feb': '02',
              'mar': '03',
              'apr': '04',
              'may': '05',
              'jun': '06',
              'jul': '07',
              'aug': '08',
              'sep': '09',
              'oct': '10',
              'nov': '11',
              'dec': '12'}

    def cleanup(inp):
        inp = inp.replace('.', ' ')
        inp = inp.replace(',', ' ')
        inp = inp.replace('-', ' ')
        inp = inp.replace('th', '')
        inp = inp.replace('st', '')
        inp = inp.replace('nd', '')
        inp = inp.lower()
        return inp

    # 04/20/2009; 04/20/09; 4/20/09; 4/3/09 
    p1 = r'(\d{1,2}[/-]\d{1,2}[/|-]\d{2,4})'
    def f1(inp):
        inp = inp.replace('-', '/')
        month, day, year = inp.split('/')
        if len(year) == 2: year = '19%s'%year
        month = int(month)
        day = int(day)
        return '%s-%02d-%02d'%(year, month, day)

    # Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009; 
    p2 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z\s\.\-]*\d{1,2}\b[\s|\.|\-|,]*\d{2,4})'
    def f2(inp):
        inp = cleanup(inp)
        month, day, year = inp.split()
        day = int(day)
        month = all_months[month[:3]]
        return '%s-%s-%02d'%(year, month, day)

    # 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009 
    p3 = r'((?:\d{1,2}\b)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z\s\.\-,]*\d{4})'
    def f3(inp):
        inp = cleanup(inp)
        day, month, year = inp.split()
        day = int(day)
        month = all_months[month[:3]]
        return '%s-%s-%02d'%(year, month, day)

    # Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009 
    p4 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z\s\.\-]*\d{1,2}(th|st|nd)(?:\s|\.|\-|,)*\d{2,4})'
    def f4(inp):
        return f2(inp)

    # Feb 2009; Sep 2009; Oct 2010 
    p5 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b[\s\.\-,]*\d{2,4})'
    def f5(inp):
        inp = f'01 {inp}'
        return f3(inp)

    # 6/2008; 12/2009 
    p6 = r'(\d{1,2}/\d{2,4})'
    def f6(inp):
        month, year = inp.split('/')
        inp = f'{month}/1/{year}'
        return f1(inp)

    # 2009; 2010
    p7 = r'(\d{4})'
    def f7(inp):
        inp = f'1/1/{inp}'
        return f1(inp)

    dates = []
    pats = [p1, p2, p3, p4, p5, p6, p7]
    fmts = [f1, f2, f3, f4, f5, f6, f7]

    #for line in doc:
    for line in df:
        line = line.strip()
        date = None
        #print('\nline: ', line)
        for idx, p in enumerate(pats):
            m = re.search(p, line)
            if m:
                date = m.group(1)
                #print(f'pre-fmt: {date}')
                func = fmts[idx]
                date = func(date)
                dates.append(date)
                #print(f'post-fmt: {date}')
                break
        if not date:
            print(f'line not matched!')
            dates.append(None)
    print('total: ', len(dates))

    # 
    dates = [(idx, date) for idx, date in enumerate(dates)]
    dates.sort(key=lambda x: x[1])
    indices = [x[0] for x in dates]
    print(indices)
    indices = pd.Series(indices)
    return indices


######################
print(date_sorter())

