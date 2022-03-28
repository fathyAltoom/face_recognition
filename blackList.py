from PyQt5 import QtWidgets , uic 
from PyQt5.uic import  loadUi , loadUiType
from PyQt5.QtWidgets import QDialog , QApplication , QFileDialog  , QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
import sys
import cv2 as cv , imutils
import os
from os.path import dirname , join
import pandas as pd
import csv

import time



from cProfile import label
import numpy as np
import pickle
from PIL import Image


import pymysql


class List(QDialog):
	def __init__(self):
		super(List , self).__init__()
		loadUi("list.ui" , self)

		self.home.clicked.connect(self.backHome)
		self.searchButton.clicked.connect(self.search)
		self.reload.clicked.connect(self.getData)
		self.deleteButton.clicked.connect(self.delete)
		self.updateBUTTON.clicked.connect(self.update)

		self.add.clicked.connect(self.addScreen)


		self.tableWidget.setColumnWidth(0 , 50 )
		self.tableWidget.setColumnWidth(1 , 100 )
		self.tableWidget.setColumnWidth(2 , 100 )
		self.tableWidget.setColumnWidth(3 , 263 )

		self.getData()


	# get dat from database
	def getData(self):

		db = pymysql.connect(db='face_recognition', user='root', passwd='', host='localhost', port=3306, autocommit=True)
		cursor = db.cursor()
		rows = cursor.execute("SELECT * FROM person ")
		data = cursor.fetchall()
		for row in data :
			self.showTable(row)





	def showTable(self , columns):

			rowPosition = self.tableWidget.rowCount()
			self.tableWidget.insertRow(rowPosition)

			for i , column in enumerate(columns):
				self.tableWidget.setItem(rowPosition , i  ,QtWidgets.QTableWidgetItem(str(column)))

	def clearTable(self):

		self.tableWidget.clear()
		self.tableWidget.removeRow(1)


			
	def search(self):

		id =self.userId.text()

		db =  pymysql.connect(db='face_recognition', user='root', passwd='', host='localhost', port=3306, autocommit=True)

		cursor = db.cursor()
		cursor.execute("SELECT * FROM person WHERE id = '" + str(id) + "'")
		data = cursor.fetchall()
		if(data):
			for tb in data :
				id = tb[0]

				self.userid.setText(""+str(tb[0]))
				self.nakename.setText(""+tb[1])

				self.username.setText(""+tb[2])
				self.description.setText(""+tb[3])
				image = "images/"+tb[4]
			
				self.personImage.setPixmap(QtGui.QPixmap(image))
				self.personImage.setScaledContents(True)
		

		else :
				self.userid.setText("")
				self.nakename.setText("")
				self.username.setText("")
				self.description.setText("")	
				self.personImage.setPixmap(QtGui.QPixmap("./assets/open-images.png"))
				self.personImage.setScaledContents(True)

				self.messagebox("INFO", "not found")


	def delete(self):
	        id = self.userid.text()
	        con = pymysql.connect(db='face_recognition', user='root', passwd='', host='localhost', port=3306, autocommit=True)
	        cur = con.cursor()
	        sql = "DELETE FROM person WHERE id =%s"
	        data = cur.execute(sql, (id))
	        if(data):
	            self.messagebox("success", "Data deleted successfully")
	 

	        else:
	            self.messagebox("fail", "delete failed ")


	def update(self):
	        userid = self.userid.text()
	        fullname = self.username.text()
	        description = self.description.text()
	        nakename = self.nakename.text()
	
	        con = pymysql.connect(db='face_recognition', user='root', passwd='', host='localhost', port=3306, autocommit=True)
	        cur = con.cursor()
	        sql = "UPDATE person SET name = %s, nakename=%s, description=%s WHERE id=%s"
	        data = cur.execute(sql,(fullname, nakename, description, userid))
	        if(data):
	            self.messagebox("success", "Data updated successfully")
	        else:
	            self.messagebox("fail", "Fail update data")


	        

	   	


	
	def backHome(self):
		home =mainWindow()
		widget.addWidget(home)
		widget.setCurrentIndex(widget.currentIndex()+1)



	def addScreen(self):
		showAdd = Add()
		widget.addWidget(showAdd)
		widget.setCurrentIndex(widget.currentIndex()+1)







	def messagebox(self, title, message):
	        mess = QtWidgets.QMessageBox()
	        mess.setWindowTitle(title)
	        mess.setText(message)
	        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
	        mess.exec_()


