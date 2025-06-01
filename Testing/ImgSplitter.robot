*** Settings ***

Resource    ImageSplitter-HighLevel.robot

Suite Setup 	Install ImageSplitter


*** Test Cases ***
Check ImageSplitter Runs
	Run ImageSplitter
