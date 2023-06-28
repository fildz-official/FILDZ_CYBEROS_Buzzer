# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)

################################################################################
# FILDZ CYBEROS PIEZO BUZZER
#
# Fully asynchronous buzzer library for CYBEROS.
#
# Features:
# - Completely asynchronous.
# - Supports RTTTL (Ring Tone Text Transfer Language).
# - Adjustable control.

# TODO:
#  1. Setting from PWM(freq=0) to PWM(freq=100) takes some time. (first few notes are silent/skipped)

import uasyncio as asyncio
from .rtttl import RTTTL
from .tones import TONES


class Buzzer:
    def __init__(self, pin):
        self._tone = pin  # if freq=0 then first few notes are silent/skipped.
        self._vol = 2  # Buzzer volume range 0 - 1023.

    ################################################################################
    # Properties
    #
    @property
    def volume(self):
        return self._vol

    @volume.setter
    def volume(self, value):
        self._vol = value

    ################################################################################
    # Tasks
    #
    async def play_note(self, freq, msec):
        # print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
        if freq > 0:
            self._tone.freq(int(freq))
            self._tone.duty(self._vol)
        await asyncio.sleep_ms(int(0.9 * msec))
        self._tone.duty(0)
        await asyncio.sleep_ms(int(0.1 * msec))

    async def play_tone(self, tone):
        for freq, msec in tone.notes():
            await self.play_note(freq, msec)

    async def play(self, index=None, name=None):
        if index is not None:
            await self.play_tone(RTTTL(TONES[index]))
        elif name is not None:
            await self.play_tone(RTTTL(await tones.find(name)))
