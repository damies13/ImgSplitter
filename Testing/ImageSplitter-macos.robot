*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR}
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 	${CURDIR}${/}Images${/}${platform}


*** Keywords ***
Install ImageSplitter MacOS
	Open Finder To 		${CURDIR}${/}..

	Mount ImageSplitter Image

	Take A Screenshot
	Fail    Install ImageSplitter MacOS Not Completed

Run ImageSplitter MacOS
	Fail    Run ImageSplitter MacOS Not Implimented


Open Finder To
	[Arguments] 	${path} 	${alias}=Finder
	# https://stackoverflow.com/questions/59521456/how-to-open-finder-with-python-on-mac
	Start Process 	open 	${path} 	alias=${alias}

Mount ImageSplitter Image
	
	Take A Screenshot
	Fail    Install ImageSplitter MacOS Not Completed
