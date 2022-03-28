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

face_casecade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')


class mainWindow(QDialog):
	def __init__(self):
		super(mainWindow , self ).__init__()
		loadUi("main.ui" , self)

		self.add.clicked.connect(self.addScreen)
		self.list.clicked.connect(self.listScreen)
		self.start.released.connect(self.startVideo)
		self.reset.clicked.connect(self.resetSys)
		self.statuesButton.clicked.connect(self.statuesScreen)
		

		self.screen.clicked.connect(self.savePhoto)


		


		self.stateTable.setColumnWidth(0 , 50 )
		self.stateTable.setColumnWidth(1 , 100 )
		self.stateTable.setColumnWidth(2 , 150 )
		self.stateTable.setRowCount(18)




	
	
	def startVideo(self):


		recognizer = cv.face.LBPHFaceRecognizer_create()
		recognizer.read("trainner.yml")


		labels = {"person_name": 1 }
		with open("labels.pickle" , "rb") as f:
		    org_labels = pickle.load(f)
		    labels = {v:k for k,v in org_labels.items()}

		cap =cv.VideoCapture("videos/yasser2.mp4")
		row = 0
		csv_writer = csv.writer(open('records.csv' , 'a') , delimiter=',')
					
		while(cap.isOpened()):
		    self.img,self.image = cap.read()

		    self.image = imutils.resize(self.image , width=701 , height=661)

		    self.gray =  cv.cvtColor(self.image , cv.COLOR_RGB2GRAY)

		


		
		    faces = face_casecade.detectMultiScale(self.image , scaleFactor=1.5 , minNeighbors= 5 , 
		     minSize = (80,80) , 
                flags = cv.CASCADE_SCALE_IMAGE)


		    
		    for (x,y,w,h) in faces:
		        
		        #print(x,y,w,h)    
		        roi_gray = self.gray[y:y+h , x:x+w]
		        roi_color = self.image[y:y+h , x:x+w]
		        
		        ###predict the face
		        id_ ,conf = recognizer.predict(roi_gray)
		        if conf >=45 and conf <=100:


		        	self.state.setText("system in danger")
		        	self.state.setStyleSheet("background-color: rgb(243, 101, 101);\n"
		        		"color:rgb(255, 255, 255);\n"
		        	 "font: 75 14pt \"MS Shell Dlg 2\";")



		        	

		        	

			        self.stateTable.setItem(row , 0 , QTableWidgetItem(str(id_) ))
			        self.stateTable.setItem(row , 1 , QTableWidgetItem( labels[id_]))
			        self.stateTable.setItem(row , 2 , QTableWidgetItem(str(time.strftime("%Y-%b-%d at %H.%M.%S "))))
			        csv_writer.writerow([id_ , labels[id_] , str(time.strftime("%Y-%b-%d at %H.%M.%S ")) ])
		

			        row = row + 1

			        if row > 18 :
			        	row = 0

			        	

		        	font = cv.FONT_HERSHEY_SIMPLEX
		        	name = str(round(conf , 2))
		        	color = (255,255,255)
		        	storke = 2
		        	cv.putText(self.image , name ,(x,y) ,  font , 1 , color , storke , cv.LINE_AA)
		        
		            # print(id_)
		            # print(labels[id_])
		      
		            
		     
		        
		        #for drow retangle
		        color = (255 , 0 , 0)
		        storke = 2
		        end_x = x+w
		        end_y = y+h
		        
		        cv.rectangle(self.image , (x,y) , (x+w , y+h ) , (10 , 228 , 220) , 5 )

		    self.update()  

		    key = self.stopVideo() 
		    if key == 0 :
		    	cv.waitKey(-1)



		    if cv.waitKey(20) & 0xFF == ord('q'):
		     break
		 
		cap.release()
		cv.destroyAllWindows()


	def stopVideo(self):
		key = 0
		return key 

	def resetSys(self):
		self.state.setText("system is save")
		self.state.setStyleSheet("background-color: rgb(70, 255, 138);\n" "color:rgb(255, 255, 255);\n"
		        	 "font: 75 14pt \"MS Shell Dlg 2\";")


	def savePhoto(self):
		self.fileName = 'snapshot'+str(time.strftime("%Y-%b-%d at %H.%M.%S "))+'.png'

		cv.imwrite("./screenShot/"+self.fileName, self.tmp)
		print("image saves as : " ,  self.fileName)
   		


	def setVideo(self , image):
		self.tmp = image
		imahe =imutils.resize(image,width=701 , height=661)
		frame = cv.cvtColor(image,cv.COLOR_BGR2RGB)
		image = QImage(frame , frame.shape[1],frame.shape[0],frame.strides[0] , QImage.Format_RGB888 )
		self.videoset.setPixmap(QtGui.QPixmap.fromImage(image))

	def update(self):
		self.setVideo(self.image)



	def addScreen(self):
		showAdd = Add()
		widget.addWidget(showAdd)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def listScreen(self):
		showList = List()
		widget.addWidget(showList)
		widget.setCurrentIndex(widget.currentIndex()+1)


	def statuesScreen(self):
		show = Statues()
		widget.addWidget(show)
		widget.setCurrentIndex(widget.currentIndex()+1)



			 

class Add(QDialog):
	def __init__(self):
		super(Add , self ).__init__()
		loadUi("add.ui" , self)


		self.home.clicked.connect(self.backHome)
		self.listScr.clicked.connect(self.listScreen)


		self.save.clicked.connect(self.saveToFile)
		self.train.clicked.connect(self.trainData)
		self.takePicer.clicked.connect(self.takePic)
		self.message.setText("")

	


	def trainData(self):
		
		recognizer = cv.face.LBPHFaceRecognizer_create()


		base_base = os.path.dirname(os.path.abspath(__file__))
		images = os.path.join(base_base , "images")


		current_id = 0
		label_ids = {}
		y_label = []
		x_train = []

		for root , dirs , files in os.walk(images):
		    for file in files:
		        if file.endswith("png") or file.endswith("jpg") :
		            path = os.path.join(root , file)
		            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
		               
		            if  not label in label_ids:
		                label_ids[label] = current_id
		                current_id += 1
		                
		            id_ = label_ids[label]
		            
		           
		            pil_iamge = Image.open(path).convert("L") #gray scale
		             
		            
		            image_array = np.array(pil_iamge , "uint8")
		            
		           # print( image_array)
		            
		            faces = face_casecade.detectMultiScale(image_array , scaleFactor=1.5 , minNeighbors= 5 , 
		     minSize = (80,80) , 
                flags = cv.CASCADE_SCALE_IMAGE ) 
		            
		            for(x,y,w,h) in faces:
		                roi = image_array[y:y+h , x:x+w]
		                x_train.append(roi)
		                y_label.append(id_)
		###save the label ids in file
		with open("labels.pickle" , "wb") as f:
		    pickle.dump(label_ids, f )
		    
		    
		recognizer.train(x_train , np.array(y_label))
		recognizer.save("trainner.yml")
		self.message.setText("Train complete , press save to complete")


	def takePic(self ):
 

	        num_of_images = 0
	        nakename = self.nakename.text()
	        path = "./images/"+nakename
	
	        detector = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
	        try:
	            os.makedirs(path)
	        except:
	            print('Directory Already Created , Change The Nake Name')
	        vid = cv.VideoCapture("videos/yasser2.mp4")
	        while True:

	            ret, img = vid.read()
	            new_img = None
	            grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	            face = detector.detectMultiScale(image=grayimg, scaleFactor=1.5, minNeighbors=5)
	            for x, y, w, h in face:
	                cv.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
	                cv.putText(img, "Face Detected", (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
	                cv.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
	                new_img = img[y:y+h, x:x+w]
	            cv.imshow("FaceDetection", img)
	            key = cv.waitKey(1) & 0xFF


	            try :
	                cv.imwrite(str(path+"/"+str(num_of_images)+nakename+".jpg"), new_img)
	                num_of_images += 1
	            except :

	                pass
	            if key == ord("q") or key == 27 or num_of_images > 300:
	                break
	        cv.destroyAllWindows()
	        self.messagebox("success", "taking picture Complete ")
	        return num_of_images





	def saveToFile(self):
	

	        name = self.name.text()
	        description = self.description.text()
	        nakename = self.nakename.text()
	        image = str(nakename+"/"+"0"+nakename+".jpg")
	        insert = (nakename , name, description, image)


	        con = pymysql.connect(db='face_recognition', user='root', passwd='', host='localhost', port=3306, autocommit=True)
	        cur = con.cursor()
	        sql = "INSERT INTO person (nakename , name, description, image) VALUES " + str(insert)
	        data = cur.execute(sql)
	        if(data):
	        	
	        	self.messagebox("success", "Data Saved")
	            

	        else:
	            self.messagebox("fail", "Fail Load Data")

	def messagebox(self, title, message):
	        mess = QtWidgets.QMessageBox()
	        mess.setWindowTitle(title)
	        mess.setText(message)
	        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
	        mess.exec_()

	        
	def listScreen(self):
		showList = List()
		widget.addWidget(showList)
		widget.setCurrentIndex(widget.currentIndex()+1)


	   	


	
	def backHome(self):
		home =mainWindow()
		widget.addWidget(home)
		widget.setCurrentIndex(widget.currentIndex()+1)









class Statues(QDialog):
	def __init__(self):
		super(Statues , self).__init__()
		loadUi("statues.ui" , self)

		self.home.clicked.connect(self.backHome)

		self.showTable()

		self.statTable.setColumnWidth(0 , 31 )
		self.statTable.setColumnWidth(1 , 500 )
		self.statTable.setColumnWidth(2 , 500 )

	def backHome(self):
		home =mainWindow()
		widget.addWidget(home)
		widget.setCurrentIndex(widget.currentIndex()+1)


	def showTable(self ):

				rows = 0

				for row in csv.reader(open('records.csv' , 'r') , delimiter=','):
					if len(row) > 0 :
						# print(row[0]+' '+row[1]+' '+row[2])
						rowPosition = self.statTable.rowCount()
						
						self.statTable.insertRow(rowPosition)

						self.statTable.setItem(rowPosition , 0 , QTableWidgetItem(str(row[0]) ))
						self.statTable.setItem(rowPosition , 1 , QTableWidgetItem(str(row[1]) ))
						self.statTable.setItem(rowPosition , 2 , QTableWidgetItem(str(row[2]) ))
				
					# 	self.tableWidget.setItem(rowPosition , i  ,QtWidgets.QTableWidgetItem(str(column)))
	 





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




    
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = mainWindow()
widget.addWidget(mainwindow)
widget.setFixedHeight(700)
widget.setFixedWidth(1024)
widget.show()







sys.exit(app.exec_())