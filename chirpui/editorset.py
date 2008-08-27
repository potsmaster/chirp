#!/usr/bin/python
#
# Copyright 2008 Dan Smith <dsmith@danplanet.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import gtk

from chirp import ic9x, ic2820, ic2200, id800
import memedit

def radio_class_from_file(filename):
    size = os.stat(filename).st_size

    for cls in [ic2820.IC2820Radio, ic2200.IC2200Radio, id800.ID800v2Radio]:
        if cls._memsize == size:
            return cls

    raise Exception("Unknown file format")

class EditorSet(gtk.VBox):
    def __init__(self, filename):
        gtk.VBox.__init__(self, True, 0)
        self.filename = filename

        rclass = radio_class_from_file(filename)
        self.radio = rclass(filename)

        self.memedit = memedit.MemoryEditor(self.radio)

        self.pack_start(self.memedit.root)
        self.memedit.root.show()

    def save(self, fname=None):
        if not fname:
            fname = self.filename
        else:
            self.filename = fname

        self.radio.save_mmap(fname)

    def get_tab_title(self):
        return os.path.basename(self.filename)

