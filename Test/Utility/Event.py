import unittest
from Utility.Event import Event

class TestEvent(unittest.TestCase):
	def setUp(self):
		self.event = Event(binding=self)
		self.value = 0

	def tearDown(self):
		del self.event

	def defaultCallback(self):
		self.value += 1

	def testEventAddition(self):
		self.event.add('foo')
		self.assertIn('foo', self.event.names)
		self.assertIn('foo', self.event.events)

		self.event.add(['foo', 'bar'])
		self.assertEqual(2, len(self.event.names))
		self.assertEqual(2, len(self.event.events))

	def testEventFiring(self):
		self.event.add('foo')
		self.event.on('foo', self.defaultCallback)

		self.event.fire('foo')
		self.assertEqual(self.value, 1)

	def testCallbackRemoval(self):
		def cb1(self):
			self.value += 1

		def cb2(self):
			self.value += 1

		self.event.add('foo')
		self.event.on('foo', cb1)
		self.event.on('foo', cb2)

		self.event.removeCallback('foo', cb1)
		self.event.removeCallback('foo', cb2)
		
		self.event.fire('foo')
		self.assertEqual(self.value, 0)

	def testEventClearing(self):
		self.event.add('foo')
		self.event.on('foo', self.defaultCallback)
		self.event.on('foo', self.defaultCallback)

		self.event.clear('foo')
		self.assertEqual(self.value, 0)

	def testArgumentsFromOn(self):
		def cb(self, a):
			self.assertEqual(a, 42)

		self.event.add('foo')
		self.event.on('foo', cb, args=[42])

	def testArgumentsFromFire(self):
		def cb(self, a):
			self.assertEqual(a, 42)

		self.event.add('foo')
		self.event.on('foo', cb)
		self.event.fire('foo', args=[42])

	def testArgumentsFromBothSources(self):
		def cb(self, a, b):
			self.assertEqual(a, 42)
			self.assertEqual(b, 3.14)

		self.event.add('foo')
		self.event.on('foo', cb, args=[42])
		self.event.fire('foo', args=[3.14])

	def testOneTimeEvents(self):
		self.event.add('foo')
		self.event.once('foo', self.defaultCallback)

		for i in range(0, 5):
			self.event.fire('foo')
		self.assertEqual(self.value, 1)

	def testForwarding(self):
		class Unto():
			pass
		unto = Unto()

		self.event.add(['foo bar', 'foo-bar-baz'])
		self.event.forward(unto, forward=['on'])

		self.assertTrue(hasattr(unto, 'onFooBar'))
		self.assertTrue(hasattr(unto, 'onFooBarBaz'))
