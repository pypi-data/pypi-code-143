from deposit import __version__
from deposit.datasource.abstract_filesource import AbstractFileSource
from deposit.store.abstract_delement import AbstractDElement
from deposit.store.dobject import DObject
from deposit.store.dclass import DClass

from deposit.utils.fnc_serialize import (json_data_to_store, GRAPH_ATTRS)

import json

class DJSONEncoder(json.JSONEncoder):
	
	def default(self, o):
		
		if isinstance(o, AbstractDElement):
			element_data = o.to_dict()
			return element_data
		return o.__dict__

class JSON(AbstractFileSource):
	
	EXTENSION = "json"
	
	def save_data(self, store, resources, path):
		
		self.update_progress(1, 10, text = "Saving data")
		
		with open(path, "w") as f:
			json.dump(dict(
				object_relation_graph = store.G.objects_to_json(GRAPH_ATTRS),
				class_relation_graph = store.G.classes_to_json(GRAPH_ATTRS),
				class_membership_graph = store.G.members_to_json(GRAPH_ATTRS),
				local_folder = store._local_folder,
				max_order = store._max_order,
				user_tools = store._user_tools,
				queries = store._queries,
				deposit_version = __version__,
			), f, cls = DJSONEncoder)
		
		self.update_progress(10)
		
		return True
	
	def load_data(self, path):
		
		with open(path, "r") as f:
			data = json.load(f)
		return data
	
	def data_to_store(self, data, store):
		
		return json_data_to_store(data, store, self._progress)
