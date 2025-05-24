import kivy
kivy.require('2.3.0')

# from glob import glob
# from random import randint
# from os.path import join, dirname
from kivymd.app import MDApp
# from kivy.logger import Logger, LOG_LEVELS
from applogger import AppLogger

from kivy.clock import Clock

from kivy.config import Config

# from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from kivy.core.window import Window

from kivy.utils import platform

from kivy.graphics import *

# import easygui
# import tkinter as tk
# from tkinter import filedialog
import filedialpy

from threading import Thread
from PIL import Image

import os, sys
from kivy.resources import resource_add_path, resource_find

class ImgSplitterApp(MDApp):

	appwindow = None

	def build_config(self, config):
		config.setdefaults('ImgSplitter', {
			'Templates': 'default,',
			'Seleted_Template': 'default'
		})

		config.setdefaults('default', {
			'Offset_Left': 28,
			'Offset_Top': 38,
			'Seperation_Vertical': 32,
			'Seperation_Horizontal': 32,
			'SubImage_Width': 64,
			'SubImage_Height': 64,
			'Grid_Columns': 5,
			'Grid_Rows': 5
		})

	def build(self):

		#  ValueError: ThemeManager.primary_palette is set to an invalid option 'LightYellow'. Must be one of:
		# ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

		self.theme_cls.theme_style = "Light"
		# self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Brown"
		# self.theme_cls.primary_palette = "Orange"
		# self.theme_cls.accent_palette = "Amber"
		self.theme_cls.accent_palette = "Yellow"

		self.appwindow = ImgSplitterWindow()

		return self.appwindow

	def on_start(self, **kwargs):
		# Logger.setLevel(LOG_LEVELS["debug"])
		# Config.set('kivy', 'log_level', 'debug')	# can just set this in the kivy ini file ~/.kivy/config.ini

		# AppLogger.log("debug", "ImgSplitter", f"log level debug = { LOG_LEVELS['debug'] }")

		AppLogger.log("debug", "ImgSplitterApp.on_start", "ImgSplitterApp APP LOADED")

		self.appwindow.on_start()

	def set_theme(self, theme, primary, accent):
		self.theme_cls.theme_style = theme
		self.theme_cls.primary_palette = primary
		self.theme_cls.accent_palette = accent



class ImgSplitterWindow(MDBoxLayout):
# class ImgSplitterWindow(Screen):

	__version__ = "0.2.0"

	dialogue = None

	version_display = StringProperty(f"Version: {__version__}")

	background_colour = ColorProperty([1, 1, 1, 1])
	# font_colour = ColorProperty([0, 0, 0, 1])
	# button_colour = ColorProperty([.5, .5, .5, 1])

	# img_src = 'data/images/transperent.png'
	img_src = StringProperty('data/images/transperent.png')
	src_dir = None

	# status_bar = StringProperty('')
	status_bar = StringProperty("Status Bar")

	crop_bars = {}
	img_data = {}
	cell_data = {}

	is_animated = False

	subimg = {}
	# subimg_top = NumericProperty(38)
	# subimg_left = NumericProperty(28)
	#
	# subimg_horz = NumericProperty(32)
	# subimg_vert = NumericProperty(32)
	#
	# subimg_height = NumericProperty(64)
	# subimg_width = NumericProperty(64)
	#
	# subimg_cols = NumericProperty(5)
	# subimg_rows = NumericProperty(5)

	def on_start(self, **kwargs):
		# self.layout.label.text = "APP LOADED"
		AppLogger.log("debug", "ImgSplitterWindow.on_start", "ImgSplitterWindow APP LOADED")
		# t = Thread(target=self.delayed_start)
		# t.run()

		Window.bind(on_drop_file=self.handle_on_drop_file)


		# self.tkroot = tk.Tk()

		AppLogger.log("debug", "ImgSplitterWindow.on_start", "__file__:", __file__)
		self.src_dir = os.path.dirname(__file__)
		tmp_img_src = os.path.join(*f"{self.img_src}".split("/"))
		self.img_src = os.path.abspath(os.path.join(self.src_dir, tmp_img_src))

		Clock.schedule_once(self.draw_cut_bars, 1)

	# def safe_path_join(self, *paths):
	# 	outpaths = []
	# 	for path in paths:
	# 		pathparts =

	def split_images(self):

		AppLogger.log("debug", "ImgSplitter", "cell_data:", self.cell_data)

		pathprefix, pathsuffix = os.path.splitext(self.img_src)

		with Image.open(self.img_src) as imgdata:
			for r in range(app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'grid_rows')):
				for c in range(app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'grid_columns')):
					AppLogger.log("debug", "ImgSplitter", "row:", r, " col:", c)
					subImage = self.get_subImage(imgdata, r, c)
					AppLogger.log("debug", "ImgSplitter", "subImage:", subImage)
					outpath = f"{pathprefix}_{r}_{c}{pathsuffix}"
					AppLogger.log("debug", "ImgSplitter", "outpath:", outpath)
					if self.is_animated:
						subImage.save(outpath, save_all=True)
					else:
						subImage.save(outpath)

		self.ok_dialogue("Finished exporting images.")

	def get_subImage(self, imgdata, row, col):
		AppLogger.log("debug", "ImgSplitter", "row:", row, " col:", col)
		rid = f"R{row}"
		cid = f"C{col}"

		x = self.cell_data[cid]
		y = self.cell_data[rid]
		w = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_width') + x
		h = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_height') + y

		workingimg = imgdata.copy()
		subimg = workingimg.crop((x, y, w, h))

		return subimg

	def ok_dialogue(self, message):
		AppLogger.log("debug", "ImgSplitter", "ok_dialogue message:", message)
		if not self.dialogue:
			self.dialogue = MDDialog(
				text=message,
				buttons=[
					MDRaisedButton(
						text="OK",
						# theme_text_color="Custom",
						# text_color=self.theme_cls.primary_color,
						# on_press=self.close_dialogue,
						on_release=self.close_dialogue,
						# on_release=self.dialogue.dismiss(force=True),
					),
				],
			)
			self.dialogue.open()
		AppLogger.log("debug", "ImgSplitter", "ok_dialogue message:", message)

	def close_dialogue(self, *kwargs):
		self.dialogue.dismiss(force=True)
		AppLogger.log("debug", "ImgSplitter", "close_dialogue")

	# def calculate_something(self):
	# 	pass

	def draw_cut_bars(self, *kwargs):

		# AppLogger.log("debug", "draw_cut_bars", "seleted_template: ", app.config.get('ImgSplitter', 'seleted_template'))
		# config.get('section1', 'key1'),
		# AppLogger.log("debug", "draw_cut_bars", "offset_left: ", app.config.get(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left'))

		app.config.write()


		AppLogger.log("debug", "draw_cut_bars", "self", self)
		# AppLogger.log("debug", "ImgSplitter", "self.img_canvas", self.img_canvas)
		AppLogger.log("debug", "draw_cut_bars", "self.ids", self.ids)
		# AppLogger.log("debug", "ImgSplitter", "self.ids.imgbox", self.ids.imgbox)

		# AppLogger.log("debug", "ImgSplitter", "self.root:", self.root)
		# AppLogger.log("debug", "ImgSplitter", "self.root.ids:", self.root.ids)

		AppLogger.log("debug", "draw_cut_bars", "self.ids.img_canvas", self.ids.img_canvas)
		AppLogger.log("debug", "draw_cut_bars", "self.ids.img_canvas.ids", self.ids.img_canvas.ids)


		img_canvas = self.ids["img_canvas"]
		AppLogger.log("debug", "draw_cut_bars", "img_canvas:", img_canvas)
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.size:", img_canvas.size)
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.ids:", img_canvas.ids)
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.canvas:", img_canvas.canvas)


		# AppLogger.log("debug", "ImgSplitter", "img_canvas.canvas.ids:", img_canvas.canvas.ids)
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.canvas.children:", img_canvas.canvas.children)
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.canvas.children[-1]:", img_canvas.canvas.children[-1])
		# AppLogger.log("debug", "ImgSplitter", "img_canvas.canvas.group:", img_canvas.canvas.group)

		# img_canvas.canvas.add(Rectangle(pos=(13, 13), size=(13, 13)))
		# app = MDApp.get_running_app()
		# AppLogger.log("debug", "ImgSplitter", "app:", app)
		# AppLogger.log("debug", "ImgSplitter", "app.ids:", app.ids)

		# img_canvas.canvas.ask_update()
		AppLogger.log("debug", "draw_cut_bars", "img_canvas.size:", img_canvas.size)
		# img_canvas.size = 1280, 720
		# img_canvas.canvas.ask_update()
		# AppLogger.log("debug", "ImgSplitter", "img_canvas.size:", img_canvas.size)


		# self.crop_bars["R0"] = InstructionGroup()
		# self.crop_bars["R0"].add(Color(1, .5, 0.5, 0.4))
		# self.crop_bars["R0"].add(Rectangle(pos=(0, 550), size=(615, 10)))
		# img_canvas.canvas.add(self.crop_bars["R0"])

		# img_canvas.canvas.ask_update()

		self.update_img_data()
		self.get_img_ratios()

		self.remove_cut_bars()

		self.cut_row(0)
		for r in range(app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'grid_rows')):
			AppLogger.log("debug", "ImgSplitter", "row:", r)
			self.cut_row(r+1)

		# w = self.calculate_row_width()
		# self.cut_row(1)

		self.cut_col(0)
		# self.cut_col(1)
		for c in range(app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'grid_columns')):
			AppLogger.log("debug", "ImgSplitter", "col:", c)
			self.cut_col(c+1)

		img_canvas.canvas.ask_update()

	def remove_cut_bars(self):
		for id in self.crop_bars.keys():
			self.ids["img_canvas"].canvas.remove(self.crop_bars[id]["ig"])

		self.cell_data = {}

	def cut_col(self, colnum):

		x = 0
		y = self.calculate_col_position(colnum)
		w = self.calculate_col_width(colnum)
		h = self.ids["img_canvas"].height
		id = f"C{colnum}"

		if id in self.crop_bars:
				self.ids["img_canvas"].canvas.remove(self.crop_bars[id]["ig"])
		self.crop_bars[id] = {}
		self.crop_bars[id]["x"] = x
		self.crop_bars[id]["y"] = y
		self.crop_bars[id]["w"] = w
		self.crop_bars[id]["h"] = h
		self.crop_bars[id]["ig"] = InstructionGroup()
		self.crop_bars[id]["ig"].add(Color(1, .5, 0.5, 0.4))
		AppLogger.log("debug", "ImgSplitter", "col", colnum, ": x:", x, " y:", y, " w:", w, " h:", h)
		self.crop_bars[id]["ig"].add(Rectangle(pos=(self.crop_bars[id]["y"], self.crop_bars[id]["x"]), size=(self.crop_bars[id]["w"], self.crop_bars[id]["h"])))
		self.ids["img_canvas"].canvas.add(self.crop_bars[id]["ig"])
		AppLogger.log("debug", "ImgSplitter", "added col", colnum, " to canvas")

	def calculate_col_width(self, colnum):
		if colnum > 0:
			dispwidth = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical') / self.img_ratios["x"]
			AppLogger.log("debug", "ImgSplitter", "calculate_col_width:", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical'), " / ", self.img_ratios["x"], " = dispwidth:", dispwidth)
			return dispwidth
		else:
			dispwidth = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left') / self.img_ratios["x"]
			AppLogger.log("debug", "ImgSplitter", "calculate_col_width:", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left'), " / ", self.img_ratios["x"], " = dispwidth:", dispwidth)
			return dispwidth

	def calculate_col_position(self, colnum):
		img_pos = 0
		if colnum > 0:
			img_pos = (app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left') + (app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical') + app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_width') ) * colnum) - app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical')
			AppLogger.log("debug", "ImgSplitter", "calculate_col_position", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left'), " + (", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical'), " + ", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_width'), ") * ", colnum, " - ", app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical'), " = ", img_pos)
		else:
			# img_pos = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left')
			img_pos = 0

		if colnum > 0:
			self.cell_data[f"C{colnum}"] = img_pos + app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical')
		else:
			self.cell_data[f"C{colnum}"] = img_pos + app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left')

		AppLogger.log("debug", "ImgSplitter", f"self.cell_data[C{colnum}]:", self.cell_data[f"C{colnum}"])

		# rev_img_pos = self.img_data[self.img_src].width - img_pos
		AppLogger.log("debug", "ImgSplitter", "colnum:", colnum, "	img_pos:", img_pos)

		disp_pos = img_pos / self.img_ratios["x"]
		AppLogger.log("debug", "ImgSplitter", "colnum:", colnum, "	disp_pos:", disp_pos)
		return disp_pos

	def cut_row(self, rownum):

		x = self.calculate_row_position(rownum)
		y = 0
		w = self.ids["img_canvas"].width
		h = self.calculate_row_height(rownum)
		id = f"R{rownum}"

		if id in self.crop_bars:
				self.ids["img_canvas"].canvas.remove(self.crop_bars[id]["ig"])
		self.crop_bars[id] = {}
		self.crop_bars[id]["x"] = x
		self.crop_bars[id]["y"] = y
		self.crop_bars[id]["w"] = w
		self.crop_bars[id]["h"] = h
		self.crop_bars[id]["ig"] = InstructionGroup()
		self.crop_bars[id]["ig"].add(Color(1, .5, 0.5, 0.4))
		AppLogger.log("debug", "ImgSplitter", "row", rownum, ": x:", x, " y:", y, " w:", w, " h:", h)
		self.crop_bars[id]["ig"].add(Rectangle(pos=(self.crop_bars[id]["y"], self.crop_bars[id]["x"]), size=(self.crop_bars[id]["w"], self.crop_bars[id]["h"])))
		self.ids["img_canvas"].canvas.add(self.crop_bars[id]["ig"])
		AppLogger.log("debug", "ImgSplitter", "added row", rownum, " to canvas")

		# self.crop_bars[id]["x"] = x
		# self.crop_bars[id]["y"] = y
		# self.crop_bars[id]["w"] = w
		# self.crop_bars[id]["h"] = h
		# AppLogger.log("debug", "ImgSplitter", "x:", x, " y:", y, " w:", w, " h:", h)

		# AppLogger.log("debug", "ImgSplitter", "img_canvas group:", self.ids["img_canvas"].canvas.group)
		# AppLogger.log("debug", "ImgSplitter", "img_canvas children:", self.ids["img_canvas"].canvas.children)

	def calculate_row_height(self, rownum):
		if rownum > 0:
			dispheight = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_horizontal') / self.img_ratios["y"]
			AppLogger.log("debug", "ImgSplitter", "dispheight:", dispheight)
			return dispheight
		else:
			dispheight = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_top') / self.img_ratios["y"]
			AppLogger.log("debug", "ImgSplitter", "dispheight:", dispheight)
			return dispheight

	def calculate_row_position(self, rownum):
		img_pos = 0
		if rownum > 0:
			img_pos = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_top') + (app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_horizontal') + app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_height')) * rownum
		else:
			img_pos = app.config.getint(app.config.get('ImgSplitter', 'seleted_template'), 'offset_top')


		self.cell_data[f"R{rownum}"] = img_pos
		AppLogger.log("debug", "ImgSplitter", f"self.cell_data[R{rownum}]:", self.cell_data[f"R{rownum}"])

		rev_img_pos = self.img_data[self.img_src].height - img_pos
		AppLogger.log("debug", "ImgSplitter", "rownum:", rownum, "	img_pos:", rev_img_pos)

		disp_pos = rev_img_pos / self.img_ratios["y"]
		AppLogger.log("debug", "ImgSplitter", "rownum:", rownum, "	disp_pos:", disp_pos)
		return disp_pos

	def get_img_ratios(self):
		self.img_ratios = {"x": 0, "y": 0}
		AppLogger.log("debug", "ImgSplitter", "self.img_data[self.img_src][size]", self.img_data[self.img_src].size)

		img_canvas = self.ids["img_canvas"]
		AppLogger.log("debug", "ImgSplitter", "img_canvas:", img_canvas)
		AppLogger.log("debug", "ImgSplitter", "img_canvas.size:", img_canvas.size)

		image_x = self.img_data[self.img_src].width
		image_y = self.img_data[self.img_src].height

		canvas_x = img_canvas.size[0]
		canvas_y = img_canvas.size[1]

		AppLogger.log("debug", "ImgSplitter", "x ratio", image_x / canvas_x)
		AppLogger.log("debug", "ImgSplitter", "y ratio", image_y / canvas_y)

		self.img_ratios["x"] = image_x / canvas_x
		self.img_ratios["y"] = image_y / canvas_y

	def update_img_data(self):

		AppLogger.log("debug", "ImgSplitter", "self.img_src", self.img_src)
		AppLogger.log("debug", "ImgSplitter", "self.img_data", self.img_data)
		self.is_animated = False
		is_animatable = False

		file, ext = os.path.splitext(self.img_src)
		if ext in [".gif", ".png"]:
			is_animatable = True
			AppLogger.log("debug", "ImgSplitter", "is_animatable", is_animatable)

		if self.img_src not in self.img_data.keys():
			# self.img_data[self.img_src] = {}
			self.img_data = {} 		# clear old image
			img = Image.open(self.img_src)
			# get width and height
			AppLogger.log("debug", "ImgSplitter", "img:", img)
			self.img_data[self.img_src] = img

			if is_animatable:
				self.is_animated = img.is_animated
				AppLogger.log("debug", "ImgSplitter", "img.is_animated", img.is_animated)

			img.close()
			AppLogger.log("debug", "ImgSplitter", "self.img_data", self.img_data)
			AppLogger.log("debug", "ImgSplitter", "self.is_animated", self.is_animated)

			# animated gif and apng
			# https://stackoverflow.com/questions/1412529/how-do-i-programmatically-check-whether-a-gif-image-is-animated

	def set_subimg_top(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'offset_top', instance.text)
		self.draw_cut_bars()

	def set_subimg_left(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'offset_left', instance.text)

		self.draw_cut_bars()

	def set_subimg_horz(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_horizontal', instance.text)
		self.draw_cut_bars()

	def set_subimg_vert(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'seperation_vertical', instance.text)
		self.draw_cut_bars()

	def set_subimg_height(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_height', instance.text)
		self.draw_cut_bars()

	def set_subimg_width(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'subimage_width', instance.text)
		self.draw_cut_bars()

	def set_subimg_cols(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'grid_columns', instance.text)
		self.draw_cut_bars()

	def set_subimg_rows(self, instance):
		app.config.set(app.config.get('ImgSplitter', 'seleted_template'), 'grid_rows', instance.text)
		self.draw_cut_bars()

	def on_button_press(self, instance):
		AppLogger.log("debug", "ImgSplitter", "{} Button pressed!".format(instance.text))

	# def on_button_press_open_file(self, instance):
	def on_button_press_open_file(self, **kwargs):
		AppLogger.log("debug", "ImgSplitter", "Open File pressed!")
		filename = "../examples/cat_1.png"
		AppLogger.log("debug", "ImgSplitter", f"Selecting file: {filename}")
		# self.img.source = filename
		# instance.source = filename
		AppLogger.log("debug", "ImgSplitter", "self.img_src", self.img_src)
		self.img_src = filename


		# if "parent" in kwargs:
		# 	AppLogger.log("debug", "ImgSplitter", kwargs["parent"])
		# 	AppLogger.log("debug", "ImgSplitter", kwargs["parent"].ids)

		AppLogger.log("debug", "ImgSplitter", "self.ids", self.ids)
		# AppLogger.log("debug", "ImgSplitter", "self.ids.imgbox", self.ids.imgbox)
		# AppLogger.log("debug", "ImgSplitter", "self.ids.imgbox.ids", self.ids.imgbox.ids)
		# self.ids.img.source = filename

	# def build(self):
	#   open_file.bind(on_press = self.on_button_press)

	def dismiss_popup(self):
		self._popup.dismiss()

	def open_file(self):

		if platform == "android":
			self.show_load()
		else:

			# filetypes = (
			# 	('PNG', '*.png'),
			# 	('All files', '*.*'),
			# 	None
			# )
				# ('JPEG', '*.jpeg', '*.jpg'),
				# ('GIF', '*.gif'),
				# ('JPG', '*.jpg'),

			# filename = filedialog.askopenfilename(
			# 	title='Select a file',
			# 	initialdir='~',
			# 	filetypes=filetypes)

			# filename = filedialog.askopenfilename()

			# filename = easygui.fileopenbox()

			filefilter = " ".join(["*.jpeg","*.jpg","*.png","*.gif","*"])
			AppLogger.log("debug", "open_file", "filefilter:", filefilter)

			filetitle = "Select an image file"

			# filename = filedialpy.openFile(initial_dir="~", title=filetitle, filter=filefilter)
			filename = filedialpy.openFile(title=filetitle, filter=filefilter)
			# filename = filedialpy.openFile(title=filetitle)
			# filename = filedialpy.openFile(initial_dir="~")
			# filename = filedialpy.openFile()

			AppLogger.log("debug", "open_file", "filename", filename)
			if os.path.isfile(filename):
				self.load_file(filename)
			else:
				AppLogger.log("debug", "Caneled", "Clcked Cancel")

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

	# def show_save(self):
	# 	content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
	# 	PATH = "."
	# 	if platform == "android":
	# 	  from android.permissions import request_permissions, Permission
	# 	  request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
	# 	  app_folder = os.path.dirname(os.path.abspath(__file__))
	# 	  PATH = "/storage/emulated/0" #app_folder
	# 	content.ids.filechooser.path = PATH
	# 	self._popup = Popup(title="Save file", content=content,
	# 						size_hint=(0.9, 0.9))
	# 	self._popup.open()

	def load(self, path, filename):
		# with open(os.path.join(path, filename[0])) as stream:
		# 	self.text_input.text = stream.read()

		filepath = os.path.join(path, filename[0])
		self.load_file(filepath)

		self.dismiss_popup()

	def load_file(self, filepath):

		AppLogger.log("debug", "load_file", "filepath", filepath)

		# AppLogger.log("debug", "ImgSplitter", "self.img_src", self.img_src)
		self.img_src = filepath
		# AppLogger.log("debug", "ImgSplitter", "self.img_src", self.img_src)
		self.status_bar = f"Loaded file {filepath}"

		self.update_img_data()
		self.get_img_ratios()
		self.draw_cut_bars()


	# def save(self, path, filename):
	# 	with open(os.path.join(path, filename), 'w') as stream:
	# 		stream.write(self.text_input.text)
	#
	# 	self.dismiss_popup()

	def handle_on_drop_file(self, window, filename, x, y):
	    # print(window, filename, x, y)
		# AppLogger.log("debug", "on_drop_file", "window:", window, "filename:", filename, "x & y:", x, y)
		AppLogger.log("debug", "on_drop_file", "x & y:", x, y)
		AppLogger.log("debug", "on_drop_file", "window:", window)
		AppLogger.log("debug", "on_drop_file", "filename:", filename.decode('utf-8') )

		if os.path.isfile(filename.decode('utf-8')):
			self.load_file(filename.decode('utf-8'))


class LoadDialog(MDFloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


# class SaveDialog(MDFloatLayout):
# 	save = ObjectProperty(None)
# 	text_input = ObjectProperty(None)
# 	cancel = ObjectProperty(None)
#


if __name__ == '__main__':
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
	app = ImgSplitterApp()
	app.run()
