from bs4 import BeautifulSoup
import requests
import os
import urllib2
from getch import *

download_path = "/Users/kat/Documents/papers/"
script_path = "/Users/kat/Documents/arxiv-scan/"

def download_file(download_url, title):
	title = title.replace(" ", "_")
	response = urllib2.urlopen(download_url)
	file = open(download_path + title.replace("\"", "") + ".pdf", 'wb')
	file.write(response.read())
	file.close()
	print("Download Completed")

url = "https://arxiv.org/list/quant-ph/new"
base_url = "https://arxiv.org"

print "Starting..."

data = 0
data2 = 1

while (data != data2):
	r = requests.get(url)
	r2 = requests.get(url)
	data = r.text
	data2 = r2.text
soup = BeautifulSoup(data, 'html.parser')

#checking date
date_div = soup.find('div', {'class': 'list-dateline'})
date = date_div.text[-10:]
datefile = open(script_path + 'date.txt', 'rw')
prev_date = datefile.read()
if date == prev_date:
	date_choice = raw_input("You are up to date. Quit?")
	if date_choice == 1:
		exit()

authors = [None] * 40
choice = 0

link_elements = soup.find_all('dt')
title_divs = soup.find_all('div', {'class': 'list-title mathjax'})
all_author_divs = soup.find_all('div', {'class' : 'list-authors'})
comment_divs = soup.find_all('div', {'class' : 'list-comments'})
subject_divs = soup.find_all('div', {'class' : 'list-subjects'})
journal_divs = soup.find_all('div', {'class' : 'list-journal-ref'})
abstract_elements = soup.find_all('p')

print "Total number of papers:", len(abstract_elements), ", ", len(link_elements)

#new submissions and cross-lists
i = 0
c = 0 #comment_count
journal_count = 0
journal_check = 0
comment_check = 0 
while i < len(title_divs):
	comment_check = 0
	journal_check = 0
	pdf_url = base_url + link_elements[i].find_all('a')[2].get('href')
	title = title_divs[i].text[8:].replace("\n", "")
	authors_div = all_author_divs[i].find_all('a')
	for j in range(len(authors_div)):
		authors[j] = authors_div[j].text
	if i < len(abstract_elements):
		abstract = abstract_elements[i].text.replace("\n", " ")
	subjects = subject_divs[i].text.replace("\n", " ")
	if all_author_divs[i].find_next('div').text[:5] == "\nComm":
		comments = comment_divs[c].text.replace("\n", " ")
		c = c + 1
		comment_check = 1
	else:
		comment_check = 0
	if comment_check == 1:
		if comment_divs[c-1].find_next('div').text[:5] == "\nJour":
			journal = journal_divs[journal_count].text[14:]
			journal_count = journal_count + 1
			journal_check = 1
		else:
			journal_check = 0
	if title_divs[i].find_next('div').find_next('div').text[:5] == "\nJour":
		journal_check = 1
		journal = journal_divs[journal_count].text[14:]
		journal_count = journal_count + 1
	print str(i + 1) + "/" + str(len(abstract_elements)) + ", " + str(len(link_elements) - len(abstract_elements))
	print "\n\nTitle:   ", title
	print "Authors: ", ", ".join(x for x in authors[:(j+1)])
	print subjects[1:]
	if comment_check == 1:
		print comments[1:]
	if journal_check == 1:
		print "Journal: ", journal
	print "\n"
	if i < len(abstract_elements):
		print abstract + "\n"
	print("a/s/d")
	choice = myGetch()
	if choice == 's':
		print "Downloading..."
		download_file(pdf_url, title)
	unused_variable = os.system("clear")
	if choice == 'a':
		i = i - 1
		if comment_check == 1:
			c = c - 2
		if journal_check == 1:
			journal_count = journal_count - 2
		continue
	i = i + 1

datefile = open('date.txt', 'w')
datefile.write(date)
datefile.close()
