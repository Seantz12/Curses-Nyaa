import urwid
import nyaa_linker
import os
import subprocess

# I know these suck, but right now can't think of another way to do this
# These are variables that remain constant throughout the code
class trt:
    page = 1
    webpage = 1
    entry_mode = 0
    last_webpage = 0
    test = 0
    magnet_links =''
    name = ''
    welcome_message = 'Welcome to the Nyaa torrent downloader!'
    torrent_client = 'transmission-gtk'

# Color scheme
palette = [
    ('title', 'light cyan', 'black'),
    ('controls', 'light blue', 'black'),
    ('category', 'dark magenta', 'black'),
    ('torrent_title', 'white', 'black'),
    ('seeders', 'light green', 'black'),
    ('leechers', 'light red', 'black')]

# Header info
header_text = urwid.Text(u"Nyaa Torrent Downloader 1.0", align='center')
header = urwid.AttrMap(header_text, 'title')

# Control section
control_info = urwid.Edit(('controls', \
    "I-> Input search term              D-> Download torrents\n" + \
    "J-> Next Page                      K-> Previous page\n" + \
    "Enter-> Search torrents            Q-> Exit program\n\n>"),
    u"")
# fill = QuestionBox(control_info)

# Section to store torrents
torrent_text = urwid.Text(u"Welcome to the Nyaa torrent downloader!")
# This creates the border surrounding the main text
torrent_filler = urwid.Filler(torrent_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(torrent_filler, left=1, right=1)
torrent_section = urwid.LineBox(v_padding)

# t = ListOfTorrents

# Put it all into one layout
layout = urwid.Frame(header=header, body=torrent_section, footer=control_info)

def list_torrents(c, t, s, l, section): # Converts lists to a string to be displayed easily
    string = []
    lower_bound = (section-1)*5 # Makes the index ranges (0-4, 5-9, etc.)
    # if isinstance(all_torrents, basestring): # This only happens when one result, or error result so yeah
    #     string += all_torrents
    if len(c) < lower_bound + 5: # In case we reach the end, doesn't go over bounds
        for index in range(lower_bound, len(c)):
            # This formats and colors the text to be returned
            string.append(('category', c[index]))
            string.append('\n')
            string.append(('titles', t[index]))
            string.append('\n')
            string.append(('seeders', s[index]))
            string.append('     ')
            string.append(('leechers', l[index]))
            string.append('\n\n')
    else:
        for index in range(lower_bound, (lower_bound + 5)):
            string.append(('category', c[index]))
            string.append('\n')
            string.append(('titles', t[index]))
            string.append('\n')
            string.append(('seeders', s[index]))
            string.append('     ')
            string.append(('leechers', l[index]))
            string.append('\n\n')
    if len(string) == 0:
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

def write_settings(): # Work in progress
    file = open("settings", "w")

def get_torrents(): # Self explanatory
    if(trt.webpage != trt.last_webpage): # Only gets the url and everything IF needed
        everything = nyaa_linker.return_torrents(read_settings(), trt.name, trt.webpage)
        trt.categories = everything[0]
        trt.titles = everything[1]
        trt.seeders = everything[2]
        trt.leechers = everything[3]
        trt.magnet_links = everything[4]
        trt.last_webpage += 1
        if(trt.last_webpage == trt.webpage + 2): # This covers the going back previous pages
            trt.last_webpage -= 2
    entries = list_torrents(trt.categories, trt.titles, trt.seeders, trt.leechers, trt.page)
    if trt.categories == 'N': # Hard coded, need to fix this as well
        return 'No results found, try a different search term'
    return entries

def reset():
    trt.page = 1
    trt.webpage = 1
    trt.last_webpage = 0

def handle_input(key):
    if key == 'I' or key == 'i':
        # Changes the focus to the bottom so that they can actually type
        layout.set_focus('footer')
        trt.entry_mode = 1
    elif key == 'enter':
        # Ok, I would like to apologize for this. Basically, to get input
        # I've made it so that it changes focus to the edit text
        if trt.entry_mode == 1:
            reset()
            layout.set_focus('header')
            trt.name = control_info.edit_text
            torrent_section.base_widget.set_text(('torrent', 'Retrieving torrents...'))
            loop.draw_screen()
            torrent_section.base_widget.set_text(get_torrents())
            control_info.set_edit_text('')
        elif trt.entry_mode == 2:
            # try:
            num = int(control_info.edit_text)
            if num <= 5 and num >= 1:
                magnet_index = (trt.page-1)*5 + (num-1)
                FNULL = open(os.devnull, 'w')
                try:
                    subprocess.Popen([trt.torrent_client, trt.magnet_links[magnet_index]], \
                        stdin=subprocess.PIPE, stdout=FNULL, stderr=subprocess.STDOUT)
                except IndexError:
                    print trt.torrent_client
                    print magnet_index
                    print trt.magnet_links
                control_info.set_edit_text('')
                layout.set_focus('header')
            # except ValueError:
            #     control_info.set_edit_text('Try again')
    elif key == 'D' or key == 'd':
        layout.set_focus('footer')
        trt.entry_mode = 2
    elif key == 'j': # Advances to the next page
        trt.page += 1
        if trt.page == 16: # Nyaa has maximum 75 entries, therefore after the 15th page it needs to load something new
            trt.webpage += 1
            trt.page = 1
            torrent_section.base_widget.set_text(('torrent', 'Retrieving torrents...'))
            loop.draw_screen()
        torrent_section.base_widget.set_text(get_torrents())
    elif key == 'k' and not(trt.page == 1 and trt.webpage == 1): # Goes back to previous page
        trt.page -= 1
        if trt.page == 0:
            trt.webpage -= 1
            trt.page = 15
            torrent_section.base_widget.set_text(('torrent', 'Retrieving torrents...'))
            loop.draw_screen()    
        torrent_section.base_widget.set_text(get_torrents())
    elif key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
loop.run()