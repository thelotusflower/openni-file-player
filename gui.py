from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QBasicTimer
import oni_func

class Player(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.framesColor = []
        self.framesDepth = []
        self.tick = 0
        self.timer = QBasicTimer()
        self.buttonPlay = QtWidgets.QPushButton()
        self.initUI()


    def initUI(self):
        widget = QtWidgets.QWidget(self)
        widget.setGeometry(0,20,1280,480)
        grid = QtWidgets.QGridLayout(widget)

        graphicsView = QtWidgets.QGraphicsView()

        scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        graphicsView.setScene(scene)

        graphicsView2 = QtWidgets.QGraphicsView()

        scene2 = QtWidgets.QGraphicsScene()
        self.pixmap2 = QtWidgets.QGraphicsPixmapItem()
        scene2.addItem(self.pixmap2)
        graphicsView2.setScene(scene2)

        graphicsView.resize(640,480)
        graphicsView.resize(640,480)
        grid.addWidget(graphicsView2,0,0)
        grid.addWidget(graphicsView,0,1)
        grid.setColumnMinimumWidth(0, 640)
        grid.setColumnMinimumWidth(1, 640)

        widget.setLayout(grid)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setGeometry(10, 500, 1260, 20)
        self.slider.sliderReleased.connect(self.valueChanged)
        self.slider.sliderPressed.connect(self.valueChanged)
        self.slider.sliderMoved.connect(self.valueChanged)

        self.buttonPlay = QtWidgets.QPushButton('Play', self)
        self.buttonPlay.clicked.connect(self.playerControl)
        self.buttonPlay.move(120, 550)

        self.buttonForward = QtWidgets.QPushButton('>', self)
        self.buttonBackward = QtWidgets.QPushButton('<', self)
        self.buttonForward.move(230, 550)
        self.buttonForward.setToolTip('Move 1 frame forward')
        self.buttonBackward.setToolTip('Move 1 frame backward')
        self.buttonBackward.move(10, 550)

        self.buttonForward.clicked.connect(self.moveFrame)
        self.buttonBackward.clicked.connect(self.moveFrame)


        openFile = QtWidgets.QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.fileDialog)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 1280, 600)
        graphicsView.resize(1920,1080)
        self.setWindowTitle('Test')
        self.show()


    def moveFrame(self):
        sender = self.sender()

        if sender.text() == '>':
            #self.tick += 1
            self.play()
        else:
            self.tick -= 2
            self.play()


    def fileDialog(self):
        self.framesColor.clear()
        self.framesDepth.clear()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        b = str.encode(fileName)
        type(fileName)
        self.framesColor, self.framesDepth = oni_func.getVideo(b)
        self.play()


    def tickPosition(self):
        self.slider.setValue(self.tick)


    def valueChanged(self):
        self.tick = self.slider.value()
        self.play()


    def timerEvent(self, *args, **kwargs):
        self.play()
        self.tickPosition()


    def playerControl(self):
        if self.timer.isActive():
            self.timer.stop()
            self.buttonPlay.setText('Play')
        else:
            self.timer.start(28, self)
            self.slider.setRange(0, len(self.framesColor))
            self.buttonPlay.setText('Stop')


    def play(self):
        if self.tick >= len(self.framesColor):
            self.tick = 0
        input_image = self.framesColor[self.tick]
        input_depth = self.framesDepth[self.tick]
        bytesPerLine = 3*640
        qImg = QtGui.QImage(input_image.data, 640, 480, bytesPerLine, QtGui.QImage.Format_RGB888)
        qImg2 = QtGui.QImage(input_depth.data, 640, 480, bytesPerLine, QtGui.QImage.Format_Indexed8)
        print(qImg2.depth())
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        pixmap02 = QtGui.QPixmap.fromImage(qImg2)
        self.tick += 1
        self.pixmap2.setPixmap(pixmap02)
        self.pixmap.setPixmap(pixmap01)

