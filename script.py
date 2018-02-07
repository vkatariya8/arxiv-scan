from bs4 import BeautifulSoup
import requests
import os
import urllib2
from tiddler_integration import *
from getch import *

download_path = "/Users/kat/Documents/papers/"

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

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

#checking date
date_div = soup.find('div', {'class': 'list-dateline'})
date = date_div.text[-10:]
datefile = open('date.txt', 'rw')
prev_date = datefile.read()
if date == prev_date:
	date_choice = raw_input("You are up to date. Quit?")
	if date_choice == 1:
		exit()

tiddler_file = open('tiddler.txt', 'w')

authors = [None] * 20
choice = 0

link_elements = soup.find_all('dt')
title_divs = soup.find_all('div', {'class': 'list-title mathjax'})
all_author_divs = soup.find_all('div', {'class' : 'list-authors'})
comment_divs = soup.find_all('div', {'class' : 'list-comments'})
subject_divs = soup.find_all('div', {'class' : 'list-subjects'})

abstract_elements = soup.find_all('p')

print "Total number of papers:", len(abstract_elements), ", ", len(link_elements)

#new submissions and cross-lists
i = 0
c = 0 #comment_count
while i < len(abstract_elements):
	pdf_url = base_url + link_elements[i].find_all('a')[2].get('href')
	title = title_divs[i].text[8:].replace("\n", "")
	authors_div = all_author_divs[i].find_all('a')
	for j in range(len(authors_div)):
		authors[j] = authors_div[j].text
	abstract = abstract_elements[i].text.replace("\n", " ")
	subjects = subject_divs[i].text.replace("\n", " ")
	if all_author_divs[i].find_next('div').text[:5] == "\nSubj":
		comments = comment_divs[c].text.replace("\n", " ")
		c = c + 1
	print i + 1
	print "\n\nTitle:   ", title
	print "Authors: ", ", ".join(x for x in authors[:(j+1)])
	print subjects[1:]
	print comments[1:]
	print "\n"
	print abstract + "\n"
	#choice = raw_input('1/0\n')
	print("a/s/d")
	choice = myGetch()
	if choice == 's':
		download_file(pdf_url, title)
		tiddler_subtext = add_tiddler_subtext(title,pdf_url)
		for y in range(len(tiddler_subtext)):
			try:
				tiddler_file.write(tiddler_subtext[y])
				tiddler_file.write("\n")
			except:
				continue
	unused_variable = os.system("clear")
	if choice == 'a':
		i = i - 1
		continue
	i = i + 1

#replacements
#for k in range(i, len(title_divs)):
while i < len(title_divs):
	pdf_url = base_url + link_elements[i].find_all('a')[2].get('href')
	title = title_divs[i].text[8:].replace("\n", "")
	subjects = subject_divs[i].text.replace("\n", " ")
	authors_div = all_author_divs[i].find_all('a')
	if all_author_divs[i].find_next('div').text[:5] == "\nSubj":
		comments = comment_divs[c].text.replace("\n", " ")
		c = c + 1
	for j in range(len(authors_div)):
		authors[j] = authors_div[j].text
	print i + 1
	print "\n\nTitle:   ", title
	print "Authors: ", ", ".join(x for x in authors[:(j+1)])
	print subjects[1:]
	print comments[1:]
	#choice = raw_input('1/0?')
	print("a/s/d")
	choice = myGetch()
	if choice == "s":
		download_file(pdf_url, title)
		tiddler_subtext = add_tiddler_subtext(title,pdf_url)
		for y in range(len(tiddler_subtext)):
			try:
				tiddler_file.write(tiddler_subtext[y])
				tiddler_file.write("\n")
			except:
				continue
	unused_variable = os.system("clear")
	if choice == "a":
		i = i - 1
		continue
	i = i + 1
datefile = open('date.txt', 'w')
datefile.write(date)
