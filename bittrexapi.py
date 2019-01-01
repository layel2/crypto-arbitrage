import requests
import hashlib
import time
import hmac

key = ""
secret = ""


def createOrder(pairing,tradeType,amount,rate): #type buy or sell
	pairing=DOGcheck(pairing)
	nonce = str(time.time())
	if(tradeType=='buy'):
		amount = amount/rate

	amount = amount*0.99
	url = "https://api.bittrex.com/api/v1.1/market/"+tradeType+"limit?"
	url = url+"apikey="+key+"&nonce="+nonce+"&market="+pairing+"&quantity="+str(amount)+"&rate="+str(rate)
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()

def getBalance(currency):
	currency=DOGcheck(currency)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/account/getbalance?"
	url = url+"apikey="+key+"&nonce="+nonce+"&currency="+currency
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()['result']['Balance']

def getDepositAddr(currency):
	currency=DOGcheck(currency)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/account/getdepositaddress?"
	url = url+"apikey="+key+"&nonce="+nonce+"&currency="+currency
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()

def withdraw(currency,amount,addr,payId=None):
	currency=DOGcheck(currency)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/account/withdraw?"
	if(currency == 'XRP' and (payId!=None) ):
		url = 	url = url+"apikey="+key+"&nonce="+nonce+"&currency="+currency+"&quantity="+str(amount)+"&address="+addr.split('?dt=')[0]+"&paymentid="+addr.split('?dt=')[1]
	else:
		url = url+"apikey="+key+"&nonce="+nonce+"&currency="+currency+"&quantity="+str(amount)+"&address="+addr
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()

def orderHistory(pairing):
	pairing=DOGcheck(pairing)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/account/getorderhistory?"
	url = url+"apikey="+key+"&nonce="+nonce+"&market="+pairing
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()

def getPrice(pairing,tradeType):
	pairing=DOGcheck(pairing)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/public/getorderbook?"
	url = url+"apikey="+key+"&nonce="+nonce+"&market="+pairing+"&type="+tradeType
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()['result'][0]['Rate'] , r.json()['result'][0]['Quantity']

def DOGcheck(pairing):
	tempPair = pairing.split('-')
	if(len(tempPair) == 1):
		if(pairing == 'DOG'):
			pairing = 'DOGE'
	elif(len(tempPair) == 2):
		if(tempPair[0] == 'DOG'):
			tempPair[0] = 'DOGE'
			pairing = '%s-%s'%(tempPair[0],tempPair[1])
		elif(tempPair[1] == 'DOG'):
			tempPair[1] = 'DOGE'
			pairing = '%s-%s'%(tempPair[0],tempPair[1])
	return pairing
def pairCheck(pairing):
	pairing=DOGcheck(pairing)
	nonce = str(time.time())
	url = "https://api.bittrex.com/api/v1.1/public/getticker?"
	url = url+"apikey="+key+"&nonce="+nonce+"&market="+pairing
	signature = hmac.new(secret.encode('ASCII'),url.encode('ASCII'),hashlib.sha512).hexdigest()
	r=requests.get(url,headers={'apisign':signature})
	return r.json()['success']

#a = orderHistory('BTC-BSV')
#print(a)
'''bx_sent_cur = ['BTC','ETH','REP','BCH','BSV','XCN','DAS','DOG','EOS','EVX','FTC','GNO','HYP','LTC','NMC','OMG','PND','XPY','PPC','POW','XPM','XRP','ZEC','XZC','ZMN']
for i in bx_sent_cur:
	print(getDepostiAddr(i))'''

#print(getPrice('BTC-XRP','sell'))
#print(type(getBalance('BTC')))
#print(createOrder('ETH-DOGE','buy',1,1))
#print(DOGcheck('DOG'))
#print(getDepositAddr('BSV'))

'''a=getBalance('XRP')
print(a)
print(a == None)'''
#print(pairCheck('XRP-BTC'))