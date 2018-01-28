#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser, getopt, os, sys

def main():
	installed = getinstalledlist()
	modlist, sections, sh_file, rtest = getoption()
	testlist, huntinglist = getconfig(modlist, sections)
	creat_empty_cmd = '>'+sh_file
	os.system(creat_empty_cmd)
	with open(sh_file, 'w') as fh:
		fh.write('#!/bin/sh\n')
		for importname, modulename in zip(testlist, huntinglist):
			if modulename in installed:
				print('%s is already installed: ' % modulename)
				os.system('conda list %s' % modulename)
			else:
				fh.write('conda install -y %s\n' % modulename)

def usage():
	print('Usage: %s [-l|-s|-n|-t] [-h]' % sys.argv[0])

def getoption():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'l:s:tn:h', ['help', 'list=', 'section=', 'shfile=', 'runtest'])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

	run_test, module_list, shfile, sec_list = False, 'module.list', None, ['all']
	for opt, arg in opts:
		if opt in ('-l', '--list'):
			module_list = arg
		elif opt in ('-h', '--help'):
			usage()
			sys.exit(1)
		elif opt in ('-s', '--section'):
			sec_list = arg.split(',')
		elif opt in ('-n', '--shfile'):
			shfile = arg
		elif opt in ('-t', '--runtest'):
			run_test = True
		else:
			assert False, 'Unknown option'
	if shfile is None:
		shfile = 'install_%s.sh' % '_'.join(sec_list)
	return module_list, sec_list, shfile, run_test

def getconfig(modfile, sections):
	config = configparser.ConfigParser()
	config.read(modfile)
	if len(sections) == 1 and sections[0] == 'all':
		sections = config.sections()
	importlist, modlist = [], []
	for sec in sections:
		for importname, modulename in config[sec].items():
			importlist.append(importname)
			modlist.append(modulename)
	return importlist, modlist

def getinstalledlist():
	cmd = "conda list | awk '{print $1}'"
	output = os.popen(cmd)
	return output.read().splitlines()

if __name__ == '__main__':
	main()
	# usage()