#mksrc.py

mksrc.py is a template based file generator that's geared towards Unreal 4, but it's not strictly limited to being used for that. 

###Usage

mksrc.py should be called with a list of files that you want to generate along with the templates you want to apply to them. The syntax is Filename-Template. You can separate multiple files with commas or spaces. If no template is specified, mksrc will use the default template. The provided one contains a header and cpp file that include the .generated.h file in the header, and the project PCH & header in the cpp file. 

```sh 
mksrc.py AFileUsingTheDefaultTemplate,AUObject-UObject AUStruct-UStruct,AUEnum-UEnum
```