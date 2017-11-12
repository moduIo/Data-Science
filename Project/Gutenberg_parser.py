######
# Parses Gutenberg files into cleaned data.
######
import zipfile, fnmatch, os, sys, re
import matplotlib.pyplot as plt

###
# Main
###
rootPath = 'Data/Gutenberg/aleph.gutenberg.org/1/'

# If the first arg is True, unzip all zipped files
if sys.argv[1] == 'True':
	pattern = '*.zip'

	for root, dirs, files in os.walk(rootPath):
		for filename in fnmatch.filter(files, pattern):
			print(os.path.join(root, filename))
			zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))

# Generate summary statistics on year representation
if sys.argv[2] == 'True':
	year_counts = dict.fromkeys(range(1800,2001,10), 0)

	with open('Data/Gutenberg/years.txt', 'r') as f:
		data = f.read()

	for year in data.split('\n'):
		y = year.split('-')[0]
		
		# Ignore bad data
		if y == '????' or y == '' or int(y) < 1800 or int(y) > 2000:
			continue
		else:
			# Replace last digit with 0 to get decade resolution
			y = y[0:-1] + '0'
			year_counts[int(y)] = year_counts[int(y)] + 1
	
	# Print histogram
	counts = []
	for year in sorted(year_counts):
		print str(year) + ' ' + str(year_counts[year])
		counts.append(year_counts[year])

	plt.bar(range(len(year_counts)), counts, align='center')
	plt.xticks(range(len(year_counts)), sorted(year_counts))

	plt.show()

	# Print total valid datapoints
	total = 0
	for year in sorted(year_counts):
		total = total + year_counts[year]

	print total

	exit()

# Gather all txt files
pattern = '[0-9][0-9][0-9][0-9][0-9].txt'
records = len(open('Data/Gutenberg/years.txt').read().split('\n')) - 1
years = open('Data/Gutenberg/years.txt', 'a')

i = 1
for root, dirs, files in os.walk(rootPath):
	for filename in fnmatch.filter(files, pattern):
		if i > records:

			with open(root + '/' + filename, 'r') as f:
				lines = f.read()
				
				print '\n======================================='
				print filename
				print '=======================================\n'
				print '\n'.join(lines.split('\n')[20:200])
				
				# Save publication date
				year = raw_input("\n\nPublication date: ")

				while year == '':
					year = raw_input("\n\nPublication date: ")

				years.write(year + '-' + filename)
				years.write('\n')

		i = i + 1

