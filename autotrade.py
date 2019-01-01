import numpy as np
import bxapi
import bittrexapi
import time
import requests

def bxTrade(pairing):
	tradeA = pairing.split('-')[0]
	tradeB = pairing.split('-')[1]
	if(bxapi.getPairID(pairing) == None):
		pairing = "%s-%s"%(tradeB,tradeA)
		tradeType = 'sell'
	else:
		tradeType = 'buy'
	amount = bxapi.getBalance(tradeA)
	if(tradeType == 'buy'):
		tradeTypeCheck = 'sell'
	elif(tradeType == 'sell'):
		tradeTypeCheck = 'buy'
	rate,maxAm = bxapi.getPrice(pairing,tradeTypeCheck)
	beforeTrade = bxapi.getBalance(tradeB)
	order = bxapi.createOrder(pairing,tradeType,amount,rate)
	print(order)
	if(order['success'] == False):
		print("error bxTrade()")
		print(order['error'])
		exit()

	while True:
		time.sleep(10)
		afterTrade = bxapi.getBalance(tradeB)
		if(tradeType == 'buy'):
			if(float(afterTrade) > float(beforeTrade)+0.8*amount/rate):
				break;
		elif(tradeType == 'sell'):
			if(float(afterTrade) > float(beforeTrade)+0.8*amount*rate):
				break;
		else:
			amount = bxapi.getBalance(tradeA)
			rate,maxAm = bxapi.getPrice(pairing,tradeTypeCheck)
			order = bxapi.createOrder(pairing,tradeType,amount,rate)
			print(order)
		pass
	print('Success')

def bittrexTrade(pairing):
	tradeA = pairing.split('-')[0]
	tradeB = pairing.split('-')[1]
	allm = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets").json()
	for i in range(0,len(allm['result'])):
		if(allm['result'][i]['BaseCurrency']==tradeA and allm['result'][i]['MarketCurrency']==tradeB):
			tradePair = allm['result'][i]['MarketName']
			tradeType = 'buy'
		elif(allm['result'][i]['BaseCurrency']==tradeB and allm['result'][i]['MarketCurrency']==tradeA):
			tradePair = allm['result'][i]['MarketName']
			tradeType = 'sell'

	amount = bittrexapi.getBalance(tradeA)
	if(tradeType == 'buy'):
		tradeTypeCheck = 'sell'
	elif(tradeType == 'sell'):
		tradeTypeCheck = 'buy'

	rate,maxAm = bittrexapi.getPrice(tradePair,tradeTypeCheck)
	beforeTrade = bittrexapi.getBalance(tradeB)
	print(pairing)
	print(tradeType)
	print(amount)
	print(rate)
	print(amount/rate)
	order = bittrexapi.createOrder(tradePair,tradeType,amount,rate)
	print(order)
	if(order['success'] == False):
		print("error bittrexTrade()")
		print(order['message'])
		exit()

	while True:
		time.sleep(10)
		afterTrade = bittrexapi.getBalance(tradeB)
		if(tradeType == 'buy'):
			if(float(afterTrade) > float(beforeTrade)+0.8*amount/rate):
				break;
		elif(tradeType == 'sell'):
			if(float(afterTrade) > float(beforeTrade)+0.8*amount*rate):
				break;
		else :
			amount = bittrexapi.getBalance(tradeA)
			rate,maxAm = bittrexapi.getPrice(tradePair,tradeTypeCheck)
			order = bittrexapi.createOrder(tradePair,tradeType,amount,rate)
			print(order)
		pass
	print("Success")


def routeTrade(profit,tradeRoute):
    maxR = np.argmax(profit)
    route = tradeRoute[maxR]
    print("Start Trade")
    print(route)
    #---bx THB->A ----
    print("In Bx Trading")
    bxTrade(route[0])
    print("In Bx Trade Success")
    #--- bx->bittrex ---
    print("Sending to bittrex")
    sendCur1 = route[0].split('-')[1]
    print(sendCur1)
    sendAmount1 = bxapi.getBalance(sendCur1)
    sendA1 = bittrexapi.getDepositAddr(sendCur1)
    if(sendA1['success'] == False):
    	exit()
    sendAddr1 = sendA1['result']['Address']
    if(sendCur1 == 'XRP'):
    	sendAddr1 = '' #xrp addr
    #print(sendAddr1)
    beforeSend1 = bittrexapi.getBalance(sendCur1)
    tran1 = bxapi.withdraw(sendCur1,sendAmount1,sendAddr1)
    print(tran1)
    if(tran1['success'] == False):
    	print('Trans1 error')
    	print(tran1['error'])
    	exit()
    while True:
    	time.sleep(90)
    	afterSend1 = bittrexapi.getBalance(sendCur1)
    	if(afterSend1 == None or beforeSend1 == None):
    		if(afterSend1 != None):
    			break;
    	elif(afterSend1 > beforeSend1):
    		break;
    	pass
    print('Now at bittrex')
    #----@bittrex B/A
    print("In Bittrex Trading")
    bittrexTrade(route[1])
    print("In Bittrex Trade Success")
    #----@bittrex B/C
    print("In Bittrex Trading")
    bittrexTrade(route[2])
    print("In Bittrex Trade Success")
    #send back to bx
    sendCur2 = route[2].split('-')[1]
    sendAmount2 = bittrexapi.getBalance(sendCur2)
    '''sendA2 = bxapi.getDepositAddr2(sendCur2)
    if(sendA2['success'] == False):
    	exit()'''
    sendAddr2 = bxapi.getDepositAddr2(sendCur2)
    beforeSend2 = bxapi.getBalance(sendCur2)
    print("Sending to Bx")
    tran2 = bittrexapi.withdraw(sendCur2,sendAmount2,sendAddr2)
    print(tran2)
    if(tran2['success']==False):
    	print('trans 2 error')
    	print(tran2['message'])
    	exit()
    while True:
    	time.sleep(90)
    	afterSend2 = bxapi.getBalance(sendCur2)
    	if(afterSend2 > beforeSend2):
    		break;
    	pass
    print("Now at Bx")
    #BX trade back to thb
    print("In Bx Trading")
    bxTrade(route[3])
    print("In Bx Trade Success")
    print("In Bx Trading")
    bxTrade(route[4])
    print("In Bx Trade Success")
    print("Program Trade Complete")
    return "Trade Complete"

#profit = [0,2]
#tradeRoute = [[],['THB-GNO','GNO-BTC','BTC-DOG','DOG-BTC','BTC-THB']]
#routeTrade(profit,tradeRoute)
#bittrexTrade("BTC-FTC")