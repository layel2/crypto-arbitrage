import requests
from myFunc import *
from routeKucoin import *
import datetime as dt
from lineMsg import *
import numpy as np
from autotrade import *

def fullAutoTrade():
	noti_token = "" #Line Token
	noti_url = "https://notify-api.line.me/api/notify"
	noti_headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+noti_token}
	#select = {1:getRoute(bx,bt),2:getRoute2(),3:getRoute3(bx,kucoin),4:getRoute4(bt,kucoin)}
	bx = getBx()
	bt = getBittrex()
	kucoin = getKucoin()
	Route = getRoute(bx,bt)

	if(Route.tradeRoute != []):
		noti_msg = str(dt.datetime.now()) +'Bx -> Bt'+"\n"
		for i in range(len(Route.tradeRoute)):
			noti_msg += str(Route.tradeRoute[i]) + "\n" + str(Route.profit[i]) +"\n" +"---------"+"\n"
			#print(r.text)		
	r=requests.post(noti_url,headers = noti_headers ,data = {'message':noti_msg})
	if(Route.tradeRoute != []):
		if(np.max(Route.profit) > 5):
			print("Trade!")
			sentLine("Start Trade")
			maxR = np.argmax(Route.profit)
			route = Route.tradeRoute[maxR]
			sentLine("Route "+ str(route))
			Trade = routeTrade(Route.profit,Route.tradeRoute)
			sentLine(Trade)

while True:
	fullAutoTrade()
	pass



