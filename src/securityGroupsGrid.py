import curses
import threading
import time

import npyscreen
import pyperclip

import main
import selectableGrid
import securityRulesForm
import virtualMachine
import createVm
import popup


class SecurityGroupsGrid(selectableGrid.SelectableGrid):
    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords, column_width=20)
        self.refresh()
        self.col_titles = ["SECURITY GROUPS ID", "SECURITY GROUPS NAME"]
        groups = main.GATEWAY.ReadSecurityGroups()["SecurityGroups"]
        values = list()
        for g in groups:
            values.append([g["SecurityGroupId"], g["SecurityGroupName"]])
        self.values = values

        def on_selection(line):
            popup.editSecurityGroup(self.form, line)

        self.on_selection = on_selection

class SecurityGroupsGridForOneInstance(selectableGrid.SelectableGrid):
    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords, column_width=20)
        self.refresh()
        self.col_titles = ["SECURITY GROUPS ID", "SECURITY GROUPS NAME"]
        groups = main.VM["SecurityGroups"]
        values = list()
        for g in groups:
            values.append([g["SecurityGroupId"], g["SecurityGroupName"]])
        self.values = values

        def on_selection(line):
            popup.editSecurityGroup(self.form, line)

        self.on_selection = on_selection

