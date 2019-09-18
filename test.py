from trackGits import *
import os
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
	
	
