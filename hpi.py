# !/usr/bin/python3
# pip3 install -r /path/requirements.txt
# Edit 12/7/20

import os
import requests
from phue import Bridge

dir_win = 'C:/phue/ip.txt'
dir_lin = '/home/pi/phue-timer/ip.txt'

def os_type(): # Detect OS
	if (os.name == 'nt'):
		return 'win'
	else:
		return 'lin'

def read_ip(): # Try to connect ip from .txt or scrape from api
	try: # ip ok -> connect
		if (os_type() == 'win'):
			with open(dir_win, 'r') as f:
				b = Bridge(f.read())
				b.connect()
		else:
			with open(dir_lin, 'r') as f:
				b = Bridge(f.read())
				b.connect()
	except Exception as e: # ip error -> scrape api
		ip = requests.get('https://discovery.meethue.com/').json()[0]['internalipaddress']
		if (os_type() ==  'win'):
			with open(dir_win, 'w') as f:
				f.write('{}'.format(ip))
				b = Bridge(ip)
		else:
			with open(dir_lin, 'w') as f:
				f.write('{}'.format(ip))
				b = Bridge(ip)
		print('* NEW IP *'.center(size))
	return b

def do_light(mode=None, brilho=254, tt=0, *lights_list): # Control on/off, brightness, transition time of all lights

	list_t = []
	for i in range(len(lights_list)):
		if(lights_list[i] != 0):
			i+=1
			list_t.append(i) # List of lights for alteration


	if mode == None: # Controls turning on and off
		for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
			if (b.get_light(list_t[i], 'on') == True): # Detecta ON
				b.set_light(list_t[i], 'on', False, transitiontime=tt) # Apaga as acessas
			elif (i == len(list_t)-1): # J é o ultimo loop ?
				for i in range(len(list_t)): # Loopa dnv
					b.set_light(list_t[i], 'on', True, transitiontime=tt) # Liga as apagadas
					lights[list_t[i]].brightness=brilho


	elif mode == False: # Use false only to turn off given list
		for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
			if (b.get_light(list_t[i], 'on') == True): # Detecta ON
				b.set_light(list_t[i], 'on', False, transitiontime=tt) # Apaga as acessas


	elif mode == True:
		for i in range(len(list_t)): # Loopa sobre as luzes selecionadas
			b.set_light(list_t[i], 'on', True, transitiontime=tt) # Liga as apagadas
			lights[list_t[i]].brightness=brilho

	# perc = brilho / 254 * 100
	# return list_t, brilho, perc, tt
	return list_t

def is_on(*lights_list): # Return a matrix with the state of all lights and brightness
	lights_list = []
	for i in lights:
		lights_list.append(i)

	lights_on = [] # Return which lights are on
	lights_bri = [] # Return each brightness

	for i in range(len(lights_list)):
		try:
			if (b.get_light(lights_list[i], 'on') == True):
				lights_on.append(True)
				bri = b.get_light(lights_list[i], 'bri')
				bri = round(bri / 254 * 100, 2)
				lights_bri.append(bri)
			else:
				lights_on.append(False)
				lights_bri.append(0)
		except Exception as e: ## ARRUMAR ISSO QND TIRAR LUZ
			lights_on.insert(0,False)
			lights_bri.insert(0,0)
	return lights_on, lights_bri

def change_bri(x, *lights_list): # 0 =< x =< 254

	list_t = []
	for i in range(len(lights_list)):
		if(lights_list[i] != 0):
			i+=1
			list_t.append(i) # List of lights for alteration

	for i in range(len(list_t)):
		# print(list_t[i])
		lights[list_t[i]].brightness = int(x)

def change_xy(list, *lights_list): # CIE 1931

	list_t = []
	for i in range(len(lights_list)):
		if(lights_list[i] != 0):
			i+=1
			list_t.append(i) # List of lights for alteration

	for i in range(len(list_t)):
		lights[list_t[i]].xy = list

def wake_up(*list, min=30): # Alternative to app, set time to fade in
	from time import sleep
	tick = 2.5
	print('set = {}\nt = {} min.\n'.format(list,min))
	# print(list, '\nt =',min, '\n')
	# list = [0,1,0,1]
	do_light(True,0,0, *list)
	change_xy([.3, .3], *list)
	it = 254 / min
	# print('Increasing', it, '\n')
	i = 0
	while True:
		i += 1
		if tick >= 254:
			change_bri(255, *list)
			break
			do_light(True,254,0, *list)
			print('Lights on\n')
		change_bri(tick, *list)
		print('Iteration', i)
		print(is_on(*list)[1],'\n')
		tick += it
		# print(tick, i)
		sleep(60)

b = read_ip()
lights = b.get_light_objects('id')

wake_up(0,1,0,1,min=30)
