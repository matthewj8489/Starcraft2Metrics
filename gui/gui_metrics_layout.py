import PySimpleGUI as sg

def getWindow():
    menu_def = [['Settings', ['Add Replay Folder...', 'Add Build to Library...']]]

    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Frame(layout=[
            [sg.Checkbox('Include vs A.I.')],
            [sg.Text('Past Games to Average'), sg.Spin(values=["{:02d}".format(x) for x in range(1, 61)], initial_value=30)]], title='Analysis and Display Options', relief=sg.RELIEF_SUNKEN)],
        [sg.Multiline(disabled=True, key='-OUTPUT-', size=(45, 15)), sg.Image('C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\gui\\Acropolis.png')],
        [sg.Button('Refresh'), sg.Button('Exit')],
    ]

    window = sg.Window('Replay Analysis', layout)

    return window