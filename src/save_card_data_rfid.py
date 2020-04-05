#!/usr/bin/env python

import binascii
import json
import numbers
import json
import sys
from json_tricks import dump, dumps, load, loads, strip_comments

########################################################################################################################
# Library functions
########################################################################################################################

mf1k_bytes_per_block = 16
mf1k_chars_per_block = (mf1k_bytes_per_block * 2)
mf1k_filler_char = str("0")
mf1k_blocks = list([1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 45, 46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 62])

class Card(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    name = str('')
    price = float(0.00)
    category = str('')
    rent_base = float(0.00)
    rent_house1 = float(0.00)

def chunks(list, chunk_size):
    for i in xrange(0, len(list), chunk_size): yield list[i:i + chunk_size]

def save_to_card(text_data):
    hexed = binascii.b2a_hex(text_data.encode('utf-8'))
    hex_chunks = list(chunks(hexed, mf1k_chars_per_block))
    last_block_length = len(hex_chunks[-1])

    if last_block_length != mf1k_chars_per_block:
        hex_chunks[-1] = str(hex_chunks[-1]).ljust(mf1k_chars_per_block, mf1k_filler_char)
    
    available_blocks = list(mf1k_blocks)
    available_blocks.reverse()

    for data_chunk in hex_chunks:
        target_block = available_blocks.pop()
        display_block = ("0" if len(str(target_block)) == 1 else "") + str(target_block)
        print('hf mf wrbl ' + display_block + ' A FFFFFFFFFFFF ' + ''.join(str(c) for c in data_chunk))

    for i in range(0, len(available_blocks), 1):
        target_block = available_blocks.pop()
        display_block = ("0" if len(str(target_block)) == 1 else "") + str(target_block)
        print('hf mf wrbl ' + display_block + ' A FFFFFFFFFFFF ' + ''.join(str(mf1k_filler_char) for x in range(0,mf1k_chars_per_block)))

########################################################################################################################
# End of Library
########################################################################################################################


########################################################################################################################
# Script execution 
########################################################################################################################

# create an example Monopoly card
park_place = Card(name = "Park Place", category="Property", price=350, rent_base=75, rent1_house=200)

# convert the Monopoly card object into a JSON format
json_serialized = dumps(park_place)

# just for demo/testing purposes - deserialize the JSON representation of our object back into an object just for verification it worked while I am testing
card = loads(json_serialized)

# save the data to the RFID card
save_to_card(json_serialized)

########################################################################################################################
# End of script execution 
########################################################################################################################
