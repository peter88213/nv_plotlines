"""Provide a service class for the plotline viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_plotlines
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from mvclib.controller.sub_controller import SubController


class PlotlinesService(SubController):
    SETTINGS = dict(
        window_geometry='600x800',
    )
    OPTIONS = dict(
    )

    def __init__(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self.plotlineView = None

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
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

    def start_viewer(self, windowsTitle):
        if not self._mdl.prjFile:
            return

        print(windowsTitle)
