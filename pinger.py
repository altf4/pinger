#!/usr/bin/env python
#
# Pinger.py -- A ping tool that sits in your system tray
# Copyright 2013 Will Bradley
#
# Authors: Will Bradley <bradley.will@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of either or both of the following licenses:
#
# 1) the GNU Lesser General Public License version 3, as published by the 
# Free Software Foundation; and/or
# 2) the GNU Lesser General Public License version 2.1, as published by 
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the applicable version of the GNU Lesser General Public 
# License for more details.
#
# You should have received a copy of both the GNU Lesser General Public 
# License version 3 and version 2.1 along with this program.  If not, see 
# <http://www.gnu.org/licenses/>
#

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

# Timer
from gi.repository import GObject as gobject
# Pinging
import subprocess
# Regex
import re

# Vars
host = "4.2.2.2"

class HelloWorld:

  def ping(self, widget=None, data=None):
    ping = subprocess.Popen(
        ["ping", "-c", "1", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = ping.communicate()
    if error:
      label = "!! FAIL !!"
    else:
      m = re.search('time=(.*) ms', out)
      label = m.group(1)+" ms"
    ind.set_label (label, "100.0 ms")
    #self.ping_menu_item.set_label(out)
    gobject.timeout_add_seconds(self.timeout, self.ping)

  def destroy(self, widget, data=None):
    print "destroy signal occurred"
    Gtk.main_quit()

  def __init__(self):
    # register a periodic timer
    self.counter = 0
    self.timeout = 10
    gobject.timeout_add_seconds(self.timeout, self.ping)
    self.ping()


def menuitem_response(w, buf):
  print buf


def create_menu_item(menu, text, callback):

  menu_items = Gtk.MenuItem(text)

  menu.append(menu_items)

  menu_items.connect("activate", callback, text)

  # show the items
  menu_items.show()

  return menu_items

if __name__ == "__main__":
  ind = appindicator.Indicator.new (
                        "pinger",
                        "", #indicator-messages
                        appindicator.IndicatorCategory.COMMUNICATIONS)
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)
  #ind.set_attention_icon ("indicator-messages-new")
  ind.set_label ("0.0 ms", "100.0 ms")

  # create a menu
  menu = Gtk.Menu()

  # and the app
  hello = HelloWorld()

  # create menu items
  #hello.ping_menu_item = create_menu_item(menu, "Ping", hello.ping)
  create_menu_item(menu, "Exit", hello.destroy)

  # Add the menu to our statusbar
  ind.set_menu(menu)

  # Runtime loop
  Gtk.main()
