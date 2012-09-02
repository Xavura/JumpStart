import types
import functools

class Event():
	"""
	A simple event emitter implementation.
	"""

	@staticmethod
	def validateEventName(name):
		name = name.replace('_', ' ').replace('-', ' ').title().replace(' ', '')
		return name[:1].lower() + name[1:]

	def __init__(self, events=None, binding=None, aliases=False):
		self.names   = []
		self.events  = {}
		self.options = {}
		self.binding = binding
		self.aliases = aliases

		if events:
			self.add(events)

	def isEvent(self, name):
		"""
		Checks that an event [name] exists.
		"""

		return name in self.names

	def on(self, name, callback, args=[], once=False):
		"""
		Schedules a callback [callback] to run when an event [name] is fired.

		[args] - Call the callback with these arguments.
		[once] - Remove this callback after the event has fired once.
		"""

		if not self.isEvent(name):
			self.add(name)

		if not hasattr(callback, '__call__'):
			return False

		to_apply = []

		# TODO: This seems a little hacky but it IS what we want, since Python's binding is
		# implicit/conventional and we don't really want to apply our binding if the method
		# is already bound.
		if self.binding and not isinstance(callback, types.MethodType) or \
		  (isinstance(callback, types.MethodType) and callback.im_self == None):
			to_apply.append(self.binding)

		if args:
			to_apply += args

		self.events[name].append([functools.partial(callback, *to_apply), once])

	def once(self, name, callback, args = []):
		"""
		Shortcut to schedule a one-time callback via on().
		"""

		self.on(name, callback, args=args, once=True)

	def add(self, name, options = {}):
		"""
		Creates an event [name].
		"""

		if type(name) is list:
			for i in name:
				self.add(i)
			return

		if not self.isEvent(name):
			self.events[name]  = []
			self.options[name] = {}

			self.names.append(name)
			# self.setOptions(name, options)

	def remove(self, name):
		"""
		Shortcut to clear an event's callbacks and also remove the event.
		"""

		if self.isEvent(name):
			self.clear(name, True)

	def fire(self, name, args = []):
		"""
		Runs an event [name].

		[args] - Optional arguments for the callback, will be merged with arguments from on().
		"""

		if not self.isEvent(name):
			return False

		to_remove = []

		for i, j in enumerate(self.events[name]):
			callback, once = j

			if args:
				callback = functools.partial(callback, *args)

			callback.__call__()

			if once:
				to_remove.append(i)

		if len(to_remove) > 0:
			for i in to_remove:
				del self.events[name][i]

		# limit = self.options[name].limit
		# count = self.options[name].count

		# if limit:
		# 	count += 1
		# 	if count == limit:
		# 		self.fire('after_%s' % (name))
		# 		self.clear(name, True)
		# 		self.clear('after_%s' % (name), True)

	def clear(self, name, remove = False):
		"""
		Removes all callbacks from event [name].

		[remove] - Also, remove the event itself.
		"""

		if self.isEvent(name):
			if remove == True:
				del self.events[name]
				del self.options[name]
				del self.names[self.names.index(name)]
			else:
				self.events[name] = []
		elif name == True:
			for name in self.names:
				self.clear(name, remove)

	def removeCallback(self, name, callback):
		"""
		Removes a single callback [callback] from an event [name].
		"""

		to_remove = []
		for i, j in enumerate(self.events[name]):
			if j[0] == callback or (type(j[0]) == functools.partial and j[0].func == callback):
				to_remove.append(i)

		for i in to_remove:
			del self.events[name][i]

	def forward(self, object_, forward=['on', 'fire']):
		"""
			Create delegates to one or more methods of the event instance on an instance.

			event.add('foo')
			event.forward(an_instance)
			an_instance.fireFoo()
		"""
		for i in self.names:
			for j in forward:
				name = Event.validateEventName('%s %s' % (j, i))
				setattr(object_, name, functools.partial(getattr(self, j), self))

class Group():
	def __init__(self):
		pass

	def create(name, enable=False):
		pass

	def open(name):
		pass

	def close(name):
		pass

	def enable(name):
		pass

	def disable(name):
		pass

	def is_group(name):
		pass
