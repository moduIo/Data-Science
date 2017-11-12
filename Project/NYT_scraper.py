######
# Implementation of a scraper using the NYT API.
######
import sys
import csv
import requests
import json
import time
import re

year = sys.argv[1]
start = sys.argv[2]
key = '457a378e47b945fd9213116d8d285d85'
f = open('Data/New York Times/' + year + '.txt', 'a+')

# Get all results (only 10 are given at a time)
for i in range(int(start), int(start) + 200):

	time.sleep(5)  # Avoid API timeout

	data = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json?sort=oldest&page=' + str(i) + '&facet_field=day_of_week&begin_date=' + year + '0101&end_date=' + year + '1231&api-key=' + key).json()

	print data

	docs = data[u'response'][u'docs']

	print i

	for doc in docs:

		if doc.get('abstract'):
			f.write(re.sub(r'\w*\.\.\.', '', doc['abstract'].encode('utf-8')))
			f.write('\n')

		if doc.get('snippet'):
			f.write(re.sub(r'\w*\.\.\.', '', doc['snippet'].encode('utf-8')))
		
		f.write('\n\n')

	if i > 200:
		break

f.close()