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
from multi_text_box import MultiTextBox

class FlexibleGroupBox(MultiTextBox):
	hooks = [
		hook.subscribe.addgroup,
		hook.subscribe.changegroup,
		hook.subscribe.client_killed,
		hook.subscribe.client_managed,
		hook.subscribe.client_urgent_hint_changed,
		hook.subscribe.current_screen_change,
		hook.subscribe.delgroup,
		hook.subscribe.group_window_add,
		hook.subscribe.setgroup,
	]

	def __init__(self, formatter, **config):
		MultiTextBox.__init__(self, self.__update, hooks = FlexibleGroupBox.hooks, **config)
		self.__formatter  = formatter

	def __update(self, *args, **kwargs):
		for group in self.qtile.groups:
			result = self.__formatter(group, self.qtile)
			if result is None: continue
			yield result
