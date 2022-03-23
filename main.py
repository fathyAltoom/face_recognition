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

face_casecade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")


labels = {"person_name": 1 }
with open("labels.pickle" , "rb") as f:
	    org_labels = pickle.load(f)
	    labels = {v:k for k,v in org_labels.items()}



face_casecade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

class mainWindow(QDialog):
	def __init__(self):
		super(mainWindow , self ).__init__()
		loadUi("main.ui" , self)

		self.add.clicked.connect(self.addScreen)
		self.list.clicked.connect(self.listScreen)
		self.start.released.connect(self.startVideo)


		self.stateTable.setColumnWidth(0 , 50 )
		self.stateTable.setColumnWidth(1 , 100 )
		self.stateTable.setColumnWidth(2 , 150 )
		self.stateTable.setRowCount(18)




	
	
	def startVideo(self):
		cap =cv.VideoCapture("deheeh.mp4")
		row = 0
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
		    #cv.imshow("main",self.image)

		        

		        
		  
		    # self.setVideo(frame)


		    
		    if cv.waitKey(20) & 0xFF == ord('q'):
		     break
		 
		cap.release()
		cv.destroyAllWindows()

 

		        #print(x,y,w,h)    
		        # roi_gray = gray[y:y+h , x:x+w]
		        # roi_color = frame[y:y+h , x:x+w]
		        
		        ###predict the face
		        # id_ ,conf = recognizer.predict(roi_gray)
		        # if conf >=45 and conf <=85:
		        #     print(id_)
		        #     print(labels[id_])
		        #     font = cv.FONT_HERSHEY_SIMPLEX
		        #     name = labels[id_]
		        #     color = (255,255,255)
		        #     storke = 2
		        #     cv.putText(frame , name ,(x,y) ,  font , 1 , color , storke , cv.LINE_AA)
		            
		        
		        
		        #for drow retangle
		        # frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		        # image = QImage(frame,shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
		        # self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))


		


	def setVideo(self , image):
		self.tmp = image
		imahe =imutils.resize(image,width=701 , height=661)
		frame = cv.cvtColor(image,cv.COLOR_BGR2RGB)
		image = QImage(frame , frame.shape[1],frame.shape[0],frame.strides[0] , QImage.Format_RGB888 )
		self.videoset.setPixmap(QtGui.QPixmap.fromImage(image))

	def update(self):
		self.setVideo(self.image)


	# def update(self):
 #        img = self.changeBrightness(self.image , self.brig_now)
 #        img = self.changeBlur(img , self.blur_now)
 #        # text = 'FBS :' + str(self.fps)
 #        # img = ps.putBText(img , text , text_offset_x = 20 , text_offset_y = 30 , vspace=20 , hspace=10,font_scale=1.0,background_RGB=(10,20,222) , text_RGB = (255,255,255) )

 #        self.setVideo(img)



 

    # def setVideo(self,image):
    #     self.tmp=image
    #     imahe = imutils.resize(image,width=640 , height=480)
    #     frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    #     image = QImage(frame , frame.shape[1],frame.shape[0],frame.strides[0] , QImage.Format_RGB888 )
    #     self.label.setPixmap(QtGui.QPixmap.fromImage(image))


	# def setvideo(self,image):
 #         self.tmp=image
 #         imahe = imutils.resize(image,width=640 , height=480)
 #         frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
 #         image = QImage(frame , frame.shape[1],frame.shape[0],frame.strides[0] , QImage.Format_RGB888 )
 #         self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))


	def addScreen(self):
		showAdd = Add()
		widget.addWidget(showAdd)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def listScreen(self):
		showList = List()
		widget.addWidget(showList)
		widget.setCurrentIndex(widget.currentIndex()+1)



			 

class Add(QDialog):
	def __init__(self):
		super(Add , self ).__init__()
		loadUi("add.ui" , self)


		self.home.clicked.connect(self.backHome)
		self.save.clicked.connect(self.saveToFile)
		self.train.clicked.connect(self.trainData)
		self.message.setText("")

	
	def backHome(self):
		home =mainWindow()
		widget.addWidget(home)
		widget.setCurrentIndex(widget.currentIndex()+1)

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
		            
		           # print(label_ids)
		            ##comare image to array
		            pil_iamge = Image.open(path).convert("L") #gray scale
		            
		            #        size = (550 , 550)
		            # final_iamage = pil_iamge.resize(size , Image.ANTIALIAS)
		            # image_array = np.array(final_iamage , "uint8")
		            
		            
		            image_array = np.array(pil_iamge , "uint8")
		            
		           # print( image_array)
		            
		            faces = face_casecade.detectMultiScale(image_array , scaleFactor=1.5 , minNeighbors= 5)
		            
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



	def takePic():

		face_casecade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
		# cap =cv.VideoCapture("http://192.168.43.52:8080/video")
		cap =cv.VideoCapture(0)
		i = 0
		while True :
		    rec , frame = cap.read()
		    gray = cv.cvtColor(frame , cv.COLOR_RGB2GRAY)
		    
		    faces = face_casecade.detectMultiScale(gray , scaleFactor=1.5 , minNeighbors= 5)
		    

		    for (x,y,w,h) in faces:
		        
		        #print(x,y,w,h)    
		        roi_gray = gray[y:y+h , x:x+w]
		        roi_color = frame[y:y+h , x:x+w]
		        
		        #for drow retangle
		        color = (255 , 0 , 0)
		        storke = 2
		        end_x = x+w
		        end_y = y+h
		        
		        cv.rectangle(frame , (x,y) , (end_x , end_y) , color , storke)
		        img_name = "img.jpg"
		        cv.imwrite(img_name , roi_color)
		        
		        
		    cv.imshow('frame' , frame)
		    
		    if cv.waitKey(20) & 0xFF == ord('q'):
		     break 
		 
		cap.release()
		cv.destroyAllWindows()

		 





	def saveToFile(self):
		id=self.id.text()
		name=self.name.text()
		description=self.description.text()
		csv_writer = csv.writer(open('record.csv' , 'a') , delimiter=',')
		csv_writer.writerow([id , name , description])


		self.message.setText("data saved")



class List(QDialog):
	def __init__(self):
		super(List , self).__init__()
		loadUi("list.ui" , self)

		self.home.clicked.connect(self.backHome)

		self.all_data = pd.read_csv("record.csv")

		numRows = len(self.all_data.index)

		self.tableWidget.setColumnCount(len(self.all_data.columns))
		self.tableWidget.setRowCount(numRows)
		self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)

		for i in range(numRows):
			for j in range(len(self.all_data.columns)):
				self.tableWidget.setItem(i,j,QTableWidgetItem(str(self.all_data.iat[i,j])))


	
	def backHome(self):
		home =mainWindow()
		widget.addWidget(home)
		widget.setCurrentIndex(widget.currentIndex()+1)




# def startVideo(self):

# 	vid = cv2.VideoCapture(0)
# 	cnt=0
# 	frames_to_count=20
# 	st=0
# 	fbs=0

#         # labels = {"person_name": 1 }
#         # with open("labels.pickle" , "rb") as f:
#         #    org_labels = pickle.load(f)
#         #    labels = {v:k for k,v in org_labels.items()}
# 	while(vid.isOpened()):
	        	
# 	            img,self.image = vid.read()
# 	            self.image = imutils.resize(self.image , height = 480)

# 	            gray = cv2.cvtColor(self.image , cv2.COLOR_BGR2GRAY)
# 	            faces = face_casecade.detectMultiScale(gray , 
# 	                scaleFactor = 1.15 ,
# 	                minNeighbors = 7 , 
# 	                minSize = (80,80) , 
# 	                flags = cv2.CASCADE_SCALE_IMAGE)

# 	            for(x,y,w,h) in faces:
# 	                cv2.rectangle(self.image , (x,y) , (x+w , y+h ) , (10 , 228 , 220) , 5 )

# 	                  #print(x,y,w,h)    
# 	                roi_gray = gray[y:y+h , x:x+w]
# 	                roi_color = self.image[y:y+h , x:x+w]
	                
# 	                ###predict the face
# 	                # id_ ,conf = recognizer.predict(roi_gray)
# 	                # if conf >=45 and conf <=85:
# 	                #     print(id_)
# 	                #     print(labels[id_])
# 	                #     font = cv2.FONT_HERSHEY_SIMPLEX
# 	                #     name = labels[id_]
# 	                #     color = (255,255,255)
# 	                #     storke = 2
# 	                #     cv2.putText(self.image , name ,(x,y) ,  font , 1 , color , storke , cv2.LINE_AA)
	              


# 	                if cnt == frames_to_count:
# 	                    try:  
# 	                        print(frames_to_count/(time.time()-st))

# 	                        st=time.time()
# 	                        cnt=0

# 	                    except:
# 	                        pass

# 	                cnt+=1

# 	                if cv2.waitKey(20) & 0xFF == ord('q'):
# 	                  break
	             

			

    
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = mainWindow()
widget.addWidget(mainwindow)
widget.setFixedHeight(700)
widget.setFixedWidth(1024)
widget.show()







sys.exit(app.exec_())