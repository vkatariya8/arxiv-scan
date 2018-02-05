from bs4 import BeautifulSoup
import requests
import urllib2

download_path = "/Users/kat/Documents/papers/"

def download_file(download_url, title):
    response = urllib2.urlopen(download_url)
    file = open(download_path + title + ".pdf", 'wb')
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

authors = [None] * 20
choice = 0

link_elements = soup.find_all('dt')
title_divs = soup.find_all('div', {'class': 'list-title mathjax'})
all_author_divs = soup.find_all('div', {'class' : 'list-authors'})
abstract_elements = soup.find_all('p')

print "Total number of papers:", len(abstract_elements), ", ", len(link_elements)

#new submissions and cross-lists
for i in range(len(abstract_elements) - 1):
	pdf_url = base_url + link_elements[i].find_all('a')[2].get('href')
	title = title_divs[i].text[8:].replace("\n", "")
	authors_div = all_author_divs[i].find_all('a')
	for j in range(len(authors_div)):
		authors[j] = authors_div[j].text
	abstract = abstract_elements[i].text.replace("\n", " ") 
	print "\n\nTitle: ", title
	print "Authors: ", ", ".join(x for x in authors[:(j+1)])
	print "Abstract\n"
	print abstract + "\n"
	choice = raw_input('1/0?\n')
	if choice == str(1):
		download_file(pdf_url, title)

#replacements
i = i + 1
for k in range(i, len(title_divs)):
	pdf_url = base_url + link_elements[k].find_all('a')[2].get('href')
	title = title_divs[k].text[8:].replace("\n", "")
	authors_div = all_author_divs[k].find_all('a')
	for j in range(len(authors_div)):
		authors[j] = authors_div[j].text
	print "Title: ", title
	print "Authors: ", ", ".join(x for x in authors[:(j+1)])
	choice = raw_input('1/0?')
	if choice == str(1):
		download_file(pdf_url, title)

datefile = open('date.txt', 'w')
datefile.write(date)
