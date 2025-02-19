import npyscreen
import pyperclip

import main
import popup
import selectableGrid

class Grid(selectableGrid.SelectableGrid):
    def __init__(self, screen,  *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.col_titles = ["Id", "Net Id", "Service Name", "State"]

        def on_selection(line):
            popup.editNetAccessPoint(self.form, line)

        self.on_selection = on_selection
        
    def refresh(self, name_filter=None):
        groups = main.GATEWAY.ReadNetAccessPoints(form=self.form)['NetAccessPoints']
        values = list()
        for g in groups:
            values.append([g['NetAccessPointId'], g['NetId'], g['ServiceName'],
                           g['State']])
        self.values = values

    def custom_print_cell(self, cell, cell_value):
        #Cheking if we are in the table and not in the title's row.
        if not isinstance(cell.grid_current_value_index, int):
            y, _ = cell.grid_current_value_index
            state = self.values[y][3]
            cell.highlight_whole_widget = True
            if state == "deleted":
                cell.color = "DANGER"
            else:
                cell.color = "GOODHL"
