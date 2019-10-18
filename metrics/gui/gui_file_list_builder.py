import PySimpleGUI as sg
from gui_locate_file_and_name import GuiLocateFileAndName

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

        def __str__(self):
            return "{}".format(self.name)

    def __init__(self, file_list = []):
        self.file_list = file_list
        self._tmp_file_list = file_list.copy()

        # Main window
        self._column1 = [[sg.Button('Add')],
                [sg.Button('Edit')],
                [sg.Button('Remove')]]

        self._layout = [
            [sg.Listbox(values=self._tmp_file_list,  key='-FILELIST-', size=(30, 3)), sg.Column(self._column1)],
            [sg.Button('Ok')]
        ]

        self.window = sg.Window('File Locations', self._layout)


    def show_dialog(self):
        while True:
            event, values = self.window.Read()

            if event == 'Add':
                loc_file = GuiLocateFileAndName()
                event_add = loc_file.show_dialog()
                if event_add == 'Ok':
                    self._tmp_file_list.append(GuiFileListBuilder.FileListTuple(loc_file.name, loc_file.filename))
                    self.window['-FILELIST-'].Update(self._tmp_file_list)
                    
            if event == 'Ok':
                self.file_list = self._tmp_file_list
                break

            if event == 'Cancel':
                break

        self.window.Close()


# if __name__ == '__main__':
#     showFileListBuilder()