import PySimpleGUI as sg


# def showFileListBuilder():
#     # Add file
#     layout_add = [
#         [sg.Text('Name', size=(15,1)), sg.InputText()],
#         [sg.Text('Location', size=(15,1)), sg.Input(), sg.FolderBrowse()],
#         [sg.Button('Ok'), sg.Button('Cancel')]
#     ]


#     # Main window
#     column1 = [[sg.Button('Add')],
#             [sg.Button('Edit')],
#             [sg.Button('Remove')]]

#     layout = [
#         [sg.Listbox(values=('Name1 : Location1', 'Name2 : Location2'), size=(30, 3)), sg.Column(column1)],
#         [sg.Button('Ok')]
#     ]

#     window = sg.Window('File Locations', layout)

#     while True:
#         event, values = window.Read()

#         if event == 'Add':
#             one_shot_win = sg.Window('Add File', layout_add)
#             event_add, values_add = one_shot_win.Read()
#             if event_add == 'Ok':
#                 one_shot_win.Close()
#             if event_add == 'Cancel':
#                 one_shot_win.Close()
                
#         if event == 'Ok':
#             break

#         if event == 'Cancel':
#             break

#     window.Close()

class GuiFileListBuilder(object):

    class FileListTuple(object):
        def __init__(self, fn, nm):
            self.filename = fn
            self.name = nm

    def __init__(self):
        self.file_list = []

        # Add file
        self._layout_add = [
            [sg.Text('Name', size=(15,1)), sg.InputText()],
            [sg.Text('Location', size=(15,1)), sg.Input(), sg.FolderBrowse()],
            [sg.Button('Ok'), sg.Button('Cancel')]
        ]


        # Main window
        self._column1 = [[sg.Button('Add')],
                [sg.Button('Edit')],
                [sg.Button('Remove')]]

        self._layout = [
            [sg.Listbox(values=('Name1 : Location1', 'Name2 : Location2'), size=(30, 3)), sg.Column(self._column1)],
            [sg.Button('Ok')]
        ]

        self.window = sg.Window('File Locations', self._layout)


    def show_dialog(self):
        while True:
            event, values = self.window.Read()

            if event == 'Add':
                one_shot_win = sg.Window('Add File', self._layout_add)
                event_add, values_add = one_shot_win.Read()
                if event_add == 'Ok':
                    self.file_list.append(GuiFileListBuilder.FileListTuple(values_add[0], values_add[1]))
                    one_shot_win.Close()
                if event_add == 'Cancel':
                    one_shot_win.Close()
                    
            if event == 'Ok':
                break

            if event == 'Cancel':
                break

        self.window.Close()


# if __name__ == '__main__':
#     showFileListBuilder()