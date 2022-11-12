#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os


def get_copies_number():

	parser = ConfigParser()
	parser.read('config.ini')

	return int(parser.get("basic", "default_copies_number"))

def get_database_name():

	parser = ConfigParser()
	parser.read('config.ini')

	return parser.get("database", "name")

def get_printers():

	parser = ConfigParser()
	parser.read('config.ini')

	return (
		parser.get("printers", "default_printer"),
		parser.get("printers", "codebar_printer")
		)
