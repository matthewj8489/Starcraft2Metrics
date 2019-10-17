import PySimpleGUI as sg

BUILD_LIBRARY_FILENAME = 'build_library.json'

def open_add_build_window():
    add_build_layout = [
        [sg.Text('Build Name')],
        [sg.InputText()],
        [sg.Text('Player Name')],
        [sg.InputText()],
        [sg.Text('Replay File')],
        [sg.Input(), sg.FileBrowse()],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    add_build_window = sg.Window('Add Build', add_build_layout)

    build_name = ''
    player_name = ''
    file_name = ''

    while True:
        event, values = add_build_window.Read()

        if event is None or event == 'Cancel':
            break

        if event == 'Ok':
            build_name = values[0]
            player_name = values[1]
            file_name = values[2]
            break

    add_build_window.close()

    return build_name, player_name, file_name


def open_build_lib_window():
    build_lib_column = [
        [sg.Button('Add')],
        [sg.Button('Remove')]
    ]

    build_lib_layout = [
        [sg.Listbox(values=['None'], key='-BUILDLIST-', size=(30, 3)), sg.Column(build_lib_column)],
        [sg.Button('Ok')]
    ]

    build_lib_window = sg.Window('Build Library', build_lib_layout)

    while True:
        event, values = build_lib_window.Read()

        if event is None or event == 'Ok':
            break

        if event == 'Add':
            build_name, player_name, file_name = open_add_build_window()
            

    build_lib_window.close()


def open_bod_window():
    bod_menu = [['Settings', ['Build Library...']]]

    bod_layout = [
        [sg.Menu(bod_menu, tearoff=True)],
        [sg.Text('Replay')],
        [sg.Input(), sg.FileBrowse()],
        [sg.Multiline(disabled=True, key='-OUTPUT-', size=(45, 15))],
        [sg.Button('Exit')]
    ]

    bod_window = sg.Window('Build Order Deviation', bod_layout)

    while True:
        event, values = bod_window.Read()

        if event is None or event == 'Exit':
            break

        if event == 'Build Library...':
            open_build_lib_window()

    bod_window.close()


if __name__ == '__main__':
    open_bod_window()