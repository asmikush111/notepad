
from tkinter import *
from tkinter import filedialog,messagebox,colorchooser,simpledialog

class Note:
    openfile=None

    def new(self,event=""):
            if  self.txt.get(0.0,END).strip():
                k=messagebox.askyesnocancel("save","Do you want to save this file?")
                if k==True:
                    self.save(self)
                    self.clear(self)
                elif k==False:
                    self.clear(self)
            root.title("Notepad-Untitled")

    def exit(self,event=""):
        if not self.txt.get(0.0,END).strip():
            quit()
        else:
            k = messagebox.askyesnocancel("save", "Do you want to save this file?")
            if k == True:
                self.save(self)
                quit()
            elif k == False:
                quit()


    def open(self,event=""):
        self.new(self)
        res = filedialog.askopenfile(initialdir="/", title="Select File to Open",
                                    filetype=(("Text File", "*.txt"), ("All File", "*.*")))
        self.openfile=res.name
        root.title("Notepad-"+res.name)
        for data in res:
            self.txt.insert(INSERT, data)




    def save(self, event=""):
        if self.openfile==None:
            self.saveas(self)
        else:
            f=open(self.openfile,mode="w")
            f.write(self.txt.get(1.0,END))
            f.close()
            self.openfile= None

    def saveas(self, event=""):
        res = self.txt.get(1.0, END)
        f = filedialog.asksaveasfile(mode='w', defaultextension=("Text File","*.txt"))
        f.write(res)
        self.openfile=None
        self.clear()
        f.close()

    def print(self,event=""):
        g=self.txt.get(1.0,END)
        print(g)

    def cut(self):
        self.copy()
        self.txt.delete('sel.first', 'sel.last')

    def copy(self,event=""):
        self.txt.clipboard_clear()
        self.txt.clipboard_append(self.txt.selection_get())


    def paste(self):
        self.txt.insert(INSERT, self.txt.clipboard_get())

    def delete(self,event=""):
        self.w2=self.txt.selection_get()
        i=self.txt.search(self.w2,1.0,END)
        l=int(i.split('.')[1])+len(self.w2)
        e=i.split('.')[0]+"."+str(l)
        self.j=i
        self.txt.delete(i,e)

    def sa(self,event=""):
        self.txt.clipboard_append(self.txt.get(0.0,END))
        print("\033[1;33;41m ",self.txt.get(0.0,END))


    def clear(self,event=""):
        self.txt.delete(1.0,END)

    def  bgcolor(self):
        c = colorchooser.askcolor()
        self.txt.configure(background=c[1])

    def fgcolor(self):
        c = colorchooser.askcolor()
        self.txt.configure(foreground=c[1])
    i=0
    fd=""
    def find(self,event=""):
        self.fd=simpledialog.askstring("title","Find What:")
        t=self.txt.get(1.0,END)
        self.i=int(t.find(self.fd))
        print(self.i)

    def replace(self,event=""):
        if self.fd=="":
            self.find()
        nw=simpledialog.askstring("title","Replace With:")
        t=self.txt.get(1.0,END)
        self.clear()
        self.txt.insert(INSERT,t.replace(self.fd,nw))
        fd=""


    def findnext(self):
        s = self.txt.search(self.fd, 1.0, END)
        l = int(s.split('.')[1]) + len(self.fd)
        e = s.split('.')[0] + "." + str(l)
        z=self.txt.search(self.fd, e, END)
        print(z[2])







    def __init__(self,master):
        master.title("Notepad-Untitled")
        master.wm_iconbitmap("notepad.ico")
        master.geometry("500x500+400+100")
        master.bind("<Alt-n>",self.new)
        master.bind("<Alt-o>", self.open)
        master.bind("<Alt-s>", self.saveas)
        master.bind("<Alt-p>", self.print)
        master.bind("<Alt-c>", self.copy)
        master.bind("<Alt-x>", self.cut)
        master.bind("<Alt-v>", self.paste)
        master.bind("<Alt-a>", self.sa)
        master.bind("<Alt-f>", self.find)
        master.bind("<Alt-h>", self.replace)

        self.outermenu=Menu(master)
        master.config(menu=self.outermenu)
        self.txt = Text(master,width=20,height=29,wrap=WORD,padx=10,pady=10,bd=5,selectbackground="red",undo=True)
        scroll = Scrollbar(root)
        scroll.config(command=self.txt.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.txt.pack(fill=BOTH, expand=1)

        self.filem=Menu(self.outermenu,tearoff=0)
        self.outermenu.add_cascade(label="File",menu=self.filem)

        self.filem.add_command(label="New", accelerator="Alt+n",command=self.new)
        self.filem.add_command(label="Open ", accelerator="Alt+o",command=self.open)
        self.filem.add_command(label="Save ", accelerator="Alt+s",command=self.save)
        self.filem.add_command(label="SaveAs ", accelerator="Alt+s ",command=self.saveas)
        self.filem.add_separator()
        self.filem.add_command(label="PageSetup")
        self.filem.add_command(label="Print", accelerator="Alt+p",command=self.print)
        self.filem.add_separator()
        self.filem.add_command(label="Exit",command=self.exit)

        self.editm=Menu(self.outermenu,tearoff=0)
        self.outermenu.add_cascade(label="Edit",menu=self.editm)

        self.editm.add_command(label="Undo",accelerator="Alt+z",command=self.txt.edit_undo)
        self.editm.add_command(label="Redo",accelerator="Alt+y",command=self.txt.edit_redo)
        self.editm.add_separator()
        self.editm.add_command(label="Cut",accelerator="Alt+x",command=self.cut)
        self.editm.add_command(label="Copy",accelerator="Alt+c",command=self.copy)
        self.editm.add_command(label="Paste",accelerator="Alt+v",command=self.paste)
        self.editm.add_command(label="Delete",accelerator="del",command=self.delete)
        self.editm.add_separator()
        self.editm.add_command(label="Find  ",accelerator="Alt+f",command=self.find)
        self.editm.add_command(label="FindNext",command=self.findnext)
        self.editm.add_command(label="Replace", accelerator="Alt+h",command=self.replace)
        self.editm.add_command(label="GoTo   ", accelerator="Alt+g")
        self.editm.add_separator()
        self.editm.add_command(label="SelectAll ", accelerator="Alt+a",command=self.sa)
        self.editm.add_command(label="Time/Date")

        self.formatm=Menu(self.outermenu,tearoff=0)
        self.outermenu.add_cascade(menu=self.formatm,label="Format")

        self.formatm.add_command(label="WordWrap")
        self.formatm.add_command(label="Font")
        self.formatm.add_command(label="BgColor",command=self.bgcolor)
        self.formatm.add_command(label="FgColor",command=self.fgcolor)

        self.viewm = Menu(self.outermenu,tearoff=0)
        self.outermenu.add_cascade(menu=self.viewm, label="View")

        self.viewm.add_command(label="Status")

        self.helpm = Menu(self.outermenu,tearoff=0)
        self.outermenu.add_cascade(menu=self.helpm, label="Help")

        self.helpm.add_command(label="ViewHelp")
        self.helpm.add_separator()
        self.helpm.add_command(label="About Notebook")




root=Tk()
b=Note(root)
mainloop()


