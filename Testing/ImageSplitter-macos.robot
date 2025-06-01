*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR} 	screenshot_folder=${OUTPUT DIR}
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 		${CURDIR}${/}Images${/}${platform}
${PROJECT_DIR} 		${CURDIR}${/}..
${ImageTimeout} 	${600}

*** Keywords ***
Install ImageSplitter MacOS
	Open Finder To 		${PROJECT_DIR}

	Mount ImageSplitter Image

	Sleep    2
	Take A Screenshot
	Fail    Install ImageSplitter MacOS Not Completed

Run ImageSplitter MacOS
	Fail    Run ImageSplitter MacOS Not Implimented


Open Finder To
	[Arguments] 	${path} 	${alias}=Finder
	# https://stackoverflow.com/questions/59521456/how-to-open-finder-with-python-on-mac
	Start Process 	open 	${path} 	alias=${alias}
	Wait For 	Finder Favorites 	timeout=${ImageTimeout}
	# Sleep    2
	Take A Screenshot

Get ImageSplitter Image Path
	@{files}= 	List Files In Directory 	${PROJECT_DIR} 	*.dmg 		absolute
	Log 	Files: ${files} 		console=True
	# Should Be True 		${files}
	Should Be True 		${files} 	msg=no dmg files found in ${PROJECT_DIR}
	RETURN 		${files}[0]

Mount ImageSplitter Image

	${dmg file}= 	Get ImageSplitter Image Path
	Start Process 	open 	${dmg file} 	alias=dmg

	Sleep    2
	Take A Screenshot
	Fail    Mount ImageSplitter Image Not Completed
