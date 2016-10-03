# -*- coding: utf-8 -*-
from jasper import plugin
from subprocess import call
import time
import logging

class LightsPlugin(plugin.SpeechHandlerPlugin):
    COMMAND_LIGHTS_ON = 'pilight-send -p "rsl366" --systemcode=2 --programcode=2 --on'
    COMMAND_LIGHTS_OFF = 'pilight-send -p "rsl366" --systemcode=2 --programcode=2 --off'

    def __init__(self, *args, **kwargs):
        super(LightsPlugin, self).__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

    def get_phrases(self):
        return self.get_phrases1() + self.get_phrases2()

    def get_phrases1(self):
        return [self.gettext('LIGHTS'), self.gettext('LIGHT')]

    def get_phrases2(self):
        return [self.gettext('ON'), self.gettext('OFF')]

    def handle(self, text, mic):
	text = text.upper()

        if self.gettext('ON') in text:
            for i in xrange(5):
                self.sendcommand(self.COMMAND_LIGHTS_ON)
                time.sleep(0.2)

        elif self.gettext('OFF') in text:
            for i in xrange(5):
                self.sendcommand(self.COMMAND_LIGHTS_OFF)
                time.sleep(0.2)

    def sendcommand(self, command):
        self._logger.info('sending command %s' % command)
        call([command], shell=True)

    def is_valid(self, text):
        return any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases1()) and any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases2())
