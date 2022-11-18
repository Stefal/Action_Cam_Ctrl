#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import requests
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET


key_translate ={
    '1001':{'cmd':'take photo'},
    '1002':{'cmd':'set photo size', '1':'12MP', '2':'8MP'},
    '1003':{'cmd':'get freepic number'},
    '2001':{'cmd':'2001'},
    '2002':{'cmd':'get video size',
                '0': '2880x2160 24fps 16/9', 
                '1': '2880x2160 24fps 4/3', 
                '2': '2560x1440 30fps 16/9', 
                '3':'1920x1440 30fps 4/3', 
                '4':'2304x1296 30fps 16/9', 
                '5': '1920x1080 60fps 16/9', 
                '6':'1920x1080 30fps 16/9',
                '7':'1440x1080 60fps 4/3',
                '8': '1280x720 120fps 16/9',
                '9': '1280x720 60fps 16/9',
                '10': '1280x720 30fps 16/9',
                '11':'848x480 30fps 16/9',
                '12':'640x480 240fps 16/9',

    },
    '2003':{'cmd':'set loop recording', '0':'off', '1':'2mn', '2':'3mn', '3':'5mn', '4':'10mn'},
    '2004':{'cmd': 'set wdr', '0':'off', '1':'on'},
    '2005':{'cmd': 'set EV compensation', '0':'+2.0', '1':'+1.6', '2':'+1.3', '3':'+1', '4':'+0.6',
                '5':'+0.3', '6':'0', '7':'-0.3', '8':'-0.6', '9':'-1', '10':'-1.3', '11':'-1.6', '12':'-2.0'},
    '2006':{'cmd': 'set motion detect', '0':'off', '1':'on'},
    '2007':{'cmd': 'set record audio', '0':'off', '1':'on'},
    '2008':{'cmd': 'set date stamp', '0':'off', '1':'on'},
    '2009':{'cmd': 'max rec time'},
    '2010':{'cmd': 'liveview size'},
    '2011':{'cmd': 'g-sensors sensitivity', '0':'off', '1':'low', '2':'medium', '3':'high'},
    '2012':{'cmd': 'autorec'},
    '2013':{'cmd': 'video bitrate'},
    '2014':{'cmd': 'liveview bitrate'},
    '2015':{'cmd': 'enabled liveview'},
    '2016':{'cmd': 'rec time'},
    '2017':{'cmd': 'take video snapshot'},
    '2018':{'cmd': 'save snapshot file'},
    '3001':{'cmd': 'set mode', '0': 'photo', '1': 'video', '2': 'playback'},
    '3002':{'cmd': 'list commands'},
    '3003':{'cmd': 'set ssid'},
    '3004':{'cmd': 'set wifi password'},
    '3005':{'cmd': 'set date yy-mm-dd'},
    '3006':{'cmd': 'set hour hh-mn-ss'},
    '3007':{'cmd': 'poweroff time', '0':'off', '1':'1mn', '2':'3mn', '3':'5mn', '4':'10m', '5':'15mn', '6':'30mn', '7':'60mn'},
    '3008':{'cmd': 'langage', '0':'english', '1':'français', '2':'espanol', '3':'po', '4':'deutsch', '5':'italian', '6':'sc', '7':'tc', '8':'russian', '9':'japan', '10':'cz', '11':'pl', '12':'nl'},
    '3009':{'cmd': 'tv format', '0':'ntsc', '1':'pal'},
    '3010':{'cmd': 'format SD card'},
    '3011':{'cmd': 'Reset to default settings'},
    '3012':{'cmd': 'Show version'},
    '3013':{'cmd': 'FW update'},
    '3014':{'cmd': 'show status'},
    '3015':{'cmd': 'file list'},
    '3016':{'cmd': 'ping cam'},
    '3017':{'cmd': 'get free space'},
    '3018':{'cmd': 'reconnect wifi'},
    '3019':{'cmd': 'get battery level', '0':'full', '1':'med', '2':'low', '3':'empty', '4':'exhstd???', '5':'charge on'},
    '3020':{'cmd': 'socket port 3333'},
    '3021':{'cmd': 'save settings to flash'},
    '3022':{'cmd': 'get hardware capacity'},
    '3023':{'cmd': 'remove last user'},
    '3024':{'cmd': 'get SD card status', '0':'rem', '1':'inserted', '2':'locked'},
    '3028':{'cmd': '3028'},
    '3029':{'cmd': 'show ssid/password'},
    '3030':{'cmd': 'return video mode list'},
    '3031':{'cmd': 'show some commands'},
    '9001':{'cmd': 'shutter speed', '0':'auto', '1':'1/2000s', '2':'1/1000s', '3':'1/500s', '4':'1/250s', '5':'1/125s', '6':'1/30s', '7':'1s', '8':'2s', '9':'5s', '10':'10s', '11':'15s', '12':'20s', '13':'30s', '14':'60s'},
    '9002':{'cmd': 'date stamp', '0':'off', '2':'on'},
    '9003':{'cmd': 'timelapse mode ?', '0':'off', '1': '0.5s', '2':'1s', '3':'2s', '4':'5s', '5':'10s', '6':'30s'},
    '9004':{'cmd': 'Self timer', '0':'off', '1': '3s', '2':'5s', '3':'10s', '4':'15s', '5':'30s'},
    '9006':{'cmd': 'RAW', '0':'off', '1':'on'},
    '9010':{'cmd': 'photo White Balance', '0':'auto', '1':'daylight', '2':'cloudy', '3':'tungsten', '4':'fluorescent', '5':'blue', '6':'light blue', '7':'red', '8':'light red', '9':'custom'},
    '9011':{'cmd': 'ISO', '0':'auto', '1':'50', '2':'100', '3':'200', '4':'400', '5':'800', '6':'1600'},
    '9012':{'cmd': 'photo color', '0':'normal', '1':'black & white', '2':'sepia', '3':'colorful', '4':'vivid'},
    '9015':{'cmd': 'contrast', '0':'low', '1':'normal', '2':'high'},
    '9016':{'cmd': 'Zoom A', '0':'1x', '1':'1.2x', '2':'1.6x', '3':'2.2x', '4':'2.8x'},
    '9017':{'cmd': 'photo GPS stamp', '0':'off', '1':'both', '2':'speed', '3':'coordinate'},
    '9202':{'cmd': 'audio level', '0':'off', '1':'low', '2':'medium', '3':'high'},
    '9203':{'cmd': 'video White Balance', '0':'auto', '1':'daylight', '2':'cloudy', '3':'tungsten', '4':'fluorescent', '5':'blue', '6':'light blue', '7':'red', '8':'light red', '9':'custom'},
    '9205':{'cmd': 'video color', '0':'normal', '1':'black & white', '2':'sepia', '3':'colorful', '4':'vivid'},
    '9206':{'cmd': 'sharpness', '0':'low', '1':'medium', '2':'high'},
    '9207':{'cmd': 'metering', '0':'average', '1':'center', '2':'Spot', '3':'Car DVR'},
    '9210':{'cmd': 'video stabilization', '0':'off', '1':'on'},
    '9211':{'cmd': 'Auto low light', '0':'off', '1':'on'},
    '9212':{'cmd': 'video bitrate', '0':'low', '1':'medium', '2':'high'},
    '9213':{'cmd': 'Zoom B', '0':'1x', '1':'1.2x', '2':'1.6x', '3':'2.2x', '4':'2.8x'},
    '9214':{'cmd': 'video GPS stamp', '0':'off', '1':'both', '2':'speed', '3':'coordinate'},
    '9403':{'cmd': 'beep', '0':'off', '1':'on'},
    '9404':{'cmd': 'OSD', '0':'on', '1':'rec dot', '2':'off'},
    '9405':{'cmd': 'lock/screen saver', '0':'off', '1':'1mn', '2':'3mn', '3':'5mn', '4':'10m', '5':'15mn', '6':'30mn', '7':'60mn' },
    '9406':{'cmd': 'light frequency', '0':'50Hz', '1':'60Hz'},
    '9409':{'cmd': 'quick capture', '0':'off', '1':'on'},
    '9410':{'cmd': 'enable GPS', '0':'off', '1':'on'},
    '9412':{'cmd': 'speed unit', '0':'mph', '1':'kmh'},
    '9413':{'cmd': 'image rotation', '0':'off', '1':'180°', '2':'slave cam 180°', '3':'both cam 180°'},
    '9414':{'cmd': 'status led', '1':'all off', '2':'front off', '3':'side off', '4':'only front on', '5':'only back on'},
    '9415':{'cmd': 'external power', '0':'charge', '1':'power on', '2':'recording'},
    '9416':{'cmd': 'date format', '0':'year month day', '1':'month day year', '2':'day month year'},
}

class cam_ctrl(object):

    G3_DUO_IP_ADDRESS = "192.168.1.254"


    def __init__(self, cam_ip=G3_DUO_IP_ADDRESS , name='G3 Duo'):
        self.ip = cam_ip
        self.name = name
        self.api = key_translate
        self.rev_api = self.reverse_dict(key_translate)

    def reverse_dict(self, dict_to_reverse):
        reverse = {}
        for key, value in key_translate.items():
            reverse[value['cmd']] = {sub_value:sub_key for sub_key, sub_value in value.items()}
            reverse[value['cmd']].update({'cmd':key})
            del(reverse[value['cmd']][value['cmd']])
        return reverse

    def convert_to_human_keys_values(self,hard_to_read_dict, translate_table_dict):
        human_dict = {}
        for key in hard_to_read_dict:
            try:
                if translate_table_dict.get(key) is not None:
                    #human_dict[translate_table_dict[key]] = translate_table_dict[key][hard_to_read_dict[key]]
                    new_key = translate_table_dict[key]['cmd']
                    new_value = translate_table_dict[key].get(hard_to_read_dict[key], hard_to_read_dict[key])
                    human_dict[new_key] = new_value
                else:
                    human_dict[key] = hard_to_read_dict[key]
                
            except Exception as e:
                print('Exception: ', e)
        return human_dict

    def xml_to_dict(self, xml_string):

        tree = ET.fromstring(xml_string)
        Cam_dict = {}
        for child in tree:
            if child.tag == 'Cmd':
                #Cam_dict[child.text] = ''
                last_cmd = child.text
            if child.tag == 'Status':
                Cam_dict[last_cmd] = child.text
                del last_cmd
        return Cam_dict

    def dict_diff(self, dict1, dict2):

        #find the identical key in the two dicts
        d_same_key = {key:dict2[key] for key in dict1 if key in dict2}
        #find the keys with diffent values
        diff_value = {key:d_same_key[key] for key in d_same_key if dict1[key] != d_same_key[key]}
        #find keys in dict2 inexistant in dict1
        new_keys = {key:dict2[key] for key in dict2 if key not in dict1}

        result = {}
        result['New_key'] = new_keys if len(new_keys) != 0 else None
        result['New_value'] = diff_value if len(diff_value) !=0 else None

        return result

    def capture_mode(self, capture_mode):
        """
        mode photo, video, playback
        """
        try:
            self.send_cmd(self, self.rev_api['set mode'][capture_mode])
        except Exception as e:
            return e


    def send_cmd(self, cmd, param=''):
        
        #tosend = 'http://' + cam_address + '/' + '?custom=1' + 'cmd='
        param = "?par={0}".format(param) if param != '' else ''
        tosend = "http://{0}/?custom=1&cmd={1}{2}".format(self.ip, cmd, param)
        try:
            r = requests.get(tosend)
            return r.text
        except Exception as e:
            return e

def diff_test1():

    #test same dict
    dct1 = dct2 = {'1002': 1, '2016': 0, '2001': 0}
    result = dict_diff(dct1, dct2)
    assert result == {'New_key': None, 'New_value': None}, result

    #test new value
    dct2 = {'1002': 1, '2016': 1, '2001': 0}
    result = dict_diff(dct1, dct2)
    assert result == {'New_key': None, 'New_value': {'2016':1}}, result

    #test new key
    dct2 = {'1002': 1, '2016': 0, '2001': 0, '9999': 9}
    result = dict_diff(dct1, dct2)
    assert result == {'New_key': {'9999': 9}, 'New_value': None}, result

    #test new key and new value
    dct2 = {'1002': 1, '2016': 1, '2001': 0, '9999': 9}
    result = dict_diff(dct1, dct2)
    assert result == {'New_key': {'9999': 9}, 'New_value': {'2016':1}}, result

    #test new keys and new values
    dct2 = {'1002': 4, '2016': 1, '2001': 0, '9999': 9, '666': 'hell'}
    result = dict_diff(dct1, dct2)
    assert result == {'New_key': {'9999': 9, '666': 'hell'}, 'New_value': {'2016': 1, '1002': 4}}, result



def test_speed(count, cmd=1001, par=''):
    for i in range(count):
        start = time.time()
        send_cmd(cmd, par)
        end = time.time()
        res = end - start
        print(res)