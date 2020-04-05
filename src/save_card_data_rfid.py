#!/usr/bin/env python

import warnings
#warnings.filterwarnings('always')
warnings.filterwarnings('ignore', 
                        '.*', 
                        UserWarning
                        )

#import warnings_filtering

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

class Cards:
    PARK_PLACE = 1
    BOARDWALK = 2

class Card(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    name = str('')
    price = float(0.00)
    category = str('')
    rent_base = float(0.00)
    rent_two = float(0.00)
    rent_three = float(0.00)
    rent_set = float(0.00)
    rent_house1 = float(0.00)
    rent_house2 = float(0.00)
    rent_house3 = float(0.00)
    rent_house4 = float(0.00)
    rent_hotel = float(0.00)

def chunks(list, chunk_size):
    for i in xrange(0, len(list), chunk_size): yield list[i:i + chunk_size]

def get_card_data(cardtype):
    if cardtype == Cards.BOARDWALK:
        return "7B225F5F696E7374616E63655F747970655F5F223A205B6E756C6C2C202243617264225D2C202261747472696275746573223A207B2263617465676F7279223A202250726F7065727479222C202272656E745F62617365223A203130302C202272656E74315F686F757365223A203235302C20227072696365223A203430302C20226E616D65223A2022426F61726477616C6B227D7D"
    if cardtype == Cards.PARK_PLACE:
        return "7b225f5f696e7374616e63655f747970655f5f223a205b6e756c6c2c202243617264225d2c202261747472696275746573223a207b2263617465676f7279223a202250726f7065727479222c202272656e745f62617365223a2037352c202272656e74315f686f757365223a203230302c20227072696365223a203335302c20226e616d65223a20225061726b20506c616365227d7d"
    return ""

def read_from_card(cardtype):
    return binascii.a2b_hex(get_card_data(cardtype))

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


mode = "READ"
#cardtype = Cards.BOARDWALK
cardtype = Cards.PARK_PLACE


if mode == "WRITE":
    # create an example Monopoly card
    park_place = Card(name = "Park Place", category="Property", price=350, rent_base=75, rent1_house=200)
    #boardwalk = Card(name = "Boardwalk", category="Property", price=400, rent_base=100, rent1_house=250)

    # convert the Monopoly card object into a JSON format
    #json_serialized = dumps(boardwalk)
    json_serialized = dumps(park_place)
    print(json_serialized)

    # save the data to the RFID card
    save_to_card(json_serialized)

if mode == "READ":
    my_json_data = read_from_card(cardtype)
    print('\n\n\n')
    print(my_json_data)

    my_card = loads(my_json_data)

    print('\n\n')
    print('name:\t\t' + my_card.name)
    print('category:\t' + my_card.category)
    print('price:\t\t' + str(my_card.price))
    print('')
    print('rent_base:\t' + str(my_card.rent_base))
    print('rent_two:\t' + str(my_card.rent_two))
    print('rent_three:\t' + str(my_card.rent_three))
    print('rent_set:\t' + str(my_card.rent_set))
    print('')
    print('rent_house1:\t' + str(my_card.rent_house1))
    print('rent_house2:\t' + str(my_card.rent_house2))
    print('rent_house3:\t' + str(my_card.rent_house3))
    print('rent_house4:\t' + str(my_card.rent_house4))
    print('rent_hotel:\t' + str(my_card.rent_hotel))

########################################################################################################################
# End of script execution 
########################################################################################################################
