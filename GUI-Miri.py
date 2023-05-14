from tkinter import *
from tkinter import ttk
import json
from tkinter import messagebox


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

        # Treview

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background="#0099CC")
        self.tree = ttk.Treeview(self.group, show='headings', height=8)
        self.tree.pack()
        self.tree["columns"] = ("email","password", "ip", "approve", "pending")
        self.tree.heading("email", text="Email")
        self.tree.column("email", anchor='center')
        self.tree.heading("password", text="Password")
        self.tree.column("password", width=90, anchor='center')
        self.tree.heading("ip", text="IP")
        self.tree.column("ip", width=120, anchor='center')
        self.tree.heading("approve", text="Approved")
        self.tree.column("approve", width=70, anchor='center')
        self.tree.heading("pending", text="Pending")
        self.tree.column("pending", width=70, anchor='center')

        # group function
        self.group_func = LabelFrame(main, padx=5, pady=5)
        self.group_func.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.group_func, text="Add", command=self.add_config)
        self.add_button.grid(row=1, column=0, columnspan=5, pady=5)

        self.del_button = ttk.Button(self.group_func, text="Delete", command=self.delete_item)
        self.del_button.grid(row=2, column=0, columnspan=5, pady=5)


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
        with open('config', 'r+') as f:
            data = json.load(f)
            data.append({
                "email": email,
                "password": password,
                "IP": ip,
                "approve": 0,
                "pending": 0
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
                self.tree.insert("", "end", values=(email, password, ipaddress, approve, pending))
        # self.save_config()

    def delete_item(self):
        try:
            cur_item = self.tree.focus()
            item_data = self.tree.item(cur_item)["values"]
            if cur_item:
                self.tree.delete(cur_item)
            with open('config', 'r+') as f:
                data = json.load(f)
                for i, item in enumerate(data):
                    if item['email'] == item_data[0]:
                        del data[i]
                        break
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
            messagebox.showerror("Erorr", "Item not selected")

    def edit_item(self, event):
        cur_item = self.tree.focus()
        item_data = self.tree.item(cur_item)["values"]
        if item_data:
            x, y, width, height = self.tree.bbox(cur_item, "ip")
            self.edit_ip_entry = Entry(self.tree, width=width, justify='center')
            self.edit_ip_entry.place(x=x, y=y, width=width, height=height)
            self.edit_ip_entry.insert(0, item_data[1])
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
            email, password, ip, approve, pending = values
            data.append({
                "email": email,
                "password": password,
                "IP": ip,
                "approve": approve,
                "pending": pending
            })
        with open("config", "w") as f:
            json.dump(data, f)



if __name__ == "__main__":
    app = MiriCanvas()
    app.title("Auto Control MiriCanvas")
    app.mainloop()



# import tkinter as tk
# from tkinter import ttk

# # root window
# root = tk.Tk()
# root.geometry('400x300')
# root.title('Notebook Demo')

# # create a notebook
# notebook = ttk.Notebook(root)
# notebook.pack(pady=10, expand=True)

# # create frames
# frame1 = ttk.Frame(notebook, width=400, height=280)
# frame2 = ttk.Frame(notebook, width=400, height=280)

# frame1.pack(fill='both', expand=True)
# frame2.pack(fill='both', expand=True)

# # add frames to notebook

# notebook.add(frame1, text='General Information')
# notebook.add(frame2, text='Profile')


# root.mainloop()