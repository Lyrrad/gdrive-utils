#!/usr/bin/python


# pip install PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import socket
import logging
import httplib2
import os
from mimetypes import guess_type

# sudo pip install --upgrade google-api-python-client
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

import argparse



gauth = GoogleAuth()
gauth.LoadCredentials()
if gauth.credentials is None:
	gauth.CommandLineAuth()
elif gauth.access_token_expired:
	gauth.Refresh()
else:
	gauth.Authorize()



drive = GoogleDrive(gauth)

parser = argparse.ArgumentParser(description='Upload a file to Google Drive.')
parser.add_argument('file_path', nargs='+', help='path to file(s) to upload')
parser.add_argument('-f', '--folder', nargs='*', help='ID of destination folder')
args = parser.parse_args(sys.argv[1:])


def uploadFile(cur_file_path, drive_service, folder):
	try:
		with open(cur_file_path) as f: pass
	except IOError as e:
		print(e)
		sys.exit(1)	
	print "Uploading " + cur_file_path


	file_name = cur_file_path.split('/')[-1]
	mime_type = guess_type(cur_file_path)[0]
	mime_type = mime_type if mime_type else 'text/plain'
	media_body = MediaFileUpload(cur_file_path, mimetype=mime_type, resumable=True)
	parents = []
	if folder is not None:
		for cur_folder in folder:
			parents.append({"id": cur_folder})
	body = {
	  'title': file_name,
	  'description': 'Test Backup',
	  'mimeType': 'mime_type',
	  'parents' : parents,
	}

	try: 
		file = drive_service.files().insert(body=body, media_body=media_body).execute()
		#print 'File ID: %s' % file['id']
		#print 'Download Link: %s' % file['webContentLink']
		print "Upload complete"
		return file
	except errors.HttpError, error:
		print 'An error occured: %s' % error
		return None


	

for cur_file in args.file_path:
	if os.path.isdir(cur_file):
		print "Directory given:",cur_file
		print "Should provide filename instead"
		sys.exit(1)
	uploadFile(cur_file, gauth.service, args.folder)



