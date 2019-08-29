import sys
import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from mailsM import All, Person
from gui import CustomWindow, GUI, VERTICAL_L

FORMAT_CHOICES = ("Seulement les mails (*.txt)", "Tout (*.txt)", "Tout Excel (*.xlsx)")


class Main(object):
	def __init__(self):
		self.gui = GUI(True)
		self._initGui()

		self.win = self._initWindow()

		self.createWin()

		self.win.setFixedSize(self.win.size())

		self.dataAll = []
		self.dataPerson = []

		self.findChildren()

		self.setModels()

		self.setActions()

		self.itemExample()

	def createWin(self):
		MainW = self.win

		MainW.setObjectName("Mailator")
		MainW.resize(896, 540)
		centralwidget = QtWidgets.QWidget(MainW)
		centralwidget.setObjectName("centralwidget")
		listAll = QtWidgets.QListView(centralwidget)
		listAll.setGeometry(QtCore.QRect(20, 40, 151, 371))
		listAll.setObjectName("listAll")
		textBrowser = QtWidgets.QTextBrowser(centralwidget)
		textBrowser.setGeometry(QtCore.QRect(20, 430, 851, 61))
		textBrowser.setObjectName("textBrowser")
		listPersons = QtWidgets.QListView(centralwidget)
		listPersons.setGeometry(QtCore.QRect(200, 40, 361, 371))
		listPersons.setObjectName("listPersons")
		bImport = QtWidgets.QPushButton(centralwidget)
		bImport.setGeometry(QtCore.QRect(630, 50, 75, 23))
		bImport.setObjectName("bImport")
		bExport = QtWidgets.QPushButton(centralwidget)
		bExport.setGeometry(QtCore.QRect(740, 50, 75, 23))
		bExport.setObjectName("bExport")
		bDel = QtWidgets.QPushButton(centralwidget)
		bDel.setGeometry(QtCore.QRect(630, 150, 191, 23))
		bDel.setObjectName("bDel")
		bAnd = QtWidgets.QPushButton(centralwidget)
		bAnd.setGeometry(QtCore.QRect(630, 250, 191, 23))
		bAnd.setObjectName("bAnd")
		bOr = QtWidgets.QPushButton(centralwidget)
		bOr.setGeometry(QtCore.QRect(630, 300, 191, 23))
		bOr.setObjectName("bOr")
		bLess = QtWidgets.QPushButton(centralwidget)
		bLess.setGeometry(QtCore.QRect(630, 350, 191, 23))
		bLess.setObjectName("bLess")
		MainW.setCentralWidget(centralwidget)
		menubar = QtWidgets.QMenuBar(MainW)
		menubar.setGeometry(QtCore.QRect(0, 0, 896, 21))
		menubar.setObjectName("menubar")
		menuFichier = QtWidgets.QMenu(menubar)
		menuFichier.setObjectName("menuFichier")
		menuAide = QtWidgets.QMenu(menubar)
		menuAide.setObjectName("menuAide")
		MainW.setMenuBar(menubar)
		statusbar = QtWidgets.QStatusBar(MainW)
		statusbar.setObjectName("statusbar")
		MainW.setStatusBar(statusbar)
		menubar.addAction(menuFichier.menuAction())
		menubar.addAction(menuAide.menuAction())

		_translate = QtCore.QCoreApplication.translate
		MainW.setWindowTitle(_translate("MainW", "Mailator"))
		bImport.setText(_translate("MainW", "Importer"))
		bExport.setText(_translate("MainW", "Exporter"))
		bDel.setText(_translate("MainW", "Supprimer Groupe"))
		bAnd.setText(_translate("MainW", "Communs (ET)"))
		bOr.setText(_translate("MainW", "Fusion (OU)"))
		bLess.setText(_translate("MainW", "Moins (-)"))
		menuFichier.setTitle(_translate("MainW", "Fichier"))
		menuAide.setTitle(_translate("MainW", "Aide"))

		QtCore.QMetaObject.connectSlotsByName(MainW)

	def _initGui(self):
		self.gui.setDarkPalette()

	def _initWindow(self):
		win = self.gui.addWindow()
		win.setWindowIcon(QtGui.QIcon(self.getRes("logo-mail.ico")))
		win.setWindowTitle("Mailator")
		return win

	def findChildren(self):
		self.contentWidget = self.win.findChildren(QtWidgets.QWidget, "centralwidget")[0]
		self.listAll = self.contentWidget.findChildren(QtWidgets.QListView, "listAll")[0]
		self.listPersons = self.contentWidget.findChildren(QtWidgets.QListView, "listPersons")[0]
		self.textBrowser = self.contentWidget.findChildren(QtWidgets.QTextEdit, "textBrowser")[0]

		self.bImport = self.contentWidget.findChildren(QtWidgets.QPushButton, "bImport")[0]
		self.bImport.clicked.connect(self.fImport)

		self.bExport = self.contentWidget.findChildren(QtWidgets.QPushButton, "bExport")[0]
		self.bExport.clicked.connect(self.fExport)

		self.bDel = self.contentWidget.findChildren(QtWidgets.QPushButton, "bDel")[0]
		self.bDel.clicked.connect(self.fDel)

		self.bAnd = self.contentWidget.findChildren(QtWidgets.QPushButton, "bAnd")[0]
		self.bAnd.clicked.connect(self.fAnd)

		self.bOr = self.contentWidget.findChildren(QtWidgets.QPushButton, "bOr")[0]
		self.bOr.clicked.connect(self.fOr)

		self.bLess = self.contentWidget.findChildren(QtWidgets.QPushButton, "bLess")[0]
		self.bLess.clicked.connect(self.fMinus)

		self.menuF = self.win.findChildren(QtWidgets.QMenu, "menuFichier")[0]
		self.menuA = self.win.findChildren(QtWidgets.QMenu, "menuAide")[0]

	def menuStyle(self):
		self.menuF.setStyleSheet("padding-left: -15px; padding-right: 10px;")
		self.menuA.setStyleSheet("padding-left: -15px; padding-right: 10px;")

	def setModels(self):
		self.modelAll = QtGui.QStandardItemModel(self.listAll)
		self.modelPersons = QtGui.QStandardItemModel(self.listPersons)

	def setActions(self):
		aImport = QtWidgets.QAction("Importer", self.menuF)
		aImport.setIconVisibleInMenu(False)
		aImport.triggered.connect(self.fImport)

		aExport = QtWidgets.QAction("Exporter", self.menuF)
		aExport.setIconVisibleInMenu(False)
		aExport.triggered.connect(self.fExport)

		aExit = QtWidgets.QAction("Quitter", self.menuF)
		aExit.setIconVisibleInMenu(False)
		aExit.triggered.connect(sys.exit)

		self.menuF.addAction(aImport)
		self.menuF.addAction(aExport)
		self.menuF.addAction(aExit)

		aHelp = QtWidgets.QAction("Consulter l'aide", self.menuA)
		aHelp.setIconVisibleInMenu(False)
		aHelp.triggered.connect(self.helpWindow)

		self.menuA.addAction(aHelp)

		self.menuStyle()

	def manageButtons(self):
		if not self.listAll.selectedIndexes():
			self.bExport.setEnabled(False)
		else:
			self.bExport.setEnabled(True)

	def itemExample(self):
		x = All(name="Exemple Groupe", mails=set(["mail2@mail2.fr", "mail@mail.com"]))
		x.add(Person("Bad", "Jack", "a@2.com"))
		x.add(Person("Al", "La", "la@al.la"))
		x.add(Person("Testeur", "Jean", "jeantesteur@mail.com"))

		self.dataAll.append(x)

		self.updateListAll()

	def updateListAll(self):
		self.modelAll.clear()

		self.listAll.setIconSize(QtCore.QSize(30, 30))

		for i in range(len(self.dataAll)):
			item = QtGui.QStandardItem(i)
			item.setSizeHint(QtCore.QSize(100, 50))

			item.setIcon(QtGui.QIcon(self.getRes("all.png")))
			item.setText(self.dataAll[i].name)
			item.setEditable(False)

			self.modelAll.appendRow(item)

		self.listAll.setModel(self.modelAll)
		self.listAll.clicked.connect(self.clickOnAll)

	def clickOnAll(self, clickedIndex):
		clicked = self.dataAll[clickedIndex.row()]
		self.showAll(clicked)

		self.dataPerson = list(clicked.persons) + list(clicked.mails)

		self.modelPersons.clear()

		for i in range(len(self.dataPerson)):
			item = QtGui.QStandardItem(i)
			item.setSizeHint(QtCore.QSize(30, 15))

			if type(self.dataPerson[i]) == Person:
				item.setText(str(clicked.persons[self.dataPerson[i]]))
			else:
				item.setText('(' + str(self.dataPerson[i]) + ')')

			item.setEditable(False)

			self.modelPersons.appendRow(item)

		self.listPersons.setModel(self.modelPersons)
		self.listPersons.clicked.connect(self.showPersonOrMail)

	def getInteger(self, title, msg, maxi=1000):
		return QtWidgets.QInputDialog.getInt(self.win, title, msg, 0, 0, maxi, 1,
		                                     flags=QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

	def getString(self, title, msg):
		result, right = QtWidgets.QInputDialog.getText(self.win, title, msg,
		                                               flags=QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
		if not right:
			return None
		return result

	def setTextEdit(self, string):
		self.textBrowser.setText(string)

	def setError(self, msg):
		self.textBrowser.setText("ERREUR : " + msg)

	def showAll(self, allO):
		self.setTextEdit(str(allO))

	def showPersonOrMail(self, index):
		self.setTextEdit(str(self.dataPerson[index.row()]))

	def fImport(self):
		a = All()

		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self.win, "Choisir un fichier", os.environ["USERPROFILE"],
		                                                    "Excel Files (*.xls; *.xlsx);;Text Files (*.txt);;")
		if not filename:
			self.setError("Choose file")

		if filename.endswith("txt"):
			question = QtWidgets.QMessageBox.question(self.win, "Répondre à la question",
			                                          "Le fichier texte contient uniquement des mails ?",
			                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
			                                          QtWidgets.QMessageBox.No)

			if question == QtWidgets.QMessageBox.Yes:
				a.loadTxt(filename, True)
			else:
				a.loadTxt(filename, False)

		else:
			nameC, nameB = self.getInteger("Ajouter une valeur", "Numéro de la colonne du nom :")
			if not nameB:
				self.setError("Sélectionnez une colonne valide pour le nom.")
				return

			surnameC, surnameB = self.getInteger("Ajouter une valeur", "Numéro de la colonne du prénom :")
			if not surnameB:
				self.setError("Sélectionnez une colonne valide pour le prénom.")
				return

			mailC, mailB = self.getInteger("Ajouter une valeur", "Numéro de la colonne du mail :")
			if not mailB:
				self.setError("Sélectionnez une colonne valide pour le mail.")
				return

			a.loadAlice(filename, nameC, surnameC, mailC)

		groupName = self.getString("Importation", "Choisissez un nom pour le nouveau groupe :")
		if groupName is None:
			self.setError("Sélectionnez un nom valide pour le nouveau groupe.")
			return
		a.name = groupName

		self.dataAll.append(a)
		self.updateListAll()

	def fExport(self):
		selected = self.selectionMenu("Exportation", "Choisissez un groupe à exporter :",
		                              [x.name for x in self.dataAll])
		format = self.selectionMenu("Exportation", "Choisissez un format d'exportation :", FORMAT_CHOICES)

		if selected is None or format is None:
			self.setError("Besoin de 2 données pour exportation")
			return

		a = [x for x in self.dataAll if x.name == selected][0]

		direc = QtWidgets.QFileDialog.getExistingDirectory(self.win, "Choisissez le dossier d'exportation",
		                                                   os.environ["USERPROFILE"])

		if (format in FORMAT_CHOICES[:2] and os.path.exists(os.path.join(direc, a.name + ".txt"))) or (format == FORMAT_CHOICES[2] and os.path.exists(
				os.path.join(direc, a.name + ".xlsx"))):
			question = QtWidgets.QMessageBox.question(self.win, "Confirmer",
			                                          "Un fichier de ce nom existe déja, voulez-vous l'écraser ?",
			                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
			                                          QtWidgets.QMessageBox.No)

			if question == QtWidgets.QMessageBox.Yes:
				pass
			else:
				self.setError("Vous avez refusé d'écraser le fichier")
				return

		if format == FORMAT_CHOICES[0]:
			a.toTxt(os.path.join(direc, a.name + ".txt"), True)
		elif format == FORMAT_CHOICES[1]:
			a.toTxt(os.path.join(direc, a.name + ".txt"), False)
		else:
			a.toXl(os.path.join(direc, a.name + ".xlsx"))

		self.setTextEdit("Exportation terminée.")

	def fBool(self, title, exception):
		names = [x.name for x in self.dataAll]
		a1 = self.selectionMenu(title, "Choisissez le premier groupe", names)
		if a1 is None:
			self.setError("Données entrées invalides lors de " + exception)
			return

		names.remove(a1)

		a2 = self.selectionMenu(title, "Choisissez le deuxième groupe", names)
		if a2 is None:
			self.setError("Données entrées invalides lors de " + exception)
			return

		groupName = self.getString(title, "Choisissez un nom pour le nouveau groupe :")
		if groupName is None:
			self.setError("Données entrées invalides lors de " + exception)
			return

		all1 = [x for x in self.dataAll if x.name == a1][0]
		all2 = [x for x in self.dataAll if x.name == a2][0]

		return all1, all2, groupName

	def fDel(self):
		gName = self.selectionMenu("Sélectionner Groupe", "Choisir groupe à supprimer :", [x.name for x in self.dataAll])
		if gName is None:
			self.setError("Veuillez sélectionner un groupe.")
			return

		g = [x for x in self.dataAll if x.name == gName][0]

		self.dataAll.remove(g)
		self.updateListAll()

		self.setTextEdit("Suppression terminée.")

	def fAnd(self):
		r = self.fBool("Personnes et mails communs", "ET")
		if r is None:
			return

		all1, all2, groupName = r

		all3 = all1.et(all2)
		all3.name = groupName

		self.dataAll.append(all3)
		self.updateListAll()

	def fOr(self):
		r = self.fBool("Personnes et mails fusionnés", "OR")
		if r is None:
			return

		all1, all2, groupName = r

		all3 = all1 + all2
		all3.name = groupName

		self.dataAll.append(all3)
		self.updateListAll()

	def fMinus(self):
		r = self.fBool("Personnes et mails soustraits", "MINUS")
		if r is None:
			return

		all1, all2, groupName = r

		all3 = all1 - all2
		all3.name = groupName

		self.dataAll.append(all3)
		self.updateListAll()

	def selectionMenu(self, title, label, ite):
		chosen, right = QtWidgets.QInputDialog.getItem(self.win, title, label, ite, editable=False,
		                                               flags=QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
		if right:
			return chosen
		return None

	def helpWindow(self):
		QtWidgets.QMessageBox.about(self.win, "Aide concernant l'utilisation de Mailator",
		                            """- Les personnes (nom, prénom, mail) + mails seuls sont stockés dans des groupes.
- Les groupes sont visibles dans la colonne de gauche.\n
- Il est possible d'importer un groupe depuis un fichier texte ou un fichier Excel.
- Il est possible d'exporter un groupe vers un fichier texte ou un fichier Excel.
- Si vous importez un fichier Excel, il faudra donner le numéro des colonnes de chaque information.
\n3 types d'opérations binaires sont possibles sur les groupes : 
- ET qui va créer 1 groupe à partir des personnes et mails communs de 2 groupes.
- OR qui va créer 1 groupe à partir du total des personnes et mails de 2 groupes.
- Moins qui va créer un groupe de personnes et mails présents dans le 1er groupe sélectionné mais non présents dans le deuxième.
\nPour utiliser la fonctionnalité de condition dans l'import, utiliser le programme en mode textuel.\n
Les fichiers exportés se trouvent dans le dossier 'exported'."""
		                            )

	def getRes(self, name):
		return self.gui.appCT.get_resource(name)

	def go(self):
		self.gui.showWindow(0)
		self.gui.start()


if __name__ == "__main__":
	main = Main()
	sys.exit(main.go())
