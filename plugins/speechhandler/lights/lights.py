# -*- coding: utf-8 -*-
from jasper import plugin
from subprocess import call
import time

class LightsPlugin(plugin.SpeechHandlerPlugin):
    COMMAND_LIGHTS_ON = 'pilight-send -p raw -c "294 1029 294 1029 882 441 294 1029 294 1029 882 441 294 1176 882 441 882 441 882 441 294 1029 882 441 294 1029 294 1176 882 441 294 1029 147 1029 882 441 882 441 147 1029 294 1029 294 1029 1029 441 294 1029 294 1029 294 1029 882 441 294 1029 294 4998"'
    COMMAND_LIGHTS_OFF = 'pilight-send -p raw -c "294 1029 294 1176 882 294 294 1029 294 1029 882 441 882 441 294 1029 882 441 294 1029 294 1029 294 1029 882 441 294 1029 882 441 882 294 882 441 882 441 294 1029 294 1029 294 1029 882 441 294 1176 294 1029 882 441 882 441 882 441 294 1029 294 4998"'

    def __init__(self, *args, **kwargs):
        super(LightsPlugin, self).__init__(*args, **kwargs)

    def get_phrases(self):
        return self.get_phrases1() + self.get_phrases2()

    def get_phrases1(self):
        return [self.gettext('LIGHTS'), self.gettext('LIGHT')]

    def get_phrases2(self):
        return [self.gettext('ON'), self.gettext('OFF')]

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        if self.gettext('ON') in text:
            for i in xrange(5):
                call([self.COMMAND_LIGHTS_ON], shell=True)
                time.sleep(0.2)

        elif self.gettext('OFF') in text:
            for i in xrange(5):
                call([self.COMMAND_LIGHTS_OFF], shell=True)
                time.sleep(0.2)

    def is_valid(self, text):
        """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases1()) and any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases2())
