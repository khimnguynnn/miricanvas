from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import threading
import sys
from time import sleep
from queue import Queue
sys.path.append('./lib')
from lib.seleniumFunc import *
from lib.funcFile import *
from lib.logger import *
from lib.miricanvasFunc import miricanvasFeature


class MiriCanvas(Tk):
    def __init__(self):
        super().__init__()

        tab_control = ttk.Notebook(self)
        main = ttk.Frame(tab_control)
        log = ttk.Frame(tab_control)
        tab_control.add(main, text='Main')
        tab_control.add(log, text='Log')
        tab_control.grid(row=0)

        # frame
        self.group = Frame(main, padx=5, pady=5)
        self.group.grid(row=0, column=0, padx=10, pady=10)
        
        # scrollbar treeview
        self.treescroll = ttk.Scrollbar(self.group)
        self.treescroll.pack(side=RIGHT, fill=Y)
        
        # Treview
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background="#0099CC")
        self.tree = ttk.Treeview(self.group, show='headings', height=8, yscrollcommand=self.treescroll.set)
        self.tree.pack()
        self.tree["columns"] = ("email","password", "ip", "approve", "pending", "balance")
        self.tree.heading("email", text="Email")
        self.tree.column("email", anchor='center')
        self.tree.heading("password", text="Password")
        self.tree.column("password", width=90, anchor='center')
        self.tree.heading("ip", text="IP")
        self.tree.column("ip", width=145, anchor='center')
        self.tree.heading("approve", text="Approved")
        self.tree.column("approve", width=80, anchor='center')
        self.tree.heading("pending", text="Pending")
        self.tree.column("pending", width=85, anchor='center')
        self.tree.heading("balance", text="Balance (USD)")
        self.tree.column("balance", width=100, anchor='center')
        
        # link scrollbar to treeview
        self.treescroll.config(command=self.tree.yview)
        
        # group control account
        self.group_func = LabelFrame(main, text="Main Control", padx=42, pady=5)
        self.group_func.grid(row=1, column=0, rowspan=2, columnspan=2)
        self.add_button = ttk.Button(self.group_func, text="Add", command=self.add_config)
        self.add_button.grid(row=0, column=0, pady=5, padx=5, sticky=W)
        self.del_button = ttk.Button(self.group_func, text="Delete", command=self.delete_item)
        self.del_button.grid(row=0, column=1, pady=5, padx=5, sticky=W)
        
        # group main
        self.startButton = ttk.Button(self.group_func, text="Start", command=self.startThread)
        self.startButton.grid(row=0, column=3, pady=5, padx=5)
        self.stopButton = ttk.Button(self.group_func, text="Stop", command=self.StopProgram)
        self.stopButton.grid(row=0, column=4, pady=5, padx=5)
        self.label_count = Label(self.group_func, text="Packs per Acc")
        self.label_count.grid(row=0, column=7, rowspan=2, sticky=N)
        self.entry_elements = ttk.Entry(self.group_func, width=14)
        self.entry_elements.grid(row=0, column=7, rowspan=2, sticky=S)
        self.entry_elements.insert(0, "10")

        self.openButton = ttk.Button(self.group_func, text="Open Profile", command=self.threadOpenProfile)
        self.openButton.grid(row=0, column=5, pady=5, padx=5)
        self.checkbox_var = IntVar()
        self.checkbox = ttk.Checkbutton(self.group_func, text="Loop", variable=self.checkbox_var)
        self.checkbox.grid(row=0, column=6, pady=10, padx=10, sticky=E)

        #textbox for logging
        self.frame_log = Frame(log)
        self.frame_log.grid(row=0, column=0, padx=5, pady=5)
        self.scrollbar = Scrollbar(self.frame_log)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.logbox = Listbox(self.frame_log, height=18, width=117, yscrollcommand=self.scrollbar.set)
        self.logbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config( command = self.logbox.yview)
        
        #catch handle and load config
        self.LoadConfig()
        self.tree.bind('<Return>', self.edit_item)
        self.tree.bind("<Delete>", lambda event: self.delete_item())
        self.edit_ip_entry = None

    def add_config(self):
    # Tạo hộp thoại để nhập thông tin cấu hình
        add_window = Toplevel(self)
        add_window.title("Add Config")
        email_label = Label(add_window, text="Email:")
        email_label.grid(row=0, column=0, sticky=W)
        email_entry = Entry(add_window, width=30)
        email_entry.grid(row=0, column=1)
        passw_label = Label(add_window, text="Password:")
        passw_label.grid(row=1, column=0, sticky=W)
        passw_entry = Entry(add_window, width=30)
        passw_entry.grid(row=1, column=1)
        proxy_label = Label(add_window, text="Proxy:")
        proxy_label.grid(row=2, column=0, sticky=W)
        proxy_entry = Entry(add_window, width=30)
        proxy_entry.grid(row=2, column=1)
        save_button = Button(add_window, text="Save", command=lambda: self.saveAccount(email_entry.get(), passw_entry.get(), proxy_entry.get(), add_window))
        save_button.grid(row=4, column=0, columnspan=2)


    def saveAccount(self, email, password, ip, window):
        if ip == "":
            ip = None
        with open('config', 'r+') as f:
            data = json.load(f)
            data.append({
                "email": email,
                "password": password,
                "IP": ip,
                "approve": 0,
                "pending": 0,
                "balance": 0
            })
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            
        window.destroy()
        self.LoadConfig()


    def LoadConfig(self):
        self.tree.delete(*self.tree.get_children())
        with open('config', 'r') as f:
            data = json.load(f)
            for item in data:
                email = item.get("email")
                password = item.get("password")
                ipaddress = item.get("IP")
                approve = item.get("approve")
                pending = item.get("pending")
                balance = item.get("balance")
                self.tree.insert("", "end", values=(email, password, ipaddress, approve, pending, balance))
        # self.save_config()

    def delete_item(self):
        selection = self.tree.selection()
        if (len(selection)) < 1:
            messagebox.showerror("Error", "Not Select Item Yet")
            return
        for item in selection:
            values = self.tree.item(item)['values']
            if selection:
                self.tree.delete(item)
            with open('config', 'r+') as f:
                data = json.load(f)
                for i, item in enumerate(data):
                    if item['email'] == values[0]:
                        del data[i]
                        break
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()



    def edit_item(self, event):
        cur_item = self.tree.focus()
        item_data = self.tree.item(cur_item)["values"]
        if item_data:
            x, y, width, height = self.tree.bbox(cur_item, "ip")
            self.edit_ip_entry = Entry(self.tree, width=width, justify='center')
            self.edit_ip_entry.place(x=x, y=y, width=width, height=height)
            self.edit_ip_entry.insert(0, item_data[2])
            self.edit_ip_entry.focus()
            self.edit_ip_entry.bind("<Return>", lambda event: self.update_ip(cur_item))

    def update_ip(self, cur_item):
        new_ip = self.edit_ip_entry.get()
        self.tree.set(cur_item, "ip", new_ip)
        self.save_config()
        self.edit_ip_entry.destroy()


    def save_config(self):
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            email, password, ip, approve, pending, balance = values
            data.append({
                "email": email,
                "password": password,
                "IP": ip,
                "approve": approve,
                "pending": pending,
                "balance": balance
            })
        with open("config", "w") as f:
            json.dump(data, f)

    def GetChildren(self, openProfile=None):
        children = []
        items = []
        if openProfile == None:
            selected_items = self.tree.selection()
            if selected_items:
                for item in selected_items:
                    values = self.tree.item(item, 'values')
                    children.append(values)
                    items.append(item)
            else:
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    children.append(values)
                    items.append(item)
            
        else:
            selected_items = self.tree.selection()
            if selected_items:
                for item in selected_items:
                    values = self.tree.item(item, 'values')
                    children.append(values)
                    items.append(item)
            else:
                children = None
                items = None
        return children, items

    def update_columns(self, child, approved, pending, balance):

        self.tree.set(child, "#4", approved)
        self.tree.set(child, "#5", pending)
        self.tree.set(child, "#6", balance)
        self.save_config()

    def threadOpenProfile(self):
        threading.Thread(target=self.openProfile).start()

    def openProfile(self):
        childs, items = self.GetChildren(openProfile="openProfile")
        
        if items is None:
            messagebox.showerror("Error", "Not Select Account Yet")
            return
        
        for index, child in enumerate(childs):
            email = child[0]
            passwd = child[1]
            prx = child[2]
            cookie_result = Queue()
            insertLog(self.logbox, f"Start Open Profile {email}")
            thread = threading.Thread(target=openChrome, args=(email, passwd, prx, "OK", cookie_result))
            thread.start()
            sleep(3)
            thread.join()
            self.updateAccountInfo(items[index], cookie_result.get(), email, prx)
            
    def find_value(self, value):
        items = self.tree.get_children()  
        for item in items:
            item_value = self.tree.item(item)['values'][0]  
            if item_value == value:
                return self.tree.item(item)['values'][-1]
        return None

    def reStateofTkinter(self, state):
        self.startButton["state"] = state
        self.checkbox["state"] = state
        self.entry_elements["state"] = state
        self.checkbox["state"] = state
    
    def updateAccountInfo(self, item, cookie, email, prx):

        miri = miricanvasFeature(cookie, prx)
        pendingEle =miri.PendingElements()
        approvedEle = miri.ApprovedElements()
        balance = miri.checkBalance()
        
        rowItem = self.find_value(email)
        
        insertLog(self.logbox, f"Account {email} found {pendingEle} Elements Pending")
        insertLog(self.logbox, f"Account {email} found {approvedEle} Elements Approved")
        insertLog(self.logbox, f"Account {email} Balance change from {rowItem} USD to {balance} USD")
        self.update_columns(item, approvedEle, pendingEle, balance)
        insertLog(self.logbox, f"Account {email} successful update information")


    #---------------------------------------------------------------------------------------------------#
    def threadStop(self):
        threading.Thread(target=self.StopProgram).start()

    def StopProgram(self):
        insertLog(self.logbox, f"Program is Stopping --> Wait")
        messagebox.showwarning("Notification", "Program is Stopping")
        self.isStopped = True
    #---------------------------------------------------------------------------------------------------#
    def startThread(self):
        self.isStopped = False
        insertLog(self.logbox, "Application started")
        self.reStateofTkinter("disabled")
        try:

            self.eleCounts = int(self.entry_elements.get())
            self.childs, self.items = self.GetChildren()
            self.looping = self.checkbox_var.get()

        except:
            messagebox.showerror("Error", "Element Count not Input yet")
            self.reStateofTkinter("enabled")
            return
        
        newThread = threading.Thread(target=self.MainUpload)
        newThread.start()


    def MainUpload(self):

        for indexx, child in enumerate(self.childs):

            email = child[0]
            passwd = child[1]
            prx = child[2]
            insertLog(self.logbox, f"Currently Logged Account {email}")
            driver = openChrome(email, passwd, prx)
            sleep(3)
            cookie = getCookies(driver)
            self.miriClass = miricanvasFeature(cookie, prx)
            
            insertLog(self.logbox, f"Got cookie for requesting {cookie}")
            handle_count = 0
            for _ in range (5):
                try:
                    memId = self.miriClass.memberID()
                    break
                except:
                    handle_count += 1
                    continue
            if handle_count == 5:
                insertLog(self.logbox, f"Account {email} get error --> skip {email} account") 
                continue
            
            insertLog(self.logbox, f"Got Member ID for requesting {memId}") 
            for iii in range(0, self.eleCounts):
                while True:

                    try:
                        folderEle = random.choice(getImageFolders())

                    except:

                        insertLog(self.logbox, f"Cannot Select Folder")
                        driver.quit()
                        return
                    
                    try:
                        insertLog(self.logbox, f"Folder Selected {folderEle}")
                        elements = getItemsInFolder(folderEle)
                        insertLog(self.logbox, f"Checking Element in folder {folderEle}")
                        if len(elements) < 2:
                            insertLog(self.logbox, f"No Elements Found in Folder --> Folder {folderEle} Removed")
                            RemoveEmptyFolder(folderEle)
                            continue
                        else:
                            insertLog(self.logbox, f"Got {len(elements)} Elements in Folder {folderEle}")
                            break

                    except Exception as e:
                        insertLog(self.logbox, e)
                        continue

                    
                insertLog(self.logbox, f"Redirect to Upload Dashboard")

                driver.get("https://designhub.miricanvas.com/element/upload")
                sleep(3)
                eleToPlus = []

                for j in range(len(elements)):
                    try:
                        eleToPlus.append(elements[j])
                    except:
                        pass
                
                string_Path = plusImages(folderEle, eleToPlus)
                insertLog(self.logbox, f"Started Upload Pack {folderEle} pack {iii+1}/{self.eleCounts}")

                if UploadtoMiris(driver, string_Path):
                    eleid, name = self.miriClass.getElementsID()

                    for index, ele in enumerate(eleid):
                        redis_break = 0
                        for _ in range(5):
                            try:
                                arrHashtag, source = hashtagList(name[index])
                                insertLog(self.logbox, f"keyword [{name[index].upper()}] success get from {source.upper()}")
                                redis_break = 0
                                break
                            except:
                                insertLog(self.logbox, f"error check from redis")
                                sleep(1)
                                redis_break += 1
                        
                        if redis_break > 0: 
                            insertLog(self.logbox, f"Connection Failed to Redis")
                            self.reStateofTkinter("enabled")
                            driver.quit()
                            return
                        
                        if self.miriClass.submitItem(ele, name[index], arrHashtag):

                            insertLog(self.logbox, f"Account {email} success upload element --> {name[index]}.svg")

                        else:
                            insertLog(self.logbox, f"Account {email} failed upload element --> {name[index]}.svg")
                            self.miriClass.DeleteErrorElement(ele)
                            insertLog(self.logbox, f"Success Delete Error Element --> {name[index]}.svg")
                            
                for ele in eleToPlus:

                    DelImage(folderEle, ele)

            self.updateAccountInfo(self.items[indexx], cookie, email, prx)
            driver.quit()

            if self.isStopped == True:
                
                insertLog(self.logbox, f"Program Stopped at account {email}")
                self.reStateofTkinter("enabled")

                return

        if self.looping == 1:

            insertLog(self.logbox, f"Start Looping All Account")
            self.MainUpload()

        self.reStateofTkinter("enabled")
        insertLog(self.logbox, "All Done")

if __name__ == "__main__":
    app = MiriCanvas()
    app.title("Auto Control MiriCanvas")
    app.resizable(width=False, height=False)
    app.iconbitmap("icon.ico")
    app.mainloop()