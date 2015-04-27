import re, json

##Colors & Formatting
class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def PrintColored(color,str):
	print color + str + colors.RESET

def FatalError(str):
	PrintColored(colors.RED,str)
	exit()

def Nag(str):
	PrintColored(colors.YELLOW, str)

def GoodOutput(str):
	PrintColored(colors.GREEN,str)

#templates
class ParseError:
	def __init__(self):
		pass

class SourceTemplate:

	def __init__(self,filename):
		self.Sections = {}
		with open(filename) as File:
			self.ParseTemplate(File.read())


	def ParseTemplate(self, FileContents):
		
		for Section in FileContents.split("!!!"):
			Section = Section.strip()
			if Section == "": #split before the first !!!
				continue
			SectionName = re.match("(__)(.+)(__)",Section)
			if not SectionName: #regex didn't match a filename
				raise ParseError()
			SectionFileType = SectionName.groups()[1]

			SectionText = Section[:SectionName.start()] + Section[SectionName.end():]
			SectionText = SectionText.strip() #strip once more for good measure
			self.Sections[SectionFileType] = SectionText



	def ApplyFormatting(self,Replacements):
		RetVal = {}
		for FileExt,SectionText in self.Sections.iteritems():
			CurrentSectionText = SectionText
			for ReplaceSearch,ReplaceValue in Replacements.iteritems():
				CurrentSectionText=CurrentSectionText.replace("{{" + ReplaceSearch + "}}",ReplaceValue)
			RetVal[FileExt] = CurrentSectionText
		return RetVal

#json helpers
def LoadJsonFromFile(Location):
	ret = False
	with open(Location,"r") as JsonFile:
		ret = json.loads(JsonFile.read().replace("\\","\\\\")) #damn unicode escape characters
	return ret

def SaveJsonToFile(Location,obj):
	with open(Location,"w+") as JsonFile:
		SaveString = json.dumps(obj,sort_keys=True,indent=4,separators=(',', ': '))
		SaveString = SaveString.replace("\\\\","\\")
		JsonFile.write(SaveString)

