from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from colorsys import rgb_to_hls, hls_to_rgb

import os
import subprocess

from flexible_group_box import FlexibleGroupBox
from multi_text_box import MultiTextBox

import util

mod = "mod4"

keys = [
	# Switch between windows in current stack pane
	Key([mod], "Right", lazy.layout.next()),
	Key([mod], "Left", lazy.layout.previous()),

	# Grow or shrink current window
	Key([mod], "Up", lazy.layout.grow()),
	Key([mod], "Down", lazy.layout.shrink()),

	# Move windows up or down in current stack
	Key([mod, "shift"], "Right", lazy.layout.shuffle_down()),
	Key([mod, "shift"], "Left", lazy.layout.shuffle_up()),

	# Swap with main window
	Key([mod, "shift"], "Return", lazy.layout.swap_main()),

	# Toggle between different layouts as defined below
	Key([mod], "space", lazy.next_layout()),

	# Reset layout.
	Key([mod, "shift"], "space", lazy.layout.reset()),

	# Move focus to screen
	Key([mod], "w", lazy.to_screen(1)),
	Key([mod], "e", lazy.to_screen(0)),
	# Move window to screen
	Key([mod, "shift"], "w", lazy.window.toscreen(1)),
	Key([mod, "shift"], "e", lazy.window.toscreen(0)),

	# Spawn terminal
	Key([mod], "Return", lazy.spawn("exo-open --launch TerminalEmulator")),

	# Kill current window
	Key([mod], "q", lazy.window.kill()),

	# Toggle floating status
	Key([mod], "t", lazy.window.toggle_floating()),

	# Toggle fullscreen status
	Key([mod], "f", lazy.hide_show_bar()),

	Key([mod, "shift"], "q", lazy.restart()),
	#Key([mod, "control"], "q", lazy.shutdown()),
	Key([mod], "d", lazy.spawn("dmenu_run -i -b -fn 'DejaVu Sans Mono'")),

	# Screenshots
	Key(["shift"], "Print", lazy.spawn("xfce4-screenshooter")),
	Key([], "Print", lazy.spawn("xfce4-screenshooter -f")),
]

# Define groups (key, name)
groups_info = [
	("1", "dev"),
	("2", "web"),
	("3", "mail"),
	("4", "chat"),
	("5", "doc"),
	("6", "misc"),
	("7", "viz"),
	("8", "8"),
	("9", "9"),
	("0", "0"),
]

# Create groups
groups = []
for key, name in groups_info:
	# append to list of groups
	groups.append(Group(name))

	# mod1 + letter of group = switch to group
	keys.append(Key([mod], key, lazy.group[name].toscreen()))

	# mod1 + shift + letter of group = switch to & move focused window to group
	keys.append(Key([mod, "shift"], key, lazy.window.togroup(name)))

white = (0, 1, 0)
black = (0, 0, 0)

def toQtileColor(hls):
	r, g, b = hls_to_rgb(*hls)
	return r * 255, g * 255, b * 255

def toHexColor(hls):
	r, g, b = hls_to_rgb(*hls)
	return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

def screenColor(screen):
	if screen == 0: return 195 / 360.0, 0.25, 1.0
	if screen == 1: return 140 / 360.0, 0.25, 1.0
	if screen == 2: return 210 / 360.0, 0.5, 0.5
	return                 270 / 360.0, 0.5, 0.5

def lsMultiply(hls, l, s):
	return hls[0], hls[1] * l, hls[2] * s

def background(hls):
	return lsMultiply(hls, 0.6, 0.7)

def fade(hls):
	return lsMultiply(hls, 0.7, 0.6)

def highlight(hls):
	return lsMultiply(hls, 1.0, 1.0)

# Define layout color settings
layout_color = dict(
	border_focus  = '#004d99',
	border_normal = "#222222",
	border_width  = 2,
)

# Define layouts
layouts = [
	layout.MonadTall(name="Tall",    **layout_color),
	layout.Matrix(   name="Matrix",  **layout_color),
	layout.Wmii(     name="Stack",   **layout_color),
	layout.Zoomy(    name="Zoomy",   **layout_color),
	layout.Max(      name="Full",    **layout_color),
]

def groupColors(group_screen, bar_screen, focus, windows, urgents):
	if urgents:                return white,       (0, 0.6, 0)
	if group_screen and focus: return white,       screenColor(group_screen.index)
	if group_screen:           return fade(white), fade(screenColor(group_screen.index))
	if windows and focus:      return black,       (0.0, 0.4, 0.0)
	if windows:                return black,       fade((0.0, 0.4, 0.0))
	return (0.0, 0.7, 0.0), background(screenColor(bar_screen.index))

def formatGroup(widget, group, qtile):
	screen = widget.bar.screen
	focus = qtile.currentScreen == screen
	urgents = filter(lambda x: x.urgent, group.windows)
	fg, bg = groupColors(group.screen, screen, focus, len(group.windows), 0)
	return dict(
		text      = ' {} '.format(group.name),
		fg_colour = toQtileColor(fg),
		bg_colour = toQtileColor(bg),
	)

def formatLayout(widget, qtile):
	screen = widget.bar.screen
	focus = qtile.currentScreen == screen
	group = screen.group
	text  = group.layout.name if group else ''
	return [dict(
		text      = ' {} '.format(text),
		fg_colour = '#ffffff' if focus else '#b0b0b0',
		bg_colour = toQtileColor(background(screenColor(screen.index))),
	)]

def formatTitle(widget, qtile):
	screen = widget.bar.screen
	focus  = qtile.currentScreen == screen
	group  = screen.group
	window = group.currentWindow if group else None
	text   = window.name if window and window.name else ''
	return [dict(
		text      = ' {} '.format(text),
		fg_colour = "#ffffff" if focus else '#bbbbbb',
	)]

update_hooks = [
	hook.subscribe.changegroup,
	hook.subscribe.float_change,
	hook.subscribe.focus_change,
	hook.subscribe.layout_change,
	hook.subscribe.window_name_change,
]

# Define widget settings
widget_defaults = dict(
	font     = "xft:monospace:size = 9:bold:antialias = true",
	fontsize = 13,
	padding  = 3,
)

# Define graph settings
graph_settings = dict(
	line_width = 1,
)

# Define separator settings
separator_settings = dict(
	padding = 15,
)

# Define battery widget settings
battery_name = util.find_battery_name()
battery_settings   = dict(
	battery_name   = battery_name,
	low_percentage = 0.1,
	format         = "{percent:2.0%}",
)
battery_icon_settings = dict(
	battery_name = battery_name,
	theme_path   = os.path.expanduser("~/.config/qtile/icons/battery"),
)

def makeBar(screen):
	widgets = [
		# Groups
		FlexibleGroupBox(formatGroup, font_size=12),
		widget.Spacer(length=8),

		# Current layout
		MultiTextBox(formatLayout, hooks=update_hooks, font_size=12),
		widget.Spacer(length=8),

		# Current window
		MultiTextBox(formatTitle, hooks=update_hooks, font_size=12),
		widget.Spacer(length=bar.STRETCH),

		# CPU usage graph
		widget.Image(filename="~/.config/qtile/icons/cpu.png"),
		widget.CPUGraph(**graph_settings),
		widget.Sep(**separator_settings),

		# Memory usage graph
		widget.Image(filename="~/.config/qtile/icons/memory.png"),
		widget.MemoryGraph(**graph_settings),
		widget.Sep(**separator_settings),

		# Network usage graph
		widget.Image(filename="~/.config/qtile/icons/lan.png"),
		widget.NetGraph(**graph_settings),
		widget.Sep(**separator_settings),
	]

	if screen == 0:
		if battery_name:
			widgets.extend([
				# Battery widget
				widget.BatteryIcon(**battery_icon_settings),
				widget.Battery(**battery_settings),
			])

		widgets.extend([
			# System tray
			widget.Systray(),
			widget.Spacer(length=8),
		])

	widgets.extend([
		# Clock
		widget.Clock(format='%a %d %b %Y %H:%M:%S', font='xft:monospace', fontsize=12, foreground='#ffaa00'),
		widget.Spacer(length=8),
	])

	bg_color =  toQtileColor(background(screenColor(screen)))

	return bar.Bar(widgets, 20, background=bg_color)

# Define bars on screens
screens = [
	Screen(top=makeBar(0)),
]

def makeScreensConfig(qtile):
	''' Configure each screen found by qtile. '''
	screens = len(qtile.conn.pseudoscreens)
	return [Screen(top=makeBar(i)) for i in range(screens)]


# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size()),
	#Click([mod], "Button2", lazy.window.bring_to_front())
]

# Misc settings
dgroups_key_binder         = None
dgroups_app_rules          = []
follow_mouse_focus         = False
bring_front_click          = False
cursor_warp                = False
floating_layout            = layout.Floating(**layout_color)
auto_fullscreen            = False
focus_on_window_activation = "focus"
wmname                     = "LG3D" # Because Java is braindead.

@hook.subscribe.client_new
def floating_dialogs(window):
	dialog = window.window.get_wm_type() == 'dialog'
	transient = window.window.get_wm_transient_for()
	if dialog or transient:
		window.floating = True

@hook.subscribe.screen_change
def on_screen_change(qtile):
	qtile.cmd_restart()

def main(qtile):
	qtile.config.screens = makeScreensConfig(qtile)
