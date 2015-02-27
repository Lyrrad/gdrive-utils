#!/usr/bin/python

# GDrive utils
# Copyright (C) 2015 Darryl Tam

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import argparse
# Requires 7z / 7za
# Part of the p7zip-full package
# Requires pydrive

import os
import sys
import pipes



def removeDirectory (file_path):
	if os.path.isdir(file_path):
		for new_file_path in os.listdir(file_path):
			removeDirectory(file_path+"/"+new_file_path)
		os.rmdir(file_path)
	else:
		os.remove(file_path)


def getFiles (file_path):
	fileList = []
	if os.path.isdir(file_path):
		for root, dirs, files in os.walk(".", topdown=True):
			for name in files:
				print (name)
			for name in dirs:
				print (name)

	else:
		os.remove(file_path)


parser = argparse.ArgumentParser(description='Encrypt and upload file to Google Drive.')
parser.add_argument('file_path', help='path to file to encrypt and upload')
parser.add_argument('-p', '--password', help='password for file (required)', required = True)
parser.add_argument('-f', '--folder', nargs='*', help='ID of destination folder', required = True)
# TODO add options for 7zip
args = parser.parse_args(sys.argv[1:])


cur_dir = os.path.abspath(".")

if len(sys.argv) == 1:
	print 'Need path to upload'
	sys.exit(1)

time_string = datetime.now().strftime("%Y-%m-%d-%H%M%S-%f")
print time_string
file_string = time_string+"-ENCRYPTED.7z"
result = os.system("7z a "+file_string+" " +pipes.quote(args.file_path) + " -p"+ pipes.quote(args.password) + " -mhe=on -mx0")
if result is not 0:
	print "return code: ",result
	sys.exit(1)

folder_string = ""
for folder_name in args.folder:
	folder_string = folder_string + pipes.quote(folder_name) + " "

#print cur_dir+"/upload.py "+file_string + " --folder "+pipes.quote(folder_string)
result = os.system(cur_dir+"/upload.py "+file_string + " --folder "+folder_string)
#print "File uploaded!"


#os.remove(file_string)
#print "File Removed!"

if result is not 0:
	print "return code: ",result
	sys.exit(1)



