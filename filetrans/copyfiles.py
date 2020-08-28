#!/usr/bin/env python
'''
author: 1nd0l3
date: 20191023
purpose: grab files and copy them
place in your root extraction directory and run program
'''
# import modules
import os, shutil, tkinter
import tkinter.filedialog as tkfd

#################### GLOBALS #################### 
####################
# get current working directory
cwd = os.getcwd()
# init loop in main
redo = 'y'
####################

#################### FUNCTIONS BELOW ####################
####################
def pathSelect():
	# select root path to search for files
	root = tkinter.Tk()
	root.withdraw()
	path = tkfd.askdirectory(initialdir='.',title='Select a source path: ')
	if not path:
		print('----------')
		print('----------')
		print('Goodbye!')		
		print('----------')
		exit()
	src = os.path.join(os.path.abspath(path))
	
	return (src)
####################
####################
def copyfiles(file_xt, src):
	# create folder (if doesn't exist)
	filefold = str(file_xt)
	if not os.path.exists(filefold):
		os.mkdir(file_xt)
	targetdir = os.path.join(cwd, filefold)
    
	print('----------')
	print('Getting all ' +str(file_xt)+ ' files from ' +str(src)+ '...')
	print('----------')
	print('----------')
    
	# loop thru folders within source path
	for root,dirs,files in os.walk(src):
		for filename in files:
			# find files and copy over to target
			if (filename.endswith(file_xt)):
				files = os.path.join(root, filename)
				print('Copied: ' +files)
				try:
					shutil.copy(files, targetdir)
				except:
					continue
	
	# created a directory even if empty. now check if empty to confirm whether files copied
	emptydir = os.listdir(targetdir)
	chk_empty(emptydir)
####################
####################
def chk_empty(emptydir):
	# if the source files did not exist and no files were copied
	# directory can still exist to be populated manually or for future use
	if (len(emptydir) == 0):
		print('Files not found!')
		print('----------')
	else:
		print('----------')
		print('----------')
		print('All files copied.')
		print('----------')
####################

#################### MAIN PROGRAM BELOW ####################
####################
# find a path
src = pathSelect()
# call the menu loop and all functions
while (redo == 'y'):
	print ('----------')
	menu = input('Select files to copy: \n\n\t(1) Python\n\t(2) Bash\n\t(3) PDF\n\t(4) Other \n\n\t(Or any key to Exit) \n\t: ')	
	menu = menu.strip()
	if menu == '1':
		file_xt = 'py'
		copyfiles(file_xt,src)
	elif menu == '2':
		file_xt = 'sh'
		copyfiles(file_xt,src)
	elif menu == '3':
		file_xt = 'pdf'
		copyfiles(file_xt,src)
	# user defined file types i.e. csv, xls(x), doc(x), mp3, etc.
	elif menu == '4':
		file_xt = input('\nEnter file extension: ')
		copyfiles(file_xt,src)
	else:
		print('\n')
		print('----------')
		print('----------')
		print('Exiting...')		
		print('----------')
		exit()
	# repeat menu
	redo = input('Return to Menu? <y>/<n>: ')
	redo = redo.strip()		
	redo = redo.lower()
	print('----------')
# close out
print('\n')
print('----------')
print('----------')
print('Goodbye!')		
print('----------')
exit()
