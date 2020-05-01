import curses
from curses import wrapper
import urwid
import nyaa_linker
import time
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")

# OUTDATED AND NOT USEFUL ANYMORE! DO NOT USE THIS FILE! IT REMAINS AS A BACKUP FOR ANYTHING
# TAHT GOES WRONG WITH URWID! BUT NOTHING IS RIGHT NOW! SO THIS FILE SUCKS!

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    # Creating the windows before hand for where everything goes
    entry_window = stdscr.subwin(2, 0)
    torrent_window = stdscr.subwin(5, 0)
    #info_window = stdscr.subwin(50, 0)

    #curses.resizeterm(50, 75)
    # Variables are pretty self-explanatory
    page = 1
    webpage = 1
    last_webpage = 0
    torrent_client = 'transmission-gtk '
    terminal_client = 'gnome-terminal '
    anime = ''
    running = True


    while running:
        stdscr.addstr(0, 0, "Nyaa torrent downloader 1.0") # Welcome message
        stdscr.refresh()

        # Gets an entry and populates torrent list with it, only after user presses right button
        if(anime != ''):
            if webpage != last_webpage: # If needed to advance webpage on nyaa itself
                everything = nyaa_linker.return_torrents(read_settings(), anime, webpage)
                all_results = everything[0]
                magnet_links = everything[1]
                last_webpage += 1
                # TEMP FIX, tired from coding, will fix later
                if(last_webpage == webpage + 2):
                    last_webpage -= 2
            entries = list_torrents(all_results, page)
            torrent_window.addstr(0, 0, entries) # Displays the five entries
            torrent_window.refresh()

        #info_window.addstr("i to search entries, j to go to next page, k to go to previous page, q to quit")
        curses.noecho()
        c = entry_window.getch()
        if c == ord('i'): # Takes in a new input
            curses.curs_set(1) # Shows cursor as typing
            entry_window.clear()
            anime = get_input(entry_window, 0, 0, "Please type in a search term") # Prompts user for input
            # Resets everything
            page = 1
            webpage = 1
            last_webpage = 0
            entry_window.refresh()
            torrent_window.clear()
            curses.curs_set(0) # Hides it again
        elif c == ord('j') and anime != '' and entries[0:2] != 'No': # Advances to the next page
            page += 1
            torrent_window.clear()
            if page == 16: # Nyaa has maximum 75 entries, therefore after the 15th page it needs to load something new
                webpage += 1
                page = 1
        elif c == ord('k') and anime != '' and not(page == 1 and webpage == 1): # Goes back to previous page
            page -= 1
            if page == 0:
                webpage -= 1
                page = 15
            torrent_window.clear()
        elif c == ord('d') and anime != '':
            curses.curs_set(1)
            # FIX cannot clear torrent selection line, wtf
            while True:
                selection = get_input(torrent_window, 38, 0, "Enter a number between 1-5" +\
                    " (1 for top torrent, 5 for bottom).") #Prompts user selection
                try:
                    if int(selection) <= 5 and int(selection) >= 1:
                        #torrent_window.refresh()
                        magnet_index = (page-1)*5 + (int(selection)-1)
                        os.system(torrent_client + magnet_links[magnet_index])
                        torrent_window.clear()
                        break
                    else:
                        torrent_window.addstr(37, 0, "Please enter a number between 1-5")
                except ValueError:
                    torrent_window.addstr(37, 0, "Please enter a number between 1-5")
            torrent_window.clear() # temp fix, just testing out
        elif c == ord('q'): # Quits the program
            curses.endwin()
            running = False

def get_input(stdscr, r, c, prompt_string): # Long story short, prompts user for input
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 50)
    return input

def list_torrents(all_torrents, section): # Converts lists to a string to be displayed easily
    string = ''
    lower_bound = (section-1)*5 # Makes the index ranges (0-4, 5-9, etc.)
    if isinstance(all_torrents, basestring): # This only happens when one result, or error result so yeah
        string += all_torrents
    elif len(all_torrents) < lower_bound + 5: # In case we reach the end, doesn't go over bounds
        for index in range(lower_bound, len(all_torrents)):
            string += all_torrents[index]
    else:
        for index in range(lower_bound, (lower_bound + 5)):
            string += all_torrents[index]
    if string == '':
        return 'Nothing left!'
    else:
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

def write_settings():
    file = open("settings", "w")

wrapper(main)