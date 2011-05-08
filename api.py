mport os
import sys
import ConfigParser
import shutil
import argparse


def ReadIni(ini_file):
	#Set Config Parser Handle for ini_file
	ini = ConfigParser.ConfigParser()
	ini.read(ini_file)
	return ini

def GetIniParam(ini_file,section):
	#Get ini parameters
	# ini_files is return of ReadIni
	dict1 = {}
	options = ini_file.options(section)

	for option in options:
		try:
			dict1[option] = ini_file.get(section, option)

			if not option in dict1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

def SetIniParam(ini_file,section,option,value):
	open_ini_file = open(ini_file)
	ini = ReadIni(ini_file)
	ini.set(section,option,value)
	ini.write(open_ini_file)
	open_ini_file.close()

def CleanCache():
	print "Cache directory is removing..."
	shutil.rmtree(cache_dir+"/",ignore_errros=False,onerror=None)
	print "Fresh cache directory is creating..."
	os.mkdir(cache_dir)
	print "File permissions are setting..."
	os.fchmod(cache_dir,777)
	print "Cache clean finished..."

def CreateAppCache(app,type):
	
	
	app_full_name = ReadAppFullName(app)
	app_build_dir = cache_dir+"/"+app_full_name+"/build/"
	#check for source directory
	app_src_dir = cache_dir+"/"+app_full_name+"/src/"
	if not os.path.exists(app_src_dir):
		os.makedirs(app_src_dir)

	#check for build directory
	if not os.path.exists(app_build_dir):
		os.makedirs(app_build_dir)

	#download build.ini
	remote_build_ini = repo_url+app_full_name+"/build.ini"
	local_build_ini = app_build_dir+"build.ini"
	wget = "wget -O "+local_build_ini+" "+remote_build_ini
	os.system(wget)
	if not os.path.exists(local_build_ini):
		print "Build file can not download.. Please try again."
		exit(1)

	#download source file
	read_local_build_ini = ReadIni(local_build_ini)
	source_url = GetIniParam(read_local_build_ini,"info")["url"]
	source_file = GetIniParam(read_local_build_ini,"info")["file"]
	wget = "wget -O "+app_src_dir+source_file+" "+source_url
	os.system(wget)
	if not os.path.exists(app_src_dir+source_file):
		print "Source file can not download.. Please try again."
		exit(1)



def ReadAppFullName(app):
	#Read application name with version number
	app_dict = GetIniParam(repo_cache,"packages")
	if app in app_dict:
		app_full_name = app_dict[app]
		return app_full_name
	else:
		print str(app) + " cant find in repositories...."
		exit(1)



def MakeList(string,sperator):
	#make list from string by sperator
	new_list = string.strip(sperator)
	return new_list


def IsInstall(app,ini_file):
	#Installed.ini den bak
	version = GetIniParam(ini_file,"core")[app]
	if version != "":
		return 1
	else:
		return 0


def Dependency(app):
	#return dependency tree

	app_full_name = ReadAppFullName(app)
	build_ini_file = cache_dir+"/"+app_full_name+"/build/build.ini"
	if not os.path.exists(build_ini_file):
		get_app = download(app)
	build = ReadIni(build_ini_file)
	read_dep = GetIniParam(build,"info")["Dependencies"]
	dep_list = MakeList(read_dep,",")
	for dep in dep_list:
		print dep

def install(app):

	CreateAppCache(app)
	app_full_name = ReadAppFullName(app)
	app_build_file = cache_dir+"/"+app_full_name+"/build/build.ini"
	app_src_file = cache_dir+"/"+app_full_name+"/src/"
	
	#filename = GetIniParam(build_ini,"info")["file"]
	build = GetIniParam(build_ini,"build")

	os.chdir(app_src_file)
	print app+" is installing...\n"
	os.chdir(app_full_name)
	os.system(build["install"])
	print "Every thing seems ok."

def remove(app):
	
	app_build_file = cache_dir+"/"+app_full_name+"/build/build.ini"
	
	if not os.path.exists(app_buil_file):
		CreateAppCache(app)
	
	build_ini = ReadIni(app_build_file)
	build = GetIniParam(build_ini,"build")
	print app+" is removing...\n"
	os.system(build["remove"])
	print "Every thing seems ok."


conf_ini = "/etc/api.ini"
config = ReadIni(conf_ini)
cache_dir = GetIniParam(config,"base")["cachedir"]
repo_url = GetIniParam(config,"repos")["core"]
pid_file = GetIniParam(config,"base")["pidfile"]




#repo_cache is  repocache.ini
repo_cache = ReadIni(GetIniParam(config,"base")["repocache"])

arguments = sys.argv

command = arguments[1]

parser = argparse.ArgumentParser()
parser.add_argument("--install",type=install,nargs=+)
parser.add_argument("--remove",type=remove,nargs=+)
parser.parse_args()

