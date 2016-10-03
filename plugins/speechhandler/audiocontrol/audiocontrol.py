# -*- coding: utf-8 -*-
from jasper import plugin
from subprocess import call
import logging

class AudioControlPlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(AudioControlPlugin, self).__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)

        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

    def get_phrases(self):
        return [self.gettext('AUDIO'), self.gettext('SOUND'), self.gettext('MUSIC')]

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """

        _ = self.gettext  # Alias for better readability

        #mic.say(_("Please give me a moment, I'm starting the music mode."))

        phrases = [
            _('LOUDER'), _('SOFTER'),
            _('MUTE'), _('UNMUTE'), _('EXIT')
        ]

        self._logger.warn('starting audio control mode...')
        mic.say(_('Music Mode started!'))

        with mic.special_mode('audio', phrases):

            mode_not_stopped = True
            while mode_not_stopped:
                speech = mic.active_listen()

                text = ''
                if speech:
                    text = ', '.join(speech).upper()

                if not text:
                    #mic.say(_('Pardon?'))
                    #here's a bug, when he says pardon it gets picked up as an input and therefore triggers an "pardon" loop
                    continue
                else:
                    print "there has been some text: %s" % text

                print "handling input..."
                mode_not_stopped = self.handle_music_command(text, mic)

        mic.say(_('Music Mode stopped!'))
        self._logger.debug("Music mode stopped.")

    def handle_music_command(self, command, mic):
        _ = self.gettext  # Alias for better readability

        if _('MUTE').upper() in command:
            call(["amixer","sset","Digital","mute"])

        elif _('UNMUTE').upper() in command:
            call(["amixer", "sset", "Digital", "unmute"])

        elif _('LOUDER').upper() in command:
            call(["amixer", "sset", "Digital", "2%+"])

        elif _('SOFTER').upper() in command:
            call(["amixer", "sset", "Digital", "2%-"])

        elif any(cmd.upper() in command for cmd in (_('CLOSE'), _('EXIT'))):
            print 'exiting the audio control mode'
            return False

        return True

    def is_valid(self, text):
        """
        Returns True if the input is related to audio

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return False
        return any(self.get_phrases())
