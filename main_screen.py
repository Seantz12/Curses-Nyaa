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
    # Make stdscr.getch non-blocking
    preferences = nyaa_linker.read_settings()
    stdscr.clear()
    width = 4
    count = 0
    direction = 1
    while True:
    	anime = get_input(stdscr, 0, 0, "Please type in a search term").lower()
    	stdscr.addstr(3, 0, nyaa_linker.return_torrents(preferences, anime))
        c = stdscr.getch()
        if c == ord('q'):
        	quit()
        else:
        	stdscr.clear()

def get_input(stdscr, r, c, prompt_string):
	curses.echo()
	stdscr.addstr(r, c, prompt_string)
	stdscr.refresh()
	input = stdscr.getstr(r + 1, c, 20)
	return input

def quit():
	curses.endwin()

wrapper(main)