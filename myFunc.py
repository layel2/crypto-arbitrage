#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import bxapi

# In[7]:


class getBx():
    def __init__(self):
        self.data()
    def data(self):
        bx_pair = requests.get('https://bx.in.th/api/pairing/')
        bx_data_pair = bx_pair.json()
        #money = 800 ;
        money = bxapi.getBalance('THB')
        print(f"Current Money : {money}")
        bx_price = [0]*40
        bx_price_buy = [0]*40
        bx_price_sell = [0]*40
        bx_name_pri = [0]*40
        bx_name_sec = [0]*40
        for i in range(1,35):
            try:
                bx_price[i] = requests.get('https://bx.in.th/api/orderbook/?pairing='+str(i))
                bx_price[i] = bx_price[i].json()
                bx_price_sell[i] = float(bx_price[i]['asks'][0][0])
                bx_price_buy[i] = float(bx_price[i]['bids'][0][0])
                bx_name_pri[i] = bx_data_pair[str(i)]['primary_currency']
                bx_name_sec[i] = bx_data_pair[str(i)]['secondary_currency']


            except:
                pass

        THB_id = []
        bx_cur_to_thb = []

        for i in range(1,35):
            try:
                if(bx_data_pair[str(i)]['primary_currency']=='THB'):
                    THB_id.append(i)
                    bx_cur_to_thb.append(bx_data_pair[str(i)]['secondary_currency'])
            except:
                pass
        self.price = bx_price
        self.priceSell = bx_price_sell
        self.priceBuy = bx_price_buy
        self.namePri = bx_name_pri
        self.nameSec = bx_name_sec
        self.dataPair = bx_data_pair
        self.THBid = THB_id
    


# In[20]:


class getBittrex():
    def __init__(self):
        self.data()
    def data(self):
        bt_pair_name = []
        bt_price_buy = []
        bt_price_sell = []
        bt_name_pri = []
        bt_name_sec = []
        url = 'https://api.bittrex.com/api/v1.1/public/getmarketsummaries'
        r = requests.get(url)
        data = r.json()['result']
        for i in range(len(data)):
            #print(data[i]['MarketName'])
            splitTemp = data[i]['MarketName'].split('-')
            bt_pair_name.append(data[i]['MarketName'])
            bt_name_pri.append(splitTemp[0])
            bt_name_sec.append(splitTemp[1])
            bt_price_buy.append(data[i]['Bid'])
            bt_price_sell.append(data[i]['Ask'])

        for i in range(len(bt_name_pri)):
            if(bt_name_pri[i] == 'DOGE'):
                bt_name_pri[i] = 'DOG'
            if(bt_name_sec[i] == 'DOGE'):
                bt_name_sec[i] = 'DOG'
        self.priceSell = bt_price_sell
        self.priceBuy = bt_price_buy
        self.namePri = bt_name_pri
        self.nameSec = bt_name_sec
        self.pairName = bt_pair_name

class getOkex():
    def __init__(self):
        self.data()
    def data(self):
        okex_pair_name = []
        okex_price_buy = []
        okex_price_sell = []
        okex_name_pri = []
        okex_name_sec = []
        
        url = 'https://www.okex.com/api/spot/v3/instruments/ticker'
        r = requests.get(url)
        data = r.json()
        
        for i in range(len(data)):
            splitTemp = data[i]['instrument_id'].split('-')
            okex_pair_name.append(data[i]['instrument_id'])
            okex_name_pri.append(splitTemp[1])
            okex_name_sec.append(splitTemp[0])
            okex_price_buy.append(float(data[i]['bid']))
            okex_price_sell.append(float(data[i]['ask']))

        for i in range(len(okex_name_pri)):
            if(okex_name_pri[i] == 'DOGE'):
                okex_name_pri[i] = 'DOG'
            if(okex_name_sec[i] == 'DOGE'):
                okex_name_sec[i] = 'DOG'
        self.priceSell = okex_price_sell
        self.priceBuy = okex_price_buy
        self.namePri = okex_name_pri
        self.nameSec = okex_name_sec
    
class getKucoin():
    def __init__(self):
        self.data()
    def data(self):
        kucoin_pair_name = []
        kucoin_price_buy = []
        kucoin_price_sell = []
        kucoin_name_pri = []
        kucoin_name_sec = []
        
        url = 'https://api.kucoin.com/api/v1/market/allTickers'
        r= requests.get(url)
        data = r.json()['data']['ticker']
        #print(data[25])
        
        for i in range(len(data)):
            splitTemp = data[i]['symbol'].split('-')
            kucoin_pair_name.append(data[i]['symbol'])
            kucoin_name_pri.append(splitTemp[1])
            kucoin_name_sec.append(splitTemp[0])
            kucoin_price_buy.append(float(data[i]['buy']))
            kucoin_price_sell.append(float(data[i]['sell']))
            self.priceSell = kucoin_price_sell
            self.priceBuy = kucoin_price_buy
            self.namePri = kucoin_name_pri
            self.nameSec = kucoin_name_sec
            self.pairName = kucoin_pair_name

# In[21]:


class getRoute():
    def __init__(self,bx,bt):
        self.route(bx,bt)
    def route(self,bx,bt):
        temp_cur = [0]*5
        temp_tradeA = [0]*5
        temp_tradeB = [0]*5
        temp_value = [0]*5
        money = 500
        profit = []
        tradeRoute = []
        THB_id = bx.THBid
        for i in THB_id:
            value = money/bx.priceSell[i]
            value_cur = bx.dataPair[str(i)]['secondary_currency']
            if(value_cur == "GNO" or value_cur == "REP" or value_cur == 'BSV' or value_cur == 'XZC' or value_cur == 'BCH'):
                continue
            #print("%f %s"%(value,value_cur))
            value = value-bx_fee[value_cur] #Send to bittrex
            temp_cur[0] = value_cur;
            temp_tradeA[0]=bx.dataPair[str(i)]['primary_currency']
            temp_tradeB[0]=bx.dataPair[str(i)]['secondary_currency']
            temp_value[0] = value
            #print('b')
            #---------------Sent to Bittrex ---------------
            for j in range(300):
                value = temp_value[0]
                if(temp_cur[0] == bt.namePri[j]):
                    value = value/bt.priceSell[j] 
                    value_cur = bt.nameSec[j]
                    temp_tradeA[1] = bt.namePri[j]
                    temp_tradeB[1] = bt.nameSec[j]
                elif(temp_cur[0] == bt.nameSec[j]):
                    value = value*bt.priceBuy[j]
                    value_cur = bt.namePri[j]
                    temp_tradeA[1] = bt.nameSec[j]
                    temp_tradeB[1] = bt.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((bt.namePri[k] or bt.nameSec[k]) in bt_sent_cur):
                        if(temp_cur[1] == bt.namePri[k]):
                            value = value/bt.priceSell[k] 
                            value_cur = bt.nameSec[k]
                            temp_tradeA[2] = bt.namePri[k]
                            temp_tradeB[2] = bt.nameSec[k]
                            
                        elif(temp_cur[1] == bt.nameSec[k]):
                            value = value*bt.priceBuy[k]
                            value_cur = bt.namePri[k]
                            temp_tradeA[2] = bt.nameSec[k]
                            temp_tradeB[2] = bt.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in bt_sent_cur)):
                            continue;
                        value = value - bt_fee[value_cur]
                        temp_cur[2] = value_cur;
                        temp_value[2] = value
                        #--------------Send back to Bx-------------
                        #print('d')
                        for l in range(40):
                            value=temp_value[2]
                            if(temp_cur[2] == bx.namePri[l]):
                                value = value/bx.priceSell[l] 
                                value_cur = bx.nameSec[l]
                                temp_tradeA[3]=bx.namePri[l]
                                temp_tradeB[3]=bx.nameSec[l]
                            elif(temp_cur[2] == bx.nameSec[l]):
                                value = value*bx.priceBuy[l]
                                value_cur = bx.namePri[l]
                                temp_tradeA[3]=bx.nameSec[l]
                                temp_tradeB[3]=bx.namePri[l]
                            else : continue
                            temp_cur[3] = value_cur;
                            temp_value[3] = value
                            #print('e')
                            for m in THB_id:
                                value = temp_value[3]
                                if(temp_cur[3] == bx.nameSec[m]):
                                    value = value*bx.priceBuy[m]
                                    temp_tradeA[4]=bx.nameSec[m]
                                    temp_tradeB[4]=bx.namePri[m]
                                    value_cur=bx.namePri[m]
                                    temp_value[4] = value
                                    #print('zzz')
                                    #print(f'Result money {value} Profit{value-money}')
                                    #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                    #print(" THB > %s/%s >|| %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4]))
                                    #print("")
                                    if(value > money):
                                        #print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                        #print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        profit.append(value-money)
                                        tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("End Route1")

class getRoute11():
    def __init__(self,bx,bt):
        self.route(bx,bt)
    def route(self,bx,bt):
        temp_cur = [0]*5
        temp_tradeA = [0]*5
        temp_tradeB = [0]*5
        temp_value = [0]*5
        money = 0.003
        profit = []
        tradeRoute = []
        BTC_id = []
        for i in range(1,35):
            #try:
            if(bx.namePri[i]=='BTC'):
                if(bx.nameSec[i] in ['ZET','CPT','LEO']) : continue
                BTC_id.append(i)
                #bx_cur_to_thb.append(bx_data_pair[str(i)]['secondary_currency'])
            #except:
            #    pass
        print(BTC_id)
        for i in [2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 17, 18, 20]:
            print(bx.namePri[i] + " " +bx.nameSec[i])
        for i in BTC_id:
            value = money/bx.priceSell[i]
            value_cur = bx.dataPair[str(i)]['secondary_currency']
            if(value_cur == "GNO" or value_cur == "REP"):
                continue
            #print("%f %s"%(value,value_cur))
            value = value-bx_fee[value_cur] #Send to bittrex
            temp_cur[0] = value_cur;
            temp_tradeA[0]=bx.dataPair[str(i)]['primary_currency']
            temp_tradeB[0]=bx.dataPair[str(i)]['secondary_currency']
            temp_value[0] = value
            #print('b')
            #---------------Sent to Bittrex ---------------
            for j in range(300):
                value = temp_value[0]
                if(temp_cur[0] == bt.namePri[j]):
                    value = value/bt.priceSell[j] 
                    value_cur = bt.nameSec[j]
                    temp_tradeA[1] = bt.namePri[j]
                    temp_tradeB[1] = bt.nameSec[j]
                elif(temp_cur[0] == bt.nameSec[j]):
                    value = value*bt.priceBuy[j]
                    value_cur = bt.namePri[j]
                    temp_tradeA[1] = bt.nameSec[j]
                    temp_tradeB[1] = bt.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((bt.namePri[k] or bt.nameSec[k]) in bt_sent_cur):
                        if(temp_cur[1] == bt.namePri[k]):
                            value = value/bt.priceSell[k] 
                            value_cur = bt.nameSec[k]
                            temp_tradeA[2] = bt.namePri[k]
                            temp_tradeB[2] = bt.nameSec[k]
                            
                        elif(temp_cur[1] == bt.nameSec[k]):
                            value = value*bt.priceBuy[k]
                            value_cur = bt.namePri[k]
                            temp_tradeA[2] = bt.nameSec[k]
                            temp_tradeB[2] = bt.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in bt_sent_cur)):
                            continue;
                        value = value - bt_fee[value_cur]
                        temp_cur[2] = value_cur;
                        temp_value[2] = value
                        #--------------Send back to Bx-------------
                        #print('d')
                        for l in range(40):
                            value=temp_value[2]
                            if(temp_cur[2] == bx.namePri[l]):
                                value = value/bx.priceSell[l] 
                                value_cur = bx.nameSec[l]
                                temp_tradeA[3]=bx.namePri[l]
                                temp_tradeB[3]=bx.nameSec[l]
                            elif(temp_cur[2] == bx.nameSec[l]):
                                value = value*bx.priceBuy[l]
                                value_cur = bx.namePri[l]
                                temp_tradeA[3]=bx.nameSec[l]
                                temp_tradeB[3]=bx.namePri[l]
                            else : continue
                            temp_cur[3] = value_cur;
                            temp_value[3] = value
                            #print('e')
                            for m in BTC_id:
                                value = temp_value[3]
                                if(temp_cur[3] == bx.nameSec[m]):
                                    value = value*bx.priceBuy[m]
                                    temp_tradeA[4]=bx.nameSec[m]
                                    temp_tradeB[4]=bx.namePri[m]
                                    value_cur=bx.namePri[m]
                                    temp_value[4] = value
                                    #print('zzz')
                                    print(f'Result money {value} Profit{value-money}')
                                    #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                    print(" THB > %s/%s >|| %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4]))
                                    #print("")
                                    if(value > money):
                                        print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                        print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        profit.append(value-money)
                                        tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("End Route11")

'''class showRoute():
    def __init__():
        self.getIt()
    def getIt():
        bx = getBx()
    bt = getBittrex()
    Route = getRoute(bx,bt)'''


def getSentBt():
    sentDict = {};
    sentCur = []
    url = 'https://api.bittrex.com/api/v1.1/public/getcurrencies'
    r = requests.get(url)
    data = r.json()['result']
    
    for i in range(len(data)):
        cur = data[i]['Currency']
        fee = data[i]['TxFee']
        sentCur.append(cur)
        sentDict[cur] = fee
    return sentCur,sentDict

# In[22]:


bx_sent_cur = ['BTC','ETH','REP','BCH','BSV','XCN','DAS','DOG','EOS','EVX','FTC','GNO','HYP','LTC','NMC','OMG','PND','XPY','PPC','POW','XPM','XRP','ZEC','XZC','ZMN']
bt_sent_cur = ['BTC','ETH','REP','BCH','BSV','DAS','DOG','DOGE','EOS','FTC','GNO','LTC','OMG','POW','XRP','ZEC','XZC']
bt_fee = {'BTC':0.0005000,'ETH':0.0060000,'REP':0.1000000,'BCH':0.0010000,'BSV':0.00010000,'DAS':0.0500000,'DOG':2.0000000,'DOGE':2.0000000,'EOS':0.0200000,'FTC':0.2000000,'GNO':0.0200000,'LTC':0.0100000,'OMG':0.3500000,'POW':5.0000000,'XRP':1.0000000,'ZEC':0.0050000,'XZC':0.0200000}
bx_fee = {'BTC':0.0005000,'ETH':0.0050000,'REP':0.0100000,'BCH':0.0001000,'BSV':0.00100000,'XCN':0.0100000,'DAS':0.0050000,'DOG':5.0000000,'EOS':0.0001000,'EVX':0.0100000,'FTC':0.0100000,'GNO':0.0100000,'HYP':0.0100000,'LTC':0.0050000,'NMC':0.0100000,'OMG':0.2000000,'PND':2.0000000,'XPY':0.0050000,'PPC':0.0200000,'POW':0.0100000,'XPM':0.0200000,'XRP':0.0100000,'ZEC':0.0050000,'XZC':0.0050000,'ZMN':0.0100000}
#bt_sent_cur , bt_fee = getSentBt()
#print(len(bt_sent_cur))
