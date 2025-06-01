*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR} 	screenshot_folder=${OUTPUT DIR} 	 confidence=0.9
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 	${CURDIR}${/}Images${/}${platform}
# %userprofile%\Desktop
${DESKTOP_DIR} 	%{USERPROFILE}${/}Desktop
# ${ImageTimeout} 	${600}
${ImageTimeout} 	${60}

*** Keywords ***
Install ImageSplitter Windows
	Copy File    ${CURDIR}${/}..${/}dist${/}ImgSplitter.exe    ${DESKTOP_DIR}
	Open Explorer To 	${DESKTOP_DIR}

Run ImageSplitter Windows
	Start Process 	${DESKTOP_DIR}${/}ImgSplitter.exe 	alias=ImageSplitter
	# Sleep    2
	${running}= 	Is Process Running 		ImageSplitter
	Sleep    ${ImageTimeout * 10}
	Take A Screenshot

Open Explorer To
	[Arguments] 	${path} 	${alias}=Explorer
	# https://stackoverflow.com/questions/59521456/how-to-open-finder-with-python-on-mac
	Start Process 	explorer 	${path} 	alias=${alias}
	Wait For 	Explorer Quick Access 	timeout=${ImageTimeout}
	# Sleep    2
	Take A Screenshot

Quit ImageSplitter Windows
	Take A Screenshot
	${running}= 	Is Process Running 		ImageSplitter
	IF 	${running}
		Wait For 	Close Window 	timeout=${ImageTimeout}
		Take A Screenshot
		Click Image 	Close Window
		${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	ELSE
		# ${result}= 	Get Process Result 		ImageSplitter
		${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	END

	Log 	rc: ${result.rc} 		console=True
	Log 	stdout: ${result.stdout} 		console=True
	Log 	stderr: ${result.stderr} 		console=True
	Should Be Empty 	${result.stderr}

#
