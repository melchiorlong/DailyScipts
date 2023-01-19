class ObjectWrapper(object):
	def __init__(self):
		self.target = None

	def set_target_object(self, target):
		if target is not None and self.target is None:
			self.target = target

	def __call__(self):
		def _lookup():
			rv = self.target
			return rv

		return _lookup


config_object = ObjectWrapper()
config = config_object()
