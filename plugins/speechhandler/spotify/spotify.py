# -*- coding: utf-8 -*-
from jasper import plugin
import urllib2
import logging

class SpotifyControlPlugin(plugin.SpeechHandlerPlugin):
    API_PROTOCOL = 'http'
    API_HOST = '192.168.2.102'
    API_PORT = '4000'
    API_PATH = 'api/playback/'

    def __init__(self, *args, **kwargs):
        super(SpotifyControlPlugin, self).__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

    def get_phrases(self):
        return self.get_phrases1() + self.get_phrases2()

    def get_phrases1(self):
        return [self.gettext('SPOTIFY')]

    def get_phrases2(self):
        return [self.gettext('PLAY'), self.gettext('PAUSE'), self.gettext('NEXT'), self.gettext('PREVIOUS')]

    def handle(self, text, mic):
        self._logger.info('handling command(s): %s' % text)
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        if self.gettext('PLAY') in text:
            self.send_command('play')

        elif self.gettext('PAUSE') in text:
            self.send_command('pause')

        elif self.gettext('NEXT') in text:
            self.send_command('next')

        elif self.gettext('PREVIOUS') in text:
            self.send_command('prev')

        #elif self.gettext('WELCHES LIED') in text:
        #    self.send_command('prev')
        #http://192.168.2.102:4000/api/info/metadata gibt JSON: {"album_name":"Hopelessly Coping (Remixes)","album_uri":"spotify:album:1JDUdwzRfTqFkYQB1SPGLC","artist_name":"Wilkinson","artist_uri":"spotify:artist:6m8itYST9ADjBIYevXSb1r","context_uri":"spotify:user:spotifydiscover:playlist:0XDczFGsXrwaP1W1KRHTSX","cover_uri":"spotify:image:a41716b57d5494a441f3e800efaf0af5a7fda168","data0":"","duration":283249,"track_name":"Hopelessly Coping - Hanami Remix","track_uri":"spotify:track:0eh54iiUtp2CEbTJieM3Jx","volume":65535}
            
    def send_command(self, command):
        url = self.API_PROTOCOL + '://' + self.API_HOST + ':' + self.API_PORT + '/' + self.API_PATH + command
        self._logger.info('sending %s to spotify connect API, url %s' % (command,url))
        urllib2.urlopen(url).read()

    def get_priority(self):
        return 100

    def is_valid(self, text):
        """
        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases1()) and any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases2())