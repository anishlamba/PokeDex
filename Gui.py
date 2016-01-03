import pandas as pd
import sys, urllib2
import requests
from PyQt4 import QtGui, QtCore

class PokeDex(QtGui.QWidget):

	def __init__(self):
		super(PokeDex,self).__init__()

		self.initUI()
	def initUI(self):

		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)

		self.df = pd.read_json('Data.json')
		self.df = self.df.set_index(['#'])

		self.dropdown = QtGui.QComboBox(self)
		self.names = self.df['Name'].values
		self.dropdown.addItems(self.names)
		self.grid.addWidget(self.dropdown,0,0,1,1)

		self.btn=QtGui.QPushButton('Search',self)
		self.btn.clicked.connect(self.runSearch)
		self.grid.addWidget(self.btn,0,1,1,1)

		self.img=QtGui.QLabel(self)
		self.grid.addWidget(self.img,1,1,1,1)

		self.label = QtGui.QLabel(self)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setText('\nName:\n\nType:\n\nHP:\n\nAttack\n\nSp.Attack:\n\nDefense:\n\nSp.Defense:\n\nSpeed:\n\nTotal:')
		self.label.setAlignment(QtCore.Qt.AlignLeft)
		self.grid.addWidget(self.label,1,0,1,1)

		self.resize(500,250)
		self.center()
		self.setWindowTitle('PokeDex')
		self.show()
	def runSearch(self):
		index=self.dropdown.currentIndex()
		val=self.names[index]
		cond= self.df['Name']==val

		base= 'http://img.pokemondb.net/artwork/'
		img_url = base+val.lower()+'.jpg'
		data=urllib2.urlopen(img_url).read()
		image=QtGui.QImage()
		image.loadFromData(data)
		self.img.setPixmap(QtGui.QPixmap(image))

		name='Name:\t\t\t'+val +'\n\n'
		ty= 'Type:\t\t\t'+','.join(self.df[cond]['Type'].values[0])+'\n\n'
		hp=	'HP:\t\t\t'+str(self.df[cond]['HP'].values[0])+'\n\n'
		atk= 'Attack:\t\t\t'+str(self.df[cond]['Attack'].values[0])+'\n\n'
		satk= 'Sp. Attack:\t\t\t'+str(self.df[cond]['Sp. Atk'].values[0])+'\n\n'
		deff= 'Defense:\t\t\t'+str(self.df[cond]['Defense'].values[0])+'\n\n'
		sdef ='Sp. Defense:\t\t\t'+str(self.df[cond]['Sp. Def'].values[0])+'\n\n'
		speed ='Speed:\t\t\t'+str(self.df[cond]['Speed'].values[0])+'\n\n'
		total ='Total:\t\t\t'+str(self.df[cond]['Total'].values[0])+'\n\n'

		final=name+ty+hp+atk+satk+deff+sdef+speed+total
		self.label.setText(final)
	def center(self):
		qr=self.frameGeometry()
		cp=QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

def main():
	app=QtGui.QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)

	gui= PokeDex()
	sys.exit(app.exec_())
if __name__== '__main__':
	main()
