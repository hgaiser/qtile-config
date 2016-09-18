from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import os
import subprocess

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

	# Move focus to primary screen
	Key([mod], "w", lazy.to_screen(0)),

	# Move focus to secondary screen
	Key([mod], "e", lazy.to_screen(1)),

	# Spawn terminal
	Key([mod], "Return", lazy.spawn("urxvt")),

	# Kill current window
	Key([mod], "c", lazy.window.kill()),

	# Toggle floating status
	Key([mod], "t", lazy.window.toggle_floating()),

	# Toggle fullscreen status
	Key([mod], "f", lazy.window.toggle_fullscreen()),

	Key([mod, "shift"], "q", lazy.restart()),
	#Key([mod, "control"], "q", lazy.shutdown()),
	Key([mod], "d", lazy.spawn("dmenu_run -i -b -fn 'DejaVu Sans Book-10'")),
]

# Define groups (key, name)
groups_info = [
	("1", "dev"),
	("2", "doc"),
	("3", "web"),
	("4", "media"),
	("5", "mus"),
	("6", "chat"),
	("7", "7"),
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

# Define layout color settings
layout_color = dict(
	border_focus  = '#004d99',
	border_normal = "#222222",
)

# Define layouts
layouts = [
	layout.MonadTall(name="Tall",    **layout_color),
	layout.Matrix(   name="Matrix",  **layout_color),
	layout.Wmii(     name="Stack",   **layout_color),
	layout.Zoomy(    name="Zoomy",   **layout_color),
	layout.Max(      name="Full",    **layout_color),
]

# Define GroupBox settings
group_settings = dict(
	borderwidth                = 1,
	highlight_method           = "block",
	inactive                   = "#737373",
	this_current_screen_border = "#3492B3",
	other_screen_border        = "#00171F",
	disable_drag               = True,
)

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
battery_name = "BAT1"
battery_settings   = dict(
	battery_name   = battery_name,
	low_percentage = 0.1,
	format         = "{percent:2.0%}",
)
battery_icon_settings = dict(
	battery_name = battery_name,
	theme_path   = os.path.expanduser("~/.config/qtile/icons/battery"),
)

def get_bar():
	return bar.Bar(
		[
			# Groups
			widget.GroupBox(**group_settings),
			widget.Sep(**separator_settings),

			# Current layout
			widget.CurrentLayout(),
			widget.Sep(**separator_settings),

			# Current window
			widget.WindowName(),

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

			# System tray
			widget.Systray(),
			widget.BatteryIcon(**battery_icon_settings),
			widget.Battery(**battery_settings),
			widget.Sep(**separator_settings),

			# Clock
			widget.Clock(format='%a %b %d %H:%M:%S'),
		],
		25,
		background=["#00394d", "#104E63"],
	)

# Define bars on screens
screens = [
	Screen(top=get_bar()),
	Screen(top=get_bar()),
]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position(),
		start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),
		start=lazy.window.get_size()),
	Drag([mod], "Button2", lazy.window.set_position_floating(),
		start=lazy.window.get_position()),
	#Click([mod], "Button2", lazy.window.bring_to_front())
]

# Misc settings
dgroups_key_binder         = None
dgroups_app_rules          = []
main                       = None
follow_mouse_focus         = False
bring_front_click          = True
cursor_warp                = False
floating_layout            = layout.Floating()
auto_fullscreen            = False
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.client_new
def floating_dialogs(window):
	dialog = window.window.get_wm_type() == 'dialog'
	transient = window.window.get_wm_transient_for()
	if dialog or transient:
		window.floating = True
