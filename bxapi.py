import requests
import hashlib
import time


key = ""
secret = ""

#nonce = str(time.time())
#signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();

def createOrder(pairing,tradeType,amount,rate):
	pairID = getPairID(pairing)
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	amount = float(amount)
	rate = float(rate)
	url = "https://bx.in.th/api/order/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature,'pairing':pairID,'type':tradeType,'amount':amount,'rate':rate});
	return r.json()

def cancelOrder(pairing,order_id):
	nonce = str(time.time())
	pairID = getPairID(pairing)
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/cancel/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature,'pairing':pairID,'order_id':order_id});
	return r.json()

def getBalances():
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/balance/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature});
	return r.json()

def getBalance(currency):
		return float(getBalances()['balance'][currency]['available'])

def getDepositAddr(currency):
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/deposit/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature,'currency':currency});
	return r.json()

def getDepositAddr2(currency):
	curAddr={'BTC':'3Hy1YoEmDQYeG1p3tKJgPBDMmTAmT8sfy7','ETH':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19','REP':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19','BCH':'bitcoincash:qp6n6kn0lkkenxwhd9dsajnd90n7p5eq0cwn7zfhgj','BSV':'bitcoincash:qp6n6kn0lkkenxwhd9dsajnd90n7p5eq0cwn7zfhgj','DAS':'Xc6ibPyBwjfDtYvva4dNg7R6rP8xuJNCqG','DOG':'DByLBCnEVwCu7hEekE7H2ZXNY68ijkfRQT','DOGE':'DByLBCnEVwCu7hEekE7H2ZXNY68ijkfRQT','FTC':'6uwzEKjapNpNvs9ovhpjnyaV1jf1r9TwK9','GNO':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19','LTC':'LeqJRqF7R9VDTquVUqZosgLjshQriwwex4','OMG':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19','POW':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19','XRP':'rp7Fq2NQVRJxQJvUZ4o8ZzsTSocvgYoBbs?dt=1033113822','ZEC':'t1avqg1RmHp895os4NWVnj8uMAZyPTHAhSH','XZC':'0xFf5ec360bc180e219D36088F3F2935E629Af9F19'}
	return curAddr[currency]

def withdraw(currency,amount,addr): #for XRP addr+'?dt='+tag
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/withdrawal/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature,'currency':currency,'amount':amount,'address':addr});
	return r.json()

def wdHistory():
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/withdrawal-history/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature});
	return r.json()

def TransHistory():
	nonce = str(time.time())
	signature = hashlib.sha256((key+nonce+secret).encode('ASCII')).hexdigest();
	url = "https://bx.in.th/api/history/"
	r=requests.post(url, data = {'key':key,'nonce':nonce,'signature':signature});
	return r.json()['transactions']

def getPrice(pairing,tradeType):
	pairID = getPairID(pairing)
	url = "https://bx.in.th/api/orderbook/?pairing="+str(pairID)
	r = requests.get(url)
	data = r.json()
	if(tradeType == 'buy'):
		return float(data['bids'][0][0]),float(data['bids'][0][1])
	if(tradeType == 'sell'):
		return float(data['asks'][0][0]),float(data['asks'][0][1])

def getPairID(pairing):
	url = "https://bx.in.th/api/pairing/"
	req = requests.get(url)
	allPair = req.json()
	pairing = pairing.split('-')
	for i in range(1,35):
		try:
			if(pairing[0]==allPair[str(i)]['primary_currency'] and pairing[1]==allPair[str(i)]['secondary_currency']):
				return i
		except:
			pass

'''a,s =getPrice('THB-DOG','buy')
print(a)
print(s)'''
#print(getPairID('THB-XRP')==None)
#w=createOrder('BTC-XRP','buy',1,0.0001)
#print(w)
#print(getDepositAddr('ETH'))
#print(getPrice('THB-BTC','sell'))
#print(getDepositAddr2('DOGE'))
#print(getBalance('THB'))
#print(TransHistory()[3])
#print(getBalance('THB'))

