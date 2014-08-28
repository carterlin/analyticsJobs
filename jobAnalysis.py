#! /usr/bin/python

'''
Carter Lin
8/27/2014

Required packages: 
- requests: http://docs.python-requests.org/en/latest/
- pandas: http://pandas.pydata.org/
- BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/

Script usage:
> python jobAnalysis.py [jobSearch csv file]

Output:
- jobAnalysis file
'''

from bs4 import BeautifulSoup
import sys
import requests
import pandas as pd

def jobAnalysis(fileName):  
	df = pd.read_csv(fileName)

	skillKeywords = ['excel', 'sql', 'mysql', 'python', 'java', 'c++','sas', 'matlab', 'php', 'perl', 'hadoop', 'hive', 'pig', 'mapreduce', 'tableau', 'javascript']
	skillKeywordsCap = ['SAS', 'SPSS']
	bachelorKeywords = ['BS', 'BA', 'Bachelor', 'bachelor']
	masterKeywords = ['MS', 'Master', 'master', 'M.S.']
	phdKeywords = ['PhD', 'phd', 'Ph.D.']

	# set up new columns in the dataframe
	for k in skillKeywords:
		df[k] = 0

	for k in skillKeywordsCap:
		df[k] = 0

	df['r'] = 0
	df['linux_unix'] = 0
	df['machine_learning'] = 0
	df['bachelor'] = 0
	df['master'] = 0
	df['phd'] = 0

	  
	# scan all rows and find matched attributes  
	for row in range(len(df)):
		page = requests.get(df['url'][row])
		soup = BeautifulSoup(page.text)
		summary = str(soup.find('span','summary'))
		summaryLowerCase = summary.lower()
		
		
		# skills
		for k in skillKeywords:
		    if summaryLowerCase.find(k) > 0:
		        df[k][row] = 1
		
		for k in skillKeywordsCap:
		    if summary.find(k) > 0:
		        df[k][row] = 1
		        
		if summaryLowerCase.find('linux') > 0 or summaryLowerCase.find('unix') > 0:
		    df['linux_unix'][row] = 1
		    
		if summaryLowerCase.find(' r,') > 0 or summaryLowerCase.find(' r ') > 0:
		    df['r'][row] = 1

		if summaryLowerCase.find('machine learning') > 0:
		    df['machine_learning'][row] = 1

		
		# degree         
		for k in bachelorKeywords:
		    if summary.find(k) > 0:
		        df['bachelor'][row] = 1
		        
		for k in masterKeywords:
		    if summary.find(k) > 0:
		        df['master'][row] = 1
		        
		for k in phdKeywords:
		    if summary.find(k) > 0:
		        df['phd'][row] = 1

	outputFileName = fileName[:-8] + '.csv'
	df.to_csv(outputFileName, encoding='utf-8', index=False)


def main():
    if len(sys.argv) == 1:
	    print 'Command error: please type in a file name'
    elif len(sys.argv) == 2:
	    fileName = sys.argv[1]
	    jobAnalysis(fileName)
    else:
	    print 'Command error: too many arguments'
    
if __name__ == '__main__':
    main()
