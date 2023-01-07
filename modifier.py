import json
import re



class Modifier:
	def __init__(self):
		super(Modifier, self).__init__()
		self.base_file_path = "modifies.json"
		self._modifies = None
		self._load_base_file()


	def _load_base_file(self):
		with open(self.base_file_path, "r") as rFile:
		  self._modifies = json.load(rFile)


	def node_target(self, link):
		for modify in self._modifies:
			if re.match(modify["regex"], link):
				return modify.get("node")


# matches = re.findall(regex, str(resHtml))
