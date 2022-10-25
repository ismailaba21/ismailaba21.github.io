import os

os.environ["KIVY_VIDEO"] = "ffpyplayer"

from kivy.uix.behaviors import ButtonBehavior
from mutagen.mp4 import MP4
from kivymd.uix.label import MDIcon
from kivy.uix.video import Video
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
# from kivy.uix.videoplayer import VideoPlayer


Window.size = (350, 600)


kv = '''
#: import Thumb kivymd.uix.selectioncontrol.Thumb

MDFloatLayout:
	md_bg_color: 1, 1 , 1, 1
	MDRelativeLayout:
		id: layout
		size_hint: 1, None
		height: (root.width/16)*9
		pos_hint: {"top": 1}
		Videos:
			id: video
			source: "fall.mov"
		Image:
			id: thumbnail
			source: "images/music.gif"
		MDRelativeLayout:
			id: controls
			size_hint: 1, None
			height: "60dp"
			pos_hint: {"bottom": 1}
			md_bg_color: 0, 0, 0, 0.3
			MDProgressBar:
				id: slider
				value: 50
				size_hint: None, None
				height: 20
				width: root.width-40
				pos_hint: {"center_x": .5, "top": 1}
				color: 1, 1, 1, 1
				on_touch_move:
					if self.collide_point(args[1].pos[0], args[1].pos[1]): \
						self.value = round(((args[1].pos[0]-20)/self.width)*100); \
						video.seek(self.value/100, precise=True)
				Thumb:
					size_hint: None, None
					size: "15dp", "15dp"
					pos: (slider.value*slider.width)/100+20, slider.center_y - self.height/2 - dp(2)
					color: slider.color
			MDLabel:
				id: time_duration
				text: app.time_duration
				font_size: "12sp"
				color: 1, 1, 1, 1
				bold: True
				pos_hint: {"center_y": .4}
				padding_x: "20sp"
			IconButton:
				icon: "skip-previous"
				pos_hint: {"center_x": .4, "center_y": .4}
				theme_text_color: "Custom"
				text_color: 1, 1, 1, 1
				size_hint: None, None
				size: self.texture_size
				on_release: app.previous()
			IconButton:
				id: play_pause_button
				icon: "play"
				pos_hint: {"center_x": .5, "center_y": .4}
				theme_text_color: "Custom"
				text_color: 1, 1, 1, 1
				size_hint: None, None
				size: self.texture_size
				on_release:
					app.play_pause(self)
			IconButton:
				icon: "skip-next"
				pos_hint: {"center_x": .6, "center_y": .4}
				theme_text_color: "Custom"
				text_color: 1, 1, 1, 1
				size_hint: None, None
				size: self.texture_size
				on_release: app.next()
			IconButton:
				icon: "volume-high"
				pos_hint: {"right": 1, "center_y": .4}
				padding_x: "20dp"
				theme_text_color: "Custom"
				text_color: 1, 1, 1, 1
				size_hint: None, None
				size: self.texture_size
				on_release:
					if self.icon == "volume-high": \
						self.icon = "volume-off"; video.volume = 0
					else: \
						self.icon = "volume-high"; video.volume = 1
					
				
'''


class IconButton(ButtonBehavior, MDIcon):
	pass


class Videos(Video):

	def __init__(self, **kwargs):
		super(Videos, self).__init__(**kwargs)
		self.bind(position=MDApp.get_running_app().change_slider_value)

	def _on_eos(self, *largs):
		MDApp.get_running_app().root.ids.play_pause_button.icon = "replay"
		if MDApp.get_running_app().hide is True:
			MDApp.get_running_app().unhide_controls()

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			if MDApp.get_running_app().hide is True:
				MDApp.get_running_app().unhide_controls()
			else:
				if touch.pos[1] > 60:
					MDApp.get_running_app().hide_controls()

class CustomVideoPlayer(MDApp):

	duration = 0
	time_duration = "0:00"
	current_time = "0:00"
	hide = False

	def on_start(self):
		self.duration = MP4(self.root.ids.video.source).info.length
		minutes = self.duration/60
		secondes = minutes*60
		self.time_duration = str(round(minutes)) + ":" + str(round(secondes)).zfill(2)
		self.root.ids.time_duration.text = f"{self.current_time} / {self.time_duration}"

	def build(self):
		return Builder.load_string(kv)

	def hide_controls(self, *args):
		self.hide = True
		self.root.ids.layout.remove_widget(self.root.ids.controls)

	def unhide_controls(self, *args):
		self.hide = False
		self.root.ids.layout.add_widget(self.root.ids.controls)

	def change_slider_value(self, instance, value):
		position = (value/self.duration)*100
		self.root.ids.slider.value = position
		minutes = value/60
		secondes = minutes*60
		self.current_time = str(round(minutes)) + ":" + str(round(secondes)).zfill(2)
		self.root.ids.time_duration.text = f"{self.current_time} / {self.time_duration}"

	def play_pause(self, button):
		self.root.ids.layout.remove_widget(self.root.ids.thumbnail)

		if button.icon != "replay":
			if button.icon == "play":
				button.icon = "pause"
				self.root.ids.video.state = "play"
			else:
				button.icon = "play"
				self.root.ids.video.state = "pause"
		else:
			button.icon = "pause"
			self.root.ids.video.reload()

	def previous(self):
		self.root.ids.video.seek(0, precise=True)


	def next(self):
		self.root.ids.video.seek(1, precise=True)


if __name__ == "__main__":
	CustomVideoPlayer().run()
