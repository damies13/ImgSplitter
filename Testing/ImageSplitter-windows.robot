*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR} 	screenshot_folder=${OUTPUT DIR}
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 	${CURDIR}${/}Images${/}${platform}
# %userprofile%\Desktop
${DESKTOP_DIR} 	%{USERPROFILE}${/}Desktop
${ImageTimeout} 	${600}

*** Keywords ***
Install ImageSplitter Windows
	Copy File    ${CURDIR}${/}..${/}dist${/}ImgSplitter.exe    ${DESKTOP_DIR}
	Open Explorer To 	${DESKTOP_DIR}

Run ImageSplitter Windows
	Start Process 	${DESKTOP_DIR}${/}ImgSplitter.exe 	alias=ImageSplitter
	# Sleep    2
	${running}= 	Is Process Running 		ImageSplitter
	Sleep    ${ImageTimeout}
	${running}= 	Is Process Running 		ImageSplitter
	Take A Screenshot

Open Explorer To
	[Arguments] 	${path} 	${alias}=Explorer
	# https://stackoverflow.com/questions/59521456/how-to-open-finder-with-python-on-mac
	Start Process 	explorer 	${path} 	alias=${alias}
	Wait For 	Explorer Quick Access 	timeout=${ImageTimeout}
	# Sleep    2
	Take A Screenshot
