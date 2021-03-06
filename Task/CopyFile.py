import os
import glib

def copyFileFromServer(strFileName):
    # File resides on server itself
    try:
        FileToBeCopied = open(strFileName+".txt", "r")
    except IOError:
        return "File not found."
    
    # File to be "copied" (downloaded) to Downloads folder
    try:
        # locate Downloads directory on local system
        downloadsDir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)
        NewFile = open(os.path.join(downloadsDir+"/"+strFileName+".txt"), 'w')
    except IOError:
        return "Error in downloading file."

    # Both files are open, hence begin copying
    string = FileToBeCopied.read()
    NewFile.write(string)
    
    FileToBeCopied.close()
    NewFile.close()
    
    if not FileToBeCopied.closed and not NewFile.closed:
        return "Error in downloading file."
    else:
        return "Download complete."
