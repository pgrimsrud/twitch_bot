# coding: utf-8
#IRC BOT
# port 8100

import sys
import socket
import string
import pygame
import threading
import re
import math
import urllib
import urllib2
import json
import select
import time
import BaseHTTPServer
import cgi
import random
import smtplib
from urlparse import urlparse

SERVER_IP = "Redacted client IP"
EXTERNAL_IP = "Redacted external facing IP"
EXTERNAL_ADDRESS = "http://" + EXTERNAL_IP
SERVER_PORT = "8100"
SECRET = "requested by bitNES"

class TwitchRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        global bitnes

        header = self.headers.items()
        print("Header:\n")
        print(header)
        length = self.headers.getheader('content-length')
        data = self.rfile.read(int(length))
        jsondata = json.loads(data)
        print(jsondata)
        print("ID %s\n" % jsondata['data']['from_id'])
        print("New Follower %s\n" % GetDisplayName(jsondata['data']['from_id']))
        bitnes.add_notification(GetDisplayName(jsondata['data']['from_id']))
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        header = self.headers.items()
        data = cgi.parse_qs(urlparse(self.path).query)
        print("Header:\n")
        print(header)
        print("Data:\n")
        print(data)
        print("Address:\n")
        print(self.client_address)
        print("Path:\n")
        print(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(data['hub.challenge'][0])
        

class HttpThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        httpd = BaseHTTPServer.HTTPServer((SERVER_IP, int(SERVER_PORT)), TwitchRequestHandler)
        print "Starting HTTP server\n"
        httpd.serve_forever()


buff = ""
lines = ""
bitInfo = {'link_7777_total_bits': 0}

# In order to access private data via the Twitch API a client-id and access token is required
# see https://github.com/justintv/Twitch-API/blob/master/authentication.md for instructions
# you will need to register your app to get a client-id then have a user (yourself) authorize access to your account when authorized you will recieve an access token.
# you will also need to find your user id (which is an actual number not your handle)
APP_NAME = "link_7777"
USER_ID = "Redacted user ID (number)"
CLIENT_ID = "Redacted client ID (hash)"
ACCESS_TOKEN = "Redacted access token (hash)"

LiveAlertTimeout = 300*8
LiveAlertListLength = 11
LiveAlertList = [0 for i in range(LiveAlertListLength)]
LiveAlertList[0] =  {'game':'Star Wars: The Empire Strikes Back'}
LiveAlertList[1] =  {'game':'Time Lord'}
LiveAlertList[2] =  {'game':'Legend of the Ghost Lion'}
LiveAlertList[3] =  {'game':'Barbie'}
LiveAlertList[4] =  {'game':'Pwn Adventure Z'}
LiveAlertList[5] =  {'game':'Track & Field II'}
LiveAlertList[6] =  {'game':'Town & Country Surf Designs: Wood & Water Rage'}
LiveAlertList[7] =  {'game':"Town & Country Surf Designs II: Thrilla's Surfari"}
LiveAlertList[8] =  {'game':'Raid on Bungeling Bay'}
LiveAlertList[9] =  {'game':'Alfred Chicken'}
LiveAlertList[10] = {'game':'Super Glove Ball'}
#LiveAlertList[11] = {'game':'Zelda II: The Adventure of Link'}

NesImageCount = 177
NesImageLibrary = [0 for i in range(NesImageCount)]
NesImageLibrary[0  ] = {'name':'10-Yard Fight',                                               'file':'C:\Users\omx\NES\\bot\img\\001.bmp',    'pixels':0 }
NesImageLibrary[1  ] = {'name':'1942',                                                        'file':'C:\Users\omx\NES\\bot\img\\002.bmp',    'pixels':0 } 
NesImageLibrary[2  ] = {'name':'1943: The Battle of Midway',                                  'file':'C:\Users\omx\NES\\bot\img\\003.bmp',    'pixels':0 }
NesImageLibrary[3  ] = {'name':'3-D WorldRunner',                                             'file':'C:\Users\omx\NES\\bot\img\\004.bmp',    'pixels':0 }
NesImageLibrary[4  ] = {'name':'720°',                                                        'file':'C:\Users\omx\NES\\bot\img\\005.bmp',    'pixels':0 }
NesImageLibrary[5  ] = {'name':'8 Eyes',                                                      'file':'C:\Users\omx\NES\\bot\img\\006.bmp',    'pixels':0 }
NesImageLibrary[6  ] = {'name':'Abadox',                                                      'file':'C:\Users\omx\NES\\bot\img\\007.bmp',    'pixels':0 }
NesImageLibrary[7  ] = {'name':'The Addams Family',                                           'file':'C:\Users\omx\NES\\bot\img\\008.bmp',    'pixels':0 }
NesImageLibrary[8  ] = {'name':'The Addams Family: Pugsley\'s Scavenger Hunt',                'file':'C:\Users\omx\NES\\bot\img\\009.bmp',    'pixels':0 }
NesImageLibrary[9  ] = {'name':'Advanced Dungeons & Dragons: DragonStrike',                   'file':'C:\Users\omx\NES\\bot\img\\010.bmp',    'pixels':0 }
NesImageLibrary[10 ] = {'name':'Advanced Dungeons & Dragons: Heroes of the Lance',            'file':'C:\Users\omx\NES\\bot\img\\011.bmp',    'pixels':0 }
NesImageLibrary[11 ] = {'name':'Advanced Dungeons & Dragons: Hillsfar',                       'file':'C:\Users\omx\NES\\bot\img\\012.bmp',    'pixels':0 }
NesImageLibrary[12 ] = {'name':'Advanced Dungeons & Dragons: Pool of Radiance',               'file':'C:\Users\omx\NES\\bot\img\\013.bmp',    'pixels':0 }
NesImageLibrary[13 ] = {'name':'Adventure Island',                                            'file':'C:\Users\omx\NES\\bot\img\\014.bmp',    'pixels':0 }
NesImageLibrary[14 ] = {'name':'Adventure Island II',                                         'file':'C:\Users\omx\NES\\bot\img\\015.bmp',    'pixels':0 }
NesImageLibrary[15 ] = {'name':'Adventure Island 3',                                          'file':'C:\Users\omx\NES\\bot\img\\016.bmp',    'pixels':0 }
NesImageLibrary[16 ] = {'name':'Adventures in the Magic Kingdom',                             'file':'C:\Users\omx\NES\\bot\img\\017.bmp',    'pixels':0 }
NesImageLibrary[17 ] = {'name':'The Adventures of Bayou Billy',                               'file':'C:\Users\omx\NES\\bot\img\\018.bmp',    'pixels':0 }
NesImageLibrary[18 ] = {'name':'Adventures of Dino Riki',                                     'file':'C:\Users\omx\NES\\bot\img\\019.bmp',    'pixels':0 }
NesImageLibrary[19 ] = {'name':'The Adventures of Gilligan\'s Island',                        'file':'C:\Users\omx\NES\\bot\img\\020.bmp',    'pixels':0 }
NesImageLibrary[20 ] = {'name':'Adventures of Lolo',                                          'file':'C:\Users\omx\NES\\bot\img\\021.bmp',    'pixels':0 }
NesImageLibrary[21 ] = {'name':'Adventures of Lolo 2',                                        'file':'C:\Users\omx\NES\\bot\img\\022.bmp',    'pixels':0 }
NesImageLibrary[22 ] = {'name':'Adventures of Lolo 3',                                        'file':'C:\Users\omx\NES\\bot\img\\023.bmp',    'pixels':0 }
NesImageLibrary[23 ] = {'name':'The Adventures of Rad Gravity',                               'file':'C:\Users\omx\NES\\bot\img\\024.bmp',    'pixels':0 }
NesImageLibrary[24 ] = {'name':'The Adventures of Rocky and Bullwinkle and Friends',          'file':'C:\Users\omx\NES\\bot\img\\025.bmp',    'pixels':0 }
NesImageLibrary[25 ] = {'name':'The Adventures of Tom Sawyer',                                'file':'C:\Users\omx\NES\\bot\img\\026.bmp',    'pixels':0 }
NesImageLibrary[26 ] = {'name':'Air Fortress',                                                'file':'C:\Users\omx\NES\\bot\img\\027.bmp',    'pixels':0 }
NesImageLibrary[27 ] = {'name':'Airwolf',                                                     'file':'C:\Users\omx\NES\\bot\img\\028.bmp',    'pixels':0 }
NesImageLibrary[28 ] = {'name':'Al Unser Jr.\'s Turbo Racing',                                'file':'C:\Users\omx\NES\\bot\img\\029.bmp',    'pixels':0 }
NesImageLibrary[29 ] = {'name':'Alfred Chicken',                                              'file':'C:\Users\omx\NES\\bot\img\\030.bmp',    'pixels':0 }
NesImageLibrary[30 ] = {'name':'Alien 3',                                                     'file':'C:\Users\omx\NES\\bot\img\\031.bmp',    'pixels':0 }
NesImageLibrary[31 ] = {'name':'All-Pro Basketball',                                          'file':'C:\Users\omx\NES\\bot\img\\032.bmp',    'pixels':0 }
NesImageLibrary[32 ] = {'name':'Alpha Mission',                                               'file':'C:\Users\omx\NES\\bot\img\\033.bmp',    'pixels':0 }
NesImageLibrary[33 ] = {'name':'Amagon',                                                      'file':'C:\Users\omx\NES\\bot\img\\034.bmp',    'pixels':0 }
NesImageLibrary[34 ] = {'name':'American Gladiators',                                         'file':'C:\Users\omx\NES\\bot\img\\035.bmp',    'pixels':0 }
NesImageLibrary[35 ] = {'name':'Anticipation',                                                'file':'C:\Users\omx\NES\\bot\img\\036.bmp',    'pixels':0 }
NesImageLibrary[36 ] = {'name':'Arch Rivals',                                                 'file':'C:\Users\omx\NES\\bot\img\\037.bmp',    'pixels':0 }
NesImageLibrary[37 ] = {'name':'Archon',                                                      'file':'C:\Users\omx\NES\\bot\img\\038.bmp',    'pixels':0 }
NesImageLibrary[38 ] = {'name':'Arkanoid',                                                    'file':'C:\Users\omx\NES\\bot\img\\039.bmp',    'pixels':0 }
NesImageLibrary[39 ] = {'name':'Arkista\'s Ring',                                             'file':'C:\Users\omx\NES\\bot\img\\040.bmp',    'pixels':0 }
NesImageLibrary[40 ] = {'name':'Asterix (PAL)',                                               'file':'C:\Users\omx\NES\\bot\img\\041.bmp',    'pixels':0 }
NesImageLibrary[41 ] = {'name':'Astyanax',                                                    'file':'C:\Users\omx\NES\\bot\img\\042.bmp',    'pixels':0 }
NesImageLibrary[42 ] = {'name':'Athena',                                                      'file':'C:\Users\omx\NES\\bot\img\\043.bmp',    'pixels':0 }
NesImageLibrary[43 ] = {'name':'Athletic World',                                              'file':'C:\Users\omx\NES\\bot\img\\044.bmp',    'pixels':0 }
NesImageLibrary[44 ] = {'name':'Attack of the Killer Tomatoes',                               'file':'C:\Users\omx\NES\\bot\img\\045.bmp',    'pixels':0 }
NesImageLibrary[45 ] = {'name':'Aussie Rules Footy (PAL)',                                    'file':'C:\Users\omx\NES\\bot\img\\046.bmp',    'pixels':0 }
NesImageLibrary[46 ] = {'name':'Back to the Future',                                          'file':'C:\Users\omx\NES\\bot\img\\047.bmp',    'pixels':0 }
NesImageLibrary[47 ] = {'name':'Back to the Future Part II & III',                            'file':'C:\Users\omx\NES\\bot\img\\048.bmp',    'pixels':0 }
NesImageLibrary[48 ] = {'name':'Bad Dudes',                                                   'file':'C:\Users\omx\NES\\bot\img\\049.bmp',    'pixels':0 }
NesImageLibrary[49 ] = {'name':'Bad News Baseball',                                           'file':'C:\Users\omx\NES\\bot\img\\050.bmp',    'pixels':0 }
NesImageLibrary[50 ] = {'name':'Bad Street Brawler',                                          'file':'C:\Users\omx\NES\\bot\img\\051.bmp',    'pixels':0 }
NesImageLibrary[51 ] = {'name':'Balloon Fight',                                               'file':'C:\Users\omx\NES\\bot\img\\052.bmp',    'pixels':0 }
NesImageLibrary[52 ] = {'name':'Banana Prince (PAL)',                                         'file':'C:\Users\omx\NES\\bot\img\\053.bmp',    'pixels':0 }
NesImageLibrary[53 ] = {'name':'Bandai Golf: Challenge Pebble Beach',                         'file':'C:\Users\omx\NES\\bot\img\\054.bmp',    'pixels':0 }
NesImageLibrary[54 ] = {'name':'Bandit Kings of Ancient China',                               'file':'C:\Users\omx\NES\\bot\img\\055.bmp',    'pixels':0 }
NesImageLibrary[55 ] = {'name':'Barbie',                                                      'file':'C:\Users\omx\NES\\bot\img\\056.bmp',    'pixels':0 }
NesImageLibrary[56 ] = {'name':'The Bard\'s Tale',                                            'file':'C:\Users\omx\NES\\bot\img\\057.bmp',    'pixels':0 }
NesImageLibrary[57 ] = {'name':'Barker Bill\'s Trick Shooting',                               'file':'C:\Users\omx\NES\\bot\img\\058.bmp',    'pixels':0 }
NesImageLibrary[58 ] = {'name':'Base Wars',                                                   'file':'C:\Users\omx\NES\\bot\img\\059.bmp',    'pixels':0 }
NesImageLibrary[59 ] = {'name':'Baseball',                                                    'file':'C:\Users\omx\NES\\bot\img\\060.bmp',    'pixels':0 }
NesImageLibrary[60 ] = {'name':'Baseball Simulator 1.000',                                    'file':'C:\Users\omx\NES\\bot\img\\061.bmp',    'pixels':0 }
NesImageLibrary[61 ] = {'name':'Baseball Stars',                                              'file':'C:\Users\omx\NES\\bot\img\\062.bmp',    'pixels':0 }
NesImageLibrary[62 ] = {'name':'Baseball Stars 2',                                            'file':'C:\Users\omx\NES\\bot\img\\063.bmp',    'pixels':0 }
NesImageLibrary[63 ] = {'name':'Bases Loaded',                                                'file':'C:\Users\omx\NES\\bot\img\\064.bmp',    'pixels':0 }
NesImageLibrary[64 ] = {'name':'Bases Loaded II: Second Season',                              'file':'C:\Users\omx\NES\\bot\img\\065.bmp',    'pixels':0 }
NesImageLibrary[65 ] = {'name':'Bases Loaded 3',                                              'file':'C:\Users\omx\NES\\bot\img\\066.bmp',    'pixels':0 }
NesImageLibrary[66 ] = {'name':'Bases Loaded 4',                                              'file':'C:\Users\omx\NES\\bot\img\\067.bmp',    'pixels':0 }
NesImageLibrary[67 ] = {'name':'Batman: The Video Game',                                      'file':'C:\Users\omx\NES\\bot\img\\068.bmp',    'pixels':0 }
NesImageLibrary[68 ] = {'name':'Batman Returns',                                              'file':'C:\Users\omx\NES\\bot\img\\069.bmp',    'pixels':0 }
NesImageLibrary[69 ] = {'name':'Batman: Return of the Joker',                                 'file':'C:\Users\omx\NES\\bot\img\\070.bmp',    'pixels':0 }
NesImageLibrary[70 ] = {'name':'Battle Chess',                                                'file':'C:\Users\omx\NES\\bot\img\\071.bmp',    'pixels':0 }
NesImageLibrary[71 ] = {'name':'The Battle of Olympus',                                       'file':'C:\Users\omx\NES\\bot\img\\072.bmp',    'pixels':0 }
NesImageLibrary[72 ] = {'name':'Battle Tank',                                                 'file':'C:\Users\omx\NES\\bot\img\\073.bmp',    'pixels':0 }
NesImageLibrary[73 ] = {'name':'Battleship',                                                  'file':'C:\Users\omx\NES\\bot\img\\074.bmp',    'pixels':0 }
NesImageLibrary[74 ] = {'name':'Battletoads',                                                 'file':'C:\Users\omx\NES\\bot\img\\075.bmp',    'pixels':0 }
NesImageLibrary[75 ] = {'name':'Battletoads & Double Dragon',                                 'file':'C:\Users\omx\NES\\bot\img\\076.bmp',    'pixels':0 }
NesImageLibrary[76 ] = {'name':'Beetlejuice',                                                 'file':'C:\Users\omx\NES\\bot\img\\077.bmp',    'pixels':0 }
NesImageLibrary[77 ] = {'name':'Best of the Best: Championship Karate',                       'file':'C:\Users\omx\NES\\bot\img\\078.bmp',    'pixels':0 }
NesImageLibrary[78 ] = {'name':'Bigfoot',                                                     'file':'C:\Users\omx\NES\\bot\img\\079.bmp',    'pixels':0 }
NesImageLibrary[79 ] = {'name':'Bill & Ted\'s Excellent Video Game Adventure',                'file':'C:\Users\omx\NES\\bot\img\\080.bmp',    'pixels':0 }
NesImageLibrary[80 ] = {'name':'Bill Elliott\'s NASCAR Challenge',                            'file':'C:\Users\omx\NES\\bot\img\\081.bmp',    'pixels':0 }
NesImageLibrary[81 ] = {'name':'Bionic Commando',                                             'file':'C:\Users\omx\NES\\bot\img\\082.bmp',    'pixels':0 }
NesImageLibrary[82 ] = {'name':'The Black Bass',                                              'file':'C:\Users\omx\NES\\bot\img\\083.bmp',    'pixels':0 }
NesImageLibrary[83 ] = {'name':'Blades of Steel',                                             'file':'C:\Users\omx\NES\\bot\img\\084.bmp',    'pixels':0 }
NesImageLibrary[84 ] = {'name':'Blaster Master',                                              'file':'C:\Users\omx\NES\\bot\img\\085.bmp',    'pixels':0 }
NesImageLibrary[85 ] = {'name':'The Blue Marlin',                                             'file':'C:\Users\omx\NES\\bot\img\\086.bmp',    'pixels':0 }
NesImageLibrary[86 ] = {'name':'The Blues Brothers',                                          'file':'C:\Users\omx\NES\\bot\img\\087.bmp',    'pixels':0 }
NesImageLibrary[87 ] = {'name':'Bo Jackson Baseball',                                         'file':'C:\Users\omx\NES\\bot\img\\088.bmp',    'pixels':0 }
NesImageLibrary[88 ] = {'name':'Bomberman',                                                   'file':'C:\Users\omx\NES\\bot\img\\089.bmp',    'pixels':0 }
NesImageLibrary[89 ] = {'name':'Bomberman II',                                                'file':'C:\Users\omx\NES\\bot\img\\090.bmp',    'pixels':0 }
NesImageLibrary[90 ] = {'name':'Bonk\'s Adventure',                                           'file':'C:\Users\omx\NES\\bot\img\\091.bmp',    'pixels':0 }
NesImageLibrary[91 ] = {'name':'Boulder Dash',                                                'file':'C:\Users\omx\NES\\bot\img\\092.bmp',    'pixels':0 }
NesImageLibrary[92 ] = {'name':'A Boy and His Blob: Trouble on Blobolonia',                   'file':'C:\Users\omx\NES\\bot\img\\093.bmp',    'pixels':0 }
NesImageLibrary[93 ] = {'name':'Bram Stoker\'s Dracula',                                      'file':'C:\Users\omx\NES\\bot\img\\094.bmp',    'pixels':0 }
NesImageLibrary[94 ] = {'name':'Break Time: The National Pool Tour',                          'file':'C:\Users\omx\NES\\bot\img\\095.bmp',    'pixels':0 }
NesImageLibrary[95 ] = {'name':'BreakThru',                                                   'file':'C:\Users\omx\NES\\bot\img\\096.bmp',    'pixels':0 }
NesImageLibrary[96 ] = {'name':'Bubble Bobble',                                               'file':'C:\Users\omx\NES\\bot\img\\097.bmp',    'pixels':0 }
NesImageLibrary[97 ] = {'name':'Bubble Bobble Part 2',                                        'file':'C:\Users\omx\NES\\bot\img\\098.bmp',    'pixels':0 }
NesImageLibrary[98 ] = {'name':'Bucky O\'Hare',                                               'file':'C:\Users\omx\NES\\bot\img\\099.bmp',    'pixels':0 }
NesImageLibrary[99 ] = {'name':'The Bugs Bunny Birthday Blowout',                             'file':'C:\Users\omx\NES\\bot\img\\100.bmp',    'pixels':0 }
NesImageLibrary[100] = {'name':'The Bugs Bunny Crazy Castle',                                 'file':'C:\Users\omx\NES\\bot\img\\101.bmp',    'pixels':0 }
NesImageLibrary[101] = {'name':'Bump \'n\' Jump',                                             'file':'C:\Users\omx\NES\\bot\img\\102.bmp',    'pixels':0 }
NesImageLibrary[102] = {'name':'Burai Fighter',                                               'file':'C:\Users\omx\NES\\bot\img\\103.bmp',    'pixels':0 }
NesImageLibrary[103] = {'name':'BurgerTime',                                                  'file':'C:\Users\omx\NES\\bot\img\\104.bmp',    'pixels':0 }
NesImageLibrary[104] = {'name':'Cabal',                                                       'file':'C:\Users\omx\NES\\bot\img\\105.bmp',    'pixels':0 }
NesImageLibrary[105] = {'name':'Caesars Palace',                                              'file':'C:\Users\omx\NES\\bot\img\\106.bmp',    'pixels':0 }
NesImageLibrary[106] = {'name':'California Games',                                            'file':'C:\Users\omx\NES\\bot\img\\107.bmp',    'pixels':0 }
NesImageLibrary[107] = {'name':'Capcom\'s Gold Medal Challenge \'92',                         'file':'C:\Users\omx\NES\\bot\img\\108.bmp',    'pixels':0 }
NesImageLibrary[108] = {'name':'Captain America and The Avengers',                            'file':'C:\Users\omx\NES\\bot\img\\109.bmp',    'pixels':0 }
NesImageLibrary[109] = {'name':'Captain Planet',                                              'file':'C:\Users\omx\NES\\bot\img\\110.bmp',    'pixels':0 }
NesImageLibrary[110] = {'name':'Captain Skyhawk',                                             'file':'C:\Users\omx\NES\\bot\img\\111.bmp',    'pixels':0 }
NesImageLibrary[111] = {'name':'Casino Kid',                                                  'file':'C:\Users\omx\NES\\bot\img\\112.bmp',    'pixels':0 }
NesImageLibrary[112] = {'name':'Casino Kid 2',                                                'file':'C:\Users\omx\NES\\bot\img\\113.bmp',    'pixels':0 }
NesImageLibrary[113] = {'name':'Castelian',                                                   'file':'C:\Users\omx\NES\\bot\img\\114.bmp',    'pixels':0 }
NesImageLibrary[114] = {'name':'Castle of Dragon',                                            'file':'C:\Users\omx\NES\\bot\img\\115.bmp',    'pixels':0 }
NesImageLibrary[115] = {'name':'Castlequest',                                                 'file':'C:\Users\omx\NES\\bot\img\\116.bmp',    'pixels':0 }
NesImageLibrary[116] = {'name':'Castlevania',                                                 'file':'C:\Users\omx\NES\\bot\img\\117.bmp',    'pixels':0 }
NesImageLibrary[117] = {'name':'Castlevania II: Simon\'s Quest',                              'file':'C:\Users\omx\NES\\bot\img\\118.bmp',    'pixels':0 }
NesImageLibrary[118] = {'name':'Castlevania III: Dracula\'s Curse',                           'file':'C:\Users\omx\NES\\bot\img\\119.bmp',    'pixels':0 }
NesImageLibrary[119] = {'name':'Caveman Games',                                               'file':'C:\Users\omx\NES\\bot\img\\120.bmp',    'pixels':0 }
NesImageLibrary[120] = {'name':'Championship Bowling',                                        'file':'C:\Users\omx\NES\\bot\img\\121.bmp',    'pixels':0 }
NesImageLibrary[121] = {'name':'Championship Pool',                                           'file':'C:\Users\omx\NES\\bot\img\\122.bmp',    'pixels':0 }
NesImageLibrary[122] = {'name':'Championship Rally (PAL)',                                    'file':'C:\Users\omx\NES\\bot\img\\123.bmp',    'pixels':0 }
NesImageLibrary[123] = {'name':'Chessmaster',                                                 'file':'C:\Users\omx\NES\\bot\img\\124.bmp',    'pixels':0 }
NesImageLibrary[124] = {'name':'Chip \'n Dale: Rescue Rangers',                               'file':'C:\Users\omx\NES\\bot\img\\125.bmp',    'pixels':0 }
NesImageLibrary[125] = {'name':'Chip \'n Dale Rescue Rangers 2',                              'file':'C:\Users\omx\NES\\bot\img\\126.bmp',    'pixels':0 }
NesImageLibrary[126] = {'name':'Chubby Cherub',                                               'file':'C:\Users\omx\NES\\bot\img\\127.bmp',    'pixels':0 }
NesImageLibrary[127] = {'name':'Circus Caper',                                                'file':'C:\Users\omx\NES\\bot\img\\128.bmp',    'pixels':0 }
NesImageLibrary[128] = {'name':'City Connection',                                             'file':'C:\Users\omx\NES\\bot\img\\129.bmp',    'pixels':0 }
NesImageLibrary[129] = {'name':'Clash at Demonhead',                                          'file':'C:\Users\omx\NES\\bot\img\\130.bmp',    'pixels':0 }
NesImageLibrary[130] = {'name':'Classic Concentration',                                       'file':'C:\Users\omx\NES\\bot\img\\131.bmp',    'pixels':0 }
NesImageLibrary[131] = {'name':'Cliffhanger',                                                 'file':'C:\Users\omx\NES\\bot\img\\132.bmp',    'pixels':0 }
NesImageLibrary[132] = {'name':'Clu Clu Land',                                                'file':'C:\Users\omx\NES\\bot\img\\133.bmp',    'pixels':0 }
NesImageLibrary[133] = {'name':'Cobra Command',                                               'file':'C:\Users\omx\NES\\bot\img\\134.bmp',    'pixels':0 }
NesImageLibrary[134] = {'name':'Cobra Triangle',                                              'file':'C:\Users\omx\NES\\bot\img\\135.bmp',    'pixels':0 }
NesImageLibrary[135] = {'name':'Code Name: Viper',                                            'file':'C:\Users\omx\NES\\bot\img\\136.bmp',    'pixels':0 }
NesImageLibrary[136] = {'name':'Color a Dinosaur',                                            'file':'C:\Users\omx\NES\\bot\img\\137.bmp',    'pixels':0 }
NesImageLibrary[137] = {'name':'Commando',                                                    'file':'C:\Users\omx\NES\\bot\img\\138.bmp',    'pixels':0 }
NesImageLibrary[138] = {'name':'Conan: The Mysteries of Time',                                'file':'C:\Users\omx\NES\\bot\img\\139.bmp',    'pixels':0 }
NesImageLibrary[139] = {'name':'Conflict',                                                    'file':'C:\Users\omx\NES\\bot\img\\140.bmp',    'pixels':0 }
NesImageLibrary[140] = {'name':'Conquest of the Crystal Palace',                              'file':'C:\Users\omx\NES\\bot\img\\141.bmp',    'pixels':0 }
NesImageLibrary[141] = {'name':'Contra',                                                      'file':'C:\Users\omx\NES\\bot\img\\142.bmp',    'pixels':0 }
NesImageLibrary[142] = {'name':'Contra Force',                                                'file':'C:\Users\omx\NES\\bot\img\\143.bmp',    'pixels':0 }
NesImageLibrary[143] = {'name':'Cool World',                                                  'file':'C:\Users\omx\NES\\bot\img\\144.bmp',    'pixels':0 }
NesImageLibrary[144] = {'name':'Cowboy Kid',                                                  'file':'C:\Users\omx\NES\\bot\img\\145.bmp',    'pixels':0 }
NesImageLibrary[145] = {'name':'Crackout (PAL)',                                              'file':'C:\Users\omx\NES\\bot\img\\146.bmp',    'pixels':0 }
NesImageLibrary[146] = {'name':'Crash \'n the Boys: Street Challenge',                        'file':'C:\Users\omx\NES\\bot\img\\147.bmp',    'pixels':0 }
NesImageLibrary[147] = {'name':'Crystalis',                                                   'file':'C:\Users\omx\NES\\bot\img\\148.bmp',    'pixels':0 }
NesImageLibrary[148] = {'name':'Cyberball',                                                   'file':'C:\Users\omx\NES\\bot\img\\149.bmp',    'pixels':0 }
NesImageLibrary[149] = {'name':'Cybernoid: The Fighting Machine',                             'file':'C:\Users\omx\NES\\bot\img\\150.bmp',    'pixels':0 }
NesImageLibrary[150] = {'name':'Dance Aerobics',                                              'file':'C:\Users\omx\NES\\bot\img\\151.bmp',    'pixels':0 }
NesImageLibrary[151] = {'name':'Danny Sullivan\'s Indy Heat',                                 'file':'C:\Users\omx\NES\\bot\img\\152.bmp',    'pixels':0 }
NesImageLibrary[152] = {'name':'Darkman',                                                     'file':'C:\Users\omx\NES\\bot\img\\153.bmp',    'pixels':0 }
NesImageLibrary[153] = {'name':'Dash Galaxy in the Alien Asylum',                             'file':'C:\Users\omx\NES\\bot\img\\154.bmp',    'pixels':0 }
NesImageLibrary[154] = {'name':'Day Dreamin\' Davey',                                         'file':'C:\Users\omx\NES\\bot\img\\155.bmp',    'pixels':0 }
NesImageLibrary[155] = {'name':'Days of Thunder',                                             'file':'C:\Users\omx\NES\\bot\img\\156.bmp',    'pixels':0 }
NesImageLibrary[156] = {'name':'Deadly Towers',                                               'file':'C:\Users\omx\NES\\bot\img\\157.bmp',    'pixels':0 }
NesImageLibrary[157] = {'name':'Defender II',                                                 'file':'C:\Users\omx\NES\\bot\img\\158.bmp',    'pixels':0 }
NesImageLibrary[158] = {'name':'Defender of the Crown',                                       'file':'C:\Users\omx\NES\\bot\img\\159.bmp',    'pixels':0 }
NesImageLibrary[159] = {'name':'Defenders of Dynatron City',                                  'file':'C:\Users\omx\NES\\bot\img\\160.bmp',    'pixels':0 }
NesImageLibrary[160] = {'name':'Déjà Vu',                                                     'file':'C:\Users\omx\NES\\bot\img\\161.bmp',    'pixels':0 }
NesImageLibrary[161] = {'name':'Demon Sword',                                                 'file':'C:\Users\omx\NES\\bot\img\\162.bmp',    'pixels':0 }
NesImageLibrary[162] = {'name':'Desert Commander',                                            'file':'C:\Users\omx\NES\\bot\img\\163.bmp',    'pixels':0 }
NesImageLibrary[163] = {'name':'Destination Earthstar',                                       'file':'C:\Users\omx\NES\\bot\img\\164.bmp',    'pixels':0 }
NesImageLibrary[164] = {'name':'Destiny of an Emperor',                                       'file':'C:\Users\omx\NES\\bot\img\\165.bmp',    'pixels':0 }
NesImageLibrary[165] = {'name':'Devil World (PAL)',                                           'file':'C:\Users\omx\NES\\bot\img\\166.bmp',    'pixels':0 }
NesImageLibrary[166] = {'name':'Dick Tracy',                                                  'file':'C:\Users\omx\NES\\bot\img\\167.bmp',    'pixels':0 }
NesImageLibrary[167] = {'name':'Die Hard',                                                    'file':'C:\Users\omx\NES\\bot\img\\168.bmp',    'pixels':0 }
NesImageLibrary[168] = {'name':'Dig Dug II',                                                  'file':'C:\Users\omx\NES\\bot\img\\169.bmp',    'pixels':0 }
NesImageLibrary[169] = {'name':'Digger T. Rock: Legend of the Lost City',                     'file':'C:\Users\omx\NES\\bot\img\\170.bmp',    'pixels':0 }
NesImageLibrary[170] = {'name':'Dirty Harry: The War Against Drugs',                          'file':'C:\Users\omx\NES\\bot\img\\171.bmp',    'pixels':0 }
NesImageLibrary[171] = {'name':'Disney\'s Aladdin (PAL)',                                     'file':'C:\Users\omx\NES\\bot\img\\172.bmp',    'pixels':0 }
NesImageLibrary[172] = {'name':'Disney\'s Beauty and the Beast (PAL)',                        'file':'C:\Users\omx\NES\\bot\img\\173.bmp',    'pixels':0 }
NesImageLibrary[173] = {'name':'Disney\'s Darkwing Duck',                                     'file':'C:\Users\omx\NES\\bot\img\\174.bmp',    'pixels':0 }
NesImageLibrary[174] = {'name':'Disney\'s The Jungle Book',                                   'file':'C:\Users\omx\NES\\bot\img\\175.bmp',    'pixels':0 }
NesImageLibrary[175] = {'name':'Disney\'s The Lion King (PAL)',                               'file':'C:\Users\omx\NES\\bot\img\\176.bmp',    'pixels':0 }
NesImageLibrary[176] = {'name':'Disney\'s The Little Mermaid',                                'file':'C:\Users\omx\NES\\bot\img\\177.bmp',    'pixels':0 }
#NesImageLibrary[177] = {'name':'Donkey Kong',                                                 'file':'C:\Users\omx\NES\\bot\img\\178.bmp',    'pixels':0}
#NesImageLibrary[178] = {'name':'Donkey Kong 3',                                               'file':'C:\Users\omx\NES\\bot\img\\179.bmp',    'pixels':0}
#NesImageLibrary[179] = {'name':'Donkey Kong Classics',                                        'file':'C:\Users\omx\NES\\bot\img\\180.bmp',    'pixels':0}
#NesImageLibrary[180] = {'name':'Donkey Kong Jr.',                                             'file':'C:\Users\omx\NES\\bot\img\\181.bmp',    'pixels':0}
#NesImageLibrary[181] = {'name':'Donkey Kong Jr. Math',                                        'file':'C:\Users\omx\NES\\bot\img\\182.bmp',    'pixels':0}
#NesImageLibrary[182] = {'name':'Double Dare',                                                 'file':'C:\Users\omx\NES\\bot\img\\183.bmp',    'pixels':0}
#NesImageLibrary[183] = {'name':'Double Dragon',                                               'file':'C:\Users\omx\NES\\bot\img\\184.bmp',    'pixels':0}
#NesImageLibrary[184] = {'name':'Double Dragon II: The Revenge',                               'file':'C:\Users\omx\NES\\bot\img\\185.bmp',    'pixels':0}
#NesImageLibrary[185] = {'name':'Double Dragon III: The Sacred Stones',                        'file':'C:\Users\omx\NES\\bot\img\\186.bmp',    'pixels':0}
#NesImageLibrary[186] = {'name':'Double Dribble',                                              'file':'C:\Users\omx\NES\\bot\img\\187.bmp',    'pixels':0}
#NesImageLibrary[187] = {'name':'Dr. Chaos',                                                   'file':'C:\Users\omx\NES\\bot\img\\188.bmp',    'pixels':0}
#NesImageLibrary[188] = {'name':'Dr. Jekyll and Mr. Hyde',                                     'file':'C:\Users\omx\NES\\bot\img\\189.bmp',    'pixels':0}
#NesImageLibrary[189] = {'name':'Dr. Mario',                                                   'file':'C:\Users\omx\NES\\bot\img\\190.bmp',    'pixels':0}
#NesImageLibrary[190] = {'name':'Dragon Fighter',                                              'file':'C:\Users\omx\NES\\bot\img\\191.bmp',    'pixels':0}
#NesImageLibrary[191] = {'name':'Dragon Power',                                                'file':'C:\Users\omx\NES\\bot\img\\192.bmp',    'pixels':0}
#NesImageLibrary[192] = {'name':'Dragon Spirit',                                               'file':'C:\Users\omx\NES\\bot\img\\193.bmp',    'pixels':0}
#NesImageLibrary[193] = {'name':'Dragon Warrior',                                              'file':'C:\Users\omx\NES\\bot\img\\194.bmp',    'pixels':0}
#NesImageLibrary[194] = {'name':'Dragon Warrior II',                                           'file':'C:\Users\omx\NES\\bot\img\\195.bmp',    'pixels':0}
#NesImageLibrary[195] = {'name':'Dragon Warrior III',                                          'file':'C:\Users\omx\NES\\bot\img\\196.bmp',    'pixels':0}
#NesImageLibrary[196] = {'name':'Dragon Warrior IV',                                           'file':'C:\Users\omx\NES\\bot\img\\197.bmp',    'pixels':0}
#NesImageLibrary[197] = {'name':'Dragon's Lair',                                               'file':'C:\Users\omx\NES\\bot\img\\198.bmp',    'pixels':0}
#NesImageLibrary[198] = {'name':'Dropzone (PAL)',                                              'file':'C:\Users\omx\NES\\bot\img\\199.bmp',    'pixels':0}
#NesImageLibrary[199] = {'name':'Duck Hunt',                                                   'file':'C:\Users\omx\NES\\bot\img\\200.bmp',    'pixels':0}
#NesImageLibrary[200] = {'name':'DuckTales',                                                   'file':'C:\Users\omx\NES\\bot\img\\201.bmp',    'pixels':0}
#NesImageLibrary[201] = {'name':'DuckTales 2',                                                 'file':'C:\Users\omx\NES\\bot\img\\202.bmp',    'pixels':0}
#NesImageLibrary[202] = {'name':'Dungeon Magic: Sword of the Elements',                        'file':'C:\Users\omx\NES\\bot\img\\203.bmp',    'pixels':0}
#NesImageLibrary[203] = {'name':'Dusty Diamond's All-Star Softball',                           'file':'C:\Users\omx\NES\\bot\img\\204.bmp',    'pixels':0}
#NesImageLibrary[204] = {'name':'Dynowarz: Destruction of Spondylus',                          'file':'C:\Users\omx\NES\\bot\img\\205.bmp',    'pixels':0}
#NesImageLibrary[205] = {'name':'Elevator Action',                                             'file':'C:\Users\omx\NES\\bot\img\\206.bmp',    'pixels':0}
#NesImageLibrary[206] = {'name':'Eliminator Boat Duel',                                        'file':'C:\Users\omx\NES\\bot\img\\207.bmp',    'pixels':0}
#NesImageLibrary[207] = {'name':'Elite (PAL)',                                                 'file':'C:\Users\omx\NES\\bot\img\\208.bmp',    'pixels':0}
#NesImageLibrary[208] = {'name':'Excitebike',                                                  'file':'C:\Users\omx\NES\\bot\img\\209.bmp',    'pixels':0}
#NesImageLibrary[209] = {'name':'F-117A Stealth Fighter',                                      'file':'C:\Users\omx\NES\\bot\img\\210.bmp',    'pixels':0}
#NesImageLibrary[210] = {'name':'F-15 Strike Eagle',                                           'file':'C:\Users\omx\NES\\bot\img\\211.bmp',    'pixels':0}
#NesImageLibrary[211] = {'name':'Family Feud',                                                 'file':'C:\Users\omx\NES\\bot\img\\212.bmp',    'pixels':0}
#NesImageLibrary[212] = {'name':'Faria: A World of Mystery and Danger',                        'file':'C:\Users\omx\NES\\bot\img\\213.bmp',    'pixels':0}
#NesImageLibrary[213] = {'name':'Faxanadu',                                                    'file':'C:\Users\omx\NES\\bot\img\\214.bmp',    'pixels':0}
#NesImageLibrary[214] = {'name':'Felix the Cat',                                               'file':'C:\Users\omx\NES\\bot\img\\215.bmp',    'pixels':0}
#NesImageLibrary[215] = {'name':'Ferrari Grand Prix Challenge',                                'file':'C:\Users\omx\NES\\bot\img\\216.bmp',    'pixels':0}
#NesImageLibrary[216] = {'name':'Fester's Quest',                                              'file':'C:\Users\omx\NES\\bot\img\\217.bmp',    'pixels':0}
#NesImageLibrary[217] = {'name':'Final Fantasy',                                               'file':'C:\Users\omx\NES\\bot\img\\218.bmp',    'pixels':0}
#NesImageLibrary[218] = {'name':'Fire 'n Ice',                                                 'file':'C:\Users\omx\NES\\bot\img\\219.bmp',    'pixels':0}
#NesImageLibrary[219] = {'name':'Fisher-Price: Firehouse Rescue',                              'file':'C:\Users\omx\NES\\bot\img\\220.bmp',    'pixels':0}
#NesImageLibrary[220] = {'name':'Fisher-Price: I Can Remember',                                'file':'C:\Users\omx\NES\\bot\img\\221.bmp',    'pixels':0}
#NesImageLibrary[221] = {'name':'Fisher-Price: Perfect Fit',                                   'file':'C:\Users\omx\NES\\bot\img\\222.bmp',    'pixels':0}
#NesImageLibrary[222] = {'name':'Fist of the North Star',                                      'file':'C:\Users\omx\NES\\bot\img\\223.bmp',    'pixels':0}
#NesImageLibrary[223] = {'name':'Flight of the Intruder',                                      'file':'C:\Users\omx\NES\\bot\img\\224.bmp',    'pixels':0}
#NesImageLibrary[224] = {'name':'The Flintstones: The Rescue of Dino & Hoppy',                 'file':'C:\Users\omx\NES\\bot\img\\225.bmp',    'pixels':0}
#NesImageLibrary[225] = {'name':'The Flintstones: Surprise at Dinosaur Peak',                  'file':'C:\Users\omx\NES\\bot\img\\226.bmp',    'pixels':0}
#NesImageLibrary[226] = {'name':'Flying Dragon: The Secret Scroll',                            'file':'C:\Users\omx\NES\\bot\img\\227.bmp',    'pixels':0}
#NesImageLibrary[227] = {'name':'Flying Warriors',                                             'file':'C:\Users\omx\NES\\bot\img\\228.bmp',    'pixels':0}
#NesImageLibrary[228] = {'name':'Formula One: Built to Win',                                   'file':'C:\Users\omx\NES\\bot\img\\229.bmp',    'pixels':0}
#NesImageLibrary[229] = {'name':'Formula One Sensation (PAL)',                                 'file':'C:\Users\omx\NES\\bot\img\\230.bmp',    'pixels':0}
#NesImageLibrary[230] = {'name':'Frankenstein: The Monster Returns',                           'file':'C:\Users\omx\NES\\bot\img\\231.bmp',    'pixels':0}
#NesImageLibrary[231] = {'name':'Freedom Force',                                               'file':'C:\Users\omx\NES\\bot\img\\232.bmp',    'pixels':0}
#NesImageLibrary[232] = {'name':'Friday the 13th',                                             'file':'C:\Users\omx\NES\\bot\img\\233.bmp',    'pixels':0}
#NesImageLibrary[233] = {'name':'Fun House',                                                   'file':'C:\Users\omx\NES\\bot\img\\234.bmp',    'pixels':0}
#NesImageLibrary[234] = {'name':'G.I. Joe: A Real American Hero',                              'file':'C:\Users\omx\NES\\bot\img\\235.bmp',    'pixels':0}
#NesImageLibrary[235] = {'name':'G.I. Joe: The Atlantis Factor',                               'file':'C:\Users\omx\NES\\bot\img\\236.bmp',    'pixels':0}
#NesImageLibrary[236] = {'name':'Galaga',                                                      'file':'C:\Users\omx\NES\\bot\img\\237.bmp',    'pixels':0}
#NesImageLibrary[237] = {'name':'Galaxy 5000',                                                 'file':'C:\Users\omx\NES\\bot\img\\238.bmp',    'pixels':0}
#NesImageLibrary[238] = {'name':'Gargoyle's Quest II',                                         'file':'C:\Users\omx\NES\\bot\img\\239.bmp',    'pixels':0}
#NesImageLibrary[239] = {'name':'Gauntlet',                                                    'file':'C:\Users\omx\NES\\bot\img\\240.bmp',    'pixels':0}
#NesImageLibrary[240] = {'name':'Gauntlet II',                                                 'file':'C:\Users\omx\NES\\bot\img\\241.bmp',    'pixels':0}
#NesImageLibrary[241] = {'name':'Gemfire',                                                     'file':'C:\Users\omx\NES\\bot\img\\242.bmp',    'pixels':0}
#NesImageLibrary[242] = {'name':'Genghis Khan',                                                'file':'C:\Users\omx\NES\\bot\img\\243.bmp',    'pixels':0}
#NesImageLibrary[243] = {'name':'George Foreman's KO Boxing',                                  'file':'C:\Users\omx\NES\\bot\img\\244.bmp',    'pixels':0}
#NesImageLibrary[244] = {'name':'Ghostbusters',                                                'file':'C:\Users\omx\NES\\bot\img\\245.bmp',    'pixels':0}
#NesImageLibrary[245] = {'name':'Ghostbusters II',                                             'file':'C:\Users\omx\NES\\bot\img\\246.bmp',    'pixels':0}
#NesImageLibrary[246] = {'name':'Ghosts'n Goblins',                                            'file':'C:\Users\omx\NES\\bot\img\\247.bmp',    'pixels':0}
#NesImageLibrary[247] = {'name':'Ghoul School',                                                'file':'C:\Users\omx\NES\\bot\img\\248.bmp',    'pixels':0}
#NesImageLibrary[248] = {'name':'Goal!',                                                       'file':'C:\Users\omx\NES\\bot\img\\249.bmp',    'pixels':0}
#NesImageLibrary[249] = {'name':'Goal! Two',                                                   'file':'C:\Users\omx\NES\\bot\img\\250.bmp',    'pixels':0}
#NesImageLibrary[250] = {'name':'Godzilla: Monster of Monsters',                               'file':'C:\Users\omx\NES\\bot\img\\251.bmp',    'pixels':0}
#NesImageLibrary[251] = {'name':'Godzilla 2: War of the Monsters',                             'file':'C:\Users\omx\NES\\bot\img\\252.bmp',    'pixels':0}
#NesImageLibrary[252] = {'name':'Golf',                                                        'file':'C:\Users\omx\NES\\bot\img\\253.bmp',    'pixels':0}
#NesImageLibrary[253] = {'name':'Golf Grand Slam',                                             'file':'C:\Users\omx\NES\\bot\img\\254.bmp',    'pixels':0}
#NesImageLibrary[254] = {'name':'Golgo 13: Top Secret Episode',                                'file':'C:\Users\omx\NES\\bot\img\\255.bmp',    'pixels':0}
#NesImageLibrary[255] = {'name':'The Goonies II',                                              'file':'C:\Users\omx\NES\\bot\img\\256.bmp',    'pixels':0}
#NesImageLibrary[256] = {'name':'Gotcha! The Sport!',                                          'file':'C:\Users\omx\NES\\bot\img\\257.bmp',    'pixels':0}
#NesImageLibrary[257] = {'name':'Gradius',                                                     'file':'C:\Users\omx\NES\\bot\img\\258.bmp',    'pixels':0}
#NesImageLibrary[258] = {'name':'The Great Waldo Search',                                      'file':'C:\Users\omx\NES\\bot\img\\259.bmp',    'pixels':0}
#NesImageLibrary[259] = {'name':'Greg Norman's Golf Power',                                    'file':'C:\Users\omx\NES\\bot\img\\260.bmp',    'pixels':0}
#NesImageLibrary[260] = {'name':'Gremlins 2: The New Batch',                                   'file':'C:\Users\omx\NES\\bot\img\\261.bmp',    'pixels':0}
#NesImageLibrary[261] = {'name':'The Guardian Legend',                                         'file':'C:\Users\omx\NES\\bot\img\\262.bmp',    'pixels':0}
#NesImageLibrary[262] = {'name':'Guerrilla War',                                               'file':'C:\Users\omx\NES\\bot\img\\263.bmp',    'pixels':0}
#NesImageLibrary[263] = {'name':'Gumshoe',                                                     'file':'C:\Users\omx\NES\\bot\img\\264.bmp',    'pixels':0}
#NesImageLibrary[264] = {'name':'Gun-Nac',                                                     'file':'C:\Users\omx\NES\\bot\img\\265.bmp',    'pixels':0}
#NesImageLibrary[265] = {'name':'Gun.Smoke',                                                   'file':'C:\Users\omx\NES\\bot\img\\266.bmp',    'pixels':0}
#NesImageLibrary[266] = {'name':'Gyromite',                                                    'file':'C:\Users\omx\NES\\bot\img\\267.bmp',    'pixels':0}
#NesImageLibrary[267] = {'name':'Gyruss',                                                      'file':'C:\Users\omx\NES\\bot\img\\268.bmp',    'pixels':0}
#NesImageLibrary[268] = {'name':'Hammerin' Harry (PAL)',                                       'file':'C:\Users\omx\NES\\bot\img\\269.bmp',    'pixels':0}
#NesImageLibrary[269] = {'name':'Harlem Globetrotters',                                        'file':'C:\Users\omx\NES\\bot\img\\270.bmp',    'pixels':0}
#NesImageLibrary[270] = {'name':'Hatris',                                                      'file':'C:\Users\omx\NES\\bot\img\\271.bmp',    'pixels':0}
#NesImageLibrary[271] = {'name':'Heavy Barrel',                                                'file':'C:\Users\omx\NES\\bot\img\\272.bmp',    'pixels':0}
#NesImageLibrary[272] = {'name':'Heavy Shreddin'',                                             'file':'C:\Users\omx\NES\\bot\img\\273.bmp',    'pixels':0}
#NesImageLibrary[273] = {'name':'High Speed',                                                  'file':'C:\Users\omx\NES\\bot\img\\274.bmp',    'pixels':0}
#NesImageLibrary[274] = {'name':'Hogan's Alley',                                               'file':'C:\Users\omx\NES\\bot\img\\275.bmp',    'pixels':0}
#NesImageLibrary[275] = {'name':'Hollywood Squares',                                           'file':'C:\Users\omx\NES\\bot\img\\276.bmp',    'pixels':0}
#NesImageLibrary[276] = {'name':'Home Alone',                                                  'file':'C:\Users\omx\NES\\bot\img\\277.bmp',    'pixels':0}
#NesImageLibrary[277] = {'name':'Home Alone 2: Lost in New York',                              'file':'C:\Users\omx\NES\\bot\img\\278.bmp',    'pixels':0}
#NesImageLibrary[278] = {'name':'Hook',                                                        'file':'C:\Users\omx\NES\\bot\img\\279.bmp',    'pixels':0}
#NesImageLibrary[279] = {'name':'Hoops',                                                       'file':'C:\Users\omx\NES\\bot\img\\280.bmp',    'pixels':0}
#NesImageLibrary[280] = {'name':'Hudson Hawk',                                                 'file':'C:\Users\omx\NES\\bot\img\\281.bmp',    'pixels':0}
#NesImageLibrary[281] = {'name':'The Hunt for Red October',                                    'file':'C:\Users\omx\NES\\bot\img\\282.bmp',    'pixels':0}
#NesImageLibrary[282] = {'name':'Hydlide',                                                     'file':'C:\Users\omx\NES\\bot\img\\283.bmp',    'pixels':0}
#NesImageLibrary[283] = {'name':'Ice Climber',                                                 'file':'C:\Users\omx\NES\\bot\img\\284.bmp',    'pixels':0}
#NesImageLibrary[284] = {'name':'Ice Hockey',                                                  'file':'C:\Users\omx\NES\\bot\img\\285.bmp',    'pixels':0}
#NesImageLibrary[285] = {'name':'Ikari Warriors',                                              'file':'C:\Users\omx\NES\\bot\img\\286.bmp',    'pixels':0}
#NesImageLibrary[286] = {'name':'Ikari Warriors II: Victory Road',                             'file':'C:\Users\omx\NES\\bot\img\\287.bmp',    'pixels':0}
#NesImageLibrary[287] = {'name':'Ikari Warriors III: The Rescue',                              'file':'C:\Users\omx\NES\\bot\img\\288.bmp',    'pixels':0}
#NesImageLibrary[288] = {'name':'Image Fight',                                                 'file':'C:\Users\omx\NES\\bot\img\\289.bmp',    'pixels':0}
#NesImageLibrary[289] = {'name':'The Immortal',                                                'file':'C:\Users\omx\NES\\bot\img\\290.bmp',    'pixels':0}
#NesImageLibrary[290] = {'name':'The Incredible Crash Dummies',                                'file':'C:\Users\omx\NES\\bot\img\\291.bmp',    'pixels':0}
#NesImageLibrary[291] = {'name':'Indiana Jones and the Last Crusade (Taito-1991)',             'file':'C:\Users\omx\NES\\bot\img\\292.bmp',    'pixels':0}
#NesImageLibrary[292] = {'name':'Indiana Jones and the Last Crusade (Ubisoft-1993)',           'file':'C:\Users\omx\NES\\bot\img\\293.bmp',    'pixels':0}
#NesImageLibrary[293] = {'name':'Indiana Jones and the Temple of Doom',                        'file':'C:\Users\omx\NES\\bot\img\\294.bmp',    'pixels':0}
#NesImageLibrary[294] = {'name':'Infiltrator',                                                 'file':'C:\Users\omx\NES\\bot\img\\295.bmp',    'pixels':0}
#NesImageLibrary[295] = {'name':'International Cricket (PAL)',                                 'file':'C:\Users\omx\NES\\bot\img\\296.bmp',    'pixels':0}
#NesImageLibrary[296] = {'name':'Iron Tank',                                                   'file':'C:\Users\omx\NES\\bot\img\\297.bmp',    'pixels':0}
#NesImageLibrary[297] = {'name':'Ironsword: Wizards & Warriors II',                            'file':'C:\Users\omx\NES\\bot\img\\298.bmp',    'pixels':0}
#NesImageLibrary[298] = {'name':'Isolated Warrior',                                            'file':'C:\Users\omx\NES\\bot\img\\299.bmp',    'pixels':0}
#NesImageLibrary[299] = {'name':'Ivan 'Ironman' Stewart's Super Off Road',                     'file':'C:\Users\omx\NES\\bot\img\\300.bmp',    'pixels':0}
#NesImageLibrary[300] = {'name':'Jack Nicklaus' Greatest 18 Holes of Major Championship Golf', 'file':'C:\Users\omx\NES\\bot\img\\301.bmp',    'pixels':0}
#NesImageLibrary[301] = {'name':'Jackal',                                                      'file':'C:\Users\omx\NES\\bot\img\\302.bmp',    'pixels':0}
#NesImageLibrary[302] = {'name':'Jackie Chan's Action Kung Fu',                                'file':'C:\Users\omx\NES\\bot\img\\303.bmp',    'pixels':0}
#NesImageLibrary[303] = {'name':'James Bond Jr.',                                              'file':'C:\Users\omx\NES\\bot\img\\304.bmp',    'pixels':0}
#NesImageLibrary[304] = {'name':'Jaws',                                                        'file':'C:\Users\omx\NES\\bot\img\\305.bmp',    'pixels':0}
#NesImageLibrary[305] = {'name':'Jeopardy!',                                                   'file':'C:\Users\omx\NES\\bot\img\\306.bmp',    'pixels':0}
#NesImageLibrary[306] = {'name':'Jeopardy! 25th Anniversary Edition',                          'file':'C:\Users\omx\NES\\bot\img\\307.bmp',    'pixels':0}
#NesImageLibrary[307] = {'name':'Jeopardy! Junior Edition',                                    'file':'C:\Users\omx\NES\\bot\img\\308.bmp',    'pixels':0}
#NesImageLibrary[308] = {'name':'The Jetsons: Cogswell's Caper!',                              'file':'C:\Users\omx\NES\\bot\img\\309.bmp',    'pixels':0}
#NesImageLibrary[309] = {'name':'Jimmy Connors Tennis',                                        'file':'C:\Users\omx\NES\\bot\img\\310.bmp',    'pixels':0}
#NesImageLibrary[310] = {'name':'Joe & Mac',                                                   'file':'C:\Users\omx\NES\\bot\img\\311.bmp',    'pixels':0}
#NesImageLibrary[311] = {'name':'John Elway's Quarterback',                                    'file':'C:\Users\omx\NES\\bot\img\\312.bmp',    'pixels':0}
#NesImageLibrary[312] = {'name':'Jordan vs. Bird: One on One',                                 'file':'C:\Users\omx\NES\\bot\img\\313.bmp',    'pixels':0}
#NesImageLibrary[313] = {'name':'Journey to Silius',                                           'file':'C:\Users\omx\NES\\bot\img\\314.bmp',    'pixels':0}
#NesImageLibrary[314] = {'name':'Joust',                                                       'file':'C:\Users\omx\NES\\bot\img\\315.bmp',    'pixels':0}
#NesImageLibrary[315] = {'name':'Jurassic Park',                                               'file':'C:\Users\omx\NES\\bot\img\\316.bmp',    'pixels':0}
#NesImageLibrary[316] = {'name':'Kabuki Quantum Fighter',                                      'file':'C:\Users\omx\NES\\bot\img\\317.bmp',    'pixels':0}
#NesImageLibrary[317] = {'name':'Karate Champ',                                                'file':'C:\Users\omx\NES\\bot\img\\318.bmp',    'pixels':0}
#NesImageLibrary[318] = {'name':'The Karate Kid',                                              'file':'C:\Users\omx\NES\\bot\img\\319.bmp',    'pixels':0}
#NesImageLibrary[319] = {'name':'Karnov',                                                      'file':'C:\Users\omx\NES\\bot\img\\320.bmp',    'pixels':0}
#NesImageLibrary[320] = {'name':'Kick Master',                                                 'file':'C:\Users\omx\NES\\bot\img\\321.bmp',    'pixels':0}
#NesImageLibrary[321] = {'name':'Kick Off (PAL)',                                              'file':'C:\Users\omx\NES\\bot\img\\322.bmp',    'pixels':0}
#NesImageLibrary[322] = {'name':'Kickle Cubicle',                                              'file':'C:\Users\omx\NES\\bot\img\\323.bmp',    'pixels':0}
#NesImageLibrary[323] = {'name':'Kid Icarus',                                                  'file':'C:\Users\omx\NES\\bot\img\\324.bmp',    'pixels':0}
#NesImageLibrary[324] = {'name':'Kid Klown in Night Mayor World',                              'file':'C:\Users\omx\NES\\bot\img\\325.bmp',    'pixels':0}
#NesImageLibrary[325] = {'name':'Kid Kool',                                                    'file':'C:\Users\omx\NES\\bot\img\\326.bmp',    'pixels':0}
#NesImageLibrary[326] = {'name':'Kid Niki: Radical Ninja',                                     'file':'C:\Users\omx\NES\\bot\img\\327.bmp',    'pixels':0}
#NesImageLibrary[327] = {'name':'King's Knight',                                               'file':'C:\Users\omx\NES\\bot\img\\328.bmp',    'pixels':0}
#NesImageLibrary[328] = {'name':'Kings of the Beach',                                          'file':'C:\Users\omx\NES\\bot\img\\329.bmp',    'pixels':0}
#NesImageLibrary[329] = {'name':'King's Quest V: Absence Makes the Heart Go Yonder!',          'file':'C:\Users\omx\NES\\bot\img\\330.bmp',    'pixels':0}
#NesImageLibrary[330] = {'name':'Kirby's Adventure',                                           'file':'C:\Users\omx\NES\\bot\img\\331.bmp',    'pixels':0}
#NesImageLibrary[331] = {'name':'Kiwi Kraze',                                                  'file':'C:\Users\omx\NES\\bot\img\\332.bmp',    'pixels':0}
#NesImageLibrary[332] = {'name':'KlashBall',                                                   'file':'C:\Users\omx\NES\\bot\img\\333.bmp',    'pixels':0}
#NesImageLibrary[333] = {'name':'Knight Rider',                                                'file':'C:\Users\omx\NES\\bot\img\\334.bmp',    'pixels':0}
#NesImageLibrary[334] = {'name':'Konami Hyper Soccer (PAL)',                                   'file':'C:\Users\omx\NES\\bot\img\\335.bmp',    'pixels':0}
#NesImageLibrary[335] = {'name':'The Krion Conquest',                                          'file':'C:\Users\omx\NES\\bot\img\\336.bmp',    'pixels':0}
#NesImageLibrary[336] = {'name':'Krusty's Fun House',                                          'file':'C:\Users\omx\NES\\bot\img\\337.bmp',    'pixels':0}
#NesImageLibrary[337] = {'name':'Kung-Fu Master',                                              'file':'C:\Users\omx\NES\\bot\img\\338.bmp',    'pixels':0}
#NesImageLibrary[338] = {'name':'Kung-Fu Heroes',                                              'file':'C:\Users\omx\NES\\bot\img\\339.bmp',    'pixels':0}
#NesImageLibrary[339] = {'name':'Laser Invasion',                                              'file':'C:\Users\omx\NES\\bot\img\\340.bmp',    'pixels':0}
#NesImageLibrary[340] = {'name':'Last Action Hero',                                            'file':'C:\Users\omx\NES\\bot\img\\341.bmp',    'pixels':0}
#NesImageLibrary[341] = {'name':'The Last Ninja',                                              'file':'C:\Users\omx\NES\\bot\img\\342.bmp',    'pixels':0}
#NesImageLibrary[342] = {'name':'The Last Starfighter',                                        'file':'C:\Users\omx\NES\\bot\img\\343.bmp',    'pixels':0}
#NesImageLibrary[343] = {'name':'Lee Trevino's Fighting Golf',                                 'file':'C:\Users\omx\NES\\bot\img\\344.bmp',    'pixels':0}
#NesImageLibrary[344] = {'name':'Legacy of the Wizard',                                        'file':'C:\Users\omx\NES\\bot\img\\345.bmp',    'pixels':0}
#NesImageLibrary[345] = {'name':'Legend of the Ghost Lion',                                    'file':'C:\Users\omx\NES\\bot\img\\346.bmp',    'pixels':0}
#NesImageLibrary[346] = {'name':'The Legend of Kage',                                          'file':'C:\Users\omx\NES\\bot\img\\347.bmp',    'pixels':0}
#NesImageLibrary[347] = {'name':'The Legend of Prince Valiant (PAL)',                          'file':'C:\Users\omx\NES\\bot\img\\348.bmp',    'pixels':0}
#NesImageLibrary[348] = {'name':'The Legend of Zelda',                                         'file':'C:\Users\omx\NES\\bot\img\\349.bmp',    'pixels':0}
#NesImageLibrary[349] = {'name':'Legendary Wings',                                             'file':'C:\Users\omx\NES\\bot\img\\350.bmp',    'pixels':0}
#NesImageLibrary[350] = {'name':'Legends of the Diamond',                                      'file':'C:\Users\omx\NES\\bot\img\\351.bmp',    'pixels':0}
#NesImageLibrary[351] = {'name':'Lemmings',                                                    'file':'C:\Users\omx\NES\\bot\img\\352.bmp',    'pixels':0}
#NesImageLibrary[352] = {'name':'Les Chevaliers du Zodiaque (PAL)',                            'file':'C:\Users\omx\NES\\bot\img\\353.bmp',    'pixels':0}
#NesImageLibrary[353] = {'name':'L'Empereur',                                                  'file':'C:\Users\omx\NES\\bot\img\\354.bmp',    'pixels':0}
#NesImageLibrary[354] = {'name':'Lethal Weapon',                                               'file':'C:\Users\omx\NES\\bot\img\\355.bmp',    'pixels':0}
#NesImageLibrary[355] = {'name':'Life Force',                                                  'file':'C:\Users\omx\NES\\bot\img\\356.bmp',    'pixels':0}
#NesImageLibrary[356] = {'name':'Little League Baseball: Championship Series',                 'file':'C:\Users\omx\NES\\bot\img\\357.bmp',    'pixels':0}
#NesImageLibrary[357] = {'name':'Little Nemo: The Dream Master',                               'file':'C:\Users\omx\NES\\bot\img\\358.bmp',    'pixels':0}
#NesImageLibrary[358] = {'name':'Little Ninja Brothers',                                       'file':'C:\Users\omx\NES\\bot\img\\359.bmp',    'pixels':0}
#NesImageLibrary[359] = {'name':'Little Samson',                                               'file':'C:\Users\omx\NES\\bot\img\\360.bmp',    'pixels':0}
#NesImageLibrary[360] = {'name':'Lode Runner',                                                 'file':'C:\Users\omx\NES\\bot\img\\361.bmp',    'pixels':0}
#NesImageLibrary[361] = {'name':'The Lone Ranger',                                             'file':'C:\Users\omx\NES\\bot\img\\362.bmp',    'pixels':0}
#NesImageLibrary[362] = {'name':'Loopz',                                                       'file':'C:\Users\omx\NES\\bot\img\\363.bmp',    'pixels':0}
#NesImageLibrary[363] = {'name':'Low G Man: The Low Gravity Man',                              'file':'C:\Users\omx\NES\\bot\img\\364.bmp',    'pixels':0}
#NesImageLibrary[364] = {'name':'Lunar Pool',                                                  'file':'C:\Users\omx\NES\\bot\img\\365.bmp',    'pixels':0}
#NesImageLibrary[365] = {'name':'M.C. Kids',                                                   'file':'C:\Users\omx\NES\\bot\img\\366.bmp',    'pixels':0}
#NesImageLibrary[366] = {'name':'M.U.L.E.',                                                    'file':'C:\Users\omx\NES\\bot\img\\367.bmp',    'pixels':0}
#NesImageLibrary[367] = {'name':'M.U.S.C.L.E.',                                                'file':'C:\Users\omx\NES\\bot\img\\368.bmp',    'pixels':0}
#NesImageLibrary[368] = {'name':'Mach Rider',                                                  'file':'C:\Users\omx\NES\\bot\img\\369.bmp',    'pixels':0}
#NesImageLibrary[369] = {'name':'Mad Max',                                                     'file':'C:\Users\omx\NES\\bot\img\\370.bmp',    'pixels':0}
#NesImageLibrary[370] = {'name':'The Mafat Conspiracy',                                        'file':'C:\Users\omx\NES\\bot\img\\371.bmp',    'pixels':0}
#NesImageLibrary[371] = {'name':'Magic Darts',                                                 'file':'C:\Users\omx\NES\\bot\img\\372.bmp',    'pixels':0}
#NesImageLibrary[372] = {'name':'Magic Johnson's Fast Break',                                  'file':'C:\Users\omx\NES\\bot\img\\373.bmp',    'pixels':0}
#NesImageLibrary[373] = {'name':'The Magic of Scheherazade',                                   'file':'C:\Users\omx\NES\\bot\img\\374.bmp',    'pixels':0}
#NesImageLibrary[374] = {'name':'Magician',                                                    'file':'C:\Users\omx\NES\\bot\img\\375.bmp',    'pixels':0}
#NesImageLibrary[375] = {'name':'MagMax',                                                      'file':'C:\Users\omx\NES\\bot\img\\376.bmp',    'pixels':0}
#NesImageLibrary[376] = {'name':'Major League Baseball',                                       'file':'C:\Users\omx\NES\\bot\img\\377.bmp',    'pixels':0}
#NesImageLibrary[377] = {'name':'Maniac Mansion',                                              'file':'C:\Users\omx\NES\\bot\img\\378.bmp',    'pixels':0}
#NesImageLibrary[378] = {'name':'Mappy-Land',                                                  'file':'C:\Users\omx\NES\\bot\img\\379.bmp',    'pixels':0}
#NesImageLibrary[379] = {'name':'Marble Madness',                                              'file':'C:\Users\omx\NES\\bot\img\\380.bmp',    'pixels':0}
#NesImageLibrary[380] = {'name':'Mario Bros.',                                                 'file':'C:\Users\omx\NES\\bot\img\\381.bmp',    'pixels':0}
#NesImageLibrary[381] = {'name':'Mario Bros. Classics Edition (PAL)',                          'file':'C:\Users\omx\NES\\bot\img\\382.bmp',    'pixels':0}
#NesImageLibrary[382] = {'name':'Mario Is Missing!',                                           'file':'C:\Users\omx\NES\\bot\img\\383.bmp',    'pixels':0}
#NesImageLibrary[383] = {'name':'Mario's Time Machine',                                        'file':'C:\Users\omx\NES\\bot\img\\384.bmp',    'pixels':0}
#NesImageLibrary[384] = {'name':'Mechanized Attack',                                           'file':'C:\Users\omx\NES\\bot\img\\385.bmp',    'pixels':0}
#NesImageLibrary[385] = {'name':'Mega Man',                                                    'file':'C:\Users\omx\NES\\bot\img\\386.bmp',    'pixels':0}
#NesImageLibrary[386] = {'name':'Mega Man 2',                                                  'file':'C:\Users\omx\NES\\bot\img\\387.bmp',    'pixels':0}
#NesImageLibrary[387] = {'name':'Mega Man 3',                                                  'file':'C:\Users\omx\NES\\bot\img\\388.bmp',    'pixels':0}
#NesImageLibrary[388] = {'name':'Mega Man 4',                                                  'file':'C:\Users\omx\NES\\bot\img\\389.bmp',    'pixels':0}
#NesImageLibrary[389] = {'name':'Mega Man 5',                                                  'file':'C:\Users\omx\NES\\bot\img\\390.bmp',    'pixels':0}
#NesImageLibrary[390] = {'name':'Mega Man 6',                                                  'file':'C:\Users\omx\NES\\bot\img\\391.bmp',    'pixels':0}
#NesImageLibrary[391] = {'name':'Mendel Palace',                                               'file':'C:\Users\omx\NES\\bot\img\\392.bmp',    'pixels':0}
#NesImageLibrary[392] = {'name':'Metal Gear',                                                  'file':'C:\Users\omx\NES\\bot\img\\393.bmp',    'pixels':0}
#NesImageLibrary[393] = {'name':'Metal Mech',                                                  'file':'C:\Users\omx\NES\\bot\img\\394.bmp',    'pixels':0}
#NesImageLibrary[394] = {'name':'Metal Storm',                                                 'file':'C:\Users\omx\NES\\bot\img\\395.bmp',    'pixels':0}
#NesImageLibrary[395] = {'name':'Metroid',                                                     'file':'C:\Users\omx\NES\\bot\img\\396.bmp',    'pixels':0}
#NesImageLibrary[396] = {'name':'Michael Andretti's World GP',                                 'file':'C:\Users\omx\NES\\bot\img\\397.bmp',    'pixels':0}
#NesImageLibrary[397] = {'name':'Mickey Mousecapade',                                          'file':'C:\Users\omx\NES\\bot\img\\398.bmp',    'pixels':0}
#NesImageLibrary[398] = {'name':'Mickey's Adventures in Numberland',                           'file':'C:\Users\omx\NES\\bot\img\\399.bmp',    'pixels':0}
#NesImageLibrary[399] = {'name':'Mickey's Safari in Letterland',                               'file':'C:\Users\omx\NES\\bot\img\\400.bmp',    'pixels':0}
#NesImageLibrary[400] = {'name':'Might and Magic Book One: The Secret of the Inner Sanctum',   'file':'C:\Users\omx\NES\\bot\img\\401.bmp',    'pixels':0}
#NesImageLibrary[401] = {'name':'Mighty Bomb Jack',                                            'file':'C:\Users\omx\NES\\bot\img\\402.bmp',    'pixels':0}
#NesImageLibrary[402] = {'name':'Mighty Final Fight',                                          'file':'C:\Users\omx\NES\\bot\img\\403.bmp',    'pixels':0}
#NesImageLibrary[403] = {'name':'Mike Tyson's Punch-Out!!',                                    'file':'C:\Users\omx\NES\\bot\img\\404.bmp',    'pixels':0}
#NesImageLibrary[404] = {'name':'Millipede',                                                   'file':'C:\Users\omx\NES\\bot\img\\405.bmp',    'pixels':0}
#NesImageLibrary[405] = {'name':'Milon's Secret Castle',                                       'file':'C:\Users\omx\NES\\bot\img\\406.bmp',    'pixels':0}
#NesImageLibrary[406] = {'name':'Miracle Piano Teaching System',                               'file':'C:\Users\omx\NES\\bot\img\\407.bmp',    'pixels':0}
#NesImageLibrary[407] = {'name':'Mission: Impossible',                                         'file':'C:\Users\omx\NES\\bot\img\\408.bmp',    'pixels':0}
#NesImageLibrary[408] = {'name':'Monopoly',                                                    'file':'C:\Users\omx\NES\\bot\img\\409.bmp',    'pixels':0}
#NesImageLibrary[409] = {'name':'Monster in My Pocket',                                        'file':'C:\Users\omx\NES\\bot\img\\410.bmp',    'pixels':0}
#NesImageLibrary[410] = {'name':'Monster Party',                                               'file':'C:\Users\omx\NES\\bot\img\\411.bmp',    'pixels':0}
#NesImageLibrary[411] = {'name':'Monster Truck Rally',                                         'file':'C:\Users\omx\NES\\bot\img\\412.bmp',    'pixels':0}
#NesImageLibrary[412] = {'name':'Motor City Patrol',                                           'file':'C:\Users\omx\NES\\bot\img\\413.bmp',    'pixels':0}
#NesImageLibrary[413] = {'name':'Mr. Gimmick! (PAL)',                                          'file':'C:\Users\omx\NES\\bot\img\\414.bmp',    'pixels':0}
#NesImageLibrary[414] = {'name':'Ms. Pac-Man (Namco)',                                         'file':'C:\Users\omx\NES\\bot\img\\415.bmp',    'pixels':0}
#NesImageLibrary[415] = {'name':'Muppet Adventure: Chaos at the Carnival',                     'file':'C:\Users\omx\NES\\bot\img\\416.bmp',    'pixels':0}
#NesImageLibrary[416] = {'name':'The Mutant Virus: Crisis in a Computer World',                'file':'C:\Users\omx\NES\\bot\img\\417.bmp',    'pixels':0}
#NesImageLibrary[417] = {'name':'Mystery Quest',                                               'file':'C:\Users\omx\NES\\bot\img\\418.bmp',    'pixels':0}
#NesImageLibrary[418] = {'name':'NARC',                                                        'file':'C:\Users\omx\NES\\bot\img\\419.bmp',    'pixels':0}
#NesImageLibrary[419] = {'name':'NES Open Tournament Golf',                                    'file':'C:\Users\omx\NES\\bot\img\\420.bmp',    'pixels':0}
#NesImageLibrary[420] = {'name':'NES Play Action Football',                                    'file':'C:\Users\omx\NES\\bot\img\\421.bmp',    'pixels':0}
#NesImageLibrary[421] = {'name':'New Ghostbusters II (PAL)',                                   'file':'C:\Users\omx\NES\\bot\img\\422.bmp',    'pixels':0}
#NesImageLibrary[422] = {'name':'NFL',                                                         'file':'C:\Users\omx\NES\\bot\img\\423.bmp',    'pixels':0}
#NesImageLibrary[423] = {'name':'Nigel Mansell's World Championship Racing',                   'file':'C:\Users\omx\NES\\bot\img\\424.bmp',    'pixels':0}
#NesImageLibrary[424] = {'name':'A Nightmare on Elm Street',                                   'file':'C:\Users\omx\NES\\bot\img\\425.bmp',    'pixels':0}
#NesImageLibrary[425] = {'name':'Nightshade',                                                  'file':'C:\Users\omx\NES\\bot\img\\426.bmp',    'pixels':0}
#NesImageLibrary[426] = {'name':'Ninja Crusaders',                                             'file':'C:\Users\omx\NES\\bot\img\\427.bmp',    'pixels':0}
#NesImageLibrary[427] = {'name':'Ninja Gaiden',                                                'file':'C:\Users\omx\NES\\bot\img\\428.bmp',    'pixels':0}
#NesImageLibrary[428] = {'name':'Ninja Gaiden II: The Dark Sword of Chaos',                    'file':'C:\Users\omx\NES\\bot\img\\429.bmp',    'pixels':0}
#NesImageLibrary[429] = {'name':'Ninja Gaiden III: The Ancient Ship of Doom',                  'file':'C:\Users\omx\NES\\bot\img\\430.bmp',    'pixels':0}
#NesImageLibrary[430] = {'name':'Ninja Kid',                                                   'file':'C:\Users\omx\NES\\bot\img\\431.bmp',    'pixels':0}
#NesImageLibrary[431] = {'name':'Nintendo Campus Challenge',                                   'file':'C:\Users\omx\NES\\bot\img\\432.bmp',    'pixels':0}
#NesImageLibrary[432] = {'name':'Nintendo World Championships',                                'file':'C:\Users\omx\NES\\bot\img\\433.bmp',    'pixels':0}
#NesImageLibrary[433] = {'name':'Nintendo World Cup',                                          'file':'C:\Users\omx\NES\\bot\img\\434.bmp',    'pixels':0}
#NesImageLibrary[434] = {'name':'Noah's Ark (PAL)',                                            'file':'C:\Users\omx\NES\\bot\img\\435.bmp',    'pixels':0}
#NesImageLibrary[435] = {'name':'Nobunaga's Ambition',                                         'file':'C:\Users\omx\NES\\bot\img\\436.bmp',    'pixels':0}
#NesImageLibrary[436] = {'name':'Nobunaga's Ambition II',                                      'file':'C:\Users\omx\NES\\bot\img\\437.bmp',    'pixels':0}
#NesImageLibrary[437] = {'name':'North & South',                                               'file':'C:\Users\omx\NES\\bot\img\\438.bmp',    'pixels':0}
#NesImageLibrary[438] = {'name':'Operation Wolf',                                              'file':'C:\Users\omx\NES\\bot\img\\439.bmp',    'pixels':0}
#NesImageLibrary[439] = {'name':'Orb-3D',                                                      'file':'C:\Users\omx\NES\\bot\img\\440.bmp',    'pixels':0}
#NesImageLibrary[440] = {'name':'Othello',                                                     'file':'C:\Users\omx\NES\\bot\img\\441.bmp',    'pixels':0}
#NesImageLibrary[441] = {'name':'Over Horizon (PAL)',                                          'file':'C:\Users\omx\NES\\bot\img\\442.bmp',    'pixels':0}
#NesImageLibrary[442] = {'name':'Overlord',                                                    'file':'C:\Users\omx\NES\\bot\img\\443.bmp',    'pixels':0}
#NesImageLibrary[443] = {'name':'P.O.W.: Prisoners of War',                                    'file':'C:\Users\omx\NES\\bot\img\\444.bmp',    'pixels':0}
#NesImageLibrary[444] = {'name':'Pac-Man (Namco)',                                             'file':'C:\Users\omx\NES\\bot\img\\445.bmp',    'pixels':0}
#NesImageLibrary[445] = {'name':'Pac-Man (Tengen)',                                            'file':'C:\Users\omx\NES\\bot\img\\446.bmp',    'pixels':0}
#NesImageLibrary[446] = {'name':'Palamedes',                                                   'file':'C:\Users\omx\NES\\bot\img\\447.bmp',    'pixels':0}
#NesImageLibrary[447] = {'name':'Panic Restaurant',                                            'file':'C:\Users\omx\NES\\bot\img\\448.bmp',    'pixels':0}
#NesImageLibrary[448] = {'name':'Paperboy',                                                    'file':'C:\Users\omx\NES\\bot\img\\449.bmp',    'pixels':0}
#NesImageLibrary[449] = {'name':'Paperboy 2',                                                  'file':'C:\Users\omx\NES\\bot\img\\450.bmp',    'pixels':0}
#NesImageLibrary[450] = {'name':'Parasol Stars: The Story of Bubble Bobble 3 (PAL)',           'file':'C:\Users\omx\NES\\bot\img\\451.bmp',    'pixels':0}
#NesImageLibrary[451] = {'name':'Parodius Da! (PAL)',                                          'file':'C:\Users\omx\NES\\bot\img\\452.bmp',    'pixels':0}
#NesImageLibrary[452] = {'name':'Peter Pan and the Pirates',                                   'file':'C:\Users\omx\NES\\bot\img\\453.bmp',    'pixels':0}
#NesImageLibrary[453] = {'name':'Phantom Fighter',                                             'file':'C:\Users\omx\NES\\bot\img\\454.bmp',    'pixels':0}
#NesImageLibrary[454] = {'name':'Pictionary',                                                  'file':'C:\Users\omx\NES\\bot\img\\455.bmp',    'pixels':0}
#NesImageLibrary[455] = {'name':'Pinball',                                                     'file':'C:\Users\omx\NES\\bot\img\\456.bmp',    'pixels':0}
#NesImageLibrary[456] = {'name':'Pinball Quest',                                               'file':'C:\Users\omx\NES\\bot\img\\457.bmp',    'pixels':0}
#NesImageLibrary[457] = {'name':'Pin*Bot',                                                     'file':'C:\Users\omx\NES\\bot\img\\458.bmp',    'pixels':0}
#NesImageLibrary[458] = {'name':'Pipe Dream',                                                  'file':'C:\Users\omx\NES\\bot\img\\459.bmp',    'pixels':0}
#NesImageLibrary[459] = {'name':'Pirates!',                                                    'file':'C:\Users\omx\NES\\bot\img\\460.bmp',    'pixels':0}
#NesImageLibrary[460] = {'name':'Platoon',                                                     'file':'C:\Users\omx\NES\\bot\img\\461.bmp',    'pixels':0}
#NesImageLibrary[461] = {'name':'Popeye',                                                      'file':'C:\Users\omx\NES\\bot\img\\462.bmp',    'pixels':0}
#NesImageLibrary[462] = {'name':'Power Blade',                                                 'file':'C:\Users\omx\NES\\bot\img\\463.bmp',    'pixels':0}
#NesImageLibrary[463] = {'name':'Power Blade 2',                                               'file':'C:\Users\omx\NES\\bot\img\\464.bmp',    'pixels':0}
#NesImageLibrary[464] = {'name':'Power Punch II',                                              'file':'C:\Users\omx\NES\\bot\img\\465.bmp',    'pixels':0}
#NesImageLibrary[465] = {'name':'Predator: Soon the Hunt Will Begin',                          'file':'C:\Users\omx\NES\\bot\img\\466.bmp',    'pixels':0}
#NesImageLibrary[466] = {'name':'Prince of Persia',                                            'file':'C:\Users\omx\NES\\bot\img\\467.bmp',    'pixels':0}
#NesImageLibrary[467] = {'name':'Princess Tomato in the Salad Kingdom',                        'file':'C:\Users\omx\NES\\bot\img\\468.bmp',    'pixels':0}
#NesImageLibrary[468] = {'name':'Pro Sport Hockey',                                            'file':'C:\Users\omx\NES\\bot\img\\469.bmp',    'pixels':0}
#NesImageLibrary[469] = {'name':'Pro Wrestling',                                               'file':'C:\Users\omx\NES\\bot\img\\470.bmp',    'pixels':0}
#NesImageLibrary[470] = {'name':'Punch-Out!!',                                                 'file':'C:\Users\omx\NES\\bot\img\\471.bmp',    'pixels':0}
#NesImageLibrary[471] = {'name':'The Punisher',                                                'file':'C:\Users\omx\NES\\bot\img\\472.bmp',    'pixels':0}
#NesImageLibrary[472] = {'name':'Puss 'n Boots: Pero's Great Adventure',                       'file':'C:\Users\omx\NES\\bot\img\\473.bmp',    'pixels':0}
#NesImageLibrary[473] = {'name':'Puzznic',                                                     'file':'C:\Users\omx\NES\\bot\img\\474.bmp',    'pixels':0}
#NesImageLibrary[474] = {'name':'Q*bert',                                                      'file':'C:\Users\omx\NES\\bot\img\\475.bmp',    'pixels':0}
#NesImageLibrary[475] = {'name':'Qix',                                                         'file':'C:\Users\omx\NES\\bot\img\\476.bmp',    'pixels':0}
#NesImageLibrary[476] = {'name':'R.B.I. Baseball',                                             'file':'C:\Users\omx\NES\\bot\img\\477.bmp',    'pixels':0}
#NesImageLibrary[477] = {'name':'R.C. Pro-Am',                                                 'file':'C:\Users\omx\NES\\bot\img\\478.bmp',    'pixels':0}
#NesImageLibrary[478] = {'name':'R.C. Pro-Am II',                                              'file':'C:\Users\omx\NES\\bot\img\\479.bmp',    'pixels':0}
#NesImageLibrary[479] = {'name':'Race America',                                                'file':'C:\Users\omx\NES\\bot\img\\480.bmp',    'pixels':0}
#NesImageLibrary[480] = {'name':'Racket Attack',                                               'file':'C:\Users\omx\NES\\bot\img\\481.bmp',    'pixels':0}
#NesImageLibrary[481] = {'name':'Rackets & Rivals (PAL)',                                      'file':'C:\Users\omx\NES\\bot\img\\482.bmp',    'pixels':0}
#NesImageLibrary[482] = {'name':'Rad Racer',                                                   'file':'C:\Users\omx\NES\\bot\img\\483.bmp',    'pixels':0}
#NesImageLibrary[483] = {'name':'Rad Racer II',                                                'file':'C:\Users\omx\NES\\bot\img\\484.bmp',    'pixels':0}
#NesImageLibrary[484] = {'name':'Raid on Bungeling Bay',                                       'file':'C:\Users\omx\NES\\bot\img\\485.bmp',    'pixels':0}
#NesImageLibrary[485] = {'name':'Rainbow Islands: The Story of Bubble Bobble 2',               'file':'C:\Users\omx\NES\\bot\img\\486.bmp',    'pixels':0}
#NesImageLibrary[486] = {'name':'Rainbow Islands: The Story of Bubble Bobble 2 (PAL)',         'file':'C:\Users\omx\NES\\bot\img\\487.bmp',    'pixels':0}
#NesImageLibrary[487] = {'name':'Rally Bike',                                                  'file':'C:\Users\omx\NES\\bot\img\\488.bmp',    'pixels':0}
#NesImageLibrary[488] = {'name':'Rambo',                                                       'file':'C:\Users\omx\NES\\bot\img\\489.bmp',    'pixels':0}
#NesImageLibrary[489] = {'name':'Rampage',                                                     'file':'C:\Users\omx\NES\\bot\img\\490.bmp',    'pixels':0}
#NesImageLibrary[490] = {'name':'Rampart',                                                     'file':'C:\Users\omx\NES\\bot\img\\491.bmp',    'pixels':0}
#NesImageLibrary[491] = {'name':'Remote Control',                                              'file':'C:\Users\omx\NES\\bot\img\\492.bmp',    'pixels':0}
#NesImageLibrary[492] = {'name':'The Ren & Stimpy Show: Buckaroo$!',                           'file':'C:\Users\omx\NES\\bot\img\\493.bmp',    'pixels':0}
#NesImageLibrary[493] = {'name':'Renegade',                                                    'file':'C:\Users\omx\NES\\bot\img\\494.bmp',    'pixels':0}
#NesImageLibrary[494] = {'name':'Rescue: The Embassy Mission',                                 'file':'C:\Users\omx\NES\\bot\img\\495.bmp',    'pixels':0}
#NesImageLibrary[495] = {'name':'Ring King',                                                   'file':'C:\Users\omx\NES\\bot\img\\496.bmp',    'pixels':0}
#NesImageLibrary[496] = {'name':'River City Ransom',                                           'file':'C:\Users\omx\NES\\bot\img\\497.bmp',    'pixels':0}
#NesImageLibrary[497] = {'name':'Road Fighter (PAL)',                                          'file':'C:\Users\omx\NES\\bot\img\\498.bmp',    'pixels':0}
#NesImageLibrary[498] = {'name':'RoadBlasters',                                                'file':'C:\Users\omx\NES\\bot\img\\499.bmp',    'pixels':0}
#NesImageLibrary[499] = {'name':'Robin Hood: Prince of Thieves',                               'file':'C:\Users\omx\NES\\bot\img\\500.bmp',    'pixels':0}
#NesImageLibrary[500] = {'name':'RoboCop',                                                     'file':'C:\Users\omx\NES\\bot\img\\501.bmp',    'pixels':0}
#NesImageLibrary[501] = {'name':'RoboCop 2',                                                   'file':'C:\Users\omx\NES\\bot\img\\502.bmp',    'pixels':0}
#NesImageLibrary[502] = {'name':'RoboCop 3',                                                   'file':'C:\Users\omx\NES\\bot\img\\503.bmp',    'pixels':0}
#NesImageLibrary[503] = {'name':'Robowarrior',                                                 'file':'C:\Users\omx\NES\\bot\img\\504.bmp',    'pixels':0}
#NesImageLibrary[504] = {'name':'Rock 'n Ball',                                                'file':'C:\Users\omx\NES\\bot\img\\505.bmp',    'pixels':0}
#NesImageLibrary[505] = {'name':'Rocket Ranger',                                               'file':'C:\Users\omx\NES\\bot\img\\506.bmp',    'pixels':0}
#NesImageLibrary[506] = {'name':'The Rocketeer',                                               'file':'C:\Users\omx\NES\\bot\img\\507.bmp',    'pixels':0}
#NesImageLibrary[507] = {'name':'Rockin' Kats',                                                'file':'C:\Users\omx\NES\\bot\img\\508.bmp',    'pixels':0}
#NesImageLibrary[508] = {'name':'Rod Land (PAL)',                                              'file':'C:\Users\omx\NES\\bot\img\\509.bmp',    'pixels':0}
#NesImageLibrary[509] = {'name':'Roger Clemens' MVP Baseball',                                 'file':'C:\Users\omx\NES\\bot\img\\510.bmp',    'pixels':0}
#NesImageLibrary[510] = {'name':'Rollerball',                                                  'file':'C:\Users\omx\NES\\bot\img\\511.bmp',    'pixels':0}
#NesImageLibrary[511] = {'name':'Rollerblade Racer',                                           'file':'C:\Users\omx\NES\\bot\img\\512.bmp',    'pixels':0}
#NesImageLibrary[512] = {'name':'RollerGames',                                                 'file':'C:\Users\omx\NES\\bot\img\\513.bmp',    'pixels':0}
#NesImageLibrary[513] = {'name':'Romance of the Three Kingdoms',                               'file':'C:\Users\omx\NES\\bot\img\\514.bmp',    'pixels':0}
#NesImageLibrary[514] = {'name':'Romance of the Three Kingdoms II',                            'file':'C:\Users\omx\NES\\bot\img\\515.bmp',    'pixels':0}
#NesImageLibrary[515] = {'name':'Roundball: 2 on 2 Challenge',                                 'file':'C:\Users\omx\NES\\bot\img\\516.bmp',    'pixels':0}
#NesImageLibrary[516] = {'name':'Rush'n Attack',                                               'file':'C:\Users\omx\NES\\bot\img\\517.bmp',    'pixels':0}
#NesImageLibrary[517] = {'name':'Rygar',                                                       'file':'C:\Users\omx\NES\\bot\img\\518.bmp',    'pixels':0}
#NesImageLibrary[518] = {'name':'S.C.A.T.: Special Cybernetic Attack Team',                    'file':'C:\Users\omx\NES\\bot\img\\519.bmp',    'pixels':0}
#NesImageLibrary[519] = {'name':'Section Z',                                                   'file':'C:\Users\omx\NES\\bot\img\\520.bmp',    'pixels':0}
#NesImageLibrary[520] = {'name':'Seicross',                                                    'file':'C:\Users\omx\NES\\bot\img\\521.bmp',    'pixels':0}
#NesImageLibrary[521] = {'name':'Sesame Street: 1-2-3',                                        'file':'C:\Users\omx\NES\\bot\img\\522.bmp',    'pixels':0}
#NesImageLibrary[522] = {'name':'Sesame Street: A-B-C',                                        'file':'C:\Users\omx\NES\\bot\img\\523.bmp',    'pixels':0}
#NesImageLibrary[523] = {'name':'Sesame Street: 1-2-3/A-B-C',                                  'file':'C:\Users\omx\NES\\bot\img\\524.bmp',    'pixels':0}
#NesImageLibrary[524] = {'name':'Sesame Street: Big Bird's Hide & Speak',                      'file':'C:\Users\omx\NES\\bot\img\\525.bmp',    'pixels':0}
#NesImageLibrary[525] = {'name':'Sesame Street: Countdown',                                    'file':'C:\Users\omx\NES\\bot\img\\526.bmp',    'pixels':0}
#NesImageLibrary[526] = {'name':'Shadow of the Ninja',                                         'file':'C:\Users\omx\NES\\bot\img\\527.bmp',    'pixels':0}
#NesImageLibrary[527] = {'name':'Shadowgate',                                                  'file':'C:\Users\omx\NES\\bot\img\\528.bmp',    'pixels':0}
#NesImageLibrary[528] = {'name':'Shatterhand',                                                 'file':'C:\Users\omx\NES\\bot\img\\529.bmp',    'pixels':0}
#NesImageLibrary[529] = {'name':'Shingen the Ruler',                                           'file':'C:\Users\omx\NES\\bot\img\\530.bmp',    'pixels':0}
#NesImageLibrary[530] = {'name':'Shooting Range',                                              'file':'C:\Users\omx\NES\\bot\img\\531.bmp',    'pixels':0}
#NesImageLibrary[531] = {'name':'Short Order / Eggsplode!',                                    'file':'C:\Users\omx\NES\\bot\img\\532.bmp',    'pixels':0}
#NesImageLibrary[532] = {'name':'Side Pocket',                                                 'file':'C:\Users\omx\NES\\bot\img\\533.bmp',    'pixels':0}
#NesImageLibrary[533] = {'name':'Silent Service',                                              'file':'C:\Users\omx\NES\\bot\img\\534.bmp',    'pixels':0}
#NesImageLibrary[534] = {'name':'Silkworm',                                                    'file':'C:\Users\omx\NES\\bot\img\\535.bmp',    'pixels':0}
#NesImageLibrary[535] = {'name':'Silver Surfer',                                               'file':'C:\Users\omx\NES\\bot\img\\536.bmp',    'pixels':0}
#NesImageLibrary[536] = {'name':'The Simpsons: Bart vs. the Space Mutants',                    'file':'C:\Users\omx\NES\\bot\img\\537.bmp',    'pixels':0}
#NesImageLibrary[537] = {'name':'The Simpsons: Bart vs. the World',                            'file':'C:\Users\omx\NES\\bot\img\\538.bmp',    'pixels':0}
#NesImageLibrary[538] = {'name':'The Simpsons: Bartman Meets Radioactive Man',                 'file':'C:\Users\omx\NES\\bot\img\\539.bmp',    'pixels':0}
#NesImageLibrary[539] = {'name':'Skate or Die!',                                               'file':'C:\Users\omx\NES\\bot\img\\540.bmp',    'pixels':0}
#NesImageLibrary[540] = {'name':'Skate or Die 2: The Search for Double Trouble',               'file':'C:\Users\omx\NES\\bot\img\\541.bmp',    'pixels':0}
#NesImageLibrary[541] = {'name':'Ski or Die',                                                  'file':'C:\Users\omx\NES\\bot\img\\542.bmp',    'pixels':0}
#NesImageLibrary[542] = {'name':'Sky Kid',                                                     'file':'C:\Users\omx\NES\\bot\img\\543.bmp',    'pixels':0}
#NesImageLibrary[543] = {'name':'Sky Shark',                                                   'file':'C:\Users\omx\NES\\bot\img\\544.bmp',    'pixels':0}
#NesImageLibrary[544] = {'name':'Slalom',                                                      'file':'C:\Users\omx\NES\\bot\img\\545.bmp',    'pixels':0}
#NesImageLibrary[545] = {'name':'Smash TV',                                                    'file':'C:\Users\omx\NES\\bot\img\\546.bmp',    'pixels':0}
#NesImageLibrary[546] = {'name':'The Smurfs (PAL)',                                            'file':'C:\Users\omx\NES\\bot\img\\547.bmp',    'pixels':0}
#NesImageLibrary[547] = {'name':'Snake Rattle 'n' Roll',                                       'file':'C:\Users\omx\NES\\bot\img\\548.bmp',    'pixels':0}
#NesImageLibrary[548] = {'name':'Snake's Revenge',                                             'file':'C:\Users\omx\NES\\bot\img\\549.bmp',    'pixels':0}
#NesImageLibrary[549] = {'name':'Snoopy's Silly Sports Spectacular',                           'file':'C:\Users\omx\NES\\bot\img\\550.bmp',    'pixels':0}
#NesImageLibrary[550] = {'name':'Snow Brothers',                                               'file':'C:\Users\omx\NES\\bot\img\\551.bmp',    'pixels':0}
#NesImageLibrary[551] = {'name':'Soccer',                                                      'file':'C:\Users\omx\NES\\bot\img\\552.bmp',    'pixels':0}
#NesImageLibrary[552] = {'name':'Solar Jetman: Hunt for the Golden Warpship',                  'file':'C:\Users\omx\NES\\bot\img\\553.bmp',    'pixels':0}
#NesImageLibrary[553] = {'name':'Solomon's Key',                                               'file':'C:\Users\omx\NES\\bot\img\\554.bmp',    'pixels':0}
#NesImageLibrary[554] = {'name':'Solstice: The Quest for the Staff of Demnos',                 'file':'C:\Users\omx\NES\\bot\img\\555.bmp',    'pixels':0}
#NesImageLibrary[555] = {'name':'Space Shuttle Project',                                       'file':'C:\Users\omx\NES\\bot\img\\556.bmp',    'pixels':0}
#NesImageLibrary[556] = {'name':'Spelunker',                                                   'file':'C:\Users\omx\NES\\bot\img\\557.bmp',    'pixels':0}
#NesImageLibrary[557] = {'name':'Spider-Man: Return of the Sinister Six',                      'file':'C:\Users\omx\NES\\bot\img\\558.bmp',    'pixels':0}
#NesImageLibrary[558] = {'name':'Spot: The Video Game',                                        'file':'C:\Users\omx\NES\\bot\img\\559.bmp',    'pixels':0}
#NesImageLibrary[559] = {'name':'Spy Hunter',                                                  'file':'C:\Users\omx\NES\\bot\img\\560.bmp',    'pixels':0}
#NesImageLibrary[560] = {'name':'Spy vs. Spy',                                                 'file':'C:\Users\omx\NES\\bot\img\\561.bmp',    'pixels':0}
#NesImageLibrary[561] = {'name':'Sqoon',                                                       'file':'C:\Users\omx\NES\\bot\img\\562.bmp',    'pixels':0}
#NesImageLibrary[562] = {'name':'Stack-Up',                                                    'file':'C:\Users\omx\NES\\bot\img\\563.bmp',    'pixels':0}
#NesImageLibrary[563] = {'name':'Stadium Events',                                              'file':'C:\Users\omx\NES\\bot\img\\564.bmp',    'pixels':0}
#NesImageLibrary[564] = {'name':'Stanley: The Search for Dr. Livingston',                      'file':'C:\Users\omx\NES\\bot\img\\565.bmp',    'pixels':0}
#NesImageLibrary[565] = {'name':'Star Force',                                                  'file':'C:\Users\omx\NES\\bot\img\\566.bmp',    'pixels':0}
#NesImageLibrary[566] = {'name':'Star Soldier',                                                'file':'C:\Users\omx\NES\\bot\img\\567.bmp',    'pixels':0}
#NesImageLibrary[567] = {'name':'Star Trek: 25th Anniversary',                                 'file':'C:\Users\omx\NES\\bot\img\\568.bmp',    'pixels':0}
#NesImageLibrary[568] = {'name':'Star Trek: The Next Generation',                              'file':'C:\Users\omx\NES\\bot\img\\569.bmp',    'pixels':0}
#NesImageLibrary[569] = {'name':'Star Voyager',                                                'file':'C:\Users\omx\NES\\bot\img\\570.bmp',    'pixels':0}
#NesImageLibrary[570] = {'name':'Star Wars',                                                   'file':'C:\Users\omx\NES\\bot\img\\571.bmp',    'pixels':0}
#NesImageLibrary[571] = {'name':'Star Wars: The Empire Strikes Back',                          'file':'C:\Users\omx\NES\\bot\img\\572.bmp',    'pixels':0}
#NesImageLibrary[572] = {'name':'Starship Hector',                                             'file':'C:\Users\omx\NES\\bot\img\\573.bmp',    'pixels':0}
#NesImageLibrary[573] = {'name':'StarTropics',                                                 'file':'C:\Users\omx\NES\\bot\img\\574.bmp',    'pixels':0}
#NesImageLibrary[574] = {'name':'Stealth ATF',                                                 'file':'C:\Users\omx\NES\\bot\img\\575.bmp',    'pixels':0}
#NesImageLibrary[575] = {'name':'Stinger',                                                     'file':'C:\Users\omx\NES\\bot\img\\576.bmp',    'pixels':0}
#NesImageLibrary[576] = {'name':'Street Cop',                                                  'file':'C:\Users\omx\NES\\bot\img\\577.bmp',    'pixels':0}
#NesImageLibrary[577] = {'name':'Street Fighter 2010: The Final Fight',                        'file':'C:\Users\omx\NES\\bot\img\\578.bmp',    'pixels':0}
#NesImageLibrary[578] = {'name':'Strider',                                                     'file':'C:\Users\omx\NES\\bot\img\\579.bmp',    'pixels':0}
#NesImageLibrary[579] = {'name':'Super C',                                                     'file':'C:\Users\omx\NES\\bot\img\\580.bmp',    'pixels':0}
#NesImageLibrary[580] = {'name':'Super Cars',                                                  'file':'C:\Users\omx\NES\\bot\img\\581.bmp',    'pixels':0}
#NesImageLibrary[581] = {'name':'Super Dodge Ball',                                            'file':'C:\Users\omx\NES\\bot\img\\582.bmp',    'pixels':0}
#NesImageLibrary[582] = {'name':'Super Glove Ball',                                            'file':'C:\Users\omx\NES\\bot\img\\583.bmp',    'pixels':0}
#NesImageLibrary[583] = {'name':'Super Jeopardy!',                                             'file':'C:\Users\omx\NES\\bot\img\\584.bmp',    'pixels':0}
#NesImageLibrary[584] = {'name':'Super Mario Bros.',                                           'file':'C:\Users\omx\NES\\bot\img\\585.bmp',    'pixels':0}
#NesImageLibrary[585] = {'name':'Super Mario Bros./Duck Hunt',                                 'file':'C:\Users\omx\NES\\bot\img\\586.bmp',    'pixels':0}
#NesImageLibrary[586] = {'name':'Super Mario Bros./Duck Hunt/World Class Track Meet',          'file':'C:\Users\omx\NES\\bot\img\\587.bmp',    'pixels':0}
#NesImageLibrary[587] = {'name':'Super Mario Bros./Tetris/Nintendo World Cup (PAL)',           'file':'C:\Users\omx\NES\\bot\img\\588.bmp',    'pixels':0}
#NesImageLibrary[588] = {'name':'Super Mario Bros. 2',                                         'file':'C:\Users\omx\NES\\bot\img\\589.bmp',    'pixels':0}
#NesImageLibrary[589] = {'name':'Super Mario Bros. 3',                                         'file':'C:\Users\omx\NES\\bot\img\\590.bmp',    'pixels':0}
#NesImageLibrary[590] = {'name':'Super Pitfall',                                               'file':'C:\Users\omx\NES\\bot\img\\591.bmp',    'pixels':0}
#NesImageLibrary[591] = {'name':'Super Spike V'Ball',                                          'file':'C:\Users\omx\NES\\bot\img\\592.bmp',    'pixels':0}
#NesImageLibrary[592] = {'name':'Super Spike V'Ball/Nintendo World Cup',                       'file':'C:\Users\omx\NES\\bot\img\\593.bmp',    'pixels':0}
#NesImageLibrary[593] = {'name':'Super Spy Hunter',                                            'file':'C:\Users\omx\NES\\bot\img\\594.bmp',    'pixels':0}
#NesImageLibrary[594] = {'name':'Super Team Games',                                            'file':'C:\Users\omx\NES\\bot\img\\595.bmp',    'pixels':0}
#NesImageLibrary[595] = {'name':'Super Turrican (PAL)',                                        'file':'C:\Users\omx\NES\\bot\img\\596.bmp',    'pixels':0}
#NesImageLibrary[596] = {'name':'Superman',                                                    'file':'C:\Users\omx\NES\\bot\img\\597.bmp',    'pixels':0}
#NesImageLibrary[597] = {'name':'Swamp Thing',                                                 'file':'C:\Users\omx\NES\\bot\img\\598.bmp',    'pixels':0}
#NesImageLibrary[598] = {'name':'Sword Master',                                                'file':'C:\Users\omx\NES\\bot\img\\599.bmp',    'pixels':0}
#NesImageLibrary[599] = {'name':'Swords and Serpents',                                         'file':'C:\Users\omx\NES\\bot\img\\600.bmp',    'pixels':0}
#NesImageLibrary[600] = {'name':'Taboo: The Sixth Sense',                                      'file':'C:\Users\omx\NES\\bot\img\\601.bmp',    'pixels':0}
#NesImageLibrary[601] = {'name':'Tag Team Wrestling',                                          'file':'C:\Users\omx\NES\\bot\img\\602.bmp',    'pixels':0}
#NesImageLibrary[602] = {'name':'TaleSpin',                                                    'file':'C:\Users\omx\NES\\bot\img\\603.bmp',    'pixels':0}
#NesImageLibrary[603] = {'name':'Target: Renegade',                                            'file':'C:\Users\omx\NES\\bot\img\\604.bmp',    'pixels':0}
#NesImageLibrary[604] = {'name':'Tecmo Baseball',                                              'file':'C:\Users\omx\NES\\bot\img\\605.bmp',    'pixels':0}
#NesImageLibrary[605] = {'name':'Tecmo Bowl',                                                  'file':'C:\Users\omx\NES\\bot\img\\606.bmp',    'pixels':0}
#NesImageLibrary[606] = {'name':'Tecmo Cup Soccer Game',                                       'file':'C:\Users\omx\NES\\bot\img\\607.bmp',    'pixels':0}
#NesImageLibrary[607] = {'name':'Tecmo NBA Basketball',                                        'file':'C:\Users\omx\NES\\bot\img\\608.bmp',    'pixels':0}
#NesImageLibrary[608] = {'name':'Tecmo Super Bowl',                                            'file':'C:\Users\omx\NES\\bot\img\\609.bmp',    'pixels':0}
#NesImageLibrary[609] = {'name':'Tecmo World Cup Soccer (PAL)',                                'file':'C:\Users\omx\NES\\bot\img\\610.bmp',    'pixels':0}
#NesImageLibrary[610] = {'name':'Tecmo World Wrestling',                                       'file':'C:\Users\omx\NES\\bot\img\\611.bmp',    'pixels':0}
#NesImageLibrary[611] = {'name':'Teenage Mutant Ninja Turtles',                                'file':'C:\Users\omx\NES\\bot\img\\612.bmp',    'pixels':0}
#NesImageLibrary[612] = {'name':'Teenage Mutant Ninja Turtles II: The Arcade Game',            'file':'C:\Users\omx\NES\\bot\img\\613.bmp',    'pixels':0}
#NesImageLibrary[613] = {'name':'Teenage Mutant Ninja Turtles III: The Manhattan Project',     'file':'C:\Users\omx\NES\\bot\img\\614.bmp',    'pixels':0}
#NesImageLibrary[614] = {'name':'Teenage Mutant Ninja Turtles: Tournament Fighters',           'file':'C:\Users\omx\NES\\bot\img\\615.bmp',    'pixels':0}
#NesImageLibrary[615] = {'name':'Tennis',                                                      'file':'C:\Users\omx\NES\\bot\img\\616.bmp',    'pixels':0}
#NesImageLibrary[616] = {'name':'The Terminator',                                              'file':'C:\Users\omx\NES\\bot\img\\617.bmp',    'pixels':0}
#NesImageLibrary[617] = {'name':'Terminator 2: Judgment Day',                                  'file':'C:\Users\omx\NES\\bot\img\\618.bmp',    'pixels':0}
#NesImageLibrary[618] = {'name':'Terra Cresta',                                                'file':'C:\Users\omx\NES\\bot\img\\619.bmp',    'pixels':0}
#NesImageLibrary[619] = {'name':'Tetris',                                                      'file':'C:\Users\omx\NES\\bot\img\\620.bmp',    'pixels':0}
#NesImageLibrary[620] = {'name':'Tetris 2',                                                    'file':'C:\Users\omx\NES\\bot\img\\621.bmp',    'pixels':0}
#NesImageLibrary[621] = {'name':'The Three Stooges',                                           'file':'C:\Users\omx\NES\\bot\img\\622.bmp',    'pixels':0}
#NesImageLibrary[622] = {'name':'Thunder & Lightning',                                         'file':'C:\Users\omx\NES\\bot\img\\623.bmp',    'pixels':0}
#NesImageLibrary[623] = {'name':'Thunderbirds',                                                'file':'C:\Users\omx\NES\\bot\img\\624.bmp',    'pixels':0}
#NesImageLibrary[624] = {'name':'Thundercade',                                                 'file':'C:\Users\omx\NES\\bot\img\\625.bmp',    'pixels':0}
#NesImageLibrary[625] = {'name':'Tiger Heli',                                                  'file':'C:\Users\omx\NES\\bot\img\\626.bmp',    'pixels':0}
#NesImageLibrary[626] = {'name':'Time Lord',                                                   'file':'C:\Users\omx\NES\\bot\img\\627.bmp',    'pixels':0}
#NesImageLibrary[627] = {'name':'Times of Lore',                                               'file':'C:\Users\omx\NES\\bot\img\\628.bmp',    'pixels':0}
#NesImageLibrary[628] = {'name':'Tiny Toon Adventures',                                        'file':'C:\Users\omx\NES\\bot\img\\629.bmp',    'pixels':0}
#NesImageLibrary[629] = {'name':'Tiny Toon Adventures 2: Trouble in Wackyland',                'file':'C:\Users\omx\NES\\bot\img\\630.bmp',    'pixels':0}
#NesImageLibrary[630] = {'name':'Tiny Toon Adventures Cartoon Workshop',                       'file':'C:\Users\omx\NES\\bot\img\\631.bmp',    'pixels':0}
#NesImageLibrary[631] = {'name':'To the Earth',                                                'file':'C:\Users\omx\NES\\bot\img\\632.bmp',    'pixels':0}
#NesImageLibrary[632] = {'name':'Toki',                                                        'file':'C:\Users\omx\NES\\bot\img\\633.bmp',    'pixels':0}
#NesImageLibrary[633] = {'name':'Tom and Jerry',                                               'file':'C:\Users\omx\NES\\bot\img\\634.bmp',    'pixels':0}
#NesImageLibrary[634] = {'name':'Tombs & Treasure',                                            'file':'C:\Users\omx\NES\\bot\img\\635.bmp',    'pixels':0}
#NesImageLibrary[635] = {'name':'Top Gun',                                                     'file':'C:\Users\omx\NES\\bot\img\\636.bmp',    'pixels':0}
#NesImageLibrary[636] = {'name':'Top Gun: The Second Mission',                                 'file':'C:\Users\omx\NES\\bot\img\\637.bmp',    'pixels':0}
#NesImageLibrary[637] = {'name':'Top Players' Tennis',                                         'file':'C:\Users\omx\NES\\bot\img\\638.bmp',    'pixels':0}
#NesImageLibrary[638] = {'name':'Total Recall',                                                'file':'C:\Users\omx\NES\\bot\img\\639.bmp',    'pixels':0}
#NesImageLibrary[639] = {'name':'Totally Rad',                                                 'file':'C:\Users\omx\NES\\bot\img\\640.bmp',    'pixels':0}
#NesImageLibrary[640] = {'name':'Touch Down Fever',                                            'file':'C:\Users\omx\NES\\bot\img\\641.bmp',    'pixels':0}
#NesImageLibrary[641] = {'name':'Town & Country Surf Designs: Wood & Water Rage',              'file':'C:\Users\omx\NES\\bot\img\\642.bmp',    'pixels':0}
#NesImageLibrary[642] = {'name':'Town & Country II: Thrilla's Surfari',                        'file':'C:\Users\omx\NES\\bot\img\\643.bmp',    'pixels':0}
#NesImageLibrary[643] = {'name':'Toxic Crusaders',                                             'file':'C:\Users\omx\NES\\bot\img\\644.bmp',    'pixels':0}
#NesImageLibrary[644] = {'name':'Track & Field',                                               'file':'C:\Users\omx\NES\\bot\img\\645.bmp',    'pixels':0}
#NesImageLibrary[645] = {'name':'Track & Field II',                                            'file':'C:\Users\omx\NES\\bot\img\\646.bmp',    'pixels':0}
#NesImageLibrary[646] = {'name':'Treasure Master',                                             'file':'C:\Users\omx\NES\\bot\img\\647.bmp',    'pixels':0}
#NesImageLibrary[647] = {'name':'Trog!',                                                       'file':'C:\Users\omx\NES\\bot\img\\648.bmp',    'pixels':0}
#NesImageLibrary[648] = {'name':'Trojan',                                                      'file':'C:\Users\omx\NES\\bot\img\\649.bmp',    'pixels':0}
#NesImageLibrary[649] = {'name':'The Trolls in Crazyland (PAL)',                               'file':'C:\Users\omx\NES\\bot\img\\650.bmp',    'pixels':0}
#NesImageLibrary[650] = {'name':'Twin Cobra',                                                  'file':'C:\Users\omx\NES\\bot\img\\651.bmp',    'pixels':0}
#NesImageLibrary[651] = {'name':'Twin Eagle',                                                  'file':'C:\Users\omx\NES\\bot\img\\652.bmp',    'pixels':0}
#NesImageLibrary[652] = {'name':'Ufouria: The Saga (PAL)',                                     'file':'C:\Users\omx\NES\\bot\img\\653.bmp',    'pixels':0}
#NesImageLibrary[653] = {'name':'Ultima III: Exodus',                                          'file':'C:\Users\omx\NES\\bot\img\\654.bmp',    'pixels':0}
#NesImageLibrary[654] = {'name':'Ultima IV: Quest of the Avatar',                              'file':'C:\Users\omx\NES\\bot\img\\655.bmp',    'pixels':0}
#NesImageLibrary[655] = {'name':'Ultima V: Warriors of Destiny',                               'file':'C:\Users\omx\NES\\bot\img\\656.bmp',    'pixels':0}
#NesImageLibrary[656] = {'name':'Ultimate Air Combat',                                         'file':'C:\Users\omx\NES\\bot\img\\657.bmp',    'pixels':0}
#NesImageLibrary[657] = {'name':'Ultimate Basketball',                                         'file':'C:\Users\omx\NES\\bot\img\\658.bmp',    'pixels':0}
#NesImageLibrary[658] = {'name':'The Uncanny X-Men',                                           'file':'C:\Users\omx\NES\\bot\img\\659.bmp',    'pixels':0}
#NesImageLibrary[659] = {'name':'Uncharted Waters',                                            'file':'C:\Users\omx\NES\\bot\img\\660.bmp',    'pixels':0}
#NesImageLibrary[660] = {'name':'Uninvited',                                                   'file':'C:\Users\omx\NES\\bot\img\\661.bmp',    'pixels':0}
#NesImageLibrary[661] = {'name':'The Untouchables',                                            'file':'C:\Users\omx\NES\\bot\img\\662.bmp',    'pixels':0}
#NesImageLibrary[662] = {'name':'Urban Champion',                                              'file':'C:\Users\omx\NES\\bot\img\\663.bmp',    'pixels':0}
#NesImageLibrary[663] = {'name':'Vegas Dream',                                                 'file':'C:\Users\omx\NES\\bot\img\\664.bmp',    'pixels':0}
#NesImageLibrary[664] = {'name':'Vice: Project Doom',                                          'file':'C:\Users\omx\NES\\bot\img\\665.bmp',    'pixels':0}
#NesImageLibrary[665] = {'name':'Videomation',                                                 'file':'C:\Users\omx\NES\\bot\img\\666.bmp',    'pixels':0}
#NesImageLibrary[666] = {'name':'Volleyball',                                                  'file':'C:\Users\omx\NES\\bot\img\\667.bmp',    'pixels':0}
#NesImageLibrary[667] = {'name':'Wacky Races',                                                 'file':'C:\Users\omx\NES\\bot\img\\668.bmp',    'pixels':0}
#NesImageLibrary[668] = {'name':'Wall Street Kid',                                             'file':'C:\Users\omx\NES\\bot\img\\669.bmp',    'pixels':0}
#NesImageLibrary[669] = {'name':'Wario's Woods',                                               'file':'C:\Users\omx\NES\\bot\img\\670.bmp',    'pixels':0}
#NesImageLibrary[670] = {'name':'Wayne Gretzky Hockey',                                        'file':'C:\Users\omx\NES\\bot\img\\671.bmp',    'pixels':0}
#NesImageLibrary[671] = {'name':'Wayne's World',                                               'file':'C:\Users\omx\NES\\bot\img\\672.bmp',    'pixels':0}
#NesImageLibrary[672] = {'name':'WCW Wrestling',                                               'file':'C:\Users\omx\NES\\bot\img\\673.bmp',    'pixels':0}
#NesImageLibrary[673] = {'name':'Werewolf: The Last Warrior',                                  'file':'C:\Users\omx\NES\\bot\img\\674.bmp',    'pixels':0}
#NesImageLibrary[674] = {'name':'Wheel of Fortune',                                            'file':'C:\Users\omx\NES\\bot\img\\675.bmp',    'pixels':0}
#NesImageLibrary[675] = {'name':'Wheel of Fortune Family Edition',                             'file':'C:\Users\omx\NES\\bot\img\\676.bmp',    'pixels':0}
#NesImageLibrary[676] = {'name':'Wheel of Fortune: Featuring Vanna White',                     'file':'C:\Users\omx\NES\\bot\img\\677.bmp',    'pixels':0}
#NesImageLibrary[677] = {'name':'Wheel of Fortune Junior Edition',                             'file':'C:\Users\omx\NES\\bot\img\\678.bmp',    'pixels':0}
#NesImageLibrary[678] = {'name':'Where in Time Is Carmen Sandiego?',                           'file':'C:\Users\omx\NES\\bot\img\\679.bmp',    'pixels':0}
#NesImageLibrary[679] = {'name':'Where's Waldo?',                                              'file':'C:\Users\omx\NES\\bot\img\\680.bmp',    'pixels':0}
#NesImageLibrary[680] = {'name':'Who Framed Roger Rabbit?',                                    'file':'C:\Users\omx\NES\\bot\img\\681.bmp',    'pixels':0}
#NesImageLibrary[681] = {'name':'Whomp 'Em',                                                   'file':'C:\Users\omx\NES\\bot\img\\682.bmp',    'pixels':0}
#NesImageLibrary[682] = {'name':'Widget',                                                      'file':'C:\Users\omx\NES\\bot\img\\683.bmp',    'pixels':0}
#NesImageLibrary[683] = {'name':'Wild Gunman',                                                 'file':'C:\Users\omx\NES\\bot\img\\684.bmp',    'pixels':0}
#NesImageLibrary[684] = {'name':'Willow',                                                      'file':'C:\Users\omx\NES\\bot\img\\685.bmp',    'pixels':0}
#NesImageLibrary[685] = {'name':'Win, Lose, or Draw',                                          'file':'C:\Users\omx\NES\\bot\img\\686.bmp',    'pixels':0}
#NesImageLibrary[686] = {'name':'Winter Games',                                                'file':'C:\Users\omx\NES\\bot\img\\687.bmp',    'pixels':0}
#NesImageLibrary[687] = {'name':'Wizardry: Proving Grounds of the Mad Overlord',               'file':'C:\Users\omx\NES\\bot\img\\688.bmp',    'pixels':0}
#NesImageLibrary[688] = {'name':'Wizardry II: The Knight of Diamonds',                         'file':'C:\Users\omx\NES\\bot\img\\689.bmp',    'pixels':0}
#NesImageLibrary[689] = {'name':'Wizards & Warriors',                                          'file':'C:\Users\omx\NES\\bot\img\\690.bmp',    'pixels':0}
#NesImageLibrary[690] = {'name':'Wizards & Warriors III: Kuros: Visions of Power',             'file':'C:\Users\omx\NES\\bot\img\\691.bmp',    'pixels':0}
#NesImageLibrary[691] = {'name':'Wolverine',                                                   'file':'C:\Users\omx\NES\\bot\img\\692.bmp',    'pixels':0}
#NesImageLibrary[692] = {'name':'World Champ',                                                 'file':'C:\Users\omx\NES\\bot\img\\693.bmp',    'pixels':0}
#NesImageLibrary[693] = {'name':'World Class Track Meet',                                      'file':'C:\Users\omx\NES\\bot\img\\694.bmp',    'pixels':0}
#NesImageLibrary[694] = {'name':'World Games',                                                 'file':'C:\Users\omx\NES\\bot\img\\695.bmp',    'pixels':0}
#NesImageLibrary[695] = {'name':'Wrath of the Black Manta',                                    'file':'C:\Users\omx\NES\\bot\img\\696.bmp',    'pixels':0}
#NesImageLibrary[696] = {'name':'Wrecking Crew',                                               'file':'C:\Users\omx\NES\\bot\img\\697.bmp',    'pixels':0}
#NesImageLibrary[697] = {'name':'Wurm: Journey to the Center of the Earth',                    'file':'C:\Users\omx\NES\\bot\img\\698.bmp',    'pixels':0}
#NesImageLibrary[698] = {'name':'WWF King of the Ring',                                        'file':'C:\Users\omx\NES\\bot\img\\699.bmp',    'pixels':0}
#NesImageLibrary[699] = {'name':'WWF WrestleMania',                                            'file':'C:\Users\omx\NES\\bot\img\\700.bmp',    'pixels':0}
#NesImageLibrary[700] = {'name':'WWF WrestleMania Challenge',                                  'file':'C:\Users\omx\NES\\bot\img\\701.bmp',    'pixels':0}
#NesImageLibrary[701] = {'name':'WWF WrestleMania: Steel Cage Challenge',                      'file':'C:\Users\omx\NES\\bot\img\\702.bmp',    'pixels':0}
#NesImageLibrary[702] = {'name':'Xenophobe',                                                   'file':'C:\Users\omx\NES\\bot\img\\703.bmp',    'pixels':0}
#NesImageLibrary[703] = {'name':'Xevious',                                                     'file':'C:\Users\omx\NES\\bot\img\\704.bmp',    'pixels':0}
#NesImageLibrary[704] = {'name':'Xexyz',                                                       'file':'C:\Users\omx\NES\\bot\img\\705.bmp',    'pixels':0}
#NesImageLibrary[705] = {'name':'Yo! Noid',                                                    'file':'C:\Users\omx\NES\\bot\img\\706.bmp',    'pixels':0}
#NesImageLibrary[706] = {'name':'Yoshi',                                                       'file':'C:\Users\omx\NES\\bot\img\\707.bmp',    'pixels':0}
#NesImageLibrary[707] = {'name':'Yoshi's Cookie',                                              'file':'C:\Users\omx\NES\\bot\img\\708.bmp',    'pixels':0}
#NesImageLibrary[708] = {'name':'Young Indiana Jones Chronicles',                              'file':'C:\Users\omx\NES\\bot\img\\709.bmp',    'pixels':0}
#NesImageLibrary[709] = {'name':'Zanac',                                                       'file':'C:\Users\omx\NES\\bot\img\\710.bmp',    'pixels':0}
#NesImageLibrary[710] = {'name':'Zelda II: The Adventure of Link',                             'file':'C:\Users\omx\NES\\bot\img\\711.bmp',    'pixels':0}
#NesImageLibrary[711] = {'name':'Zen the Intergalactic Ninja',                                 'file':'C:\Users\omx\NES\\bot\img\\712.bmp',    'pixels':0}
#NesImageLibrary[712] = {'name':'Zoda's Revenge: StarTropics II',                              'file':'C:\Users\omx\NES\\bot\img\\713.bmp',    'pixels':0}
#NesImageLibrary[713] = {'name':'Zombie Nation',                                               'file':'C:\Users\omx\NES\\bot\img\\714.bmp',    'pixels':0}

class IrcThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        global buff
        global bitnes

        while 1:
            time.sleep(1)
            dataReady = select.select([s], [], [], 0)
            if dataReady[0]:
                try:
                    buff = buff + dataReady[0][0].recv(4096).decode('utf-8', "ignore")
                    print(buff).encode(sys.stdout.encoding, errors='replace')
                    lines = buff.split("\n")
                    buff = lines.pop()
                except socket.error:
                    print(socket.error)
            else:
               lines = []
               next

            #print(lines)

            for line in lines:
                line = line.rstrip()

                command_list = open("irc_commands.txt")
                for cmd in command_list.readlines():
                    tmp = cmd.split("|")
                    match = re.search("\:\!" + tmp[0] + "$",line)
                    if match:
                        s.send("PRIVMSG #link_7777 :" + tmp[1] + "\r\n".encode())
                command_list.close()

                match = re.search('^PING', line)
                if match:
                    s.send("PONG :tmi.twitch.tv\r\n".encode())

                match = re.search('^@badges.*;bits=(.+?);.*display-name=(.+?);.*sent-ts=(.+?);.*PRIVMSG #link_7777\s+?:(.*)', line)
                #match = re.search('^@badges.*;.*display-name=(.*);emotes.*PRIVMSG #link_7777 :bits=(.*);(.*)', line)
                if match:
                    message = "PRIVMSG #link_7777:" + match.group(2) + " thank you for the " + match.group(1) + " bits!\r\n"
                    s.send(message.encode())
                    UpdateBits(match.group(3), match.group(2), int(match.group(1)))

                match = re.search('\:\!commands', line)
                if match:
                    message = "PRIVMSG #link_7777 :Commands: !new !title !time !left !remaining !mute !unmute"

                    command_list = open("irc_commands.txt")
                    for cmd in command_list.readlines():
                        tmp = cmd.split("|")
                        message = message + " !" + tmp[0]
                    command_list.close()
                    message = message + "\r\n"

                    s.send(message.encode())

                match = re.search('\:\!time', line)
                if match:
                    start_time = GetTime()
                    if start_time == None:
                        s.send("PRIVMSG #link_7777 :This stream is not live\r\n".encode())
                    else:
                        s.send("PRIVMSG #link_7777 :This stream has been live since " + start_time + "\r\n".encode())

                match = re.search('\!link_7777\@.*\:\!title\s(.*)', line)
                if match:
                    UpdateTitle(match.group(1))
                else:
                    match = re.search('\:\!title', line)
                    if match:
                        GetTitle()

                match = re.search('\!link_7777\@.*\:\!game\s(.*)', line)
                if match:
                    if match.group(1) == 'Z2':
                        UpdateGame('Zelda II: The Adventure of Link')
                    else:
                        UpdateGame(match.group(1))
                else:
                    match = re.search('\:\!game', line)
                    if match:
                        GetGame()

                match = re.search('\!link_7777\@.*\:\!bittest\s(.*)\s(.*)', line)
                if match:
                    bitnes.add_bits(match.group(1), int(match.group(2)), 1)

                match = re.search('\!link_7777\@.*\:\!mute', line)
                if match:
                    bitnes.mute()

                match = re.search('\!link_7777\@.*\:\!unmute', line)
                if match:
                    bitnes.unmute()

                match = re.search('\:\!left', line)
                if match:
                    tmp_line = "PRIVMSG #link_7777 :%d bits remaining (%d/%d)\r\n" % (bitnes.get_current_image_count() - bitnes.get_current_partial_count(),bitnes.get_current_partial_count(),bitnes.get_current_image_count())
                    s.send(tmp_line.encode())

                match = re.search('\:\!remaining', line)
                if match:
                    tmp_line = "PRIVMSG #link_7777 :%d bits remaining (%d/%d)\r\n" % (bitnes.get_current_image_count() - bitnes.get_current_partial_count(),bitnes.get_current_partial_count(),bitnes.get_current_image_count())
                    s.send(tmp_line.encode())

class BitNesCollection:
    global screen

    def __init__(self, initialCount):
        self.size = 0
        self.bgcolor = (0,0,0)
        self.font = pygame.font.SysFont("DejaVu Sans Monospace", 20)
        self.alertFont = pygame.font.SysFont("DejaVu Sans Monospace", 40)
        self.alertTimeout = 0
        self.alertText = ''
        self.alertBits = 0
        self.alertQueue = []
        self.notificationFont = pygame.font.SysFont("DejaVu Sans Monospace", 40)
        self.notificationTimeout = 0
        self.notificationText = ''
        self.notificationQueue = []
        self.notificationAnimationFlag = 0;
        self.notificationAnimationCurrentHeight = 0
        self.notificationAnimationCurrentWidth = 0
        self.notificationAnimationCurrentX = 0
        self.notificationAnimationCurrentY = 0
        pygame.mixer.music.load("C:\Users\omx\NES\\bot\img\Purple.mp3")
        self.moves = 0
        #self.pixelImage = pygame.image.load("C:\Users\omx\NES\Layouts\Battletoads.bmp")
        #self.pixelImage.set_colorkey((0,0,0,255))
        #self.pixelImageWidth = self.pixelImage.get_width()
        #self.pixelImageHeight = self.pixelImage.get_height()
        #self.pixelGhostImage = self.pixelImage.copy()
        self.currentBits = initialCount
        self.currentPartialBits = 0
        self.max_height = 0
        self.max_overall_height = 0
        #self.create_ghost(self.pixelGhostImage, self.currentBits)
        self.outstandingBits = 0
        self.previousBits = 0
        self.outstandingName = ''
        self.testMode = 0
        self.preTestBits = 0
        self.bitsQueue = []
        self.animationFlag = 0;
        self.animationCurrentHeight = 0
        self.animationCurrentWidth = 0
        self.animationCurrentX = 0
        self.animationCurrentY = 0
        self.dump_pixel_counts()
        self.currentImageIndex = self.find_current_position()
        #self.set_animation_image((0,0,0))
        self.bitImage = pygame.image.load("C:\Users\omx\NES\\bot\img\\bit.png")
        self.bitImageSmall = pygame.image.load("C:\Users\omx\NES\\bot\img\\bit_small.png")
        self.load_images()
        #self.background = ()
        self.notification_background = pygame.Surface((350,self.max_overall_height*2 + self.alertFont.size("A")[1]*2 + 4))
        self.notification_background.fill((25,25,0))
        self.notification_background = self.notification_background.convert() #makes blitting faster
        self.notificationAnimationImage = NesImageLibrary[self.currentImageIndex]['image'].copy()
        self.randomImageNum = 0
        self.muted = 0
        self.subscriptionTimeout = 604800*8

        #screen.blit(background, (0,0))
        self.draw()

    def subscriptionTick(self):
        self.subscriptionTimeout -= 1
        if self.subscriptionTimeout == 0:
            RequestFollowerNotifications()
            self.subscriptionTimeout = 604800*8

    def mute(self):
        self.muted = 1

    def unmute(self):
        self.muted = 0

    def add_bits(self, name, bits, test):
        self.bitsQueue.append((name, bits, test))
        self.alertQueue.append((name, bits))

    def add_notification(self, text):
        print("Append %s\n" % text)
        self.notificationQueue.append(text)
        
    def outstanding_bits_check(self):
        if self.alertTimeout == 0:
            if len(self.alertQueue) > 0:
                (self.alertText,self.alertBits) = self.alertQueue.pop(0)
                self.alertTimeout = 20*8
                if(self.muted == 0):
                    pygame.mixer.music.load("C:\Users\omx\NES\\bot\img\Purple.mp3")
                    pygame.mixer.music.play()
        #else:
        #    if self.animationFlag == 0:
        #        #still call do animation if in case the animation is done before the alert
        #        self.do_animation()
        #        self.draw()

        if self.animationFlag == 0:
            #print("current %d outstanding %d" % (self.currentBits, self.outstandingBits))
            if self.outstandingBits > 0:
                self.currentBits += 1
                self.outstandingBits -= 1
                self.animation_start()
                NesImageLibrary[self.currentImageIndex]['ghost'] = NesImageLibrary[self.currentImageIndex]['image'].copy()
                self.create_ghost(NesImageLibrary[self.currentImageIndex]['ghost'], self.currentPartialBits)
                #self.create_ghost(self.pixelGhostImage, self.currentBits)
            else:
                if (self.alertTimeout == 0 or self.alertTimeout == 20*8) and len(self.bitsQueue) > 0:
                    (self.outstandingName, self.outstandingBits,self.testMode) = self.bitsQueue.pop(0)
                    self.previousBits = self.outstandingBits
                    if self.testMode == 1:
                        self.preTestBits = self.currentBits

    def outstanding_notification_check(self):
        if self.notificationTimeout == 0:
            if len(self.notificationQueue) > 0:
                self.notificationText = self.notificationQueue.pop(0)
                self.notificationTimeout = 30*8
                print("Notification\n")
                if(self.muted == 0):
                    pygame.mixer.music.load("C:\Users\omx\NES\\bot\img\Purple.mp3")
                    pygame.mixer.music.play()
                self.notification_animation_start()

    def animation_start(self):
        self.load_images()
        self.animationImage = NesImageLibrary[self.currentImageIndex]['image'].copy()
        self.set_animation_image(self.get_current_bit_color())
        self.animationCurrentHeight = self.animationImage.get_height()
        self.animationCurrentWidth = self.animationImage.get_width()
        self.animationCurrentX = 0
        self.animationCurrentY = 0
        self.animationCurrentPosition = self.get_current_bit_position()
        self.animationFlag = 1
        self.draw()

    def notification_animation_start(self):
        self.load_images()
        self.randomImageNum = random.randrange(0,NesImageCount-1)
        NesImageLibrary[self.randomImageNum]['image'] = pygame.image.load(NesImageLibrary[self.randomImageNum]['file'])
        NesImageLibrary[self.randomImageNum]['image'].set_colorkey((0,0,0,255))
        self.notificationAnimationImage = pygame.transform.scale(NesImageLibrary[self.randomImageNum]['image'].copy(), (NesImageLibrary[self.randomImageNum]['image'].get_width()*2, NesImageLibrary[self.randomImageNum]['image'].get_height()*2))
        self.notificationAnimationCurrentHeight = self.notificationAnimationImage.get_height()
        self.notificationAnimationCurrentWidth = self.notificationAnimationImage.get_width()
        self.notificationAnimationCurrentX = (350-self.notificationAnimationCurrentWidth)/2
        self.notificationAnimationCurrentY = (self.max_overall_height*2 - self.notificationAnimationCurrentHeight)/2+self.max_height+50
        self.notificationAnimationFlag = 1
        self.draw()

    def do_animation(self):
        if self.animationFlag == 1:
            self.animation_reduce_size()
        if self.alertTimeout > 0:
            self.alertTimeout = self.alertTimeout - 1
            if self.animationFlag == 0:
                self.draw()

    def do_notification_animation(self):
        if self.notificationTimeout > 0:
            self.notificationTimeout = self.notificationTimeout - 1
            if self.notificationTimeout == 0:
                self.notificationAnimationFlag = 0
            if self.notificationAnimationFlag == 0:
                self.draw()

    def animation_reduce_size(self):
        #print("(%d,%d)\n" % (self.animationCurrentPosition[0],self.animationCurrentPosition[1]))
        #print("x %d y %d width %d height %d\n" % (self.animationCurrentX, self.animationCurrentY, self.animationCurrentWidth, self.animationCurrentHeight))
        if self.animationCurrentHeight == 1 and self.animationCurrentWidth == 1:
            self.animationImage.set_at((self.animationCurrentX,self.animationCurrentY), (0,0,0))
            self.animationFlag = 0
            if self.testMode == 1 and self.outstandingBits == 0:
                self.currentBits = self.preTestBits
            self.load_images()
        else:
            # Reduce height
            if self.animationCurrentHeight == 1:
                pass
            elif self.animationCurrentHeight == 2:
                if self.animationCurrentY == self.animationCurrentPosition[1]:
                    self.set_animation_row(self.animationCurrentY+1, (0,0,0))
                    self.animationCurrentHeight = 1
                else:
                    self.set_animation_row(self.animationCurrentY, (0,0,0))
                    self.animationCurrentHeight = 1
                    self.animationCurrentY += 1
            else:
                if self.animationCurrentHeight >= self.animationCurrentWidth:
                    if self.animationCurrentY == self.animationCurrentPosition[1]:
                        self.set_animation_row(self.animationCurrentY+self.animationCurrentHeight-1, (0,0,0))
                        self.set_animation_row(self.animationCurrentY+self.animationCurrentHeight-2, (0,0,0))
                        self.animationCurrentHeight -=2
                    elif (self.animationCurrentY+self.animationCurrentHeight-1) == self.animationCurrentPosition[1]:
                        self.set_animation_row(self.animationCurrentY, (0,0,0))
                        self.set_animation_row(self.animationCurrentY+1, (0,0,0))
                        self.animationCurrentHeight -=2
                        self.animationCurrentY += 2
                    else:
                        self.set_animation_row(self.animationCurrentY, (0,0,0))
                        self.set_animation_row(self.animationCurrentY+self.animationCurrentHeight-1, (0,0,0))
                        self.animationCurrentHeight -=2
                        self.animationCurrentY += 1

            # Reduce width
            if self.animationCurrentWidth == 1:
                pass
            elif self.animationCurrentWidth == 2:
                if self.animationCurrentX == self.animationCurrentPosition[0]:
                    self.set_animation_column(self.animationCurrentX+1, (0,0,0))
                    self.animationCurrentWidth = 1
                else:
                    self.set_animation_column(self.animationCurrentX, (0,0,0))
                    self.animationCurrentWidth = 1
                    self.animationCurrentX += 1
            else:
                if self.animationCurrentWidth >= (self.animationCurrentHeight+1):
                    if self.animationCurrentX == self.animationCurrentPosition[0]:
                        self.set_animation_column(self.animationCurrentX+self.animationCurrentWidth-1, (0,0,0))
                        self.set_animation_column(self.animationCurrentX+self.animationCurrentWidth-2, (0,0,0))
                        self.animationCurrentWidth -=2
                    elif (self.animationCurrentX+self.animationCurrentWidth-1) == self.animationCurrentPosition[0]:
                        self.set_animation_column(self.animationCurrentX, (0,0,0))
                        self.set_animation_column(self.animationCurrentX+1, (0,0,0))
                        self.animationCurrentWidth -=2
                        self.animationCurrentX += 2
                    else:
                        self.set_animation_column(self.animationCurrentX, (0,0,0))
                        self.set_animation_column(self.animationCurrentX+self.animationCurrentWidth-1, (0,0,0))
                        self.animationCurrentWidth -=2
                        self.animationCurrentX += 1
        self.draw()

    def set_animation_row(self, row, color):
        #print("row %d\n"%row)
        for i in range(self.animationImage.get_width()):
            self.animationImage.set_at((i,row),color)

    def set_animation_column(self, column, color):
        #print("column %d\n"%column)
        for i in range(self.animationImage.get_height()):
            self.animationImage.set_at((column,i),color)

    def get_current_bit_position(self):
        global NesImageLibrary
        count = self.currentPartialBits
        width = NesImageLibrary[self.currentImageIndex]['image'].get_width()
        height = NesImageLibrary[self.currentImageIndex]['image'].get_height()
        for i in range(height):
            for j in range(width):
                pixel = NesImageLibrary[self.currentImageIndex]['image'].get_at((j,height-i-1))
                if not (pixel.r == 0 and pixel.g == 0 and pixel.b == 0):
                    count -= 1
                    if count == 0:
                        return (j,height-i-1)

    def get_current_bit_color(self):
        global NesImageLibrary
        return NesImageLibrary[self.currentImageIndex]['image'].get_at(self.get_current_bit_position())

    def set_animation_image(self, color):
        width = self.animationImage.get_width()
        height = self.animationImage.get_height()
        for i in range(height):
            for j in range(width):
                self.animationImage.set_at((j,i), color)        

    def create_ghost(self, ghost, bits):
        width = ghost.get_width()
        height = ghost.get_height()
        count = 0
        for i in range(height):
            for j in range(width):
                pixel = ghost.get_at((j,height-i-1))
                if not (pixel.r == 0 and pixel.g == 0 and pixel.b == 0):
                    count += 1
                    if count > bits:
                        c = ghost.set_at((j,height-i-1), (64, 64, 64, 255))

    def find_current_position(self):
        global NesImageLibrary
        global NesImageCount
        tempBits = self.currentBits
        for i in range(NesImageCount):
            if tempBits <= NesImageLibrary[i]['pixels']:
                self.currentPartialBits = tempBits
                return i
            else:
                tempBits -= NesImageLibrary[i]['pixels']
        self.currentPartialBits = NesImageLibrary[NesImageCount-1]['pixels']
        return NesImageCount-1

    def get_current_image_count(self):
        return NesImageLibrary[self.currentImageIndex]['pixels']

    def get_current_partial_count(self):
        return self.currentPartialBits

    def load_images(self):
        global NesImageLibrary
        global NesImageCount
        global screen
        self.max_height = 0
        self.currentImageIndex = self.find_current_position()
        if self.currentImageIndex == 0:
            NesImageLibrary[0]['image'] = pygame.image.load(NesImageLibrary[0]['file'])
            NesImageLibrary[0]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[0]['ghost'] = NesImageLibrary[0]['image'].copy()
            self.create_ghost(NesImageLibrary[0]['ghost'], self.currentPartialBits)
            NesImageLibrary[1]['image'] = pygame.image.load(NesImageLibrary[1]['file'])
            NesImageLibrary[1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[1]['ghost'] = NesImageLibrary[1]['image'].copy()
            self.create_ghost(NesImageLibrary[1]['ghost'], 0)
            NesImageLibrary[2]['image'] = pygame.image.load(NesImageLibrary[2]['file'])
            NesImageLibrary[2]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[2]['ghost'] = NesImageLibrary[2]['image'].copy()
            self.create_ghost(NesImageLibrary[2]['ghost'], 0)
            NesImageLibrary[3]['image'] = pygame.image.load(NesImageLibrary[3]['file'])
            NesImageLibrary[3]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[3]['ghost'] = NesImageLibrary[3]['image'].copy()
            self.create_ghost(NesImageLibrary[3]['ghost'], 0)
            if NesImageLibrary[0]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[0]['image'].get_height()
            if NesImageLibrary[1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[1]['image'].get_height()
            if NesImageLibrary[2]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[2]['image'].get_height()
            if NesImageLibrary[3]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[3]['image'].get_height()
        elif self.currentImageIndex == (NesImageCount-2):
            NesImageLibrary[self.currentImageIndex-2]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex-2]['file'])
            NesImageLibrary[self.currentImageIndex-2]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex-1]['image']   = pygame.image.load(NesImageLibrary[self.currentImageIndex-1]['file'])
            NesImageLibrary[self.currentImageIndex-1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex]['file'])
            NesImageLibrary[self.currentImageIndex]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['ghost'] = NesImageLibrary[self.currentImageIndex]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex]['ghost'], self.currentPartialBits)
            NesImageLibrary[self.currentImageIndex+1]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex+1]['file'])
            NesImageLibrary[self.currentImageIndex+1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex+1]['ghost'] = NesImageLibrary[self.currentImageIndex+1]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex+1]['ghost'], 0)
            if NesImageLibrary[self.currentImageIndex-2]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-2]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex-1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-1]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex+1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex+1]['image'].get_height()
        elif self.currentImageIndex == (NesImageCount-1):
            NesImageLibrary[self.currentImageIndex-3]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex-3]['file'])
            NesImageLibrary[self.currentImageIndex-3]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex-2]['image']   = pygame.image.load(NesImageLibrary[self.currentImageIndex-2]['file'])
            NesImageLibrary[self.currentImageIndex-2]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex-1]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex-1]['file'])
            NesImageLibrary[self.currentImageIndex-1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex]['file'])
            NesImageLibrary[self.currentImageIndex]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['ghost'] = NesImageLibrary[self.currentImageIndex]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex]['ghost'], self.currentPartialBits)
            if NesImageLibrary[self.currentImageIndex-3]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-3]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex-2]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-2]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex-1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-1]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex]['image'].get_height()
        else:
            NesImageLibrary[self.currentImageIndex-1]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex-1]['file'])
            NesImageLibrary[self.currentImageIndex-1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['image']   = pygame.image.load(NesImageLibrary[self.currentImageIndex]['file'])
            NesImageLibrary[self.currentImageIndex]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex]['ghost'] = NesImageLibrary[self.currentImageIndex]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex]['ghost'], self.currentPartialBits)
            NesImageLibrary[self.currentImageIndex+1]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex+1]['file'])
            NesImageLibrary[self.currentImageIndex+1]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex+1]['ghost'] = NesImageLibrary[self.currentImageIndex+1]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex+1]['ghost'], 0)
            NesImageLibrary[self.currentImageIndex+2]['image'] = pygame.image.load(NesImageLibrary[self.currentImageIndex+2]['file'])
            NesImageLibrary[self.currentImageIndex+2]['image'].set_colorkey((0,0,0,255))
            NesImageLibrary[self.currentImageIndex+2]['ghost'] = NesImageLibrary[self.currentImageIndex+2]['image'].copy()
            self.create_ghost(NesImageLibrary[self.currentImageIndex+2]['ghost'], 0)
            if NesImageLibrary[self.currentImageIndex-1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex-1]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex+1]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex+1]['image'].get_height()
            if NesImageLibrary[self.currentImageIndex+2]['image'].get_height() > self.max_height:
                self.max_height = NesImageLibrary[self.currentImageIndex+2]['image'].get_height()
        self.animationImage = NesImageLibrary[self.currentImageIndex]['image'].copy()
        self.set_animation_image((0,0,0))
        screen = pygame.display.set_mode((350,self.max_height+50+self.max_overall_height*2 + self.alertFont.size("A")[1]*2 + 4))

    def get_pixel_count(self, image):
        width = image.get_width()
        height = image.get_height()
        count = 0
        for i in range(height):
            for j in range(width):
                pixel = image.get_at((j,height-i-1))
                if not (pixel.r == 0 and pixel.g == 0 and pixel.b == 0):
                    count += 1
        return count

    def dump_pixel_counts(self):
        global NesImageLibrary
        global NesImageCount
        total_count = 0
        image_count = 0
        for i in range(NesImageCount):
            currentImage = pygame.image.load(NesImageLibrary[i]['file'])
            image_count = self.get_pixel_count(currentImage)
            NesImageLibrary[i]['pixels'] = image_count
            if currentImage.get_height() > self.max_overall_height:
                self.max_overall_height = currentImage.get_height()
            total_count = total_count + image_count
            print("%d %d %d %s" % (i, image_count, total_count, NesImageLibrary[i]['name']))
        
    def check(self):
        for i in range(self.size):
            if self.tower[2][i] != self.size-i:
                return
        self.bgcolor = (0, 128, 0)

    def move(self, fromTower, toTower):
        #print("move %d %d" % (fromTower, toTower))
        if fromTower == toTower or self.tower[fromTower][0] == 0 or fromTower >= 3 or toTower >= 3:
            return
        for i in range(self.size+1):
            #print("%d %d" % (i, self.tower[fromTower][i]))
            if self.tower[fromTower][i] == 0:
                #print("i %d" % (i))
                for j in range(self.size+1):
                    if self.tower[toTower][j] == 0:
                        #print("j %d" % (j))
                        #print("%d %d" % (self.tower[fromTower][i-1],self.tower[toTower][j-1]))
                        if j == 0 or self.tower[fromTower][i-1] < self.tower[toTower][j-1]:
                            self.tower[toTower][j] = self.tower[fromTower][i-1]
                            self.tower[fromTower][i-1] = 0
                            self.moves = self.moves + 1
                            self.check()
                            self.draw()
                        break
                break

    def drawBitNes(self):
        screen.fill(self.bgcolor)
        screen.blit(self.font.render("NES", True, (255,0,0)).convert_alpha(), (108, 2))
        screen.blit(self.font.render("Bit", True, (190,99,255)).convert_alpha(), (108+32, 2))
        screen.blit(self.bitImageSmall, (108+52,0))
        screen.blit(self.font.render("Collection", True, (255,255,255)).convert_alpha(), (108+66, 2))
        self.displayNesImages()
        #print("alertTimeout %d\n" % (self.alertTimeout))
        if self.alertTimeout > 0:
            tmpSize = self.alertFont.size(self.alertText)
            tmpSize2 = self.alertFont.size(str(self.alertBits))
            tmpSize3 = self.alertFont.size(NesImageLibrary[self.currentImageIndex]['name'])
            screen.blit(self.alertFont.render(self.alertText, True, (255,255,255)).convert_alpha(), (350/2 - tmpSize[0]/2 - 14 - 3 - tmpSize2[0]/2, (20 + self.max_height + tmpSize3[1])/2 - tmpSize[1]/2))
            screen.blit(self.bitImage, (350/2 - tmpSize[0]/2 - 14 - 3 - tmpSize2[0]/2 + tmpSize[0] + 3,(20 + self.max_height + tmpSize3[1])/2-14))
            screen.blit(self.alertFont.render(str(self.alertBits), True, (190,99,255)).convert_alpha(), (350/2 - tmpSize[0]/2 - 14 - 3 - tmpSize2[0]/2 + tmpSize[0] + 28 + 6, (20 + self.max_height + tmpSize3[1])/2 - tmpSize2[1]/2))
        tmpSize = self.font.size(NesImageLibrary[self.currentImageIndex]['name'])
        screen.blit(self.font.render(NesImageLibrary[self.currentImageIndex]['name'], True, (255, 255, 255)).convert_alpha(), (((350/2) - (tmpSize[0]/2)), self.max_height+20))
        if not self.outstandingName == '':
            displayBits = 0
            if self.animationFlag == 0:
                displayBits = self.previousBits
            else:
                displayBits = self.outstandingBits+1
            tmpSize = self.font.size(self.outstandingName)
            tmpSize2 = self.font.size(str(displayBits))
            screen.blit(self.font.render(self.outstandingName, True, (255,255,255)).convert_alpha(), (350/2 - tmpSize[0]/2 - 7 - 3 - tmpSize2[0]/2, self.max_height+20+tmpSize[1]))
            screen.blit(self.bitImageSmall, (350/2 - tmpSize[0]/2 - 7 - 3 - tmpSize2[0]/2 + tmpSize[0] + 3, self.max_height + 20 + tmpSize[1]))
            screen.blit(self.font.render(str(displayBits), True, (190,99,255)).convert_alpha(), (350/2 - tmpSize[0]/2 - 7 - 3 - tmpSize2[0]/2 + tmpSize[0] + 14 + 6, self.max_height+20+tmpSize[1]))

    def drawNotifications(self):
        screen.blit(self.notification_background, (0,self.max_height+50))
        if self.notificationTimeout > 0:
            screen.blit(self.notificationAnimationImage, (self.notificationAnimationCurrentX,self.notificationAnimationCurrentY))
            followText = "is now following!"
            tmpSize = self.alertFont.size(self.notificationText)
            tmpSize2 = self.alertFont.size(followText)
            screen.blit(self.alertFont.render(self.notificationText, True, (255,255,255)).convert_alpha(), ((350-tmpSize[0])/2, self.notificationAnimationCurrentY+self.notificationAnimationImage.get_height()+2))
            screen.blit(self.alertFont.render(followText, True, (255,255,255)).convert_alpha(), ((350-tmpSize2[0])/2, self.notificationAnimationCurrentY+self.notificationAnimationImage.get_height()+tmpSize[1]+4))

    def draw(self):
        self.drawBitNes()
        self.drawNotifications()
        pygame.display.flip()

    def displayNesImages(self):
        global NesImageLibrary
        global NesImageCount
        if self.currentImageIndex == 0:
            screen.blit(NesImageLibrary[self.currentImageIndex]['ghost'],   ((87/2)-(NesImageLibrary[self.currentImageIndex]['image'].get_width()/2),20))
            screen.blit(NesImageLibrary[self.currentImageIndex+1]['ghost'], (87 + (87/2) - (NesImageLibrary[self.currentImageIndex+1]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex+2]['ghost'], (87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex+2]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex+3]['ghost'], (87 + 87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex+3]['image'].get_width()/2), 20))
            screen.blit(self.animationImage,((87/2)-(NesImageLibrary[self.currentImageIndex]['image'].get_width()/2),20))
        elif self.currentImageIndex == (NesImageCount-2):
            screen.blit(NesImageLibrary[self.currentImageIndex-2]['image'], ((87/2)-(NesImageLibrary[self.currentImageIndex-2]['image'].get_width()/2),20))
            screen.blit(NesImageLibrary[self.currentImageIndex-1]['image'], (87 + (87/2) - (NesImageLibrary[self.currentImageIndex-1]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex]['ghost'],   (87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex+1]['ghost'], (87 + 87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex+1]['image'].get_width()/2), 20))
            screen.blit(self.animationImage,(87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['ghost'].get_width()/2), 20))
        elif self.currentImageIndex == (NesImageCount-1):
            screen.blit(NesImageLibrary[self.currentImageIndex-3]['image'], ((87/2)-(NesImageLibrary[self.currentImageIndex-3]['image'].get_width()/2),20))
            screen.blit(NesImageLibrary[self.currentImageIndex-2]['image'], (87 + (87/2) - (NesImageLibrary[self.currentImageIndex-2]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex-1]['image'], (87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex-1]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex]['ghost'],   (87 + 87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['image'].get_width()/2), 20))
            screen.blit(self.animationImage,(87 + 87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['ghost'].get_width()/2), 20))
        else:
            screen.blit(NesImageLibrary[self.currentImageIndex-1]['image'], ((87/2)-(NesImageLibrary[self.currentImageIndex-1]['image'].get_width()/2),20))
            screen.blit(NesImageLibrary[self.currentImageIndex]['ghost'],   (87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex+1]['ghost'], (87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex+1]['image'].get_width()/2), 20))
            screen.blit(NesImageLibrary[self.currentImageIndex+2]['ghost'], (87 + 87 + 87 + (87/2) - (NesImageLibrary[self.currentImageIndex+2]['image'].get_width()/2), 20))
            screen.blit(self.animationImage,(87 + (87/2) - (NesImageLibrary[self.currentImageIndex]['ghost'].get_width()/2), 20))

    #def debugPrint(self):
    #    print("width %d" % (self.pixelImageWidth))
    #    print("height %d" % (self.pixelImageHeight))
    #    for i in range(self.pixelImageHeight):
    #        for j in range(self.pixelImageWidth):
    #            c = self.pixelImage.get_at((j,i))
    #            print("(%02X,%02X,%02X), " % (c.r, c.g, c.b))
    #        print("\n")
        
        
# to connect to the irc you'll need an oauth code for your account as a "PASS" when you connect

s = socket.socket()
s.connect(("irc.twitch.tv", 6667))
s.send("USER link_7777\r\n".encode())
s.send("PASS oauth:Redacted oauth password (hash)\r\n".encode())
s.send("NICK link_7777\r\n".encode())
s.send("JOIN #link_7777\r\n".encode())
s.send("CAP REQ :twitch.tv/tags\r\n".encode())

s.send("PRIVMSG #link_7777 :bot has joined\r\n".encode())

irc_thread = IrcThread()
irc_thread.start()

http_thread = HttpThread()
http_thread.start()

def RequestFollowerNotifications():
    info = { 'hub.callback': EXTERNAL_ADDRESS + ":" + SERVER_PORT,
             'hub.mode': 'subscribe',
             'hub.topic': 'https://api.twitch.tv/helix/users/follows?to_id=' + USER_ID,
             'hub.lease_seconds': '604800',
             'hub.secret': SECRET}
    data = urllib.urlencode(info)
    req = urllib2.Request('https://api.twitch.tv/helix/webhooks/hub', data)
    req.add_header('Client-ID',CLIENT_ID)
    req.get_method = lambda: 'POST'
    res = urllib2.urlopen(req)
    print res.read()
    print "Requested follower notifications\n"
    

def UpdateChannel(info):
    data = urllib.urlencode(info)
    req = urllib2.Request('https://api.twitch.tv/kraken/channels/' + USER_ID, data)
    req.add_header('Accept','application/vnd.twitchtv.v5+json')
    req.add_header('Authorization',"OAuth " + ACCESS_TOKEN)
    req.get_method = lambda: 'PUT'
    res = urllib2.urlopen(req)
    return res.read()

def UpdateTitle(newTitle):
    channel = json.loads(UpdateChannel({'channel[status]' : newTitle}))
    s.send(("PRIVMSG #link_7777 :Title Changed to %s\r\n" % (channel["status"])).encode())

def UpdateGame(newGame):
    channel = json.loads(UpdateChannel({'channel[game]' : newGame}))
    s.send(("PRIVMSG #link_7777 :Game Changed to %s\r\n" % (channel["game"])).encode())

def getChannelByID(userID):
    req = urllib2.Request('https://api.twitch.tv/kraken/channels/' + userID)
    req.add_header('Accept','application/vnd.twitchtv.v5+json')
    req.add_header('Client-ID', CLIENT_ID)
    res = urllib2.urlopen(req)
    return res.read()

def GetGame():
    channel = json.loads(getChannelByID(USER_ID))
    s.send(("PRIVMSG #link_7777 :Current Game: %s\r\n" % (channel["game"])).encode())
    
def GetTitle():
    channel = json.loads(getChannelByID(USER_ID))
    s.send(("PRIVMSG #link_7777 :Current Title: %s\r\n" % (channel["status"])).encode())

def GetDisplayName(userID):
    channel = json.loads(getChannelByID(userID))
    print(channel)
    return channel["display_name"]

def GetStream():
    req = urllib2.Request('https://api.twitch.tv/kraken/streams/' + USER_ID)
    req.add_header('Accept','application/vnd.twitchtv.v5+json')
    req.add_header('Client-ID',CLIENT_ID)
    res = urllib2.urlopen(req)
    return res.read()

def GetTime():
    stream = json.loads(GetStream())
    if stream["stream"] == None:
        return None
    else:
        return stream["stream"]["created_at"]

def UpdateBits(epoch, user, count):
    global bitnes
    if user in bitInfo:
        bitInfo[user] += count
    else:
        bitInfo[user] = count
    bitInfo['link_7777_total_bits'] += count
    LogBits(epoch, user, str(count))
    SaveBitInfo()
    bitnes.add_bits(user, count, 0)

def SaveBitInfo():
    bitInfoFile = open("bit_info.json", 'w')
    json.dump(bitInfo, bitInfoFile)
    bitInfoFile.close()

def LoadBitInfo():
    global bitInfo
    bitInfoFile = open("bit_info.json", 'r')
    bitInfo = json.load(bitInfoFile)
    bitInfoFile.close()

def LogBits(epoch, user, count):
    bitLog = open("bit_log.txt", 'a')
    bitLog.write(epoch + ", " + user + ", " + count + "\n")
    bitLog.close()

def SearchGame(game):
    req = urllib2.Request('https://api.twitch.tv/kraken/search/streams?query=' + urllib.quote_plus(game))
    req.add_header('Accept','application/vnd.twitchtv.v5+json')
    req.add_header('Client-ID',CLIENT_ID)
    res = urllib2.urlopen(req)
    return json.loads(res.read())

def LiveAlertCheck():
    global LiveAlertTimeout
    LiveAlertMessage = ''
    LiveAlertTimeout -= 1
    if LiveAlertTimeout == 0:
        global LiveAlertList
        LiveAlertTimeout = 300*8
        for i in range(0,LiveAlertListLength):
            theGame = LiveAlertList[i]
            tmpLiveList = {}
            print(theGame['game'])
            search_result = SearchGame(theGame['game'])
            #print(search_result['streams'])
            #if 'channel' in search_result:
            for chan in search_result['streams']:
                #print(chan)
                if repr(theGame['game']) == repr(chan['channel']['game']):
                    tmpLiveList[chan['channel']['display_name']] = chan['channel']['game']
                    print("%s %s\n" % (repr(chan['channel']['display_name']), repr(chan['channel']['game'])))
            for name in tmpLiveList:
                #print("LiveAlertList:")
                #print(LiveAlertList)
                if not 'live' in LiveAlertList[i] or not name in LiveAlertList[i]['live']:
                    LiveAlertMessage = LiveAlertMessage + name + ' is playing ' + tmpLiveList[name] + "\n"
                    #print("Message:")
                    #print(LiveAlertMessage
            LiveAlertList[i]['live'] = tmpLiveList
    if LiveAlertMessage != '':
        SendLiveAlertMessage(LiveAlertMessage)

def SendLiveAlertMessage(message):
    try:
        smtp_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_ssl.ehlo()
        smtp_ssl.login("Redacted email","Redacted password")
        smtp_ssl.sendmail("Redacted email","Redacted email","Subject: bitNES Live Alert\n\n " + message)
        smtp_ssl.close()
        print("email sent")
    except:
        error = sys.exc_info()[0]
        print("email NOT sent: " + repr(error))

LiveAlertTimeout = 1
LiveAlertCheck()
#searchResults = SearchGame('Super Glove Ball')
#for chan in searchResults['streams']:
#    print("%s %s\n" % (chan['channel']['display_name'], chan['channel']['game']))

#req = urllib2.Request('https://api.twitch.tv/kraken/search/channels?query=zelda')
#req.add_header('Accept','application/vnd.twitchtv.v5+json')
#req.add_header('Client-ID',CLIENT_ID)
#res = urllib2.urlopen(req)
#print(res.read())


LoadBitInfo()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((350,0)) #create a screen

bitnes = BitNesCollection(bitInfo['link_7777_total_bits'])

RequestFollowerNotifications()

while 1:
    clock.tick(8)
    bitnes.outstanding_bits_check()
    bitnes.outstanding_notification_check()
    bitnes.do_animation()
    bitnes.do_notification_animation()
    bitnes.subscriptionTick()
    LiveAlertCheck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            irc_thread._Thread__stop()
            http_thread._Thread__stop()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                irc_thread._Thread__stop()
                http_thread._Thread__stop()
                quit()
