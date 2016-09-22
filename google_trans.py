#!/usr/bin/env python
# -*- coding: utf-8 -*-

from StringIO import StringIO
from bs4 import BeautifulSoup
import urllib2
import datetime
import sys
import os
import gzip
import json

now = datetime.datetime.now()
t_char = str(now.year) + str(now.strftime('%m')) + str(now.strftime('%d'))

OUTPUT_DIRECTORY = 'output'
DECK_NAME = 'English Google-' + t_char + '-'

HDR = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Encoding': '', 'Accept-Language':	'es,en-US;q=0.7,en;q=0.3', 
 'Cache-Control': 'max-age=0', 'Connection':	'keep-alive', 
 'Host': 'translate.google.es', 
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:38.0) Gecko/20100101 Firefox/38.0'}

def get_pronunciation(word):
	site = "https://translate.google.es/translate_tts?ie=UTF-8&q=" + \
	word.replace(' ', '%20') + \
	"&tl=en&total=1&idx=0&textlen=13&tk=386128&client=t&prev=input"
	req = urllib2.Request(site, headers=HDR)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	if not os.path.exists(OUTPUT_DIRECTORY):
		os.makedirs(OUTPUT_DIRECTORY)
	f = open(os.path.join(OUTPUT_DIRECTORY, 'English Google-' + word + '-'+ t_char + '.mpeg'), 'w')
	f.write(page.read())

def help():
	h = open('help.txt', 'r')
	print h.read()

def get_translation(word):
	url = "https://translate.google.es/translate_a/single?client=t&sl=en&tl=es&hl=es&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=1&srcrom=0&ssel=0&tsel=0&kc=2&tk=522004|825240&q=" + word.replace(' ', '%20')
	req = urllib2.Request(url, headers=HDR)
	response = urllib2.urlopen(req)
	texto = response.read()
	texto = texto.split(',')
	texto = [t for t in texto if t != '']
	texto = [t + '"null"' if t== '[' else t for t in texto]
	texto = ','.join(texto)
	json_list = json.loads(texto)
	return json_list

def create_card(word, trans):
	anverse = word.title() + '<br>'
	reverse = trans[0][0][0].title() + '<br>"'
	sound = ' [sound:English Google-' + word + '-' + t_char + '.mpeg]'
	means = ''
	'''
	Example card ok:
	Struggle<br>	Lucha <br> "<div id="q"; style='font-family: Arial; font-size: 13px;'>
	sustantivo</div><div style='font-family: Arial; font-size: 12px;'>lucha, esfuerzo, forcejeo, contienda, conflicto</div>
	<div id="q"; style='font-family: Arial; font-size: 13px;'></div>
	<div style='font-family: Arial; font-size: 12px;'></div><div id="q"; style='font-family: Arial; font-size: 13px;'></div>
	<div style='font-family: Arial; font-size: 12px;'></div><div id="q"; style='font-family: Arial; font-size: 13px;'>verbo</div>
	<div style='font-family: Arial; font-size: 12px;'>lucha, esfuerzo, forcejeo, contienda, conflicto, luchar, forcejear, esforzarse, bregar, debatirse</div>
	<div id="q"; style='font-family: Arial; font-size: 13px;'></div><div style='font-family: Arial; font-size: 12px;'></div>
	<div id="q"; style='font-family: Arial; font-size: 13px;'></div><div style='font-family: Arial; font-size: 12px;'></div>" [sound:English Google-struggle-20150702.mpeg]
	'''
	if trans[1] != 'en':
		for t in trans[1]:
			for s in t[1]:
				if means != '':
					means = means + ', ' + s
				else:
					means = s
			reverse = reverse + """<br><div id="q"; style='font-family: Arial; font-size: 13px;'>""" + t[0] + """</div><div style='font-family: Arial; font-size: 12px;'>""" + means + """</div><div id="q"; style='font-family: Arial; font-size: 13px;'></div><div style='font-family: Arial; font-size: 12px;'></div><div id="q"; style='font-family: Arial; font-size: 13px;'></div><div style='font-family: Arial; font-size: 12px;'></div> """
			means = ''
	return (anverse, reverse + '"', sound)

def create_file_cards(words):
	if not os.path.exists(OUTPUT_DIRECTORY):
		os.makedirs(OUTPUT_DIRECTORY)
	fa = open(os.path.join(OUTPUT_DIRECTORY, DECK_NAME + 'anverse.txt'), 'w')
	fr = open(os.path.join(OUTPUT_DIRECTORY, DECK_NAME + 'reverse.txt'), 'w')
	for w in words:
		card = create_card(w, get_translation(w))
		ca = card[0] + '	' + card[1] + ' ' + card[2]
		cr = card[1] + ' ' + card[2] + '	' + card[0]
		fa.write(ca.encode('utf-8'))
		fa.write('\n')
		fa.write('\n')
		fr.write(cr.encode('utf-8'))
		fr.write('\n')
		fr.write('\n')
		get_pronunciation(w)

def get_words(file_name):
	words = []
	f = open(file_name, 'r')
	for l in f:
		words.append(l.replace('\n', ''))
	return words

if __name__ == "__main__":
	p = sys.argv
	if len(p) > 1:
		if '-h' in p[1]:
			help()
		elif '-f' in p[1]:
			get_pronunciation(p[2])
		else:
			words = get_words(p[1])
			create_file_cards(words)
