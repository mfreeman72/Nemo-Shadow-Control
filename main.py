#!/usr/bin/env python
import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Path to the gtk.css file
CSS_FILE_PATH = os.path.expanduser("~/.config/gtk-3.0/gtk.css")


class ShadowControl(Gtk.Window):
    css_contents = ""

    def __init__(self):
        # Load or create gtk.css file
        if not os.path.exists(CSS_FILE_PATH):
            with open(CSS_FILE_PATH, 'w') as css_file:
                css_file.write("")
        else:
            with open(CSS_FILE_PATH, 'r') as css_file:
                self.css_contents = css_file.read()

        # Find values from css file
        override_set = False
        horiz = 0
        vert = 0
        radius = 3
        override_check = self.css_contents.find("/* Custom drop shadow settings for Nemo */")
        if override_check != -1:
            override_set = True
            horiz = int(self.css_contents[self.css_contents.find("text-shadow:", override_check)+13:self.css_contents.find("text-shadow:", override_check)+14])
            vert = int(self.css_contents[self.css_contents.find("text-shadow:", override_check)+17:self.css_contents.find("text-shadow:", override_check)+18])
            radius = int(self.css_contents[self.css_contents.find("text-shadow:", override_check)+21:self.css_contents.find("text-shadow:", override_check)+22])

        # Create window
        Gtk.Window.__init__(self, title="Drop Shadow Control")
        self.set_default_size(400, 300)
        self.set_border_width(10)

        # Create a box to contain widgets
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        self.add(box)

        box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(box1)

        # Gradient toggle
        self.gradient_switch = Gtk.Switch()
        self.gradient_switch.set_active(override_set)
        self.gradient_switch.connect("notify::active", self.on_gradient_switch_activated)
        box1.pack_start(Gtk.Label(label="Enable Gradient Shadow:"), True, True, 0)
        box1.pack_start(self.gradient_switch, False, False, 0)

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box2)

        # Shadow radius slider
        self.radius_adjustment = Gtk.Adjustment(radius, 0, 10, 1, 10, 0)
        self.radius_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.radius_adjustment)
        self.radius_slider.set_digits(0)
        self.radius_slider.connect("value-changed", self.on_radius_slider_changed)
        box2.pack_start(Gtk.Label(label="Shadow Radius:"), True, True, 0)
        box2.pack_start(self.radius_slider, False, False, 0)

        # Shadow direction sliders
        self.horizontal_adjustment = Gtk.Adjustment(horiz, -5, 5, 1, 10, 0)
        self.vertical_adjustment = Gtk.Adjustment(vert, -5, 5, 1, 10, 0)

        self.horizontal_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                           adjustment=self.horizontal_adjustment)
        self.horizontal_slider.set_digits(0)
        self.horizontal_slider.connect("value-changed", self.on_horizontal_slider_changed)
        box2.pack_start(Gtk.Label(label="Shadow Horizontal Distance:"), True, True, 0)
        box2.pack_start(self.horizontal_slider, False, False, 0)

        self.vertical_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.vertical_adjustment)
        self.vertical_slider.set_digits(0)
        self.vertical_slider.connect("value-changed", self.on_vertical_slider_changed)
        box2.pack_start(Gtk.Label(label="Shadow Vertical Distance:"), True, True, 0)
        box2.pack_start(self.vertical_slider, False, False, 0)

        box.pack_start(box1, False, False, 0)
        box.pack_start(box2, False, False, 0)

        self.update_css(self.css_contents)

    def append_css(self, contents, new_contents):
        start = contents.find("/* Custom drop shadow settings for Nemo */")
        end = contents.find("/* End of custom drop shadow settings for Nemo */")
        temp_contents_start = contents[0:start]
        if end != -1:
            temp_contents_end = contents[end + 50:]
        else:
            temp_contents_end = ""
        contents = temp_contents_start + new_contents + temp_contents_end
        return contents

    def update_css(self, contents):
        if self.gradient_switch.get_active():
            write_string = self.append_css(contents, f"""/* Custom drop shadow settings for Nemo */
/* DO NOT edit this section */
.nemo-desktop.nemo-canvas-item {{
    color: #fff;
    text-shadow: {int(self.horizontal_adjustment.get_value())}px {int(self.vertical_adjustment.get_value())}px {int(self.radius_adjustment.get_value())}px #000, {int(self.horizontal_adjustment.get_value())}px {int(self.vertical_adjustment.get_value())}px {int(self.radius_adjustment.get_value())}px #000;
}}
.nemo-desktop.nemo-canvas-item:hover {{
    background-color: alpha(@theme_selected_bg_color, 0.33);
    background-image: none;
}}
.nemo-desktop.nemo-canvas-item:selected {{
    background-color: @theme_selected_bg_color;
    background-image: none;
    color: @theme_selected_fg_color;
    text-shadow: none;
}}
/* End of custom drop shadow settings for Nemo */
""")
        else:
            write_string = self.append_css(contents, f"")
        with open(CSS_FILE_PATH, 'w') as css_file:
            css_file.write(write_string)

    def on_gradient_switch_activated(self, switch, value):
        self.update_css(self.css_contents)

    def on_radius_slider_changed(self, scale):
        self.update_css(self.css_contents)

    def on_horizontal_slider_changed(self, scale):
        self.update_css(self.css_contents)

    def on_vertical_slider_changed(self, scale):
        self.update_css(self.css_contents)


win = ShadowControl()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
