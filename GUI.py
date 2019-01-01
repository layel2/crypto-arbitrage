from tkinter import *
from tkinter import ttk
from myFunc import *
import numpy as np
from autotrade import *
from tkinter import messagebox
import tkinter
import bxapi
import bittrexapi
import time
import datetime as dt
import threading


def run():
	ttt.configure(state=NORMAL)
	ttt.insert(END,f"Checking Route time:{str(dt.datetime.now())} \n")
	bx = getBx()
	bt = getBittrex()
	Route = getRoute(bx,bt)
	if(Route.tradeRoute == []):
		ttt.insert(END," No Route Found!\n")
		ttt.insert(END," Delaying 2 Mins\n")
		time.sleep(120)
		run()
	else :
		msg = ""
		for i in range(len(Route.tradeRoute)):
			msg += str(Route.tradeRoute[i]) + "\n" + str(Route.profit[i]) +"\n"
		ttt.insert(END,msg)
		if(np.max(Route.profit) > 5):
			ttt.insert(END,"Start Trade\n")
			maxR = np.argmax(Route.profit)
			route = Route.tradeRoute[maxR]
			ttt.insert(END,"Route "+ str(route)+"\n")
			Trade = routeTrade(Route.profit,Route.tradeRoute)
			ttt.insert(END,str(Trade)+"\n")
		else :
			ttt.insert(END,"Don't trade Profit too low(High risk)\n")
			run()


def call_run():
		if(not keyCheck()):
			messagebox.showinfo("Error", "Plseae fill the API Key at setting page first")
			return;
		ttt.configure(state=NORMAL)
		ttt.delete(1.0,END)
		ttt.configure(state=DISABLED)
		global lb1_status
		if(lb1_status == False):
			messagebox.showinfo("Title", "Program is Running !!!")
			return
		else :
			ttt.delete(1.0,END)
			thread2 = threading.Thread(target = run)
			thread2.start()

def transhistory():
	if(not keyCheck()):
		messagebox.showinfo("Error", "Plseae fill the API Key at setting page first")
		return;
	ttt2.config(state=NORMAL)
	if(Transhis_box.get() == 'bx'):
	#lif(Transhis_box.get() == 'bittrex'):
		data = bxapi.TransHistory()
		#print ("a")
		for i in range(len(data)):
			ttt2.insert(END,f"Date : {data[i]['date']} , Currency : {data[i]['currency']} , Amount : {data[i]['amount']} , Type : {data[i]['type']} \n")
	ttt2.config(state=DISABLED)

def tab3Save():
	bxapi.key = entrytab3_1.get()
	bxapi.secret = entrytab3_2.get()
	bittrexapi.key = entrytab3_3.get()
	bittrexapi.secret = entrytab3_4.get()

def keyCheck():
		if(bxapi.key == "" or bxapi.secret==""or bittrexapi.key  == "" or bittrexapi.secret==""):
			return False
		else : return True 

def showGetPrice():
	if(not keyCheck()):
		messagebox.showinfo("Error", "Plseae fill the API Key at setting page first")
		return;
	if(selEx1.get() == 'bx'):
		priceTxt = bxapi.getPrice(entrytab2_1.get(),type1.get())[0]
		labeltab2_2.config(text = priceTxt)
	elif(selEx1.get() == 'bittrex'):
		labeltab2_2.config(text = bittrexapi.getPrice(entrytab2_1.get(),type1.get())[0])

def showGetBalance():
	if(not keyCheck()):
		messagebox.showinfo("Error", "Plseae fill the API Key at setting page first")
		return;
	#print (type(selEx2))
	if(selEx2.get() == 'bx'):
		labeltab2_4.config(text = bxapi.getBalance(entrytab2_2.get()))
	elif(selEx2.get() == 'bittrex'):
		labeltab2_4.config(text = bittrexapi.getBalance(entrytab2_2.get()))
	#print(type1.get())

def findPath():
	global lb1_status
	lb1_status = False
	ttt.configure(state=NORMAL)
	ttt.delete(1.0,END)
	ttt.insert(END,'Please Wait !!!')
	#time.sleep(1)
	bx = getBx()
	bt = getBittrex()
	Route = getRoute(bx,bt)
	ttt.delete(1.0,END)
	if(len(Route.profit) == 0) : ttt.insert(END,'No Route')
	for i in range(len(Route.profit)):
		print("Profit : %f <> Route : %s \n"%(Route.profit[i],Route.tradeRoute[i]))
		ttt.insert(END,"Profit : %f <> Route : %s \n"%(Route.profit[i],Route.tradeRoute[i]))
	ttt.configure(state=DISABLED)
	lb1_status = True

def call_findPath():
	if(not keyCheck()):
		messagebox.showinfo("Error", "Plseae fill the API Key at setting page first")
		return;
	global lb1_status
	if(lb1_status == False):
		messagebox.showinfo("Title", "Program is Running !!!")
		return
	else:
		thread = threading.Thread(target = findPath)
		thread.start()

def testF():
	stop.clear()
	for i in range(1,100):
		ttt.configure(state=NORMAL)
		time.sleep(0.5)
		ttt.insert(END,str(i)+'\n')
		ttt.configure(state=DISABLED)
def stopF():
	stop.set()
	
def boom():
	gui.destroy()
"""
def showTrans():
	ttt2.config(state=NORMAL)
	transData = bxapi.TransHistory()
	print(transData)
	for i in range(len(transData)):
		print('w')
		print(f"Date : {transData[i]['date']} , Currency : {transData[i]['currency']} , Amount : {transData[i]['amount']} , Type : {transData[i]['type']}")

	ttt2.config(state=DISABLED)
"""

stop = threading.Event()

gui = Tk()
gui.title("Bx & Bittrex Arbitrage")
gui.geometry("640x640") #640x640
gui.configure(bg = "grey")

tab_ctrl = ttk.Notebook(gui)


#tab1
tab1 = ttk.Frame(tab_ctrl)
tab_ctrl.add(tab1,text="Home")
labeltab1_1 = Label(tab1,text = "Bx & Bittrex",fg = "#CD5C5C",font = (40))
labeltab1_1.place(x=260,y = 10)
labeltab1_2 = Label(tab1,text = "Arbitrage",fg = "#CD5C5C",font = (40))
labeltab1_2.place(x=270,y = 40)
buttontab1_1 = Button(tab1,text = "Run",height = 2,width = 13,command = call_run)
buttontab1_1.place(x=100 ,y = 500)
buttontab1_2 = Button(tab1,text = "Find path",height = 2,width = 13,command = call_findPath)
buttontab1_2.place(x=400 ,y = 500)
buttontab1_3 = Button(tab1,text = "Stop",height = 2,width = 13,command = boom)
buttontab1_3.place(x=100 ,y = 550)
ttt = Text(tab1,height = 25,width = 90) #big box
ttt.place(x=35,y=70)

lb1_status = True
#ttt.pack(side=LEFT, fill=Y)
#ttt.insert(END,'sdaasda')
#for i in range(1,100):
#	ttt.insert(END,str(i)+'\n')
ttt.config(state=DISABLED)
#tab2
tab2 = ttk.Frame(tab_ctrl)
tab_ctrl.add(tab2,text = "Info")
lbtype2_11 = Label(tab2,text = "Exchange",fg = 'black')
lbtype2_11.place(x=80,y = 2)
lbtype2_12 = Label(tab2,text = "Pair",fg = 'black')
lbtype2_12.place(x=150,y = 2)
lbtype2_13 = Label(tab2,text = "Trade Type",fg = 'black')
lbtype2_13.place(x=230,y = 2)


labeltab2_1 = Label(tab2,text = "Get Price",fg = 'black')
labeltab2_1.place(x=5,y = 20)
selEx1 = ttk.Combobox(tab2, values=['bx','bittrex'],height = 1,width = 5)
selEx1.place(x=80,y = 20)
entrytab2_1 = Entry(tab2,width = 10)
entrytab2_1.place(x=150,y = 20)
type1 = ttk.Combobox(tab2, values=['buy','sell'],height = 1,width = 5)
type1.place(x=230,y = 20)
buttontab2_1 = Button(tab2,text = "Ok",height = 1,width = 5,command = showGetPrice)
buttontab2_1.place(x=300,y = 20)
labeltab2_2 = Label(tab2,text = "",fg = 'black')
labeltab2_2.place(x=80,y = 40)

lbtype2_21 = Label(tab2,text = "Exchange",fg = 'black')
lbtype2_21.place(x=80,y = 60)
lbtype2_22 = Label(tab2,text = "Coin Name",fg = 'black')
lbtype2_22.place(x=150,y = 60)


labeltab2_3 = Label(tab2,text = "My Balance",fg = 'black')
labeltab2_3.place(x=5,y = 80)
selEx2 = ttk.Combobox(tab2, values=['bx','bittrex'],height = 1,width = 5)
selEx2.place(x=80,y = 80)
entrytab2_2 = Entry(tab2,width = 10)
entrytab2_2.place(x=150,y = 80)
buttontab2_2 = Button(tab2,text = "Ok",height = 1,width = 5,command = showGetBalance)
buttontab2_2.place(x=300,y = 80)
labeltab2_4 = Label(tab2,text = "",fg = 'black')
labeltab2_4.place(x=230,y = 80)

lbtype2_21 = Label(tab2,text = "Exchange",fg = 'black')
lbtype2_21.place(x=150,y = 100)

Transhis_label = Label(tab2,text = "Transactions History",fg = 'black')
Transhis_label.place(x=5 , y = 120)
Transhis_box = ttk.Combobox(tab2, values=['bx','bittrex'],height = 1,width = 5)
Transhis_box.place(x=150 , y = 120)

Transhis_box_ok = Button(tab2,text = "Ok",height = 1,width = 5,command = transhistory)
Transhis_box_ok.place(x=300,y = 120)

ttt2 = Text(tab2,height = 15,width = 100)
ttt2.place(x=5,y=160)


#ttt2.insert(END,bxapi.wdHistory())




ttt2.config(state=DISABLED)

#tab3
tab3 = ttk.Frame(tab_ctrl)
tab_ctrl.add(tab3,text="Setting")

labeltab3_1 = Label(tab3,text = "Bx",fg = 'black',font =(30))
labeltab3_1.place(x=300,y = 10)
labeltab3_2 = Label(tab3,text = "API key",fg = 'black',)
labeltab3_2.place(x=70,y = 50)
entrytab3_1 = Entry(tab3,width = 60)
entrytab3_1.place(x=150,y = 50)
labeltab3_3 = Label(tab3,text = "API secret",fg = 'black',)
labeltab3_3.place(x=70,y = 70)
entrytab3_2 = Entry(tab3,width = 60)
entrytab3_2.place(x=150,y = 70)

labeltab3_4 = Label(tab3,text = "Bittrex",fg = 'black',font =(30))
labeltab3_4.place(x=280,y = 100)
labeltab3_5 = Label(tab3,text = "API key",fg = 'black',)
labeltab3_5.place(x=70,y = 140)
entrytab3_3 = Entry(tab3,width = 60)
entrytab3_3.place(x=150,y = 140)
labeltab3_6 = Label(tab3,text = "API secret",fg = 'black',)
labeltab3_6.place(x=70,y = 160)
entrytab3_4 = Entry(tab3,width = 60)
entrytab3_4.place(x=150,y = 160)
buttontab3_1 = Button(tab3,text = "Send",height = 2,width = 13,command = tab3Save)
buttontab3_1.place(x=260,y = 200)

#push
tab_ctrl.pack(expand = 1,fill = 'both')





gui.mainloop()