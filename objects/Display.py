from blessed import Terminal
import sys
''
class Display(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.terminal = Terminal()
        self.last_search_results = []
        self.track = None
        print "Initializing... Please wait..."

    def search_results(self, search_results=[]):
        if len(search_results) == 0:
            search_results = self.last_search_results
        else:
             self.last_search_results = search_results
        if len(search_results) is 0:
            return

        # Print search results
        with self.terminal.location(0, 7):
            print "Search Results"
            self.print_line()
            for i in range(0,len(search_results)):
                print '[{0}]:\t"{1}" by {2}'.format(i, self.terminal.bold(search_results[i]['title'].encode('utf-8', errors="Ignore")), search_results[i]['artist'].encode('utf-8', errors="Ignore"))

    def now_playing(self,track=None):
        if track is None:
            track = self.track
        else:
            self.track = track

        with self.terminal.location(0,0):
            print self.terminal.clear_eol()
            self.print_line(bold=True,center=True)
            if track is not None:
                print self.terminal.center(self.terminal.bold(track['title'].encode('utf-8', errors="Ignore")))
                print self.terminal.center(track['album'].encode('utf-8', errors="Ignore"))
                print self.terminal.center(track['artist'].encode('utf-8', errors="Ignore"))
            else:
                print ""
                print self.terminal.center("N/A")
                print ""
            self.print_line(bold=True,center=True)


    def redraw(self):
        print self.terminal.clear
        self.now_playing()
        self.search_results()
        self.help()


    def help(self):
        with self.terminal.location(0, self.terminal.height-6):
            print self.terminal.bold("Playback:\t") + "play #, pause, resume, stop"
            print self.terminal.bold("Searching:\t") + "album/artist/song ___, playlist ___"
            #print self.terminal.bold("Radio:\t\t") + "create/search ___, radio #"
            print self.terminal.bold("Other:\t\t") + "help, exit"

    def get_input(self, msg):
        with self.terminal.location(0,self.terminal.height-3):
            self.print_line(bold=True)
            return raw_input(msg)

    def clear(self):
        print self.terminal.clear

    def print_line(self, bold=False, center=False):
        line = "--------------------------------------------------------------------"
        if bold:
            line = "======================================================================="
        if center:
            line = self.terminal.center(line)
        print line
