import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout, QAction, QFileDialog
import mdparser as md
import webbrowser as browser
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.editor_label = QLabel("编辑区", self)
        self.browser_label = QLabel("预览区", self)
        self.text_editor = QTextEdit(self)
        # self.text_browser = QTextBrowser(self)
        # self.text_browser = QTextEdit(self)
        self.text_browser = QWebEngineView()
        self.p = md.parser("")

        self.layout_init()
        self.text_editor_init()

    def layout_init(self):
        self.editor_v_layout = QVBoxLayout()
        self.browser_v_layout = QVBoxLayout()
        self.all_h_layout = QHBoxLayout()

        self.editor_v_layout.addWidget(self.editor_label)
        self.editor_v_layout.addWidget(self.text_editor)
        # self.editor_v_layout.setStretch(0, 1)
        # self.editor_v_layout.setStretch(1, 20)

        self.browser_v_layout.addWidget(self.browser_label)
        self.browser_v_layout.addWidget(self.text_browser)
        self.browser_v_layout.setStretch(0, 1)
        self.browser_v_layout.setStretch(1, 100)

        self.all_h_layout.addLayout(self.editor_v_layout)
        self.all_h_layout.addLayout(self.browser_v_layout)
        self.all_h_layout.setStretch(0, 1)
        self.all_h_layout.setStretch(1, 1)

        self.setLayout(self.all_h_layout)

    def text_editor_init(self):
        self.text_editor.textChanged.connect(self.show_md)

    def show_md(self):
        self.p = md.parser(self.text_editor.toPlainText())
        self.text_browser.setHtml(self.p.getHTML())


class Main_Window(QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.child = Widget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.child)
        self.setCentralWidget(self.child)
        self.setWindowTitle("Markout alpha")

        # menu bar
        menu_bar = self.menuBar()
        menu_bar_file = menu_bar.addMenu("文件")

        action_exit = QAction("退出", self)
        action_exit.triggered.connect(self.exit)

        action_save = QAction("保存", self)
        action_save.triggered.connect(self.save)

        action_open = QAction("打开", self)
        action_open.triggered.connect(self.open)

        action_export = QAction("导出到HTML", self)
        action_export.triggered.connect(self.export)

        action_browser = QAction("用默认浏览器预览", self)
        action_browser.triggered.connect(self.open_in_browser)

        menu_bar_file.addAction(action_open)
        menu_bar_file.addAction(action_save)
        menu_bar_file.addAction(action_export)
        menu_bar_file.addAction(action_browser)
        menu_bar_file.addAction(action_exit)

        dsk = QApplication.desktop()
        self.window_width = dsk.width() * 0.7
        self.window_height = dsk.height() * 0.7
        self.resize(int(self.window_width), int(self.window_height))

    def open(self):
        content = ""
        open_dir = ("", "")
        open_dir = QFileDialog.getOpenFileName(self, "打开一个Markdown文件", "./",
                                               "Markdown File (*.md)")
        if open_dir[0] != "":
            with open(open_dir[0], "rt", encoding="utf_8") as fin:
                content = fin.read()

            self.child.text_editor.clear()
            self.child.text_editor.setPlainText(content)

    def save(self):
        content = self.child.text_editor.toPlainText()
        save_dir = ("", "")
        save_dir = QFileDialog.getSaveFileName(self, "保存当前文件", "./",
                                               "Markdown File (*.md)")
        if save_dir[0] != "":
            with open(save_dir[0], "wt", encoding="utf_8") as fout:
                fout.write(content)

    def export(self):
        content = self.child.p.getHTML()
        self.export_dir = ("", "")
        self.export_dir = QFileDialog.getSaveFileName(self, "导出到HTML", "./",
                                                      "HTML File (*.html)")
        if self.export_dir[0] != "":
            with open(self.export_dir[0], "wt", encoding="utf_8") as fexp:
                fexp.write(content)

    def open_in_browser(self):
        self.export()
        browser.open(self.export_dir[0])

    def exit(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
