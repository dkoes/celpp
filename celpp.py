#!/usr/bin/env python

from FileTransfer import FtpFileTransfer
import os
import shutil

class _main_():
	
	
	def fetchData():
		 
		wd = str(os.getcwd())
		
		print('All Files will go into the celpp folder')
			
		cred = (wd + '/credentials.txt')
		try: #attempts to connect to file required to connect to ftp
			print('Trying to open credentials.txt')
			fo = open(cred, 'r')
			fo.close()
		except: #writes file required to connect to ftp if not already made
			print('Writing credentials.txt file')
			fo = open(cred, 'w')
			fo.write('host ftp.box.com\nuser nlr23@pitt.edu\npass h@il2pitt1\npath\ncontestantid 33824\nchallengepath /challengedata\nsubmissionpath /33824')
			fo.close()
		
		if(os.path.isdir(wd + '/challengedata')==False):#creates challengedata folder if it doesn't exist
			os.mkdir(wd + '/challengedata')
			os.chdir(wd + '/challengedata')
		else: #changes to challengedata folder if it exists
			os.chdir(wd + '/challengedata')
			
			
		ftp = FtpFileTransfer(cred)
		print('Connecting to ftp.box.com')
		ftp.connect() 
		print('Connected to ftp')
		
		ftp_files = ftp.list_files('challengedata')#creates list of files from box
		count = 0 #keep track number of files added to local folder
		for x in (ftp_files):
			split = os.path.splitext(x)
			dir = os.path.splitext(split[0])
			if(str(split[1]) == '.gz'):
				if os.path.isfile(x) == True:#if it finds the zip file in local folder, unzips and deletes zippped file
					print('Unzipping folder ' + str(dir[0]))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
				elif os.path.isdir(str(dir[0])) == True:#if it finds the unzipped directory in local folders
					pass
				else: #if it can't find the week in any format; downloads, unzips, and removes zipped file
					ftp.download_file('challengedata/'+ x,  wd + '/challengedata/' + x)
					print('Unzipping folder ' + str(dir[0]))
					os.system('tar -xzf ' + x)
					print('Deleting zip file: ' + x)
					os.system('rm ' + x)
					count = count + 1
					print(str(dir[0]) + ' was just added to the challengedata folder')
			else:
				ftp.download_file('challengedata/'+ x,  wd + '/challengedata/' + x)
		print('challengedata has been updated. ' + str(count) + ' week(s) was/were just added.')		
		print('Disconnecting from ftp')
		ftp.disconnect()
	
	def	align():
		wd = str(os.getcwd())
		ans = wd +'/answers'
		if os.path.isdir(ans)==False: #if the answers directory isnt formed make it
			os.mkdir(wd+'/answers')
		
		data = os.listdir(wd)
		for x in (data):#for each weeks data
			if x=="readme.txt" or x=="latest.txt" or x=="answers" : 
				pass
			else:
				toDir = wd +'/answers/' + x
				if os.path.isdir(toDir)==False: #if the path to answers dir doesnt exist 
					os.mkdir(toDir) #make directory
					#docking code here
					#get our results, output as file and zip
					#shutil.make_archive(name,'zip', toDir)
					
				else:
					filename = toDir + ".zip"
					if os.path.isfile(filename): #if the zipped answers already exist, skip
						pass
					#else: 
						#if the path exists, but there are no answers run docking
						#docking code here
						#get our results, output as file and zip
						#shutil.make_archive(name,'zip', toDir)
				
				
		
		
	def uploadData():#uploads zip files containing docking predictions to contestant folder specified in credentials.txt
		print('Uploading files to box contestant folder')
		cred = wd + '/credentials.txt'
		ftp = FtpFileTransfer(cred)
		print('Connecting to ftp.box.com')
		ftp.connect() 
		print('Connected to ftp')
		ftp_files = ftp.list_files(ftp.get_contestant_id())#creates list of files from box
		d = []
		for(_, dirnames, _) in os.walk(wd + '/protocols'):
			d.extend(dirnames)
			break
		for dir in (d):#NOT A FAN OF THE NESTED FOR LOOPS, WILL TRY TO FIND BETTER WAY TO IMPLEMENT THIS
			for(_,_,filenames) in os.walk(wd + '/protocols/' + dir):
				f = []
				f.extend(filenames)
				print('Uploading files for ' + dir)
				for x in (f): 
					if((x in ftp_files) == False):
						file = wd + '/protocols/' + dir + '/' + x
						remote_dir = ftp.get_remote_submission_dir()
						remote_file_name = os.path.basename(file)
						ftp.upload_file_direct(file, remote_dir, remote_file_name)
					else:
						pass	
		print('All the files have been uploaded. Disconnecting from ftp')
		ftp.disconnect()
	
		
	
	fetchData()
	align()
	#uploadData()


