import PySimpleGUI as sg


def open_add_build_window(mngr):
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

    while True:
        event, values = add_build_window.Read()

        if event is None or event == 'Cancel':
            break

        if event == 'Ok':
            mngr.add_to_build_library(values[0], values[1], values[2])
            break

    add_build_window.close()


def open_build_lib_window(mngr):
    build_lib_column = [
        [sg.Button('Add')],
        [sg.Button('Remove')]
    ]

    build_lib_layout = [
        [sg.Listbox(values=mngr.get_builds(), key='-BUILDLIST-', size=(30, 10), enable_events=True), sg.Column(build_lib_column)],
        [sg.Listbox(values=[], key='-BUILDORDER-', size=(45, 20))],
        [sg.Button('Ok')]
    ]

    build_lib_window = sg.Window('Build Library', build_lib_layout)

    while True:
        event, values = build_lib_window.Read()

        if event is None or event == 'Ok':
            mngr.save_build_library()
            break

        if event == 'Add':
            open_add_build_window(mngr)
            build_lib_window['-BUILDLIST-'].Update(mngr.get_builds())

        if event == 'Remove':
            if '-BUILDLIST-' in values and len(values['-BUILDLIST-']) > 0:
                mngr.remove_from_build_library(values['-BUILDLIST-'][0])
                build_lib_window['-BUILDLIST-'].Update(mngr.get_builds())

        if event == '-BUILDLIST-' and len(values['-BUILDLIST-']):
            build_lib_window['-BUILDORDER-'].Update(values['-BUILDLIST-'][0].build)            

    build_lib_window.close()


def open_bod_window(mngr):
    bod_menu = [['Settings', ['Build Library...']]]

    bod_layout = [
        [sg.Menu(bod_menu, tearoff=True)],
        [sg.Text('Replay')],
        [sg.Input(), sg.FileBrowse()],
        [sg.Text('Player Name'), sg.InputText()],
        [sg.Multiline(disabled=True, key='-OUTPUT-', size=(45, 15))],
        [sg.Button('Analyze'), sg.Button('Exit')]
    ]

    bod_window = sg.Window('Build Order Deviation', bod_layout)

    while True:
        event, values = bod_window.Read()

        if event is None or event == 'Exit':
            break

        if event == 'Build Library...':
            open_build_lib_window(mngr)

        if event == 'Analyze':
            bod_window['-OUTPUT-'].Update(mngr.get_bod_results_from_replay(values[1], values[2]), append=True)

    bod_window.close()


if __name__ == '__main__':
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))

    from metrics.gui.mngr_bod_aio import MngrBodAio
    from metrics.build_order_library import BuildOrderLibrary
    from metrics.metric_factory.spawningtool_factory import SpawningtoolFactory

    bol = BuildOrderLibrary()
    try:
        #bol.load_library("C:/Users/matthew/Documents/Starcraft2Metrics/build_library.json")
        bol.load_library("build_library.json")
    except:
        pass

    mngr = MngrBodAio(bol, SpawningtoolFactory(), "build_library.json")
    open_bod_window(mngr)