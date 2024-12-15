import kivy
kivy.require('2.3.0')

# from glob import glob
# from random import randint
# from os.path import join, dirname
from kivymd.app import MDApp
from kivy.logger import Logger

from kivy.clock import Clock

# from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.popup import Popup

from kivy.utils import platform

from kivy.graphics import *

from threading import Thread
from PIL import Image

import os


class ImgSplitterApp(MDApp):

	appwindow = None

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
		print("ImgSplitterApp APP LOADED")
		self.appwindow.on_start()

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

	crop_bars = {}
	img_data = {}
	cell_data = {}

	is_animated = False

	subimg = {}
	subimg_top = NumericProperty(38)
	subimg_left = NumericProperty(28)

	subimg_horz = NumericProperty(32)
	subimg_vert = NumericProperty(32)

	subimg_height = NumericProperty(64)
	subimg_width = NumericProperty(64)

	subimg_cols = NumericProperty(5)
	subimg_rows = NumericProperty(5)

	def on_start(self, **kwargs):
		# self.layout.label.text = "APP LOADED"
		print("ImgSplitterWindow APP LOADED")
		# t = Thread(target=self.delayed_start)
		# t.run()

		Clock.schedule_once(self.draw_cut_bars, 1)

	# def delayed_start(self):
	#
	# 	print("delayed_start APP LOADED")
	# 	self.draw_cut_bars()

	# def build(self):
	# 	self.draw_cut_bars()
	# def __init__(self, parent):
	# 	# self.root = parent
	# 	self.draw_cut_bars()
	# 	# print("self:", self)
	# 	# print("self.root:", self.root)
	# 	# print("self.parent:", self.parent)
	#
	# 	# self.theme_cls.theme_style = "Dark"
	# 	# self.theme_cls.theme_style = "Light"
	# self.theme_cls.theme_style = 'Dark'
	# 	pass

	def draw_cut_bars(self, *kwargs):

		print("self", self)
		# print("self.img_canvas", self.img_canvas)
		print("self.ids", self.ids)
		# print("self.ids.imgbox", self.ids.imgbox)

		# print("self.root:", self.root)
		# print("self.root.ids:", self.root.ids)

		print("self.ids.img_canvas", self.ids.img_canvas)
		print("self.ids.img_canvas.ids", self.ids.img_canvas.ids)


		img_canvas = self.ids["img_canvas"]
		print("img_canvas:", img_canvas)
		print("img_canvas.size:", img_canvas.size)
		print("img_canvas.ids:", img_canvas.ids)
		print("img_canvas.canvas:", img_canvas.canvas)


		# print("img_canvas.canvas.ids:", img_canvas.canvas.ids)
		print("img_canvas.canvas.children:", img_canvas.canvas.children)
		print("img_canvas.canvas.children[-1]:", img_canvas.canvas.children[-1])
		# print("img_canvas.canvas.group:", img_canvas.canvas.group)

		# img_canvas.canvas.add(Rectangle(pos=(13, 13), size=(13, 13)))
		# app = MDApp.get_running_app()
		# print("app:", app)
		# print("app.ids:", app.ids)

		# img_canvas.canvas.ask_update()
		print("img_canvas.size:", img_canvas.size)
		# img_canvas.size = 1280, 720
		# img_canvas.canvas.ask_update()
		# print("img_canvas.size:", img_canvas.size)


		# self.crop_bars["R0"] = InstructionGroup()
		# self.crop_bars["R0"].add(Color(1, .5, 0.5, 0.4))
		# self.crop_bars["R0"].add(Rectangle(pos=(0, 550), size=(615, 10)))
		# img_canvas.canvas.add(self.crop_bars["R0"])

		# img_canvas.canvas.ask_update()

		self.update_img_data()
		self.get_img_ratios()


		self.cut_row(0)
		for r in range(self.subimg_rows):
			print("row:", r)
			self.cut_row(r+1)

		# w = self.calculate_row_width()
		# self.cut_row(1)

		self.cut_col(0)
		# self.cut_col(1)
		for c in range(self.subimg_cols):
			print("col:", c)
			self.cut_col(c+1)

		img_canvas.canvas.ask_update()

	def split_images(self):

		print("cell_data:", self.cell_data)

		pathprefix, pathsuffix = os.path.splitext(self.img_src)

		with Image.open(self.img_src) as imgdata:
			for r in range(self.subimg_rows):
				for c in range(self.subimg_cols):
					print("row:", r, " col:", c)
					subImage = self.get_subImage(imgdata, r, c)
					print("subImage:", subImage)
					outpath = f"{pathprefix}_{r}_{c}{pathsuffix}"
					print("outpath:", outpath)
					if self.is_animated:
						subImage.save(outpath, save_all=True)
					else:
						subImage.save(outpath)

	def get_subImage(self, imgdata, row, col):
		print("row:", row, " col:", col)
		rid = f"R{row}"
		cid = f"R{col}"

		x = self.cell_data[cid]
		y = self.cell_data[rid]
		w = self.subimg_width + x
		h = self.subimg_height + y

		workingimg = imgdata.copy()
		subimg = workingimg.crop((x, y, w, h))

		return subimg


	def calculate_something(self):
		pass

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
		print("col", colnum, ": x:", x, " y:", y, " w:", w, " h:", h)
		self.crop_bars[id]["ig"].add(Rectangle(pos=(self.crop_bars[id]["y"], self.crop_bars[id]["x"]), size=(self.crop_bars[id]["w"], self.crop_bars[id]["h"])))
		self.ids["img_canvas"].canvas.add(self.crop_bars[id]["ig"])
		print("added col", colnum, " to canvas")


	def calculate_col_width(self, colnum):
		if colnum > 0:
			dispwidth = self.subimg_vert / self.img_ratios["x"]
			print("calculate_col_width:", self.subimg_vert, " / ", self.img_ratios["x"], " = dispwidth:", dispwidth)
			return dispwidth
		else:
			dispwidth = self.subimg_left / self.img_ratios["x"]
			print("calculate_col_width:", self.subimg_left, " / ", self.img_ratios["x"], " = dispwidth:", dispwidth)
			return dispwidth

	def calculate_col_position(self, colnum):
		img_pos = 0
		if colnum > 0:
			img_pos = self.subimg_left + (self.subimg_vert + self.subimg_width + self.subimg_vert) * colnum - self.subimg_vert
			print("calculate_col_position", self.subimg_left, " + (", self.subimg_vert, " + ", self.subimg_width, ") * ", colnum, " - ", self.subimg_vert, " = ", img_pos)
		else:
			# img_pos = self.subimg_left
			img_pos = 0

		if colnum > 0:
			self.cell_data[f"C{colnum}"] = img_pos + self.subimg_vert
		else:
			self.cell_data[f"C{colnum}"] = img_pos + self.subimg_left

		# rev_img_pos = self.img_data[self.img_src].width - img_pos
		print("colnum:", colnum, "	img_pos:", img_pos)

		disp_pos = img_pos / self.img_ratios["x"]
		print("colnum:", colnum, "	disp_pos:", disp_pos)
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
		print("row", rownum, ": x:", x, " y:", y, " w:", w, " h:", h)
		self.crop_bars[id]["ig"].add(Rectangle(pos=(self.crop_bars[id]["y"], self.crop_bars[id]["x"]), size=(self.crop_bars[id]["w"], self.crop_bars[id]["h"])))
		self.ids["img_canvas"].canvas.add(self.crop_bars[id]["ig"])
		print("added row", rownum, " to canvas")

		# self.crop_bars[id]["x"] = x
		# self.crop_bars[id]["y"] = y
		# self.crop_bars[id]["w"] = w
		# self.crop_bars[id]["h"] = h
		# print("x:", x, " y:", y, " w:", w, " h:", h)

		# print("img_canvas group:", self.ids["img_canvas"].canvas.group)
		# print("img_canvas children:", self.ids["img_canvas"].canvas.children)

	def calculate_row_height(self, rownum):
		if rownum > 0:
			dispheight = self.subimg_horz / self.img_ratios["y"]
			print("dispheight:", dispheight)
			return dispheight
		else:
			dispheight = self.subimg_top / self.img_ratios["y"]
			print("dispheight:", dispheight)
			return dispheight


	def calculate_row_position(self, rownum):
		img_pos = 0
		if rownum > 0:
			img_pos = self.subimg_top + (self.subimg_horz + self.subimg_height) * rownum
		else:
			img_pos = self.subimg_top


		self.cell_data[f"R{rownum}"] = img_pos

		rev_img_pos = self.img_data[self.img_src].height - img_pos
		print("rownum:", rownum, "	img_pos:", rev_img_pos)

		disp_pos = rev_img_pos / self.img_ratios["y"]
		print("rownum:", rownum, "	disp_pos:", disp_pos)
		return disp_pos

	def get_img_ratios(self):
		self.img_ratios = {"x": 0, "y": 0}
		print("self.img_data[self.img_src][size]", self.img_data[self.img_src].size)

		img_canvas = self.ids["img_canvas"]
		print("img_canvas:", img_canvas)
		print("img_canvas.size:", img_canvas.size)

		image_x = self.img_data[self.img_src].width
		image_y = self.img_data[self.img_src].height

		canvas_x = img_canvas.size[0]
		canvas_y = img_canvas.size[1]

		print("x ratio", image_x / canvas_x)
		print("y ratio", image_y / canvas_y)

		self.img_ratios["x"] = image_x / canvas_x
		self.img_ratios["y"] = image_y / canvas_y

	def update_img_data(self):

		print("self.img_src", self.img_src)
		print("self.img_data", self.img_data)
		self.is_animated = False
		is_animatable = False

		file, ext = os.path.splitext(self.img_src)
		if ext in [".gif", ".png"]:
			is_animatable = True
			print("is_animatable", is_animatable)

		if self.img_src not in self.img_data.keys():
			# self.img_data[self.img_src] = {}
			self.img_data = {} 		# clear old image
			img = Image.open(self.img_src)
			# get width and height
			print("img:", img)
			self.img_data[self.img_src] = img

			if is_animatable:
				self.is_animated = img.is_animated
				print("img.is_animated", img.is_animated)

			img.close()
			print("self.img_data", self.img_data)
			print("self.is_animated", self.is_animated)

			# animated gif and apng
			# https://stackoverflow.com/questions/1412529/how-do-i-programmatically-check-whether-a-gif-image-is-animated

	def set_subimg_top(self, instance):
		# print("Top New Value: ", instance.text, "	Current Value", self.subimg_top)
		self.subimg_top = int(instance.text)
		self.draw_cut_bars()

	def set_subimg_left(self, instance):
		# print("Left New Value: ", instance.text, "	Current Value", self.subimg_left)
		self.subimg_left = int(instance.text)

	def set_subimg_horz(self, instance):
		self.subimg_horz = int(instance.text)

	def set_subimg_vert(self, instance):
		self.subimg_vert = int(instance.text)

	def set_subimg_height(self, instance):
		# print("Height New Value: ", instance.text, "	Current Value", self.subimg_height)
		self.subimg_height = int(instance.text)

	def set_subimg_width(self, instance):
		# print("Width New Value: ", instance.text, "	Current Value", self.subimg_width)
		self.subimg_width = int(instance.text)

	def set_subimg_cols(self, instance):
		# print("Cols New Value: ", instance.text, "	Current Value", self.subimg_cols)
		self.subimg_cols = int(instance.text)

	def set_subimg_rows(self, instance):
		# print("Rows New Value: ", instance.text, "	Current Value", self.subimg_rows)
		self.subimg_rows = int(instance.text)

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

		# print("self.img_src", self.img_src)
		self.img_src = filepath
		# print("self.img_src", self.img_src)
		self.status_bar = f"Loaded file {filepath}"

		self.update_img_data()
		self.get_img_ratios()

		self.dismiss_popup()

	# def save(self, path, filename):
	# 	with open(os.path.join(path, filename), 'w') as stream:
	# 		stream.write(self.text_input.text)
	#
	# 	self.dismiss_popup()

class LoadDialog(MDFloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


# class SaveDialog(MDFloatLayout):
# 	save = ObjectProperty(None)
# 	text_input = ObjectProperty(None)
# 	cancel = ObjectProperty(None)
#


if __name__ == '__main__':
	ImgSplitterApp().run()
