from funcFile import timeInfor

def insertLog(listbox, message):
    listbox.insert("end", f"{timeInfor()} --> {message}\n")
    listbox.yview_moveto(1.0)

