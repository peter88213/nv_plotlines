"""A Plot lines import/export plugin for novelibre. 

Version @release

Adds a 'Add Story Templates' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_plotlines
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from nvlib.controller.plugin.plugin_base import PluginBase
from nvplotlineslib.md_plotlines import MdTemplate
from nvplotlineslib.nvplotlines_globals import Error
from nvplotlineslib.nvplotlines_globals import _
from nvplotlineslib.nvplotlines_globals import norm_path
import tkinter as tk


class Plugin(PluginBase):
    """A Plot lines import/export plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A Plot lines importer/exporter'
    URL = 'https://github.com/peter88213/nv_plotlines'
    _HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_plotlines/'

    FEATURE = _('Plot lines import/export')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._templatesMenu.entryconfig(f"{_('Load')}...", state='disabled')
        self._templatesMenu.entryconfig(f"{_('Save')}...", state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._templatesMenu.entryconfig(f"{_('Load')}...", state='normal')
        self._templatesMenu.entryconfig(f"{_('Save')}...", state='normal')

    def install(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            self._templateDir = f'{homeDir}/.novx/templates'
        except:
            self._templateDir = '.'

        # Create "Story Templates" submenu.
        self._templatesMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._templatesMenu.add_command(label=f"{_('Load')}...", command=self._load_template)
        self._templatesMenu.add_command(label=f"{_('Save')}...", command=self._save_template)
        self._templatesMenu.add_command(label=_('Open folder'), command=self._open_folder)

        # Create Tools menu entry.
        self._ui.toolsMenu.add_cascade(label=self.FEATURE, menu=self._templatesMenu)
        self._fileTypes = [(MdTemplate.DESCRIPTION, MdTemplate.EXTENSION)]

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Plot lines import/export plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def _load_template(self):
        """Create a structure of "Todo" chapters and scenes from a Markdown file."""
        fileName = filedialog.askopenfilename(
            filetypes=self._fileTypes,
            defaultextension=self._fileTypes[0][1],
            initialdir=self._templateDir
            )
        if fileName:
            try:
                templates = MdTemplate(fileName, self._mdl, self._ctrl)
                templates.read()
            except Error as ex:
                messagebox.showerror(_('Template loading aborted'), str(ex))

    def _new_project(self):
        """Create a novelibre project instance."""
        self._ctrl.new_project()
        self._load_template()

    def _open_folder(self):
        """Open the templates folder with the OS file manager."""
        try:
            os.startfile(norm_path(self._templateDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(self._templateDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(self._templateDir))
                    # Mac
                except:
                    pass

    def _save_template(self):
        """Save a structure of "Todo" chapters and scenes to a Markdown file."""
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=self._templateDir)
        if not fileName:
            return

        try:
            templates = MdTemplate(fileName, self._mdl, self._ctrl)
            templates.write()
        except Error as ex:
            messagebox.showerror(_('Cannot save template'), str(ex))

        self._ui.set_status(_('Template saved.'))

