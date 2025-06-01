*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR}
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 	${CURDIR}${/}Images${/}${platform}

# %userprofile%\Desktop
${DESKTOP_DIR} 	%{USERPROFILE}${/}Desktop

*** Keywords ***
Install ImageSplitter Windows
	Copy File    ${CURDIR}${/}..${/}dist${/}ImgSplitter.exe    ${DESKTOP_DIR}
	Take A Screenshot

Run ImageSplitter Windows
	Start Process 	${DESKTOP_DIR}${/}ImgSplitter.exe 	alias=ImageSplitter
	Take A Screenshot
