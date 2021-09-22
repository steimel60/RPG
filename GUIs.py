class Menu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.setWindowTitle('Redline Forensic Studio - Unreal Tools')

        self.toolKitFiles = [ToolKitTemplate, fbxImport]
        self.toolkits = [] #ToolKit instances will be saved here
        self.load_tool_kits()

        self.create_controls()
        self.create_layout()
        self.make_connections()

    #Create TookKit Instances
    def load_tool_kits(self):
        for toolKit in self.toolKitFiles:
            self.toolkits.append(toolKit.ToolKit())

    def create_controls(self):
        ##### Tab Bar #####
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabs = []
        for i in range(len(self.toolkits)):
            self.tabs.append(QtWidgets.QWidget())
            self.tabWidget.addTab(self.tabs[i], self.toolkits[i].toolKitName)
        ##### Test #####
        self.btn = QtWidgets.QPushButton('Test')

    def create_layout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        ##### Load ToolKit Layouts #####
        for i in range(len(self.tabs)):
            self.tabs[i].setLayout(self.toolkits[i].layout)

        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.btn)
        self.setLayout(mainLayout)

    def make_connections(self):
        self.btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        tut2.importMyAssets()
        unreal.log('Clicked')

# If Gui open, colse and open new
def open_menu():
    app = None
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)

    widget = UnrealGUI()
    widget.show()
    unreal.parent_external_window_to_slate(widget.winId())
