import PySimpleGUI as sg
import gui_metrics_layout
import gui_file_list_builder as flb

window = gui_metrics_layout.getWindow()
win_flb = flb.GuiFileListBuilder()

while True:
    event, values = window.Read()

    if event is None or event == 'Exit':
        break
    if event == 'Refresh':
        window['-OUTPUT-'].Update('BOD\r\n'
                                  '---------\r\n'
                                  'Blink/Robo : 11.08%\r\n'
                                  'Chargelot All-in : 4.89%')

    if event == 'Add Build to Library...':
        win_flb.show_dialog()
        print(win_flb.file_list)

window.Close()

    