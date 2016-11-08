# Copyright (c) 2016 Maarten de Vries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, hook
from libqtile.widget import base

class MultiTextBox(base._Widget):
	orientations = base.ORIENTATION_HORIZONTAL

	defaults = {
		'text':         '',
		'fg_colour':    '#999999',
		'bg_colour':    None,
		'font_family':  'xft:monospace',
		'font_size':    None,
		'font_shadow':  None,
		'markup':       False,
	}

	def __init__(self, formatter, hooks = [], **config):
		base._Widget.__init__(self, bar.CALCULATED, **config)
		self.__formatter     = formatter
		self.__config        = config
		self.__texts         = []
		self.__hooks         = set()
		self.__initial_hooks = hooks

	def _configure(self, qtile, bar):
		base._Widget._configure(self, qtile, bar)
		self.addHooks(self.__initial_hooks)
		self.__initial_hooks = None

	def calculate_length(self):
		result = 0
		for _, layout in self.__texts:
			result += layout.width
		return result

	def draw(self):
		offset = 0
		for config, layout in self.__texts:
			bg_colour = config['bg_colour'] or self.bar.background
			self.drawer.set_source_rgb(bg_colour)
			self.drawer.fillrect(offset, self.offsety, layout.width, self.height, 0)
			layout.draw(offset, int((self.bar.height - layout.height) / 2.0))
			offset += layout.width
		self.drawer.draw(offsetx = self.offsetx, width = self.width)

	def textClicked(self, x, y):
		''' Check which individual text was clicked. '''
		offset = 0
		for i, (_, layout) in enumerate(self.__texts):
			if x <= offset + layout.width:
				return i
			offset += layout.width
		return -1

	def __supplementConfig(self, config):
		result = dict(MultiTextBox.defaults)
		result.update(self.__config)
		result.update(config)
		return result

	def __configToLayout(self, config):
		return self.drawer.textlayout(
			text        = config['text'],
			colour      = config['fg_colour'],
			font_family = config['font_family'],
			font_size   = config['font_size'] if config['font_size'] is not None else self.height,
			font_shadow = config['font_shadow'],
			markup      = config['markup']
		)

	def updateSoon(self, *args, **kwargs):
		self.qtile.call_soon(self.update, *args, **kwargs)

	def update(self, *args, **kwargs):
		texts = [self.__supplementConfig(x) for x in self.__formatter(self, self.qtile)]
		self.__texts = [(x, self.__configToLayout(x)) for x in texts]
		self.bar.draw()

	def addHook(self, hook):
		if hook in self.__hooks: return
		self.__hooks.add(hook)
		hook(self.updateSoon)

	def addHooks(self, hooks):
		for hook in hooks: self.addHook(hook)
