# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)
# Copyright (c) 2017 David Glaude
# Copyright (c) 2016 Dave Hylands

# You can find a description of RTTTL here: https://en.wikipedia.org/wiki/Ring_Tone_Transfer_Language

NOTE = [
    440.0,  # A
    493.9,  # B or H
    261.6,  # C
    293.7,  # D
    329.6,  # E
    349.2,  # F
    392.0,  # G
    0.0,  # pad

    466.2,  # A#
    0.0,
    277.2,  # C#
    311.1,  # D#
    0.0,
    370.0,  # F#
    415.3,  # G#
    0.0,
]


class RTTTL:

    def __init__(self, tune):
        _tune_pieces = tune.split(':')
        if len(_tune_pieces) != 3:
            raise ValueError('tune should contain exactly 2 colons')
        self._tune = _tune_pieces[2]
        self._tune_idx = 0
        self._parse_defaults(_tune_pieces[1])

    def _parse_defaults(self, defaults):
        # Example: d=4,o=5,b=140
        val = 0
        _id = ' '
        for char in defaults:
            char = char.lower()
            if char.isdigit():
                val *= 10
                val += ord(char) - ord('0')
                if _id == 'o':
                    self.default_octave = val
                elif _id == 'd':
                    self.default_duration = val
                elif _id == 'b':
                    self.bpm = val
            elif char.isalpha():
                _id = char
                val = 0
        # 240000 = 60 sec/min * 4 beats/whole-note * 1000 msec/sec
        self.msec_per_whole_note = 240000.0 / self.bpm

    async def _next_char(self):
        if self._tune_idx < len(self._tune):
            char = self._tune[self._tune_idx]
            self._tune_idx += 1
            if char == ',':
                char = ' '
            return char
        return '|'

    async def notes(self):
        """Generator which generates notes. Each note is a tuple where the
           first element is the frequency (in Hz) and the second element is
           the duration (in milliseconds).
        """
        while True:
            # Skip blank characters and commas
            char = await self._next_char()
            while char == ' ':
                char = await self._next_char()

            # Parse duration, if present. A duration of 1 means a whole note.
            # A duration of 8 means 1/8 note.
            duration = 0
            while char.isdigit():
                duration *= 10
                duration += ord(char) - ord('0')
                char = await self._next_char()
            if duration == 0:
                duration = self.default_duration

            if char == '|':  # marker for end of tune
                return

            note = char.lower()
            if 'a' <= note <= 'g':
                note_idx = ord(note) - ord('a')
            elif note == 'h':
                note_idx = 1  # H is equivalent to B
            else:
                note_idx = 7  # pause
            char = await self._next_char()

            # Check for sharp note
            if char == '#':
                note_idx += 8
                char = await self._next_char()

            # Check for duration modifier before octave
            # The spec has the dot after the octave, but some places do it
            # the other way around.
            duration_multiplier = 1.0
            if char == '.':
                duration_multiplier = 1.5
                char = await self._next_char()

            # Check for octave
            if '4' <= char <= '7':
                octave = ord(char) - ord('0')
                char = await self._next_char()
            else:
                octave = self.default_octave

            # Check for duration modifier after octave
            if char == '.':
                duration_multiplier = 1.5
                char = await self._next_char()

            freq = NOTE[note_idx] * (1 << (octave - 4))
            msec = (self.msec_per_whole_note / duration) * duration_multiplier

            # print('note ', note, 'duration', duration, 'octave', octave, 'freq', freq, 'msec', msec)

            yield freq, msec
