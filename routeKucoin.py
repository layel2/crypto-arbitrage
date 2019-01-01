import requests
from myFunc import *

class getRoute3():
    def __init__(self,bx,kucoin):
        self.route(bx,kucoin)
    def route(self,bx,kucoin):
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
            #if(value_cur == "GNO" or value_cur == "REP"):
            #    continue
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
                if(temp_cur[0] == kucoin.namePri[j]):
                    value = value/kucoin.priceSell[j] 
                    value_cur = kucoin.nameSec[j]
                    temp_tradeA[1] = kucoin.namePri[j]
                    temp_tradeB[1] = kucoin.nameSec[j]
                elif(temp_cur[0] == kucoin.nameSec[j]):
                    value = value*kucoin.priceBuy[j]
                    value_cur = kucoin.namePri[j]
                    temp_tradeA[1] = kucoin.nameSec[j]
                    temp_tradeB[1] = kucoin.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((kucoin.namePri[k] or kucoin.nameSec[k]) in kucoin_sent_cur):
                        if(temp_cur[1] == kucoin.namePri[k]):
                            value = value/kucoin.priceSell[k] 
                            value_cur = kucoin.nameSec[k]
                            temp_tradeA[2] = kucoin.namePri[k]
                            temp_tradeB[2] = kucoin.nameSec[k]
                            
                        elif(temp_cur[1] == kucoin.nameSec[k]):
                            value = value*kucoin.priceBuy[k]
                            value_cur = kucoin.namePri[k]
                            temp_tradeA[2] = kucoin.nameSec[k]
                            temp_tradeB[2] = kucoin.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in kucoin_sent_cur)):
                            continue;
                        value = value - kucoin_fee[value_cur]
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
                                    #print(value)
                                    #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                    #print("THB > %s/%s >|| %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4]))
                                    if(value > money):
                                        print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                        print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        profit.append(value-money)
                                        tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("End Route3")

class getRoute4():
    def __init__(self,bt,kucoin):
        self.route(bt,kucoin)
    def route(self,bt,kucoin):
        temp_cur = [0]*5
        temp_tradeA = [0]*5
        temp_tradeB = [0]*5
        temp_value = [0]*5
        money = 17 #USD
        profit = []
        tradeRoute = []
        btUSD_id = []
        #print(bt.pairName)
        #print(bt.namePri[0])
        for i in range(len(bt.namePri)):
            if(bt.namePri[i] == 'USD'):
                #print(bt.pairName[i])
                btUSD_id.append(i)
        USD_id = btUSD_id
        for i in USD_id:
            value = money/bt.priceSell[i]
            value_cur = bt.nameSec[i]
            if(not value_cur in bt_fee):
                break
            #if(value_cur == "GNO" or value_cur == "REP"):
            #    continue
            #print("%f %s"%(value,value_cur))
            value = value-bt_fee[value_cur] #Send to bittrex
            temp_cur[0] = value_cur;
            temp_tradeA[0]=bt.namePri[i]
            temp_tradeB[0]=bt.nameSec[i]
            temp_value[0] = value
            #print('b')
            #---------------Sent to Bittrex ---------------
            for j in range(300):
                value = temp_value[0]
                if(temp_cur[0] == kucoin.namePri[j]):
                    value = value/kucoin.priceSell[j] 
                    value_cur = kucoin.nameSec[j]
                    temp_tradeA[1] = kucoin.namePri[j]
                    temp_tradeB[1] = kucoin.nameSec[j]
                elif(temp_cur[0] == kucoin.nameSec[j]):
                    value = value*kucoin.priceBuy[j]
                    value_cur = kucoin.namePri[j]
                    temp_tradeA[1] = kucoin.nameSec[j]
                    temp_tradeB[1] = kucoin.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((kucoin.namePri[k] or kucoin.nameSec[k]) in kucoin_sent_cur):
                        if(temp_cur[1] == kucoin.namePri[k]):
                            value = value/kucoin.priceSell[k] 
                            value_cur = kucoin.nameSec[k]
                            temp_tradeA[2] = kucoin.namePri[k]
                            temp_tradeB[2] = kucoin.nameSec[k]
                            
                        elif(temp_cur[1] == kucoin.nameSec[k]):
                            value = value*kucoin.priceBuy[k]
                            value_cur = kucoin.namePri[k]
                            temp_tradeA[2] = kucoin.nameSec[k]
                            temp_tradeB[2] = kucoin.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in kucoin_sent_cur)):
                            continue;
                        value = value - kucoin_fee[value_cur]
                        temp_cur[2] = value_cur;
                        temp_value[2] = value
                        #--------------Send back to bt-------------
                        #print('d')
                        for l in range(40):
                            value=temp_value[2]
                            if(temp_cur[2] == bt.namePri[l]):
                                value = value/bt.priceSell[l] 
                                value_cur = bt.nameSec[l]
                                temp_tradeA[3]=bt.namePri[l]
                                temp_tradeB[3]=bt.nameSec[l]
                            elif(temp_cur[2] == bt.nameSec[l]):
                                value = value*bt.priceBuy[l]
                                value_cur = bt.namePri[l]
                                temp_tradeA[3]=bt.nameSec[l]
                                temp_tradeB[3]=bt.namePri[l]
                            else : continue
                            temp_cur[3] = value_cur;
                            temp_value[3] = value
                            #print('e')
                            for m in USD_id:
                                value = temp_value[3]
                                if(temp_cur[3] == bt.nameSec[m]):
                                    value = value*bt.priceBuy[m]
                                    temp_tradeA[4]=bt.nameSec[m]
                                    temp_tradeB[4]=bt.namePri[m]
                                    value_cur=bt.namePri[m]
                                    temp_value[4] = value
                                    #print('zzz')
                                    print(value)
                                    #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                    print("THB > %s/%s >|| %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4]))
                                    if(value > money):
                                        print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                        print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        profit.append(value-money)
                                        tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("end")

class getRoute5():
    def __init__(self,bt,kucoin):
        self.route(bt,kucoin)
    def route(self,bt,kucoin):
        temp_cur = [0]*5
        temp_tradeA = [0]*5
        temp_tradeB = [0]*5
        temp_value = [0]*5
        money = 0.003 #BTC
        profit = []
        tradeRoute = []
        btBTC_id = []
        #print(bt.pairName)
        #print(bt.namePri[0])
        for i in range(len(bt.namePri)):
            if(bt.namePri[i] == 'BTC'):
                #print(bt.pairName[i])
                btBTC_id.append(i)
        #USD_id = btUSD_id
        for i in btBTC_id:
            value = money/bt.priceSell[i]
            value_cur = bt.nameSec[i]
            if(not value_cur in bt_fee):
                break
            #if(value_cur == "GNO" or value_cur == "REP"):
            #    continue
            #print("%f %s"%(value,value_cur))
            value = value-bt_fee[value_cur] #Send to bittrex
            temp_cur[0] = value_cur;
            temp_tradeA[0]=bt.namePri[i]
            temp_tradeB[0]=bt.nameSec[i]
            temp_value[0] = value
            #print('b')
            #---------------Sent to Bittrex ---------------
            for j in range(300):
                value = temp_value[0]
                if(temp_cur[0] == kucoin.namePri[j]):
                    value = value/kucoin.priceSell[j] 
                    value_cur = kucoin.nameSec[j]
                    temp_tradeA[1] = kucoin.namePri[j]
                    temp_tradeB[1] = kucoin.nameSec[j]
                elif(temp_cur[0] == kucoin.nameSec[j]):
                    value = value*kucoin.priceBuy[j]
                    value_cur = kucoin.namePri[j]
                    temp_tradeA[1] = kucoin.nameSec[j]
                    temp_tradeB[1] = kucoin.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((kucoin.namePri[k] or kucoin.nameSec[k]) in kucoin_sent_cur):
                        if(temp_cur[1] == kucoin.namePri[k]):
                            value = value/kucoin.priceSell[k] 
                            value_cur = kucoin.nameSec[k]
                            temp_tradeA[2] = kucoin.namePri[k]
                            temp_tradeB[2] = kucoin.nameSec[k]
                            
                        elif(temp_cur[1] == kucoin.nameSec[k]):
                            value = value*kucoin.priceBuy[k]
                            value_cur = kucoin.namePri[k]
                            temp_tradeA[2] = kucoin.nameSec[k]
                            temp_tradeB[2] = kucoin.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in kucoin_sent_cur)):
                            continue;
                        value = value - kucoin_fee[value_cur]
                        temp_cur[2] = value_cur;
                        temp_value[2] = value
                        #--------------Send back to bt-------------
                        #print('d')
                        for l in range(40):
                            value=temp_value[2]
                            if(temp_cur[2] == bt.namePri[l]):
                                value = value/bt.priceSell[l] 
                                value_cur = bt.nameSec[l]
                                temp_tradeA[3]=bt.namePri[l]
                                temp_tradeB[3]=bt.nameSec[l]
                            elif(temp_cur[2] == bt.nameSec[l]):
                                value = value*bt.priceBuy[l]
                                value_cur = bt.namePri[l]
                                temp_tradeA[3]=bt.nameSec[l]
                                temp_tradeB[3]=bt.namePri[l]
                            else : continue
                            temp_cur[3] = value_cur;
                            temp_value[3] = value
                            #print('e')
                            for m in btBTC_id:
                                value = temp_value[3]
                                if(temp_cur[3] == bt.nameSec[m]):
                                    value = value*bt.priceBuy[m]
                                    temp_tradeA[4]=bt.nameSec[m]
                                    temp_tradeB[4]=bt.namePri[m]
                                    value_cur=bt.namePri[m]
                                    temp_value[4] = value
                                    #print('zzz')
                                    print(value)
                                    #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                    print("THB > %s/%s >|| %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4]))
                                    if(value > money):
                                        print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                        print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        profit.append(value-money)
                                        tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("end")

class getRoute6():
    def __init__(self,bt,kucoin):
        self.route(bt,kucoin)
    def route(self,bt,kucoin):
        temp_cur = [0]*6
        temp_tradeA = [0]*6
        temp_tradeB = [0]*6
        temp_value = [0]*6
        money = 17 #USD
        profit = []
        tradeRoute = []
        btUSD_id = []
        send_id = []
        #print(bt.pairName)
        #print(bt.namePri[0])
        for i in range(len(bt.namePri)):
            if(bt.namePri[i] in ['BTC','ETH','USDT']):
                #print(bt.pairName[i])
                btUSD_id.append(i)
        USD_id = btUSD_id

        for i in range(len(bt.namePri)):
            if(bt.namePri[i] in ['XRP','BTC','ETH']):
                #print(bt.pairName[i])
                send_id.append(i)

        for i in USD_id:
            value = money/bt.priceSell[i]
            value_cur = bt.nameSec[i]
            if(not value_cur in bt_fee):
                break
            #if(value_cur == "GNO" or value_cur == "REP"):
            #    continue
            #print("%f %s"%(value,value_cur))
            #value = value-bt_fee[value_cur] #Send to bittrex
            temp_cur[0] = value_cur;
            temp_tradeA[0]=bt.namePri[i]
            temp_tradeB[0]=bt.nameSec[i]
            temp_value[0] = value
            #print('b')
            #----------------------st2---------------------

            for i2 in send_id:
                value = temp_value[0]
                if(temp_cur[0] == bt.namePri[i2]):
                    value = value/bt.priceSell[i2] 
                    value_cur = bt.nameSec[i2]
                    temp_tradeA[1] = bt.namePri[i2]
                    temp_tradeB[1] = bt.nameSec[i2]
                elif(temp_cur[0] == bt.nameSec[i2]):
                    value = value*bt.priceBuy[i2]
                    value_cur = bt.namePri[i2]
                    temp_tradeA[1] = bt.nameSec[i2]
                    temp_tradeB[1] = bt.namePri[i2]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value
                value = value-bt_fee[value_cur] #Send to bittrex

            #---------------Sent to Bittrex ---------------
                for j in range(300):
                    value = temp_value[1]
                    if(temp_cur[1] == kucoin.namePri[j]):
                        value = value/kucoin.priceSell[j] 
                        value_cur = kucoin.nameSec[j]
                        temp_tradeA[2] = kucoin.namePri[j]
                        temp_tradeB[2] = kucoin.nameSec[j]
                    elif(temp_cur[1] == kucoin.nameSec[j]):
                        value = value*kucoin.priceBuy[j]
                        value_cur = kucoin.namePri[j]
                        temp_tradeA[2] = kucoin.nameSec[j]
                        temp_tradeB[2] = kucoin.namePri[j]
                    else : continue
                    temp_cur[2] = value_cur;
                    temp_value[2] = value
    
                    #print('c')
                    for k in range(300):
                        value = temp_value[2]
                        if((kucoin.namePri[k] or kucoin.nameSec[k]) in kucoin_sent_cur):
                            if(temp_cur[2] == kucoin.namePri[k]):
                                value = value/kucoin.priceSell[k] 
                                value_cur = kucoin.nameSec[k]
                                temp_tradeA[3] = kucoin.namePri[k]
                                temp_tradeB[3] = kucoin.nameSec[k]
                                
                            elif(temp_cur[2] == kucoin.nameSec[k]):
                                value = value*kucoin.priceBuy[k]
                                value_cur = kucoin.namePri[k]
                                temp_tradeA[3] = kucoin.nameSec[k]
                                temp_tradeB[3] = kucoin.namePri[k]
                                #print(value_cur)
                            else: continue;
                            if(not(value_cur in kucoin_sent_cur)):
                                continue;
                            value = value - kucoin_fee[value_cur]
                            temp_cur[3] = value_cur;
                            temp_value[3] = value
                            #--------------Send back to bt-------------
                            #print('d')
                            for l in range(40):
                                value=temp_value[3]
                                if(temp_cur[3] == bt.namePri[l]):
                                    value = value/bt.priceSell[l] 
                                    value_cur = bt.nameSec[l]
                                    temp_tradeA[4]=bt.namePri[l]
                                    temp_tradeB[4]=bt.nameSec[l]
                                elif(temp_cur[3] == bt.nameSec[l]):
                                    value = value*bt.priceBuy[l]
                                    value_cur = bt.namePri[l]
                                    temp_tradeA[4]=bt.nameSec[l]
                                    temp_tradeB[4]=bt.namePri[l]
                                else : continue
                                temp_cur[4] = value_cur;
                                temp_value[4] = value
                                #print('e')
                                for m in USD_id:
                                    value = temp_value[4]
                                    if(temp_cur[4] == bt.nameSec[m]):
                                        value = value*bt.priceBuy[m]
                                        temp_tradeA[5]=bt.nameSec[m]
                                        temp_tradeB[5]=bt.namePri[m]
                                        value_cur=bt.namePri[m]
                                        temp_value[5] = value
                                        #print('zzz')
                                        print(value)
                                        #print("THB > %s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                        print("THB > %s/%s > %s/%s > || %s/%s > %s/%s >|| %s/%s > %s/%s"%(temp_tradeA[0],temp_tradeB[0],temp_tradeA[1],temp_tradeB[1],temp_tradeA[2],temp_tradeB[2],temp_tradeA[3],temp_tradeB[3],temp_tradeA[4],temp_tradeB[4],temp_tradeA[5],temp_tradeB[5]))
                                        if(value > money):
                                            print("Result money %d   Profit %d >> %s" %(value,value-money,value_cur))
                                            print("%s > %s > %s > %s >THB"%(temp_cur[0],temp_cur[1],temp_cur[2],temp_cur[3]))
                                            profit.append(value-money)
                                            tradeRoute.append([ "%s-%s"%(temp_tradeA[0],temp_tradeB[0]) , "%s-%s"%(temp_tradeA[1],temp_tradeB[1]) ,"%s-%s"%(temp_tradeA[2],temp_tradeB[2]) ,"%s-%s"%(temp_tradeA[3],temp_tradeB[3]) ,"%s-%s"%(temp_tradeA[4],temp_tradeB[4]) ])
        self.profit = profit
        self.tradeRoute = tradeRoute
        print("end")

bt_sent_cur , bt_fee = getSentBt()

bx_sent_cur = ['BTC','ETH','REP','BCH','BSV','XCN','DAS','DOG','EOS','EVX','FTC','GNO','HYP','LTC','NMC','OMG','PND','XPY','PPC','POW','XPM','XRP','ZEC','XZC','ZMN']
bx_fee = {'BTC':0.0005000,'ETH':0.0050000,'REP':0.0100000,'BCH':0.0001000,'BSV':0.00100000,'XCN':0.0100000,'DAS':0.0050000,'DOG':5.0000000,'EOS':0.0001000,'EVX':0.0100000,'FTC':0.0100000,'GNO':0.0100000,'HYP':0.0100000,'LTC':0.0050000,'NMC':0.0100000,'OMG':0.2000000,'PND':2.0000000,'XPY':0.0050000,'PPC':0.0200000,'POW':0.0100000,'XPM':0.0200000,'XRP':0.0100000,'ZEC':0.0050000,'XZC':0.0050000,'ZMN':0.0100000}
kucoin_sent_cur = ['kucoinC','ETH','NEO','KCS','USDT','TMT','LALA','CS','DOCK','ETN','IHT','KICK','WAN','APH','BAX','DATX','DEB','ELEC','GO','IOTX','LOOM','LYM','MOBI','OMX','ONT','OPEN','QKC','SHL','SOUL','SPHTX','SRN','TOMO','TRAC','COV','DADI','ELF','MAN','STK','ZIL','ZPT','BPT','CAPP','POLY','TKY','TNC','XRB','AXPR','COFI','CXO','DTA','ING','MTN','OCN','PARETO','SNC','TEL','WAX','ADB','BOS','HAT','HKN','HPB','IOST','ARY','DBC','KEY','GAT','PHX','ACAT','CV','DRGN','LTC','QLC','R','TIO','ITC','EXY','MWAT','AGI','DENT','J8T','LOCI','CAT','ACT','ARN','BCH','CAN','EOS','ETC','GAS','JNT','PLAY','CHP','DASH','DNA','EkucoinC','FOTA','PRL','PURA','UTK','CAG','GLA','SNX','SPF','TIME','Akucoin','BNTY','ELIX','ENJ','AIX','VET','AION','DAT','QTUM','WTC','DGB','SNOV','BRD','AMB','kucoinM','MANA','RHOC','XLR','XAS','CHSB','UKG','POLL','FLIXX','INS','OMG','TFL','WPR','LEND','KNC','BCD','LA','ONION','POWR','SNM','kucoinG','HC','PBL','MOD','PPT','BCPT','GVT','HST','SNT','SUB','NEBL','CVC','MTH','NULS','PAY','RDN','REQ','QSP','BHC','CBC','AOA','EDR','DCC','ZINC','DAG','SUSD','OLT','XLM','ELA','EGT','CPC','DACC','ePRX','UT','LOC','MVP','TRX','ZRX','DCR','USE','BU','COSM','IOG','EDN','CRPT','USDC','MTC','META','TUSD','PAX','VNX','PAL','STQ','FTM','NANO','VTHO','ONG','EVX','POE','ETF','BCHABC','BCHSV','LSK','GMB','GGC','OPQ','XRP','MKR','DAI','ONOT','AVA','TFD','XYO','VSYS','GRIN','kucoinT','SOLVE','MHC','LOKI','CSP','HOT','NRG','KAT','AERGO','FET','ANKR','DX','XMR','RkucoinC','RIF']
kucoin_fee={'kucoinC':	0.0005,'ETH':	0.01,'NEO':	0,'KCS':	1.3,'USDT':	4.2,'TMT':	162.8,'LALA':	704.2,'CS':	10.2,'DOCK':	69.1,'ETN':	50,'IHT':	55.93,'KICK':	219.2,'WAN':	0.1,'APH':	3,'BAX':	2825,'DATX':	331.13,'DEB':	177.9,'ELEC':	370.3,'GO':	0.01,'IOTX':	80.6,'LOOM':	11.7,'LYM':	123.1,'MOBI':	30,'OMX':	862,'ONT':	1,'OPEN':	90.91,'QKC':	22.28,'SHL':	55.62,'SOUL':	4,'SPHTX':	38,'SRN':	24.2,'TOMO':	1.4,'TRAC':	28.6,'COV':	7.1,'DADI':	13.55,'ELF':	4.41,'MAN':	7.3,'STK':	107.3,'ZIL':	41.2,'ZPT':	1,'BPT':	11.22,'CAPP':	232.5,'POLY':	6,'TKY':	10,'TNC':	1,'XRB':	0.05,'AXPR':	117,'COFI':	224.2,'CXO':	52.4,'DTA':	471.7,'ING':	102.8,'MTN':	147,'OCN':	295.8,'PARETO':	263.16,'SNC':	41.9,'TEL':	1567.3,'WAX':	16.8,'ADB':	467.29,'BOS':	1,'HAT':	0.5,'HKN':	4.3,'HPB':	3.5,'IOST':	1,'ARY':	59.52,'DBC':	1,'KEY':	264.5,'GAT':	357.14,'PHX':	1,'ACAT':	10,'CV':	1785.71,'DRGN':	7.9,'LTC':	0.001,'QLC':	1,'R':	6,'TIO':	5,'ITC':	6,'EXY':	27.1,'MWAT':	44.52,'AGI':	17.16,'DENT':	794.9,'J8T':	1351.3,'LOCI':	240.3,'CAT':	485.44,'ACT':	1,'ARN':	1.9,'BCH':	0.0005,'CAN':	43.6,'EOS':	0.1,'ETC':	0.01,'GAS':	0,'JNT':	8.71,'PLAY':	210,'CHP':	364.9,'DASH':	0.002,'DNA':	3,'EkucoinC':	38.2,'FOTA':	63.8,'PRL':	1,'PURA':	0.5,'UTK':	25.1,'CAG':	8.5,'GLA':	4,'SNX':	14.2,'SPF':	282.4,'TIME':	0.29,'Akucoin':	5.62,'BNTY':	223.8,'ELIX':	241.5,'ENJ':	6.9,'AIX':	142,'VET':	100,'AION':	0.1,'DAT':	619.5,'QTUM':	0.3,'WTC':	0.5,'DGB':	0.5,'SNOV':	467.2,'BRD':	3.7,'AMB':	12.5,'kucoinM':	7.5,'MANA':	16.6,'RHOC':	34.7,'XLR':	0.1,'XAS':	0.5,'CHSB':	87.26,'UKG':	25,'POLL':	7.5,'FLIXX':	46,'INS':	2.6,'OMG':	0.5,'TFL':	2.9,'WPR':	38.3,'LEND':	69,'KNC':	4,'BCD':	0.01,'LA':	11,'ONION':	0.1,'POWR':	7.5,'SNM':	33.5,'kucoinG':	0.001,'HC':	0.005,'PBL':	5,'MOD':	2,'PPT':	0.4,'BCPT':	13.4,'GVT':	0.15,'HST':	10.4,'SNT':	36,'SUB':	12.61,'NEBL':	0.01,'CVC':	11.4,'MTH':	27,'NULS':	1.6,'PAY':	3.1,'RDN':	2.7,'REQ':	32.5,'QSP':	34,'BHC':	1,'CBC':	115.7,'AOA':	63.6,'EDR':	24.7,'DCC':	632.9,'ZINC':	30,'DAG':	549.4,'SUSD':	0.6,'OLT':	204.9,'XLM':	0.01,'ELA':	0.1,'EGT':	1483.6,'CPC':	47.21,'DACC':	4166.6,'ePRX':	1000,'UT':	0.1,'LOC':	0.7,'MVP':	2976.1,'TRX':	1,'ZRX':	2.8,'DCR':	0.01,'USE':	609.7,'BU':	0.5,'COSM':	29.9,'IOG':	10,'EDN':	184.5,'CRPT':	5,'USDC':	1,'MTC':	112.3,'META':	96.9,'TUSD':	1.5,'PAX':	1.3,'VNX':	11200.7,'PAL':	183.8,'STQ':	2272.7,'FTM':	133.6,'NANO':	0.01,'VTHO':	21,'ONG':	0.1,'EVX':	2.5,'POE':	105,'ETF':	1,'BCHABC':	0.0005,'BCHSV':	0.0005,'LSK':	0.1,'GMB':	4478.2,'GGC':	0.01,'OPQ':	34.7,'XRP':	0.5,'MKR':	0.001,'DAI':	0.5,'ONOT':	2688.1,'AVA':	5,'TFD':	100,'XYO':	274.7,'VSYS':	10,'GRIN':	0.1,'kucoinT':	100,'SOLVE':	10,'MHC':	100,'LOKI':	3,'CSP':	144,'HOT':	5,'NRG':	1,'KAT':	173.4,'AERGO':	7.8,'FET':	3,'ANKR':	60,'DX':	3000,'XMR':	0.0001,'RkucoinC':	0.0005,'RIF':	8}