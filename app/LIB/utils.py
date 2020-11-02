#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser


def get_copies_number():

	parser = ConfigParser()
	parser.read('config.ini')

	return int(parser.get("basic", "default_copies_number"))


