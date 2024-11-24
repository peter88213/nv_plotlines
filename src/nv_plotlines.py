"""A Plot lines view plugin for novelibre. 

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
from pathlib import Path
from tkinter import ttk

from nvlib.controller.plugin.plugin_base import PluginBase
from nvplotlineslib.nvplotlines_globals import _
from nvtlviewlib.nvtlview_globals import open_help
import tkinter as tk


class Plugin(PluginBase):
    """A Plot lines import/export plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A Plot lines importer/exporter'
    URL = 'https://github.com/peter88213/nv_plotlines'
    _HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_plotlines/'

    FEATURE = _('Plot lines view')
    SETTINGS = dict(
        window_geometry='600x800',
    )
    OPTIONS = dict(
    )

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._plButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._plButton.config(state='normal')

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
        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.novx/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/plview.ini'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._open_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Plot lines view Online help'), command=open_help)

        #--- Configure the toolbar.
        self._configure_toolbar()

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None
        try:
            tlIcon = tk.PhotoImage(file=f'{iconPath}/plview.png')
        except:
            tlIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._tlButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=self.FEATURE,
            image=tlIcon,
            command=self._open_viewer
            )
        self._tlButton.pack(side='left')
        self._tlButton.image = tlIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._tlButton, self._tlButton['text'])

    def _open_viewer(self):
        if not self._mdl.prjFile:
            return

