import sys
import fbs_runtime

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, \
	QCheckBox, QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# Checks
CH_WINDOWS = "liste des fenêtres"
CH_BUTTONS = "liste des boutons"
CH_CHECKBOXES = "liste des cases à cocher"
CH_LABELS = "liste des labels"
CH_TEXTFIELDS = "liste des champs de texte"

# Buttons
LEFT_B = Qt.LeftButton
RIGHT_B = Qt.RightButton
CENTRAL_B = Qt.MidButton

# Layouts
HORIZONTAL_L = QHBoxLayout
VERTICAL_L = QVBoxLayout

# CheckBoxes
CB_TRUE = Qt.Checked
CB_FALSE = Qt.Unchecked


class IllegalArgumentError(ValueError):
	pass


def check(element, name, i):
	if not element or i >= len(element):
		raise IllegalArgumentError("Pas d'index {} dans la {} de longueur {}.".format(i, name, len(element)))


class CustomWindow(QMainWindow):
	def __init__(self):
		QWidget.__init__(self)
		self.buttons = []
		self.checkboxes = []
		self.labels = []
		self.textfields = []

		self.layoutC = None

	def _checkButtonIndex(self, i):
		check(self.buttons, CH_BUTTONS, i)

	def _checkCheckBoxIndex(self, i):
		check(self.checkboxes, CH_CHECKBOXES, i)

	def _checkLabelIndex(self, i):
		check(self.labels, CH_LABELS, i)

	def _checkTexFieldIndex(self, i):
		check(self.textfields, CH_TEXTFIELDS, i)

	def mousePressEvent(self, event):
		if event.button() == LEFT_B:
			print("Clic gauche")

		elif event.button() == RIGHT_B:
			print("Clic droit")

		else:
			print("Clic molette")

		return super().mousePressEvent(event)

	def trackMouse(self, yes):
		self.setMouseTracking(yes)

	def mouseMoveEvent(self, event):
		print(event.x(), event.y())
		return super().mouseMoveEvent(event)

	def addButton(self, text, action=None):
		button = QPushButton(text, self)
		if action is not None:
			button.clicked.connect(action)

		self.buttons.append(button)

		return button

	def chooseLayout(self, layout):
		self.layoutC = layout()

	def startLayout(self):
		self.setLayout(self.layoutC)

	def addCheckBox(self, text, state=CB_FALSE, action=None):
		cb = QCheckBox(text, self)
		cb.setCheckState(state)

		if action is not None:
			cb.stateChanged.connect(action)

		self.checkboxes.append(cb)

		return cb

	def getCBState(self, i=0):
		self._checkCheckBoxIndex(i)

		return True if self.checkboxes[i].checkState() == CB_TRUE else False

	def addLabel(self, text):
		lab = QLabel(text, self)
		self.labels.append(lab)

		return lab

	def setLabelText(self, text, i=0):
		self._checkLabelIndex(i)

		self.labels[i].setText(text)

	def addTextField(self, text=""):
		tf = QLineEdit(text, self)
		self.labels.append(tf)

		return tf

	def getTextField(self, i=0):
		self._checkTexFieldIndex(i)

		return self.textfields[i].text()


class GUI(object):
	def __init__(self, fbsApp=False):
		if not fbsApp:
			self.appCT = None
		else:
			self.appCT = ApplicationContext()

		self.fbsApp = fbsApp

		if not self.fbsApp:
			self.app = QApplication(sys.argv)
		else:
			self.app = self.appCT.app

		self.palette = QPalette()

		self.windows = []

	def addColorToPalette(self, element, color):
		self.palette.setColor(element, color)

	def usePalette(self):
		self.app.setPalette(self.palette)

	def setDarkPalette(self):
		dark_palette = QPalette()

		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.blue)
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, QColor(3, 252, 23))
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.blue)
		dark_palette.setColor(QPalette.BrightText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.HighlightedText, Qt.black)

		self.palette = dark_palette
		self.usePalette()

		self.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 0.5px solid white; }")

	def addWindow(self, custom=None):
		win = QMainWindow() if custom is None else custom()

		self.windows.append(win)

		return win

	def _checkWindowIndex(self, i):
		check(self.windows, CH_WINDOWS, i)

	def showWindow(self, i=0):
		self._checkWindowIndex(i)
		
		self.windows[i].show()
		
	def nameWindow(self, title, i=0):
		self._checkWindowIndex(i)
		
		self.windows[i].setWindowTitle(title)
		
	def resizeWindow(self, width, height, i=0):
		self._checkWindowIndex(i)
		
		self.windows[i].resize(width, height)

	def positionWindow(self, x, y, i=0):
		self._checkWindowIndex(i)

		self.windows[i].move(x, y)
		
	def start(self):
		return self.app.exec_()
	