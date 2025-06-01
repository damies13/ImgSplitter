*** Settings ***

*** Keywords ***

Set Platform
	Set Platform By Python

Set Platform By Python
	${system}= 		Evaluate 	platform.system() 	modules=platform

	IF 	"${system}" == "Darwin"
		Set Suite Variable    ${platform}    macos
	END
	IF 	"${system}" == "Windows"
		Set Suite Variable    ${platform}    windows
	END
	IF 	"${system}" == "Linux"
		Set Suite Variable    ${platform}    ubuntu
	END

Install ImageSplitter
	Set Platform
	Import Resource 	${CURDIR}${/}ImageSplitter-${platform}.robot
	Run Keyword 	Install ImageSplitter ${platform}

Run ImageSplitter
	Run Keyword 	Run ImageSplitter ${platform}

Quit ImageSplitter
	Run Keyword 	Quit ImageSplitter ${platform}
