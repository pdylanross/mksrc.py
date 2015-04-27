#!/usr/bin/env python
import os, sys, json,mksrc_core
from mksrc_core import *
from subprocess import call

#Globals
CurrentDir = os.getcwd()
ScriptDir = os.path.dirname(os.path.realpath(__file__))
TemplateDir = os.path.join(ScriptDir,"templates")
ConfigFilename = os.path.join(ScriptDir,"mksrc.conf")

DefaultTemplate = "BaseTemplate"

if os.path.isfile(ConfigFilename): #Load conf
	try:
		Config = LoadJsonFromFile(ConfigFilename)
	except ValueError as e:
		FatalError("Error loading configuration: " + str(e))
else: #Create default conf & save it
	Config = {"UProjectFile":"","UEVersionSelector":"","ProjectPCH":"","UseColors":True}
	try:
		SaveJsonToFile(ConfigFilename,Config)
	except IOError as e:
		FatalError("Error saving default configuration: " + str(e))

if not Config["UseColors"]:
	mksrc_core.WithColors=False

DEBUG = False

#Checks for instafail
if not os.path.exists(TemplateDir):
	FatalError("No template directory exists. Make some templates!")

#usage
if "-h" in sys.argv or "-help" in sys.argv or len(sys.argv)==1:
	
	print "\nmksrc.py"
	print "Made by P. Dylan Ross"
	print "Feel free to do whatever you want with this."
	print "I'm not responsible for anything that goes wrong."

	print "\nUsage:\n"

	print "\tmksrc.py File-Template,File2-Template2...\n"

	print "\t-h,-help\t\tHow you got here."
	print "\t-debug\t\t\tShow some debug info."
	print "\t-g,-generate\t\tGenerates project files. Need to set up config first."
	print "\t-sp,-set-project\tSets the current project to the project in this directory"
	exit()

#debug mode
if "-debug" in sys.argv:
	DEBUG = True

if DEBUG:
	print "Python version: ",sys.version
	print "Current: ",CurrentDir
	print "Scripts: ",ScriptDir
	print "Templates: ",TemplateDir
	print ""
	print "argc: ",len(sys.argv)
	print "Args: ", str(sys.argv)
	print ""

#set-project
#Config = {"UProjectFile":"","UEVersionSelector":"","ProjectPCH":""}
if "-sp" in sys.argv or "-set-project" in sys.argv:
	FoundUProject = False
	for File in os.listdir(CurrentDir):
		if File.endswith(".uproject"):
			FoundUProject = File
			break
	if not FoundUProject:
		FatalError("There are no .uproject files in this directory")
	ProjectName = FoundUProject.replace(".uproject","")
	Config["ProjectPCH"] = ProjectName + ".h"
	Config["UProjectFile"] = os.path.join(CurrentDir,FoundUProject)
	SaveJsonToFile(ConfigFilename,Config)

	GoodOutput("Setting the current project to "+ProjectName)
	GoodOutput("\tProjectPCH: " + Config["ProjectPCH"])
	GoodOutput("\tUProjectFile: " + Config["UProjectFile"])
	exit() #dont let people make files in their base project dir, that'd be silly. 


#copy to local var cause I dont want to pop stuff off the main one
Args = sys.argv
Args.pop(0) #remove the script arg

FilesToGenerate = {}

#parse out what files with what templates we're making today
for Arg in Args:
	if Arg.startswith("-"): #ignore switches
		continue
	if "-" in Arg:
		for ScriptToGenerate in Arg.split(","):
			SplitScript = ScriptToGenerate.split("-")
			try:
				FilesToGenerate[SplitScript[0]] = SplitScript[1]
			except IndexError:
				FilesToGenerate[SplitScript[0]] = DefaultTemplate
	else:
		FilesToGenerate[Arg] = DefaultTemplate

#create the files
LoadedTemplates = {}
for Filename,Template in FilesToGenerate.iteritems():
	if Template not in LoadedTemplates: #load template if need be
		try:
			NewTemplate = SourceTemplate(os.path.join(TemplateDir,Template + ".tmpl"))
			LoadedTemplates[Template] = NewTemplate
		except IOError: #couldn't open file
			Nag("No template \"" + Template + "\"")
			Nag("Skipping " + Filename)
			LoadedTemplates[Template] = False
			continue
		except ParseError: #regex didnt match __filetype__
			Nag(Template + " failed to parse correctly. Ensure the template has __filetype__ for each section")
			Nag("Skipping " + Filename)
			LoadedTemplates[Template] = False
			continue
		else:
			GoodOutput("Loaded template " + Template)
	
	if not LoadedTemplates[Template]:
		Nag("Skipping " + Filename)
		continue

	#set up replacements & generate file text
	Replacements = {
		"Filename" : Filename, 
		"PCH": Config["ProjectPCH"]
	}

	CreatedFiles = LoadedTemplates[Template].ApplyFormatting(Replacements)

	ShouldSkip = False

	for Filetype in CreatedFiles:
		FilePath = os.path.join(CurrentDir,Filename+"."+Filetype)
		if os.path.isfile(FilePath):
			ShouldSkip = True
			break

	if ShouldSkip:
		Nag("Skipping " + Filename + " because that file already exists")
		continue

	#save the files
	for Filetype,FileContents in CreatedFiles.iteritems():
		try:
			

			with open(os.path.join(CurrentDir,Filename+"."+Filetype),"w+") as File:
				File.write(FileContents)
				GoodOutput("Created " + Filename + "." + Filetype)
		except IOError as e:
			Nag("Error creating " + Filename + "." + Filetype+" :"+str(e))

#generate project files
if "-g" in sys.argv or "-generate" in sys.argv:
	
	if Config["UProjectFile"] == "":
		Nag("Can not generate project files without knowing where the .uproject is. Please navigate to your project folder and run `mksrc.py -sp`")
	elif Config["UEVersionSelector"] == "":
		Nag("Can not generate project files without knowing where the UEVersionSelector is.")
	else:
		GoodOutput("Generating Unreal VS Project")
		Command = [Config["UEVersionSelector"],"-projectfiles",Config["UProjectFile"]]
		call(Command)




