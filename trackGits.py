#!/usr/bin/env python3

# Autohr: Jaeyeon park
# Created: 2019-09-18
# Updated: 2019-09-18
# Note: Executable python code to add git-repo directory into the directory running git-instaweb
#		Installer built in

import os,pickle
__CONFIG_NAME = "trackGits.conf"
__INSTAWEB_DIR = "git-insta"
__SRC_DIR = os.path.dirname(os.path.abspath(__file__))
__ALIAS = 'trackgit'

def isDir(directory):
	if os.path.isdir(directory): return True
	elif os.path.exists(directory): print("{} is Not Directory".format(directory))
	else: print("{} does not exist".format(directory))
	return False

def isGit(directory):
	gitdir = os.path.join(directory,'.git')
	if os.path.isdir(gitdir): return True
	else:return False
	
	
############# FOR INSTALLER #############

def isInstalled(confPath):
	if os.path.exists(confPath):
		with open(confPath,'rb') as f:
			confs = pickle.load(f)
			instawebDir = confs['instawebDir']
			
		if isDir(instawebDir) and isGit(instawebDir): return True
		else: return False
	else: return False
	
def reinstall(instawebDir,conf):
	"""
	reinstall(instawebDir:str,conf:str) -> return True/False (success or failure)
	
	Remove old instawebDir and Initialize the given instawebDir to run git-instaweb
	Recreated configuration file
	
	instawebDir(str): absolute path of directory where to make 'git-insta' dir again
	conf(str): absolute path of trakGits.conf file
	"""
	
	if not isDir(instawebDir): return False #check if it is dir or  not

	with open(conf,'rb') as f: #load old configuration file
		confs = pickle.load(f)
		oldInstawebDir = confs['instawebDir']
	yes = input("{} will be removed. Are you sure to continue? (y/n): ".format(oldInstawebDir)).capitalize()
	if yes =="Y":
		#remove oldInstawebDir
		#then reinitialize instawebDir for git-instaweb and recreate conf file
		os.system('rm -r {}'.format(oldInstawebDir))
		return install(instawebDir,conf) #return success or failure from installation
	else:
		print("Canceled reinstallation")
		return False #return failure of reinstallation
			
def install(instawebDir,conf):
	'''
	install(instawebDir:str,conf:str) -> return True/False (success or failure)
	
	Initialize the given instawebDir(directory) to run git-instaweb
	Create configuration file
	
	instawebDir(str): absolute path of directory where to make 'git-insta' dir 
	conf(str): absolute path of trackGits.conf file
	'''
	
	#set the absolute path of conf
	if not isDir(instawebDir): return False
	
	#initialize and check instawebDir 
	instawebDir = os.path.join(instawebDir,__INSTAWEB_DIR)	
	if not os.path.exists(instawebDir):
		os.mkdir(instawebDir)
		print("Created: {}".format(instawebDir))
	else:
		print("Already Created: {}".format(instawebDir))
		
	#git-initialize and check instawebDir
	if isGit(instawebDir): 
		print("{} git-checked".format(instawebDir))
	else:
		os.system('git init {}'.format(instawebDir))
		print("git initialized: {}".format(instawebDir))
	print("ready for git-instaweb")
	
	#update conf
	if os.path.exists(conf): os.remove(conf)
		
	#SAVE CONFIGURATIONS
	with open(conf,'wb') as f:
		confs = {}
		confs['instawebDir'] = instawebDir
		pickle.dump(confs,f)
		print("generate: {}".format(conf))
		
	#REGISETER ALIAS IN RC-FILE
	rcfiles = set(['.bashrc','.zshrc'])
	homedir = os.path.expanduser('~/')
	rcfile = [ os.path.join(homedir,f) for f in os.listdir(homedir) if f in rcfiles ]
	for f in rcfile:
		with open(f,'a') as f:
			f.write('alias {}="{}"\n'.format(__ALIAS, os.path.abspath(__file__)))
		
	print("\nRun below commands")
	print("-"*5)
	for f in rcfile:
		print("$source {}".format(f))
	print("-"*5)
		
	return True


def installView(conf,installer):
	"""
	installView(conf:str, installer:func) -> return True/False (success or failure from installer)
	
	Interact with user to install or to reinstall trackGits
	installer shoulc be specified between 'install' function or 'reinstall' function
	
	conf(str): absolute path of trackGits.conf file
	installer(func): installer function. 'install' or 'reinstall'
	"""
	
	yes = input("Do you want to install 'trackGits'? (y/n): ").capitalize()
	if yes == 'Y':
		instawebDir = input('input dir-path to run git-instaweb: ')
		instawebDir = os.path.abspath(os.path.expanduser(instawebDir))
		if installer(instawebDir,conf):
			print("\nStart git-instaweb using below commands")
			print("-"*5)
			print("$ cd {}".format(os.path.join(instawebDir,__INSTAWEB_DIR)))
			print("$ git instaweb --httpd=webrick")
			print("-"*5)
			print("Success to install")
			return True
		else:
			print("Fail to Install")
			return False
	elif yes == 'N':
		print('Canceled installation')
		return False
	else:
		print("Wrong user input. not (y/n)")
		return False
	


############# FOR ADDDIR #############
	
def addDir(dirPath, conf):
	"""
	addDir(dirPath:str,conf:str) -> return True/False (success or failure to add dir into instawebDir)
	
	Add the given directory path(dirPath) into the instawebDir defined in conf file by symbol-linking it
	
	dirPath(str): absolute path of directory to add into the instawebDir
	conf(str): absolute paht of trackGits.conf file	
	"""
	
	#check whether the given dir is git project or not
	if not isDir(dirPath):
		print("Not dir: {}".format(dirPath))
		return False
	if not isGit(dirPath):
		print("Not git-repo: {}".format(dirPath))
		return False
	#continue if is directory and git project
	
	#LOAD CONFIGURATIONS
	with open(conf,'rb') as f:
		confs = pickle.load(f)
		instawebDir = confs['instawebDir']
	
	dst = os.path.join(instawebDir,os.path.basename(dirPath))
	#check whether dirPath was already added
	if os.path.islink(dst):
		print("Already added: {} -> {}".format(dirPath,dst))
		return False
	
	#link dirPath to dst by soft-link
	os.symlink(dirPath,dst)
	modifyDesc(dirPath)
	
	print("{} -> {}".format(dirPath,dst))
	if os.path.islink(dst): #link file is created successfully
		print("add success")
		return True
	else:
		print("add Fail")
		return False
	
def modifyDesc(dirPath):
	"""
	modifyDesc(dirPath:str) -> return None
	
	Modify description of the given git-project dir(dirPath)
	It will help user to know easily what projects are for in git-instaweb
	
	dirPath(str): absolute path of git-project directory. it should include '.git' directory
	"""
	
	desc = os.path.join(dirPath,'.git/description')
	with open(desc) as f:
		print("Current Desciription for {}".format(dirPath))
		print(" : {}\n".format(f.read()))
	yes = input("Are you modify description? (y/n): ")
	yes = yes.capitalize()
	if yes == "Y":
		contents = input("Description for {}\n : ".format(dirPath))
		with open(desc,'w') as f:
			f.write(contents)
			

def main(args,conf):
	"""
	main(args,conf) -> return True/False (success or failure)
	
	Run in __main__ propery depending on args
	
	args(argparse.Namespace): parsed arguments by parser.parse_args() (dir,reinstall,instawebDir)
	conf(str): absolute path of trackGits.conf
	"""
	if args.instawebDir:
		with open(conf,'rb') as f:
			confs = pickle.load(f)
		print("{}".format(confs['instawebDir']))
		return True	
	
	if args.reinstall:
		installed = installView(conf,installer=reinstall)
		if not installed: return False
		else: return True
	if args.dir == "" : dirPath = os.curdir
	else: dirPath = args.dir
	dirPath = os.path.abspath(dirPath)
	
	if not isInstalled(conf):
		installed = installView(conf,installer=install)
		if not installed: return False
		else: return True
	else:
		added = addDir(dirPath,conf)
		return added

if __name__ == "__main__":
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--dir',help="Directory path of git-project you want to add to git-instaweb. The default is current directory",default="")
	parser.add_argument('--reinstall',help="Reinstall dir for git-instaweb",action="store_true",default=False)
	parser.add_argument('-i','--instawebDir',help="show current Instaweb directory",action='store_true',default=False)
	args = parser.parse_args()
	main(args,conf)

	

