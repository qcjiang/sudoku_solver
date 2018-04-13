# -*- coding: utf-8 -*-
from __future__ import division
import random
import itertools
from copy import deepcopy
import Sudoku
from numpy import *
import wx
import random
class mainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None, -1, 'Sudoku', size=(400,580))	
		panel=wx.Panel(self)
		panel.SetBackgroundColour('White')
		insize = (25,25)
		userTextPosX = 20# 左上角起始点x坐标
		userTextPosY = 20# 左上角起始点y坐标
		textWidth = 25# 文本框宽度
		idleWidth = 10#横向间距
		idleHeight = 35#纵向间距
		sperateLength = 10 #九宫格间距
		for row in range(0,9):
			for colunm in range(0,9):	
				userText_i_j = 'self.userText'+'%d' %row+'%d' %colunm
				exec(userText_i_j + " =wx.TextCtrl(panel, -1, '0', pos = (userTextPosX + colunm * (textWidth + idleWidth) + colunm // 3 * sperateLength, userTextPosY + row * idleHeight + row // 3 * sperateLength), size = insize)")
				#exec(userText_i_j + ".SetValue(str(row*9+colunm+1))")
		self.button1 = wx.Button(panel,  label = "arti_gen", pos = (15, 350), size = (100, 30), id = 1)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button1)
		self.button2 = wx.Button(panel, label = "auto_gen", pos = (15, 380), size = (100, 30), id = 2)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button2)
		self.button3 = wx.Button(panel, label = "check_answer", pos = (15, 410), size = (100, 30), id = 3)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button3)	
		self.button4 = wx.Button(panel, label = "show_result", pos = (15, 440), size = (100, 30), id = 4)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button4)
		self.button5 = wx.Button(panel, label = "check_exit", pos = (15, 470), size = (100, 30), id = 5)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button5)
		self.button6 = wx.Button(panel, label = "all_clear", pos = (15, 500), size = (100, 30), id = 6)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button6)
		self.button7 = wx.Button(panel, label = "Solve", pos = (15, 530), size = (100, 30), id = 7)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.button7)

		self.userText2=wx.TextCtrl(panel,-1,"请输入难度1～4",pos = (125,382), size = (100,25))
		self.userText3=wx.TextCtrl(panel,-1,"result",pos = (125,410), size = (100,25))
		self.userText4=wx.TextCtrl(panel,-1,"result",pos = (125,470), size = (100,25))
		self.Sudoku = zeros((9, 9), dtype = int32)# 数独阵列
		self.Solution = zeros((9, 9), dtype = int32)# 解阵列

	def OnClick(self, event):  
		Allzero = True
		Id = event.GetId()
		
		if Id == 1:
			Label = self.button1.GetLabel() 
			if Label == "arti_gen":
				self.button1.SetLabel("Waiting...")# 按钮提示等待
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec("self.Sudoku[i][j] = " + userText_i_j + ".GetValue()")
						#print self.Sudoku[i][j]
						if self.Sudoku[i][j] not in range(0,10):
							dlg = wx.MessageDialog(self, "Only numbers (0~9, 0 for blank) allowed!", "Error", wx.OK)
							dlg.ShowModal()
							dlg.Destroy()
							self.button1.SetLabel("arti_gen")# 刷新按钮
							return
						if Allzero == True and self.Sudoku[i][j] != 0:
							Allzero =False
				if Allzero == True:
					dlg = wx.MessageDialog(self, "Please input your Sukudo!", "Error", wx.OK)
					dlg.ShowModal()
					dlg.Destroy()
					self.button1.SetLabel("arti_gen")# 刷新按钮
					return

				if Sudoku.Solve_Sudoku(self.Sudoku, 0)[1] == False:
					dlg = wx.MessageDialog(self, "无解", "Error", wx.OK)
					dlg.ShowModal()
					dlg.Destroy()
					
					self.button1.SetLabel("Clear")
				else:
					self.Solution = Sudoku.Solve_Sudoku(self.Sudoku, 0)[0]
					Sudoku.FSingleSolution = False
					for i in range(0, 9):
						for j in range(0, 9):
							userText_i_j = "self.userText" + "%d" %i  +"%d" %j
							exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
					self.button1.SetLabel("Clear")
			elif Label == "Clear":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec(userText_i_j+".SetValue('0')")
				self.button1.SetLabel("arti_gen")
		elif Id == 2:
			Label = self.button2.GetLabel() 
			if Label == "auto_gen":
				seed =random.randint(1,9)
				degree = self.userText2.GetValue()
				self.Sudoku[0][0] = seed
				self.Solution = Sudoku.Solve_Sudoku(self.Sudoku, 0)[0]
				for i in range(0, 9):
					for j in range(0, 9):
						seed2 = random.random()
						if degree == '1':
							if seed2 > 0.05:
								userText_i_j = "self.userText" + "%d" %i  +"%d" %j
								exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
						if degree == '2':
							if seed2 > 0.5:
								userText_i_j = "self.userText" + "%d" %i  +"%d" %j
								exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
						if degree == '3':
							if seed2 > 0.6:
								userText_i_j = "self.userText" + "%d" %i  +"%d" %j
								exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
						if degree == '4':
							if seed2 > 0.7:
								userText_i_j = "self.userText" + "%d" %i  +"%d" %j
								exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
				self.button2.SetLabel("Clear")
				print self.Sudoku
				print self.Solution
			elif Label == "Clear":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec(userText_i_j+".SetValue('0')")
				self.button2.SetLabel("auto_gen")
		elif Id == 3:
			Label = self.button3.GetLabel()
			if Label == "check_answer":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec("self.Sudoku[i][j] = " + userText_i_j + ".GetValue()")
			print Sudoku.check_sudoku(self.Sudoku)
			self.userText3.SetValue(str(Sudoku.check_sudoku(self.Sudoku)))
		elif Id == 4:
			Label = self.button4.GetLabel()
			if Label == "show_result":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec(userText_i_j + ".SetValue(str(self.Solution[i][j]))")
		elif Id == 5:
			Label = self.button5.GetLabel()
			if Label == "check_exit":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec("self.Sudoku[i][j] = " + userText_i_j + ".GetValue()")
			if Sudoku.Solve_Sudoku(self.Sudoku, 0)[1] == False:
				self.userText4.SetValue("False")
			else:
				self.userText4.SetValue("True")
			'''self.button5.SetLabel("Clear")
			if Label == "Clear":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec(userText_i_j+".SetValue('0')")
				self.button5.SetLabel("check_exit")'''
		elif Id ==6:
			Label = self.button6.GetLabel()
			if Label == "all_clear":
				for i in range(0,9):
					for j in range(0,9):	
						userText_i_j = "self.userText"+"%d" %i+"%d" %j
						exec(userText_i_j+".SetValue('0')")
				self.Sudoku = zeros((9, 9), dtype = int32)# 数独阵列
				self.Solution = zeros((9, 9), dtype = int32)# 解阵列
				print self.Sudoku
				print self.Solution
		elif Id ==7:
			Label = self.button7.GetLabel()
			if Label == "Solve":  
				self.button7.SetLabel("Waiting...")# 按钮提示等待  
				FAllZero = True# 全零标识  
				for i in range(0, 9):  
					for j in range(0, 9):   
						userText_i_j= "self.userText" + "%d" %i  +"%d" %j
						exec("self.Sudoku[i][j] = " + userText_i_j+ ".GetValue()")
						if self.Sudoku[i][j] != 0 and self.Sudoku[i][j] != 1 and self.Sudoku[i][j] != 2 and self.Sudoku[i][j] != 3 and self.Sudoku[i][j] != 4 and self.Sudoku[i][j] != 5 and self.Sudoku[i][j] != 6 and self.Sudoku[i][j] != 7 and self.Sudoku[i][j] != 8 and self.Sudoku[i][j] != 9:  
							dlg = wx.MessageDialog(self, "Only numbers (0~9, 0 for blank) allowed!", "Error", wx.OK)  
							dlg.ShowModal()  
							dlg.Destroy()  
							self.button7.SetLabel("Solve")# 刷新按钮  
							return  
							# 检验数独阵列是否输入  
						if FAllZero == True and self.Sudoku[i][j] != 0:  
							FAllZero = False
				if FAllZero == True:
					dlg = wx.MessageDialog(self, "Please input your Sukudo!", "Error", wx.OK)  
					dlg.ShowModal()  
					dlg.Destroy()  
					self.button7.SetLabel("Solve")# 刷新按钮  
					return   
				self.Solution = Sudoku.Solve_Sudoku1(self.Sudoku, 0)# 解数独  
				Sudoku.FSingleSolution = False# 刷新求解函数状态  
				for i in range(0, 9):  
					for j in range(0, 9):  
						userText_i_j= "self.userText" + "%d" %i  +"%d" %j# self.userText_0_0...Map_i_j...Map_8_8  
						exec(userText_i_j+ ".SetValue(str(self.Solution[i][j]))")# 输出解阵列  
						self.button7.SetLabel("Clear")
			elif Label == "Clear": 
				for i in range(0, 9):  
					for j in range(0, 9):
						userText_i_j= "self.userText" + "%d" %i  +"%d" %j# self.userText_0_0...Map_i_j...Map_8_8  
						exec(userText_i_j+ ".SetValue('0')")# 清除数独阵列  
				self.button7.SetLabel("Solve")


app=wx.PySimpleApp()
frame=mainFrame()
frame.Show()
app.MainLoop()        
		