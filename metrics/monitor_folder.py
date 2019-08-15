import os

import win32file
import win32con

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}

FILE_LIST_DIRECTORY = 0x0001

class Win32NewFileMonitor(object):

    def __init__(self, folder):        
        self._folder = folder

    def __iter__(self):
        return self
    
    def __next__(self):
        return self._monitor_folder_for_new_files()

    def _monitor_folder_for_new_files(self):

        hDir = win32file.CreateFile (
                self._folder,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
                )

        while 1:
            results = win32file.ReadDirectoryChangesW (
                        hDir,
                        1024,
                        True,
                        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                        win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                        win32con.FILE_NOTIFY_CHANGE_SIZE |
                        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                        win32con.FILE_NOTIFY_CHANGE_SECURITY,
                        None,
                        None
                        )

            for action, file in results:
                if ACTIONS.get(action, "Unknown") == "Created":
                    full_filename = os.path.join(self._folder, file)
                    win32file.CloseHandle(hDir)
                    return full_filename
            

