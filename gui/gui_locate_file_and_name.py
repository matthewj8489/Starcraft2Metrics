import PySimpleGUI as sg

class GuiLocateFileAndName(object):

    def __init__(self):
        self.filename = ""
        self.name = ""

        self._layout = [
            [sg.Text('Name', size=(15,1)), sg.InputText()],
            [sg.Text('Location', size=(15,1)), sg.Input(), sg.FileBrowse()],
            [sg.Button('Ok'), sg.Button('Cancel')]
        ]

    def show_dialog(self):
        window = sg.Window('Add File', self._layout)
        event, values = window.Read()
        self.name = values[0]
        self.filename = values[1]
        window.close()
        return event