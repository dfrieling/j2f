# -*- coding: utf-8 -*-
from jasper import plugin
from subprocess import call
import logging

class InfraredControlPlugin(plugin.SpeechHandlerPlugin):
    COMMAND_POWER = 'irsend SEND_ONCE scott KEY_POWER'
    COMMAND_PLAY = 'irsend SEND_ONCE scott KEY_PLAY'
    COMMAND_STOP = 'irsend SEND_ONCE scott KEY_STOP'
    
    def __init__(self, *args, **kwargs):
        super(InfraredControlPlugin, self).__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

    def get_phrases(self):
        return [self.gettext('ON'), self.gettext('OFF'), self.gettext('PLAY'), self.gettext('STOP'), self.gettext('PAUSE')]

    def handle(self, text, mic):
        self._logger.info('handling command(s): %s' % text)
        
        if self.gettext('POWER') in text or self.gettext('ON') in text or self.gettext('OFF') in text:
            self.sendcommand(self.COMMAND_POWER)

        elif self.gettext('PLAY') in text or self.gettext('PAUSE') in text:
            self.sendcommand(self.COMMAND_PLAY)

        elif self.gettext('STOP') in text:
            self.sendcommand(self.COMMAND_STOP)

    def sendcommand(self, command):
        self._logger.info('sending command %s' % command)
        call([command], shell=True)

    def get_priority(self):
        return 100

    def is_valid(self, text):
        """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p in text.upper() for p in self.get_phrases())
