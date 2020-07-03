# coding=utf-8
import sys
import os
import tkinter as tk
import tkinter.filedialog
import webbrowser as browser
from enum import Enum
import re


class formats(Enum):
    null = 0
    para = 1
    h1 = 2
    h2 = 3
    h3 = 4
    h4 = 5
    h5 = 6
    h6 = 7
    italic = 8
    bold = 9
    quote = 10
    ol = 11
    ul = 12
    li = 13
    codeLine = 14
    codeBlock = 15
    href = 16
    img = 17
    hr = 18
    br = 19
    radio = 20
    checkBox = 21
    text = 22


# href, img, boxes have text inside, their tags will be added while dfsing
html_tag_head = [
    "",
    "<p>",
    "<h1 ",
    "<h2 ",
    "<h3 ",
    "<h4 ",
    "<h5 ",
    "<h6 ",
    "<i>",
    "<b>",
    "<blockquote>",
    "<ol>",
    "<ul>",
    "<li>",
    "<code>",
    "<pre><code>",
    "",
    "",
    "<hr color=#CCCCCC size=1 />",
    "<br />",
    "",
    "",
    "",
]

html_tag_end = [
    "",
    "</p>",
    "</h1>",
    "</h2>",
    "</h3>",
    "</h4>",
    "</h5>",
    "</h6>",
    "</i>",
    "</b>",
    "</blockquote>",
    "</ol>",
    "</ul>",
    "</li>",
    "</code>",
    "</code></pre>",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

html_head = "<!DOCTYPE html>\n<html>\n\n<head>\n\
        <meta charset=\"utf-8\">\n\
        <title>Markdown</title>\n\
        <link rel=\"stylesheet\" href=\"github-markdown.css\">\n\
        </head>\n\n<body>\n<article class=\"markdown-body\">\n"

html_end = "\n</article>\n</body>\n\n</html>"


class parser():
    # these two strings below will be modified by the constructor
    __TOC = ""
    __CONTENT = ""

    # basic nodes
    class Cnode():
        '''
        Structure for TOC
        '''
        def __init__(self, hd: str):
            self.heading = hd
            self.children = []
            self.tag = ""

    class Node():
        '''
        Structure for contents
        '''
        def __init__(self, type: formats):
            self.type = type
            self.children = []
            self.element = ["", "", ""]

    def start(self, src: str) -> tuple:
        '''
        Process the spaces and tabs of one line
        @src str, the source string
        @return tuple, (num, substr)
            num    int, number of spaces/tabs
            substr str, src without the beginning spaces
        '''
        if len(src) == 0:
            return (0, "")
        cntspace = 0
        cnttab = 0
        for i in range(len(src)):
            if src[i] == ' ':
                cntspace += 1
            if src[i] == '\t':
                cnttab += 1
            else:
                return (cnttab + cntspace // 4, src[i:])

    def getType(self, src: str) -> tuple:
        '''
        Judge the type of one line by the head of it
        types: h1 ~ h5, codeblock, ul, ol, quote, para
        @src str the source string
        @return turple, (type, content)
            type    formats, type of this line
            content str, src without format tag
        '''
        i = 0
        while src[i] == '#':
            i += 1
        if i > 0 and src[i] == ' ':
            # value of h1 is 2
            return (formats(i - 1 + 2), src[i + 1:])

        i = 0
        if src[i:i + 3] == "```":
            return (formats.codeBlock, src[i + 3])
        if src[i:i + 2] == "- ":
            return (formats.ul, src[i + 2:])
        if src[i:i + 2] == "> ":
            return (formats.quote, src[i + 2:])
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if src[i] in digits and src[i + 1:i + 3] == ". ":
            return (formats.ol, src[i + 3:])
        return (formats.para, src)

    def isHeading(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if v is h1 ~ h6
        '''
        return (v.type.value >= formats.h1.value
                and v.type.value <= formats.h6.value)

    def isImg(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is img
        '''
        return v.type == formats.img

    def isHref(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is href
        '''
        return v.type == formats.href

    def isRadio(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is radio
        '''
        return v.type == formats.radio

    def isCheckBox(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is checkbox
        '''
        return v.type == formats.checkBox

    def isText(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is text
        '''
        return v.type == formats.text

    def findNode(self, depth: int):
        '''
        With depth of the tree, find the node
        @depth int, depth of target node
        @return Node
        '''
        ptr = self.root
        while len(ptr.children) == 0 and depth != 0:
            ptr = ptr.children[-1]
            if ptr.type == formats.li:
                depth -= 1
        return ptr

    def insert_cnode(self, v: Cnode, x: int, hd: str, tag: int):
        '''
        Insert TOC node
        @cnode Cnode, node to be father
        @x int, depth
        @hd str, content of heading
        @tag formats,  tag = formats(0)
        '''
        n = len(v.children)
        if x == 1:
            v.children.append(self.Cnode(hd))
            v.children[-1].tag = "tag" + str(tag)
            return
        if n == 0 or len(v.children[-1].heading) == 0:
            v.children.append(self.Cnode(""))
        self.insert_cnode(v.children[-1], x - 1, hd, tag)
        return

    # REWRITE, pure char
    # TODO how to make it with pure re?
    def insert_node(self, v: Node, src: str):
        inbold = False
        incode = False
        initalic = False
        v.children.append(self.Node(formats.null))
        n = len(src)
        i = 0
        while i < n:
            ch = src[i]
            # do something and change the flag
            # codeline
            if ch == '`':
                v.children.append(self.Node(
                    formats.null)) if incode else v.children.append(
                        self.Node(formats.codeLine))
                incode = not incode
                i += 1
                continue
            # bold
            if ch == '*' and (i < n - 1 and src[i + 1] == '*') and not incode:
                i += 1
                v.children.append(self.Node(
                    formats.null)) if inbold else v.children.append(
                        self.Node(formats.bold))
                inbold = not inbold
                i += 1
                continue
            # italic
            if ch == '_' and not incode and not inbold:
                v.children.append(self.Node(
                    formats.null)) if initalic else v.children.append(
                        self.Node(formats.italic))
                initalic = not initalic
                i += 1
                continue
            # img
            if ch == '!' and (i < n - 1 and src[i + 1] == '['
                              ) and not incode and not inbold and not initalic:
                v.children.append(self.Node(formats.img))
                # collect the keywords
                i += 2
                while i < n - 1 and src[i] != ']':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 2
                while i < n - 1 and src[i] != ' ' and src[i] != ')':
                    v.children[-1].element[1] += src[i]
                    i += 1
                if src[i] != ')':
                    i += 1
                    while i < n - 1 and src[i] != ')':
                        if src[i] != '\"':
                            v.children[-1].element[2] += src[i]
                        i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # href
            if ch == '[' and not incode and not inbold and not initalic:
                if i == 0 or (i > 0 and src[i - 1] != '!'):
                    v.children.append(self.Node(formats.href))
                    # collect the keywords
                    i += 1
                    while i < n - 1 and src[i] != ']':
                        v.children[-1].element[0] += src[i]
                        i += 1
                    i += 2
                    while i < n - 1 and src[i] != ' ' and src[i] != ')':
                        v.children[-1].element[1] += src[i]
                        i += 1
                    if src[i] != ')':
                        i += 1
                        while i < n - 1 and src[i] != ')':
                            if src[i] != '\"':
                                v.children[-1].element[2] += src[i]
                            i += 1
                    v.children.append(self.Node(formats.null))
                    i += 1
                    continue
            # radio
            fradio = re.compile(r"-.+<[ xX]>.+")
            if fradio.match(
                    src[i:]) and not inbold and not incode and not initalic:
                v.children.append(self.Node(formats.radio))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != '<':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 1
                if src[i] == 'x' or src[i] == 'X':
                    v.children[-1].element[2] += "checked"
                i += 2
                while i < n - 1:
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # checkbox
            fcheckbox = re.compile(r"-.+\[[ xX]\].+")
            if fcheckbox.match(
                    src[i:]) and not incode and not inbold and not initalic:
                v.children.append(self.Node(formats.checkBox))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != '[':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 1
                if src[i] == 'x' or src[i] == 'X':
                    v.children[-1].element[2] += "checked"
                i += 2
                while i < n - 1:
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # textbox
            ftext = re.compile(r"\(.+\)\[\[.+\]\]")
            if ftext.match(
                    src[i:]) and not inbold and not incode and not initalic:
                v.children.append(self.Node(formats.text))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != ')':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 3
                while i < n - 1 and src[i] != ']':
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 2
                continue
            # if none above, push into the normal null node
            v.children[-1].element[0] += ch
            i += 1
        # if a line has 2 or more ending spaces, it makrs a break(<br />)
        if len(src) >= 2:
            if src[-1] == ' ' and src[-2] == ' ':
                v.children.append(self.Node(formats.br))

    # if a line has starting "---", it marks a horizontal line <hr />
    def is_hr(self, src: str) -> bool:
        cnt = 0
        flag = True
        for c in src:
            if c != ' ' and c != '\t' and c != '-':
                flag = False
                break
            if c == '-':
                cnt += 1
        if cnt >= 3:
            flag = True
        return flag

    # use a para to warp nodes
    def make_para(self, v: Node):
        if len(v.children) == 1 and v.children[-1].type == formats.para:
            return
        if v.type == formats.para:
            return
        if v.type == formats.null:
            v.type = formats.para
            return
        x = self.Node(formats.para)
        x.children = v.children
        v.children = [x]

    def dfs_node(self, v: Node):
        if len(v.element[0]) == 0 and len(
                v.children) == 0 and v.type == formats.para:
            return
        # add head
        self.__CONTENT += html_tag_head[v.type.value]
        flag = True
        # heading
        if self.isHeading(v):
            self.__CONTENT += "id=\"" + v.element[0] + "\">"
            flag = False
        # href
        if self.isHref(v):
            self.__CONTENT += "<a  href=\"" + v.element[
                1] + "\" title=\"" + v.element[2] + "\">" + v.element[
                    0] + "</a>"
            flag = False
        # img
        if self.isImg(v):
            self.__CONTENT += "<img alt=\"" + v.element[
                0] + "\" src=\"" + v.element[1] + "\" title=\"" + v.element[
                    2] + "\" />"
            flag = False
        # radio
        if self.isRadio(v):
            self.__CONTENT += "<input type=\"radio\" name=\"" + v.element[
                0] + "\" value=\"" + v.element[
                    1] + "\" "
            if v.element[2] == "checked":
                self.__CONTENT += "checked=\"" + v.element[2] + "\">" + v.element[1]
            else:
                self.__CONTENT += "\">" + v.element[1]
            flag = False
        # checkbox
        if self.isCheckBox(v):
            self.__CONTENT += "<input type=\"checkbox\" name=\"" + v.element[
                0] + "\" value=\"" + v.element[
                    1] + "\" "
            if v.element[2] == "checked":
                self.__CONTENT += "checked=\"" + v.element[2] + "\">" + v.element[1]
            else:
                self.__CONTENT += "\">" + v.element[1]
            flag = False
        # text
        if self.isText(v):
            self.__CONTENT += "<input type=\"text\" name=\"" + v.element[0] + "\" value=\"" + v.element[1] + "\">"
            flag = False
        # none of above
        if flag:
            self.__CONTENT += v.element[0]
            flag = False
        # dfs
        for child in v.children:
            self.dfs_node(child)
        # add end
        self.__CONTENT += html_tag_end[v.type.value]

    def dfs_cnode(self, v: Cnode, idx: str):
        self.__TOC += "<li>\n"
        self.__TOC += "<a href=\"#" + v.tag + "\">" + idx + " " + v.heading + "</a>\n"
        n = len(v.children)
        if n:
            self.__TOC += "<ul>\n"
            for i in range(n):
                self.dfs_cnode(v.children[i], idx + str(i + 1) + ".")
            self.__TOC += "</ul>\n"
        self.__TOC += "</li>\n"

    def getTable(self):
        '''
        @return str, table of contents of the markdown file
        in HTML format.
        '''
        return self.__TOC

    def getContent(self):
        '''
        @return str, full contents of the markdown file in HTML format
        '''
        return self.__CONTENT

    def getHTML(self):
        '''
        @return str, complete HTML file
        '''
        return html_head + self.getTable() + self.getContent() + html_end

    def __init__(self, path: str):
        self.Croot = self.Cnode("")
        self.root = self.Node(formats.null)
        self.now = self.Node(formats.null)
        self.cntTag = 0
        self.line = ""
        self.newpara = False
        self.inblock = False
        self.preline = False
        with open(path, "rt", encoding="utf_8") as fin:
            while True:
                self.line = fin.readline()
                if self.line == "":
                    break

                # not in codeblock and need a hr
                if not self.inblock and self.is_hr(self.line):
                    self.now = self.root
                    self.now.children.append(self.Node(formats.hr))
                    self.newpara = False
                    continue

                # handle the leading space/tab
                ps = self.start(self.line)

                # if a line is not in codeblock
                # and is blank
                # it marks the start of a paragraph
                if not self.inblock and ps[1] == "\n":
                    # back to the root
                    self.now = self.root
                    self.newpara = True
                    continue

                # get type of this line
                tp = self.getType(ps[1])

                # if is codeblock
                if tp[0] == formats.codeBlock:
                    self.now.children.append(
                        self.Node(formats.null)
                    ) if self.inblock else self.now.children.append(
                        self.Node(formats.codeBlock))
                    self.inblock = not self.inblock
                    continue

                # if in codeblock, insert the content
                if self.inblock:
                    self.now.children[-1].element[0] += self.line
                    continue

                # if normal paragraph
                if tp[0] == formats.para:
                    if self.now == self.root:
                        self.now = self.findNode(ps[0])
                        self.now.children.append(self.Node(formats.para))
                        self.now = self.now.children[-1]

                    flag = False
                    if self.newpara and len(self.now.children) != 0:
                        ptr = 0
                        for child in self.now.children:
                            if child.type == formats.null:
                                ptr = child
                        if ptr != 0:
                            self.make_para(ptr)
                        flag = True
                    if flag:
                        self.now.children.append(self.Node(formats.para))
                        self.now = self.now.children[-1]

                    self.now.children.append(self.Node(formats.null))
                    self.insert_node(self.now.children[-1], tp[1])
                    self.newpara = False
                    continue

                self.now = self.findNode(ps[0])

                # if is heading
                if tp[0].value >= formats.h1.value and tp[
                        0].value <= formats.h6.value:
                    self.now.children.append(self.Node(tp[0]))
                    self.cntTag += 1
                    self.now.children[-1].element[0] = "tag" + str(self.cntTag)
                    self.insert_node(self.now.children[-1], tp[1])
                    self.insert_cnode(self.Croot,
                                      tp[0].value - formats.h1.value + 1,
                                      tp[1], self.cntTag)

                # if is ul
                if tp[0] == formats.ul:
                    if len(self.now.children
                           ) == 0 or self.now.children[-1].type != formats.ul:
                        self.now.children.append(self.Node(formats.ul))
                    self.now = self.now.children[-1]
                    flag = False
                    if self.newpara and len(self.now.children) != 0:
                        ptr = None
                        for child in self.now.children:
                            if child.type == formats.li:
                                ptr = child
                        if ptr is not None:
                            self.make_para(ptr)
                        flag = True
                    self.now.children.append(self.Node(formats.li))
                    self.now = self.now.children[-1]
                    if flag:
                        self.now.children.append(self.Node(formats.para))
                        self.now = self.now.children[-1]
                    self.insert_node(self.now, tp[1])

                # if ol
                if tp[0] == formats.ol:
                    if len(self.now.children
                           ) == 0 or self.now.children[-1].type != formats.ol:
                        self.now.children.append(self.Node(formats.ol))
                    self.now = self.now.children[-1]
                    flag = False
                    if self.newpara and len(self.now.children) != 0:
                        ptr = None
                        for child in self.now.children:
                            if child.type == formats.li:
                                ptr = child
                        if ptr is not None:
                            self.make_para(ptr)
                        flag = True
                    self.now.children.append(self.Node(formats.li))
                    self.now = self.now.children[-1]
                    if flag:
                        self.now.children.append(self.Node(formats.para))
                        self.now = self.now.children[-1]
                    self.insert_node(self.now, tp[1])

                if tp[0] == formats.quote:
                    if len(
                            self.now.children
                    ) == 0 or self.now.children[-1].type != formats.quote:
                        self.now.children.append(self.Node(formats.quote))
                    self.now = self.now.children[-1]
                    if self.newpara or len(self.now.children) == 0:
                        self.now.children.append(self.Node(formats.para))
                    self.insert_node(self.now.children[-1], tp[1])
                # done a para
                self.newpara = False
        # construct the __CONTENT
        self.dfs_node(self.root)
        # construct the __TOC
        self.__TOC += "<ul>"
        for i in range(len(self.Croot.children)):
            self.dfs_cnode(self.Croot.children[i], str(i + 1) + ".")
        self.__TOC += "</ul>"


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
        rawContent = "\n" + self.text.get(1.0, tk.END)
        with open("renderfile.md.tmp", "wt", encoding="utf_8") as fout:
            fout.write(rawContent)
        p = parser("renderfile.md.tmp")
        with open("renderfile.html", "wt", encoding="utf_8") as fin:
            fin.write(p.getHTML())
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


if __name__ == "__main__":
    widget = Note()
    widget.show()
