#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import urllib.parse 

def read_ini():
	parser = ConfigParser()
	parser.read('config.ini')

	return (
		parser.get("basic", "mail_errors"),
		parser.get("basic", "mail_copy_orders"),
		parser.get("basic", "pause_automatic_order"),
	)

def save_ini(mail_errors, mail_copy_orders, pause_automatic_order):
	parser = ConfigParser()
	parser.read('config.ini')

	parser.set("basic", "mail_errors", mail_errors)
	parser.set("basic", "mail_copy_orders", mail_copy_orders)
	parser.set("basic", "pause_automatic_order", pause_automatic_order)

	with open('config.ini', 'w') as configfile:
    		parser.write(configfile)

	return True

