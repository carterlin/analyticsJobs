#! /usr/bin/python

'''
Carter Lin
8/27/2014

Required packages: 
- pandas: http://pandas.pydata.org/ 
- indeed-python: https://github.com/indeedlabs/indeed-python

Required varialbe:
- Indeed.com publisher number

Script usage:
> python jobSearch.py [searchKeywords]

Output:
- jobAnalysis file
'''

import sys
import pandas as pd
from indeed import IndeedClient


# set up API
publisher = '' # Indeed.com publisher number
client = IndeedClient(publisher)

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

numSearchItems = 2000;

def jobSearch(keyword):
    df = pd.DataFrame()
    for s in states:
        for i in range(0,numSearchItems,25):
            params = {
                'q' : keyword,
                'l' : s,
                'userip' : "1.2.3.4",
                'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)", 
                'start' : str(i),
                'filter': '1',
                'limit' : '25',
                'latlong': '1',
                'v': '2'}
            search_response = client.search(**params)
            df = df.append(pd.DataFrame(search_response['results']))
            
    # delete unnessary columns in the data
    names = ['sponsored', 'formattedLocationFull', 'indeedApply', 'formattedLocation', 'expired', 'onmousedown', 'formattedRelativeTime', 'source', 'snippet']
    
    for name in names:
        del df[name]
    
    df = df.drop_duplicates(subset='jobkey')
    
    # convert date time and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort('date',ascending=False)

    outputFileName = keyword.replace('+','_') + '_raw.csv'
    df.to_csv(outputFileName, encoding='utf-8', index=False)


def main():
    if len(sys.argv) == 1:
	    print 'Command error: please type in search keyword(s)'
    elif len(sys.argv) == 2:
	    keyword = sys.argv[1]
	    jobSearch(keyword)
    else:
	    print 'Command error: too many arguments'
    
if __name__ == '__main__':
    main()
