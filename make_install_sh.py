#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser, getopt, os, sys

def main():
	installed = getinstalledlist()
	modlist, sections, sh_file, rtest, backup, export, sec_name = getoption()
	testlist, huntinglist = getconfig(modlist, sections)
	creat_empty_cmd = '>'+sh_file
	os.system(creat_empty_cmd)
	if backup:
		backup_list(sh_file, sec_name, testlist, huntinglist)
	elif export:
		export_env(sh_file, huntinglist)
	else:
		create_sh(sh_file, huntinglist, installed)

def backup_list(filename, sec_name, testlist, huntinglist):
	config = configparser.ConfigParser()
	config[sec_name] = {}
	for i, j in zip(testlist, huntinglist):
		config[sec_name][i] = j
	with open(filename, 'w') as fh:
		config.write(fh)

# TODO: finish this
def export_env(filename, huntinglist):
	pass

def create_sh(sh_file, huntinglist, installed):
	with open(sh_file, 'w') as fh:
		fh.write('#!/bin/sh\n')
		for modulename in huntinglist:
			if modulename in installed:
				print('%s is already installed: ' % modulename)
				os.system('conda list %s' % modulename)
			else:
				print('Put missing module: %s into install shell script' % modulename)
				fh.write('conda install -y %s\n' % modulename)
	
def usage(reason=''):
	if reason:
		print(reason)
	print('Usage: %s [-l|-s|-f|-t] [-b|-n|-l|-s|-f] [-e|-l|-s|-f] [-h]' % sys.argv[0])

def getoption():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'l:s:tf:hben:', ['backup', 'export', 'help', 'name=', 'list=', 'section=', 'file=', 'runtest'])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

	run_test, module_list, filename, sec_list, backup, export, name = False, 'module.list', None, ['all'], False, False, None
	for opt, arg in opts:
		if opt in ('-l', '--list'):
			module_list = arg
		elif opt in ('-h', '--help'):
			usage()
			sys.exit(1)
		elif opt in ('-s', '--section'):
			sec_list = arg.split(',')
		elif opt in ('-f', '--file'):
			filename = arg
		elif opt in ('-t', '--runtest'):
			run_test = True
		elif opt in ('-b', '--backup'):
			backup = True
		elif opt in ('-n', '--name'):
			name = arg
		elif opt in ('-e', '--export'):
			export = True
		else:
			assert False, 'Unknown option'
	if backup and export:
		usage('Option conflict')
		sys.exit(1)
	if (backup or export) and run_test:
		usage('Option conflict')
		sys.exit(1)
	if name and not backup:
		usage('Option not match')
		sys.exit(1)
	if filename is None:
		if backup:
			filename = 'backup_env_%s.list' % '_'.join(sec_list)
		if export:
			filename = 'export_env_%s.list' % '_'.join(sec_list)
		else:
			filename = 'install_%s.sh' % '_'.join(sec_list)
	if backup and not name:
		name = 'DEFAULT_SEC'
	return module_list, sec_list, filename, run_test, backup, export, name

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
	# cmd = "conda list | awk '{print $1}'"
	output = os.popen("conda list")
	ret = list(map(lambda x: '='.join(x.split()[:2]), output.read().splitlines()))
	ret += list(map(lambda x: x.split('=')[0], ret))
	return ret

if __name__ == '__main__':
	main()