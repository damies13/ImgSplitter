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
	${vars}= 	Get Variables
	Log    ${vars}
	Log 	Install ImageSplitter Windows 	console=True
	Copy File    ${CURDIR}${/}..${/}dist${/}ImgSplitter.exe    ${DESKTOP_DIR}
	Open Explorer To 	${DESKTOP_DIR}

Run ImageSplitter Windows
	${vars}= 	Get Variables
	Log    ${vars}
	Log 	Run ImageSplitter Windows 	console=True
	Start Process 	${DESKTOP_DIR}${/}ImgSplitter.exe 	alias=ImageSplitter
	# Sleep    2
	${running}= 	Is Process Running 		ImageSplitter

	FOR 	${i} 	IN RANGE 	10
		Sleep    ${ImageTimeout / 2}
		Take A Screenshot
	END

Open Explorer To
	[Arguments] 	${path} 	${alias}=Explorer

	Log 	Open Explorer To ${path} 	console=True

	# https://stackoverflow.com/questions/59521456/how-to-open-finder-with-python-on-mac
	Start Process 	explorer 	${path} 	alias=${alias}
	Wait For 	Explorer Quick Access 	timeout=${ImageTimeout}
	# Sleep    2
	Take A Screenshot

Quit ImageSplitter Windows
	Take A Screenshot

	Log 	Quit ImageSplitter Windows 	console=True

	${running}= 	Is Process Running 		ImageSplitter
	Log 	Quit ImageSplitter - running: ${running} 	console=True
	IF 	${running}
		Log 	Wait For Close Window 	console=True
		Wait For 	Close Window 	timeout=${ImageTimeout}
		Take A Screenshot
		Log 	Click Close Window 	console=True
		Click Image 	Close Window
		# ${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	# 	${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout}
	# ELSE
	# 	# ${result}= 	Get Process Result 		ImageSplitter
	# 	# ${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	# 	${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout}
	END

	Log 	Last Take A Screenshot 	console=True
	Take A Screenshot
	# Log 	rc: ${result.rc} 		console=True
	# Log 	stdout: ${result.stdout} 		console=True
	# Log 	stderr: ${result.stderr} 		console=True
	# Should Be Empty 	${result.stderr}

#
