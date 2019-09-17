#!/usr/bin/env python3
import os,pickle
__CONFIG_NAME = "trackGits.conf"
__INSTAWEB_DIR = "git-insta"
__SRC_DIR = os.path.dirname(os.path.abspath(__file__))

def isDir(directory):
	if os.path.isdir(directory): return True
	elif os.path.exists(directory): print("{} is Not Directory".format(directory))
	else: print("{} does not exist".format(directory))
	return False

def isGit(directory):
	gitdir = os.path.join(directory,'.git')
	if os.path.isdir(gitdir):
		return True
	else:
		return False
	
def isInstalled(confPath):
	if os.path.exists(confPath):
		with open(confPath,'rb') as f:
			confs = pickle.load(f)
			instawebDir = confs['instawebDir']
			
		if isDir(instawebDir) and isGit(instawebDir):
			return True
		else: return False
	else: return False
	
def reinstall(instawebDir,conf):
	if not isDir(instawebDir): return False

	with open(conf,'rb') as f:
		confs = pickle.load(f)
		oldInstalwebDir = confs['instawebDir']
	yes = input("{} will be removed. Are you sure to continue? (y/n): ".format(oldInstalwebDir))
	yes = yes.capitalize()
	if yes =="Y":
		os.system('rm -r {}'.format(oldInstalwebDir))
		return install(instawebDir,conf)
	else:
		print("Canceled reinstallation")
		return False
			
def install(instawebDir,conf):
	'''
	install directory to run git-instaweb
	
	instawebDir(str): absolute path of directory
	conf(str): absolute path of conf file of trackGits
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
	if isGit(instawebDir): print("{} git-checked".format(instawebDir))
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
	return True
	
def addDir(dirPath, conf):
	if not isDir(dirPath): return False
	if not isGit(dirPath): return False
	
	#LOAD CONFIGURATIONS
	with open(conf,'rb') as f:
		confs = pickle.load(f)
		instawebDir = confs['instawebDir']
	dst = os.path.join(instawebDir,os.path.basename(dirPath))
	if os.path.islink(dst):
		print("Already added: {} -> {}".format(dirPath,dst))
		return False
	
	os.symlink(dirPath,dst)
	modifyDesc(dirPath)
	
	print("{} -> {}".format(dirPath,dst))
	if os.path.islink(dst):
		print("add success")
		return True
	else:
		print("add Fail")
		return False
	
def modifyDesc(dirPath):
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
			
	
def installView(conf,installer):
	yes = input("Do you want to install 'trackGits'? (y/n): ")
	yes = yes.capitalize()
	if yes == 'Y':
		instawebDir = input('input dir-path to run git-instaweb: ')
		instawebDir = os.path.abspath(os.path.expanduser(instawebDir))
		if installer(instawebDir,conf):
			print("Success to Install\n")
			print("start git-instaweb using below commands")
			print("-"*5)
			print("$ cd {}".format(os.path.join(instawebDir,__INSTAWEB_DIR)))
			print("$ git instaweb --httpd=webrick")
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
	
def main(args,conf):
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
		
def installTest():
	"""
	Test installView with install function
	"""
	
	global __CONFIG_NAME, __SRC_DIR
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	
	if not isInstalled(conf):
		installed = installView(conf,installer=install)
		if not installed: return False
		else: return True
	else:
		return True

def addTest():
	"""
	Test addDir function
	"""
	
	global __CONFIG_NAME, __SRC_DIR
	conf = os.path.join(__SRC_DIR,__CONFIG_NAME)
	
	src = input("dirpath of git project")
	addDir(src,conf)
	
	
#print(installTest())
#print(addTest())

	

