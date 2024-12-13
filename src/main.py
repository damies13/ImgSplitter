import kivy
kivy.require('2.3.0')

# from glob import glob
# from random import randint
# from os.path import join, dirname
from kivymd.app import MDApp
from kivy.logger import Logger
# from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ColorProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.popup import Popup

from kivy.utils import platform

from kivy.graphics import *


import os


class ImgSplitterApp(MDApp):

	def build(self):

		#  ValueError: ThemeManager.primary_palette is set to an invalid option 'LightYellow'. Must be one of:
		# ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

		self.theme_cls.theme_style = "Light"
		# self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Brown"
		# self.theme_cls.primary_palette = "Orange"
		# self.theme_cls.accent_palette = "Amber"
		self.theme_cls.accent_palette = "Yellow"


		return ImgSplitterWindow()

	def set_theme(self, theme, primary, accent):
		self.theme_cls.theme_style = theme
		self.theme_cls.primary_palette = primary
		self.theme_cls.accent_palette = accent



class ImgSplitterWindow(MDBoxLayout):
# class ImgSplitterWindow(Screen):

	__version__ = "0.1.0"

	version_display = StringProperty(f"Version: {__version__}")

	background_colour = ColorProperty([1, 1, 1, 1])
	# font_colour = ColorProperty([0, 0, 0, 1])
	# button_colour = ColorProperty([.5, .5, .5, 1])

	# img_src = 'data/images/transperent.png'
	img_src = StringProperty('data/images/transperent.png')

	# status_bar = StringProperty('')
	status_bar = StringProperty("Status Bar")

	# def build(self):
	# def __init__(self):
	# 	# print("self:", self)
	# 	# print("self.root:", self.root)
	# 	# print("self.parent:", self.parent)
	#
	# 	# self.theme_cls.theme_style = "Dark"
	# 	# self.theme_cls.theme_style = "Light"
	# self.theme_cls.theme_style = 'Dark'
	# 	pass

	def on_button_press(self, instance):
		print("{} Button pressed!".format(instance.text))

	# def on_button_press_open_file(self, instance):
	def on_button_press_open_file(self, **kwargs):
		print("Open File pressed!")
		filename = "../examples/cat_1.png"
		print(f"Selecting file: {filename}")
		# self.img.source = filename
		# instance.source = filename
		print("self.img_src", self.img_src)
		self.img_src = filename


		# if "parent" in kwargs:
		# 	print(kwargs["parent"])
		# 	print(kwargs["parent"].ids)

		print("self.ids", self.ids)
		# print("self.ids.imgbox", self.ids.imgbox)
		# print("self.ids.imgbox.ids", self.ids.imgbox.ids)
		# self.ids.img.source = filename

	# def build(self):
	#   open_file.bind(on_press = self.on_button_press)

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		PATH = "."
		if platform == "android":
		  from android.permissions import request_permissions, Permission
		  request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
		  app_folder = os.path.dirname(os.path.abspath(__file__))
		  PATH = "/storage/emulated/0" #app_folder
		content.ids.filechooser.path = PATH

		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		PATH = "."
		if platform == "android":
		  from android.permissions import request_permissions, Permission
		  request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
		  app_folder = os.path.dirname(os.path.abspath(__file__))
		  PATH = "/storage/emulated/0" #app_folder
		content.ids.filechooser.path = PATH
		self._popup = Popup(title="Save file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		# with open(os.path.join(path, filename[0])) as stream:
		# 	self.text_input.text = stream.read()

		filepath = os.path.join(path, filename[0])

		# print("self.img_src", self.img_src)
		self.img_src = filepath
		# print("self.img_src", self.img_src)
		self.status_bar = f"Loaded file {filename[0]}"

		self.dismiss_popup()

	def save(self, path, filename):
		with open(os.path.join(path, filename), 'w') as stream:
			stream.write(self.text_input.text)

		self.dismiss_popup()

class LoadDialog(MDFloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


class SaveDialog(MDFloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)



if __name__ == '__main__':
	ImgSplitterApp().run()
