*** Settings ***

*** Variables ***

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
