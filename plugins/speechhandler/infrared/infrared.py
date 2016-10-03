# -*- coding: utf-8 -*-
from jasper import plugin
from subprocess import call
import logging

class InfraredControlPlugin(plugin.SpeechHandlerPlugin):
    COMMAND_SCREEN_UP = 'irsend SEND_START leinwand KEY_UP; sleep 3; irsend SEND_STOP leinwand KEY_UP'
    COMMAND_SCREEN_DOWN = 'irsend SEND_START leinwand KEY_DOWN; sleep 3; irsend SEND_STOP leinwand KEY_DOWN'
    COMMAND_SCREEN_STOP = 'irsend SEND_START leinwand KEY_STOP; sleep 3; irsend SEND_STOP leinwand KEY_STOP'
    COMMAND_PROJECTOR_ON = 'irsend SEND_START beamer KEY_POWER; sleep 3; irsend SEND_STOP beamer KEY_POWER'
    COMMAND_PROJECTOR_OFF = 'irsend SEND_START beamer KEY_EXIT; sleep 1; irsend SEND_STOP beamer KEY_EXIT; sleep 1; irsend SEND_START beamer KEY_EXIT; sleep 1; irsend SEND_STOP beamer KEY_EXIT'
    COMMAND_VOLUME_UP = 'irsend SEND_START anlage KEY_VOLUMEUP; sleep 0.3; irsend SEND_STOP anlage KEY_VOLUMEUP;'
    COMMAND_VOLUME_DOWN = 'irsend SEND_START anlage KEY_VOLUMEDOWN; sleep 0.3; irsend SEND_STOP anlage KEY_VOLUMEDOWN'
    COMMAND_HIFI_POWER = 'irsend SEND_START anlage KEY_POWER; sleep 0.2; irsend SEND_STOP anlage KEY_POWER'

    def __init__(self, *args, **kwargs):
        super(InfraredControlPlugin, self).__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

    def get_phrases(self):
        return self.get_phrases1() + self.get_phrases2()

    def get_phrases1(self):
        return [self.gettext('SCREEN'), self.gettext('PROJECTOR'), self.gettext('LOUDER'),
            self.gettext('SOFTER'), self.gettext('HIFI')]

    def get_phrases2(self):
        return [self.gettext('UP'), self.gettext('STOP'), self.gettext('DOWN'), self.gettext('LOUDER'),
            self.gettext('SOFTER'), self.gettext('ON'), self.gettext('OFF')]

    def handle(self, text, mic):
        self._logger.info('handling command(s): %s' % text)
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        if self.gettext('UP') in text:
            self.sendcommand(self.COMMAND_SCREEN_UP)

        elif self.gettext('STOP') in text:
            self.sendcommand(self.COMMAND_SCREEN_STOP)

        elif self.gettext('DOWN') in text:
            self.sendcommand(self.COMMAND_SCREEN_DOWN)

        elif self.gettext('LOUDER') in text:
            self.sendcommand(self.COMMAND_VOLUME_UP)

        elif self.gettext('SOFTER') in text:
            self.sendcommand(self.COMMAND_VOLUME_DOWN)

        elif self.gettext('HIFI ON') in text or self.gettext('HIFI OFF') in text:
            self.sendcommand(self.COMMAND_HIFI_POWER)

        elif self.gettext('PROJECTOR ON') in text:
            self.sendcommand(self.COMMAND_PROJECTOR_ON)

        elif self.gettext('PROJECTOR OFF') in text:
            self.sendcommand(self.COMMAND_PROJECTOR_OFF)

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
        return any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases1()) and any(p.lower() == t.lower() for t in text.lower().split(' ') for p in self.get_phrases2())
