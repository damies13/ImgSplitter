*** Settings ***
Library 	ImageHorizonLibrary 	reference_folder=${IMAGE_DIR} 	screenshot_folder=${OUTPUT DIR} 	 confidence=0.9
Library 	OperatingSystem
Library 	Process

*** Variables ***
${IMAGE_DIR} 		${CURDIR}${/}Images${/}${platform}
${PROJECT_DIR} 		${CURDIR}${/}..
# ${ImageTimeout} 	${600}
${ImageTimeout} 	${60}

${APPS_DIR} 		/Applications
${SRCE_APP_DIR} 	/Volumes/ImgSplitter/ImgSplitter.app
${DEST_APP_DIR} 	${APPS_DIR}/ImgSplitter.app


*** Keywords ***
Install ImageSplitter MacOS
	Open Finder To 		${PROJECT_DIR}

	Mount ImageSplitter Image

	Copy Directory 		${SRCE_APP_DIR} 	${APPS_DIR}
	Directory Should Exist 		${DEST_APP_DIR}

	MacOS Security Authorise App 	${DEST_APP_DIR}
	# Sleep    2
	# Take A Screenshot
	# Fail    Install ImageSplitter MacOS Not Completed

Run ImageSplitter MacOS
	# Fail    Run ImageSplitter MacOS Not Implimented
	Start Process 	open 	${DEST_APP_DIR} 	alias=ImageSplitter
	# Wait For 	ImgSplitter App 	timeout=${ImageTimeout}
	# ${location}= 	Locate 	ImgSplitter App
	# Move To 	${location}
	# Double Click

	FOR 	${i} 	IN RANGE 	20
		Sleep    ${ImageTimeout / 2}
		Take A Screenshot
	END

MacOS Security Authorise App
	[Arguments] 	${app_path}
	# https://github.com/archimatetool/archi/issues/555
	# xattr -r -d com.apple.quarantine /path/to/ImgSplitter.app
	${result}= 	Run Process 	xattr 	${path} 	-r 	-d 	com.apple.quarantine 	${app_path}
	Log 	rc: ${result.rc} 		console=True
	Log 	stdout: ${result.stdout} 		console=True
	Log 	stderr: ${result.stderr} 		console=True
	Should Be Empty 	${result.stderr}

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

	Wait For 	ImgSplitter App 	timeout=${ImageTimeout}
	# Sleep    2
	Take A Screenshot
	# Fail    Mount ImageSplitter Image Not Completed

	Directory Should Exist 		/Volumes
	@{items}= 	List Directory 	/Volumes 	* 		absolute

	# Directory Should Exist 		~/Desktop
	# @{items}= 	List Directory 	~/Desktop 	* 		absolute
	#
	# ${Desktop Path}= 	Normalize Path 		~/Desktop
	#
	# Directory Should Exist 		${Desktop Path}
	# @{items}= 	List Directory 	${Desktop Path} 	* 		absolute

	# Directory Should Exist 		${Desktop Path}/ImgSplitter
	# @{items}= 	List Directory 	${Desktop Path}/ImgSplitter 	*.* 		absolute


	Wait Until Created 		/Volumes/ImgSplitter 	timeout=${ImageTimeout}
	Directory Should Exist 		/Volumes/ImgSplitter
	@{items}= 	List Directory 	/Volumes/ImgSplitter 	*.* 		absolute
	Directory Should Exist 		${SRCE_APP_DIR}

Quit ImageSplitter MacOS
	Take A Screenshot
	# ${running}= 	Is Process Running 		ImageSplitter
	VAR 	${running} 		${TRUE}
	IF 	${running}
		Wait For 	Close Window 	timeout=${ImageTimeout}
		Take A Screenshot
		Click Image 	Close Window
	# 	${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	# ELSE
	# 	# ${result}= 	Get Process Result 		ImageSplitter
	# 	${result}= 	Wait For Process 		ImageSplitter 	timeout=${ImageTimeout} 	on_timeout=terminate
	END

	# Log 	rc: ${result.rc} 		console=True
	# Log 	stdout: ${result.stdout} 		console=True
	# Log 	stderr: ${result.stderr} 		console=True
	# Should Be Empty 	${result.stderr}





#
