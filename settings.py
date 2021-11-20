# imports of TinyDB
from tinydb import TinyDB, Query
# import to set current working directory
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class Settings:
	def __init__(self):
		# set working directories
		self.cwd = Path(__file__).parent
		self.cwd_images = self.cwd / "images"
		self.cfg_dir = Path.home() / ".config" / "easybright" # set user config directory
		self.cfg_dir.mkdir(exist_ok=True) # create the ~/.config/easybright/ directory, if not exists
		self.icon_dir = self.cfg_dir / "icons"
		self.icon_dir.mkdir(exist_ok=True) # create the ~/.config/easybright/icons directory, if not exists	
		
		# set db to store and restore program settings (name prefdb, with just _default table)
		self.prefdb = TinyDB(self.cfg_dir / "settings.json")
		self.query = Query()
		
		# other settings
		self.ws_server = "ws://localhost:8888"
		
	def initiate_settings(self):
		try:
			# get setting of step from db and set it
			self.step = self.prefdb.search(self.query["settings"] == "step")[0]["value"]
		except IndexError:
			self.create_default_settings()
		# set the version from poetry pyproject.toml file
		self.dialog_about.props.version = self.extract_version_from_toml()

	def write_setting(self, name, value):
		self.prefdb.update({'settings': name, 'value': value}, self.query["settings"] == name)
		# self.prefdb.update({'value': value}, where("settings") == name)
	
	def create_default_settings(self):
		# set default settings
		self.prefdb.upsert({'settings': 'step', 'value': 5}, self.query["settings"] == "step")
		# after default values are set, call initiate_settings again
		self.__init__()
	
	def extract_version_from_toml(self):
		"""Extract version from pyproject.toml file (poetry settings file)"""
		toml_path = self.cwd.parent / 'pyproject.toml'
		result = None
		if toml_path.is_file():
			with open(str(toml_path), "r") as f:
				while result == None:
					string=f.readline()
					if 'version = ' in string:
						result = string.split('"')[1]
		return result