from bs4 import BeautifulSoup
import urllib, urllib2
import curses
from curses import wrapper
import time
import nyaa_linker
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main(stdscr):
    stdscr.clear()
    width = 4
    count = 0
    direction = 1
    
    page = 1
    webpage = 1
    need_input = 'True'
    running = True

    while running:
        if(need_input == 'True'):
            anime = get_input(stdscr, 0, 0, "Please type in a search term").lower() # Prompts user for input
            all_results = nyaa_linker.return_torrents(read_settings(), anime, webpage) # Actually grabs torrent list from Nyaa
        torrent_window = stdscr.subwin(4, 0)
        torrent_window.addstr(0, 0, list_torrents(all_results, page)) # Displays the five entries
        stdscr.refresh()
        torrent_window.refresh()

        c = torrent_window.getch()
        if c == ord('q'): # Quits the program
            curses.endwin()
            running = False
        elif c == ord('n'): # Advances to the next page
            page += 1
            torrent_window.clear()
            need_input = 'False'
        elif c == ord('p') and page != 1: # Goes back to previous page
            page -= 1
            torrent_window.clear()
            need_input = 'False'
        elif c == ord('i'): # Takes in a new input
            torrent_window.clear()
            stdscr.clear()
            need_input = 'True'
            page = 1

def get_input(stdscr, r, c, prompt_string): # Long story short, prompts user for input
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input

def list_torrents(all_torrents, section): # Converts lists to a string to be displayed easily
    string = ''
    lower_bound = (section-1)*5 # Makes the index ranges (0-4, 5-9, etc.)
    if(isinstance(all_torrents, basestring)): # This only happens when one result, or error result so yeah
        string += all_torrents
    elif(len(all_torrents) < lower_bound + 5): # In case we reach the end, doesn't go over bounds
        for index in range(lower_bound, len(all_torrents)):
            string += all_torrents[index]
    else:
        for index in range(lower_bound, (lower_bound + 5)):
            string += all_torrents[index]
    return string

def read_settings(): # Reads the settings from the file
    settings = ['', '', 'false']
    file = open("settings", "r")
    types = file.readlines()
    for i in range(3):
        temp = types[i]
        temp = temp[temp.index('=')+1:]
        settings[i] = temp.rstrip('\n')
    return settings

wrapper(main)