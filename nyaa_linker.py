# TODO:
# Add a filter for anime only and other shit, subs/raws/whatever the hell else there is
# Create an actual interface (curses or gtk or whatever)
# Make code look neater
# Publish that shit yo
from bs4 import BeautifulSoup
import urllib, urllib2

settings = ['', '', 'false']

def main():
	read_settings()
	anime = raw_input('ay yo whatchu looking for: ')
	anime = urllib.quote_plus(anime)
	return_torrents(settings, anime)

def return_torrents(prefernces, anime_name):
	# Opens up the website with the search term
	# url format https://nyaa.si/?f=0&c=0_0&q=ANIME_NAME&s=SORTING&o=ACCES/DESC
	website = "https://nyaa.si/?f=0&c=0_0&q=" + anime_name + "&s=" + prefernces[0] + "&o=" + prefernces[1]
	req = urllib2.Request(website, headers={'User-Agent' : "Magic Browser"})
	page = urllib2.urlopen(req)

	soup = BeautifulSoup(page, "html.parser")

	try:
		# Locates the table with all the torrents in it
		table_body = soup.find('table')
		torrent_list = table_body.find('tbody')
	except AttributeError:
		return "\nNo results found, try a different search term\n"

	results = ''
	for row in torrent_list.findAll("tr"): # iterates through each torrent row
		quality = row.get('class')[0]
		quality[4:-2] # gets rid of the unneeded bits (['u']) part

		if(prefernces[2] == 'false' or quality == 'success'):
			results += return_category(row) + '\n'
			results += return_torrent_title(row) + '\n'
			results += return_seeder_leecher_count(row) + '\n\n'

	if results == '':
		return 'No results found, try changing your search filters'
	else:
		return results

def return_torrent_title(row):
	element = row.findAll('td') # groups individual elements of the row

	torrent_file = element[1] # this is the part that contains the torrent name
	torrent_link = torrent_file.findAll('a') # gets rid of the comment link if any

	if(len(torrent_link) > 1):
		return torrent_link[1].text.strip()
	else:
		return torrent_link[0].text.strip()

def return_seeder_leecher_count(row):
	element = row.findAll('td')
	seeders = element[5]
	leechers = element[6]

	return 'Seeders: ' + seeders.text.strip() + ' Leechers: ' + leechers.text.strip()

def return_category(row):
	element = row.find('td')
	category = element.find('a')
	return category.get('title')

#def return_magnent_link(row):


def read_settings():
	file = open("settings", "r")
	types = file.readlines()
	for i in range(3):
		temp = types[i]
		temp = temp[temp.index('=')+1:]
		settings[i] = temp.rstrip('\n')
	return settings

if __name__ == '__main__':
	main()
