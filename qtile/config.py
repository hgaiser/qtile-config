from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import os
import subprocess

mod = "mod4"

keys = [
	# Switch between windows in current stack pane
	Key(
		[mod], "Right",
		lazy.layout.next()
	),
	Key(
		[mod], "Left",
		lazy.layout.previous()
	),

	# Move windows up or down in current stack
	Key(
		[mod, "shift"], "Right",
		lazy.layout.shuffle_down()
	),
	Key(
		[mod, "shift"], "Left",
		lazy.layout.shuffle_up()
	),

	# Swap with main window
	Key(
		[mod, "shift"], "Return",
		lazy.layout.swap_main()
	),

	# Swap panes of split stack
	Key(
		[mod, "shift"], "space",
		lazy.layout.rotate()
	),

	# Spawn terminal
	Key([mod], "Return", lazy.spawn("urxvt")),

	# Toggle between different layouts as defined below
	Key([mod], "space", lazy.next_layout()),

	# Kill current window
	Key([mod], "q", lazy.window.kill()),

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
	("2", "web"),
	("3", "mail"),
	("4", "chat"),
	("5", "doc"),
	("6", "misc"),
	("7", "viz"),
	("8", "8"),
	("9", "9")
]

# Create groups
groups = []
for key, name in groups_info:
	# append to list of groups
	groups.append(Group(name))

	# mod1 + letter of group = switch to group
	keys.append(
		Key([mod], key, lazy.group[name].toscreen())
	)

	# mod1 + shift + letter of group = switch to & move focused window to group
	keys.append(
		Key([mod, "shift"], key, lazy.window.togroup(name))
	)

layout_color = dict(
	border_focus  = '#004d99',
	border_normal = "#222222",
)

# Define layouts
layouts = [
	layout.MonadTall(**layout_color),
	layout.Matrix(**layout_color),
	layout.Wmii(**layout_color),
	layout.Zoomy(**layout_color)
]

# Define widget settings
widget_defaults = dict(
	font="xft:monospace:size=9:bold:antialias=true",
	fontsize=13,
	padding=3,
)

# Define bars on screens
battery_theme_path = os.path.expanduser("~/.config/qtile/icons/battery")
battery_name = "BAT1"
screens = [
	Screen(
		top=bar.Bar(
			[
				# Groups
				widget.GroupBox(
					borderwidth=1,
					highlight_method="block",
					inactive="#737373",
					this_current_screen_border="#2a52a2",
				),
				widget.Sep(padding=15),

				# Current layout
				widget.CurrentLayout(),
				widget.Sep(padding=15),

				# Current window
				widget.WindowName(),

				# CPU usage graph
				widget.Image(filename="~/.config/qtile/icons/cpu.png"),
				widget.CPUGraph(
					line_width=1,
				),
				widget.Sep(padding=15),

				# Memory usage graph
				widget.Image(filename="~/.config/qtile/icons/memory.png"),
				widget.MemoryGraph(
					line_width=1,
				),
				widget.Sep(padding=15),

				# Network usage graph
				widget.Image(filename="~/.config/qtile/icons/lan.png"),
				widget.NetGraph(
					line_width=1,
				),
				widget.Sep(padding=15),

				# System tray
				widget.Systray(),
				widget.BatteryIcon(battery_name=battery_name, theme_path=battery_theme_path),
				widget.Battery(battery_name=battery_name, low_percentage=0.1, format="{percent:2.0%}"),
				widget.Sep(padding=15),

				# Clock
				widget.Clock(format='%Y-%m-%d  %I:%M %p'),
			],
			25,
			background="#00394d",
		),
	),
]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(),
		start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),
		start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front())
]

# Misc settings
dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = False
focus_on_window_activation = "focus"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Autostart hook
@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([autostart_script])
