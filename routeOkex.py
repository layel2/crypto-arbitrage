from myFunc import *
class getRoute2():
    def __init__(self,bt,okex):
        self.route(bt,okex)
    def route(self,bt,okex):
        temp_cur = [0]*5
        temp_tradeA = [0]*5
        temp_tradeB = [0]*5
        temp_value = [0]*5
        money = 500
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
            if(value_cur == "GNO" or value_cur == "REP"):
                continue
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
                if(temp_cur[0] == okex.namePri[j]):
                    value = value/okex.priceSell[j] 
                    value_cur = okex.nameSec[j]
                    temp_tradeA[1] = okex.namePri[j]
                    temp_tradeB[1] = okex.nameSec[j]
                elif(temp_cur[0] == okex.nameSec[j]):
                    value = value*okex.priceBuy[j]
                    value_cur = okex.namePri[j]
                    temp_tradeA[1] = okex.nameSec[j]
                    temp_tradeB[1] = okex.namePri[j]
                else : continue
                temp_cur[1] = value_cur;
                temp_value[1] = value

                #print('c')
                for k in range(300):
                    value = temp_value[1]
                    if((okex.namePri[k] or okex.nameSec[k]) in okex_sent_cur):
                        if(temp_cur[1] == okex.namePri[k]):
                            value = value/okex.priceSell[k] 
                            value_cur = okex.nameSec[k]
                            temp_tradeA[2] = okex.namePri[k]
                            temp_tradeB[2] = okex.nameSec[k]
                            
                        elif(temp_cur[1] == okex.nameSec[k]):
                            value = value*okex.priceBuy[k]
                            value_cur = okex.namePri[k]
                            temp_tradeA[2] = okex.nameSec[k]
                            temp_tradeB[2] = okex.namePri[k]
                            #print(value_cur)
                        else: continue;
                        if(not(value_cur in okex_sent_cur)):
                            continue;
                        value = value - okex_fee[value_cur]
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
        print("end")

bt_sent_cur , bt_fee = getSentBt()
okex_sent_cur = bt_sent_cur
okex_fee = bt_fee