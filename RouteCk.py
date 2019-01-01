import requests
from myFunc import *
from routeKucoin import *
import datetime as dt

def RouteCkLine():
	noti_token = ""
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
			noti_msg += str(Route.tradeRoute[i]) + "\n" + str(Route.profit) +"\n" +"---------"+"\n"
			print(noti_msg)		
			r=requests.post(noti_url,headers = noti_headers ,data = {'message':noti_msg})
			#print(r.text)

	Route = getRoute3(bx,kucoin)

	if(Route.tradeRoute != []):
		noti_msg = str(dt.datetime.now()) +'Bx -> Kucoin'+"\n"
		for i in range(len(Route.tradeRoute)):
			noti_msg += str(Route.tradeRoute[i]) + "\n" + str(Route.profit) +"\n" +"---------"+"\n"
			print(noti_msg)		
			r=requests.post(noti_url,headers = noti_headers ,data = {'message':noti_msg})
			#print(r.text)