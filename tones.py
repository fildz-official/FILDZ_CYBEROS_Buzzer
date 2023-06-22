# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)

################################################################################
# FILDZ CYBEROS PIEZO BUZZER TONES
#
# RTTTL (Ring Tone Text Transfer Language) tones for "fildz_buzzer" library.

TONES = [
    'on:d=4,o=5,b=450:4d#,4f,4b',
    'off:d=4,o=5,b=450:4b,4f,4d#',
    'paired:d=4,o=5,b=450:4d#,4p,4f#',
    'unpaired:d=4,o=5,b=450:4d#,4p,4c',
    'click:d=4,o=5,b=450:4d#'
]


async def find(name):
    for tone in TONES:
        tone_name = tone.split(':')[0]
        if tone_name == name:
            return tone
