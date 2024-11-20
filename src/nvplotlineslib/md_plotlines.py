"""Provide a class for Markdown story template representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_plotlines
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvplotlineslib.nvplotlines_globals import PL_ROOT
from nvplotlineslib.nvplotlines_globals import Error
from nvplotlineslib.nvplotlines_globals import _
from nvplotlineslib.nvplotlines_globals import norm_path


class MdTemplate:
    """Markdown story template representation.
    
    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 
    """
    DESCRIPTION = _('Story Template')
    EXTENSION = '.md'

    def __init__(self, filePath, model, controller):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            model -- Reference to the model instance of the application.
            controller -- Reference to the main controller instance of the application.
        """
        self.filePath = filePath
        self._mdl = model
        self._ctrl = controller

    def read(self):
        """Parse the Markdown file and create plot lines and plot points.
        
        Raise the "Error" exception in case of error. 
        """
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                mdLines = f.readlines()
        except(FileNotFoundError):
            raise Error(f'{_("File not found")}: "{norm_path(self.filePath)}".')

        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        targetNode = None
        newElement = None
        desc = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.desc = ''.join(desc).strip().replace('  ', ' ')
                    desc = []
                    newElement = None
                if mdLine.startswith('## '):
                    if targetNode is None:
                        continue

                    # Add a plot point.
                    newTitle = mdLine[3:].strip()
                    ppId = self._ctrl.add_plot_point(targetNode=targetNode, title=newTitle)
                    newElement = self._mdl.novel.plotPoints[ppId]
                elif mdLine.startswith('# '):
                    # Add a plot line.
                    newTitle = mdLine[2:].strip()
                    plId = self._ctrl.add_plot_line(targetNode=targetNode, title=newTitle)
                    targetNode = plId
                    newElement = self._mdl.novel.plotLines[plId]
            elif mdLine:
                desc.append(f'{mdLine} ')
            else:
                desc.append('\n')
        try:
            newElement.desc = ''.join(desc).strip().replace('  ', ' ')
        except AttributeError:
            pass

    def write(self):
        """Iterate the project structure and write the new elements to a Markdown file.
        
        Raise the "Error" exception in case of error. 
        """
        mdLines = []
        for plId in self._mdl.novel.tree.get_children(PL_ROOT):
            mdLines.append(f'# {self._mdl.novel.plotLines[plId].title}')
            desc = self._mdl.novel.plotLines[plId].desc
            if desc:
                mdLines.append(desc.replace('\n', '\n\n'))
            for ppId in self._mdl.novel.tree.get_children(plId):
                mdLines.append(f'## {self._mdl.novel.plotPoints[ppId].title}')
                desc = self._mdl.novel.plotPoints[ppId].desc
                if desc:
                    mdLines.append(desc.replace('\n', '\n\n'))

        content = '\n\n'.join(mdLines)
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

