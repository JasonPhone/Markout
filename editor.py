# coding=utf-8
import sys
import os
import tkinter as tk
import tkinter.filedialog
import webbrowser as browser
import mdparser as mk


class Note():
    def __init__(self):
        self.fname = ""
        self.filename = ""

    def show(self):
        self.tk = tk.Tk()
        self.tk.title("Markout alpha")
        self.createUI()
        self.tk.mainloop()

    def createUI(self):
        # create menu
        menubar = tk.Menu(self.tk)
        fmenu = tk.Menu(menubar, tearoff=0)
        fmenu.add_command(label='Open', command=self.open)
        fmenu.add_command(label='Save', command=self.save)
        fmenu.add_command(label='Render', command=self.render)
        fmenu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label="File", menu=fmenu)
        self.tk.config(menu=menubar)
        s1 = tk.Scrollbar()
        s1.pack(side=tk.RIGHT, fill=tk.Y)
        s2 = tk.Scrollbar(self.tk, orient=tk.HORIZONTAL)
        s2.pack(side=tk.BOTTOM, fill=tk.X)
        self.text = tk.Text(yscrollcommand=s1.set, xscrollcommand=s2.set)
        self.text.pack()

    def render(self):
        rawContent = self.text.get(1.0, tk.END)
        # with open("renderfile.md.tmp", "wt", encoding="utf_8") as fout:
        #     fout.write(rawContent)
        parser = mk.parser(rawContent)
        with open("renderfile.html", "wt", encoding="utf_8") as fin:
            fin.write(parser.getHTML())
        browser.open_new_tab("renderfile.html")

    def save(self):
        txtContent = self.text.get(1.0, tk.END)
        self.saveFile(content=txtContent)

    def open(self):
        self.filename = tkinter.filedialog.askopenfilename(
            initialdir=os.getcwd())
        filecontent = self.openFile(fname=self.filename)
        if filecontent is not -1:
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, filecontent)

    # The fname is file name with full path
    def openFile(self, fname=None):
        if fname is None:
            return -1
        self.fname = fname
        file = open(fname, "rt", encoding="utf_8")
        content = file.read()
        file.close()
        return content

    def saveFile(self, content=None):
        if content is None:
            return -1
        self.fname = tkinter.filedialog.asksaveasfilename(
            initialdir=os.getcwd())
        file = open(self.fname, "wt", encoding="utf_8")
        file.write(content)
        file.flush()
        file.close()
        return 0

    def exit(self):
        sys.exit()


if __name__ == '__main__':
    Note()
