#mksrc.py

mksrc.py is a template based file generator that's geared towards Unreal 4, but it's not strictly limited to being used for that. 

###Usage

mksrc.py should be called with a list of files that you want to generate along with the templates you want to apply to them. The syntax is Filename-Template. You can separate multiple files with commas or spaces. If no template is specified, mksrc will use the default template. The provided one contains a header and cpp file that include the .generated.h file in the header, and the project PCH & header in the cpp file. 

```sh 
mksrc.py AFileUsingTheDefaultTemplate AUObject-UObject,AUStruct-UStruct
```

To generate the Unreal VS project after you make the files, call it with -g or -generate. You can also call mksrc.py with just -g to generate project files.

```sh
mksrc.py LetsGetThisPuppyInVs -g
```

Since mksrc depends on knowing where your project is to generate the VS files, you need to set this up to use this feature. Fortunately, this is easy to do with the -sp switch. Just navigate to the folder that your .uproject is and run mksrc.py -sp. This is also useful to change projects if you are working on multiple. 
##Setup

- Get the files
- Edit mksrc.conf and set UEVersionSelector to point towards your version selector. For Launcher installed versions this is in %path-to-unreal%/Launcher/Engine/Binaries/Win64/UnrealVersionSelector.exe. For source built versions it's %path-to-unreal%/Engine/Binaries/Win64/UnrealVersionSelector.exe. Make sure to include the exe in the path. 
- Navigate to your root project folder (wherever your .uproject is) in your command line environment of choice and run mksrc.py -sp.
- If, for some reason, your project PCH isn't named the same thing as your project, then you'll need to change that in mksrc.conf. Keep in mind that running mksrc.py -sp will overwrite that change. 

##Templates

The templates that mksrc uses are located in the templates directory that lives wherever mksrc.py is. It's fairly trivial to make new templates.

All templates use the .tmpl extension, and they are referenced by their filename minus the extension. They are divided into sections and each section will generate another file when you use that template. The syntax for sections is pretty straightforward. 

```
!!!__FileExtension__
```

The extension is without the dot. For example, a section for a c++ header file will look like this:

```
!!!__h__
```

The syntax for fields that will be replaced is {{Name}}. As of right now, mksrc will replace {{Filename}} and {{PCH}}. This can easily be extended by adding more fields into the Replacements var that's about 130 lines into mksrc.py. You can look at the provided templates to get a better idea of how they're put together. Just as a quick example though, here's the AActor template:

```cpp
!!!__h__
/*
	Generated with mksrc.py
*/
#pragma once

#include "GameFramework/Actor.h"
#include "{{Filename}}.generated.h"

UCLASS(BlueprintType)
class A{{Filename}} : public AActor
{
	GENERATED_BODY()
public:
	A{{Filename}}(const FObjectInitializer& ObjectInitializer);
};

!!!__cpp__
#include "{{PCH}}"
#include "{{Filename}}.h"

A{{Filename}}::A{{Filename}}(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer)
{
	
}
```

##About

mksrc.py was a weekend project that I used to learn python. Any advice or critique is much appreciated. I don't really plan on spending a whole lot more time on this other than fixing bugs and making templates. 
