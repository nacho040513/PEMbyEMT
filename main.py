# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.widgets import SpanSelector
from matplotlib.widgets import Cursor
#import sys
#import time
from matplotlib import pyplot
import matplotlib.pyplot as plt

#Import bookstores
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

# class UI main     

class MatplotlibWidget(QMainWindow):

    def __init__(self):      
        QMainWindow.__init__(self) 
        loadUi("LikeMatlab.ui", self)  # Load desginer UI

        self.setWindowTitle("MEPbyTME Analysis - Informatic Tool")

        self.pushButton.clicked.connect(self.loadFile)
        
        self.pushButton_2.clicked.connect(self.span_select)
        self.pushButton_2.setEnabled(False)

        self.radioButton.toggled.connect(self.print_area)
        self.radioButton.setEnabled(False)
        self.radioButton_3.toggled.connect(self.rectify)
        self.radioButton_3.setEnabled(False)
        

    #graphic button
    def loadFile(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Data", "")
        data=np.loadtxt(file)
        self.x=data[:,0]
        self.y=data[:,1]

        self.i=self.x
        self.j=self.y

        self.MplWidget.canvas.axes.clear()
        
        #line = pyplot.plot(self.x,self.y)
        #self.MplWidget.pyplot.setp(line, 'color', 'b', 'linewidth', 0.5)

        self.MplWidget.canvas.axes.plot(self.x,self.y, 'r',linewidth=0.5)
        self.MplWidget.canvas.axes.set_ylabel('Voltage [V]', color='r')
        self.MplWidget.canvas.axes.set_xlabel('Time [s]', color='b')
        #self.MplWidget.canvas.axes.ion()
        #self.MplWidget.canvas.axes.set(ylabel = 'Voltage [V]', xlabel = 'Time [s]')
        #self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        title= file.split('/')
        self.label_2.setText(title[-1])
        self.pushButton_2.setEnabled(True)

        bar = QAction(self.addToolBar(QtCore.Qt.BottomToolBarArea,NavigationToolbar(self.MplWidget.canvas, self)))
        self.addAction(bar)

        self.MplWidget.canvas.draw()
        
    def print_area(self):
        x1 = self.thisx
        y1 = self.thisy
        if self.radioButton.isChecked() == True:
            self.MplWidget.canvas.axes.fill_between(x1, 0, y1,facecolor='blue')
            self.MplWidget.canvas.draw_idle()

        else:
            self.MplWidget.canvas.axes.fill_between(x1,0,y1,facecolor='white')
            self.MplWidget.canvas.draw()

    def onselect(self,vmin, vmax):
        
        indmin, indmax = np.searchsorted(self.x, (vmin, vmax))
        indmax = min(len(self.x) - 1, indmax)

        self.thisx = self.x[indmin:indmax]
        self.thisy = self.y[indmin:indmax]
        
        if(vmax != 0):
            # Next line to set off grid
            self.MplWidget.canvas.axes.grid(0)
            self.cursor.active = False
            self.span.active = False
            self.radioButton.setEnabled(True)
            self.radioButton_3.setEnabled(True)

        self.min=vmin
        self.max=vmax
        self.MplWidget.canvas.axes.axvline(x=self.min)
        self.MplWidget.canvas.axes.axvline(x=self.max)
        self.MplWidget.canvas.axes.annotate('t°', xy=(self.min, 4 ), xycoords='data')
        self.MplWidget.canvas.axes.annotate('tf', xy=(self.max, 4 ), xycoords='data')

        self.label_7.setText(str(vmin))
        self.label_8.setText(str(vmax))

    def span_select(self):
        self.cursor = Cursor(self.MplWidget.canvas.axes, useblit=False, color='blue', linewidth=1,horizOn=False,vertOn=True)
        self.span = SpanSelector(self.MplWidget.canvas.axes, self.onselect, 'horizontal', useblit=True, span_stays=True,
                    rectprops=dict(alpha=0.5, facecolor='blue'))

        self.MplWidget.canvas.axes.grid(color='r', linestyle='-', linewidth=0.1)
        
        self.span.active=True
        self.cursor.active = True


    def rectify(self):

        self.abs_x = self.x
        self.abs_y = self.y
        if self.radioButton_3.isChecked() == True:
            for i in range(len(self.abs_x)):
                for j in range(len(self.thisx)):
                    if(self.abs_x[i]==self.thisx[j]):
                        self.abs_x[i] = np.absolute(self.thisx[j])

            for i in range(len(self.abs_y)):
                for j in range(len(self.thisy)):
                    if(self.abs_y[i]==self.thisy[j]):
                        self.abs_y[i] = np.absolute(self.thisy[j])


            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(self.abs_x,self.abs_y,'r',linewidth=0.5)
            self.MplWidget.canvas.axes.set_ylabel('Voltage [V]', color='r')
            self.MplWidget.canvas.axes.set_xlabel('Time [s]', color='b')
            self.MplWidget.canvas.axes.axvline(x=self.min)
            self.MplWidget.canvas.axes.axvline(x=self.max)
            self.MplWidget.canvas.axes.axvspan(self.min, self.max, facecolor='0.5', alpha=0.5)
            self.MplWidget.canvas.axes.annotate('t°', xy=(self.min, 4 ), xycoords='data')
            self.MplWidget.canvas.axes.annotate('tf', xy=(self.max, 4 ), xycoords='data')
            self.MplWidget.canvas.draw()

        else:
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(self.i,self.j, 'r',linewidth=0.5)
            self.MplWidget.canvas.axes.set_ylabel('Voltage [V]', color='r')
            self.MplWidget.canvas.axes.set_xlabel('Time [s]', color='b')
            self.MplWidget.canvas.axes.axvline(x=self.min)
            self.MplWidget.canvas.axes.axvline(x=self.max)
            self.MplWidget.canvas.axes.axvspan(self.min, self.max, facecolor='0.5', alpha=0.5)
            self.MplWidget.canvas.axes.annotate('t°', xy=(self.min, 4 ), xycoords='data')
            self.MplWidget.canvas.axes.annotate('tf', xy=(self.max, 4 ), xycoords='data')
            self.MplWidget.canvas.draw()




app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()