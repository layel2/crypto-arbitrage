import requests
import numpy as np
from myFunc import *
from autotrade import *
from routeKucoin import *

bx = getBx()
bt = getBittrex()
#kucoin = getKucoin()
#okex = getOkex()
#Route = getRoute2(bt,okex)
#Route = getRoute3(bx,kucoin)
#Route = getRoute4(bt,kucoin)
Route = getRoute(bx,bt)
#print(Route)
print(Route.tradeRoute)
print(Route.profit)
#print(len(Route.profit))
#if(not Route.profit == []):
#	if(np.max(Route.profit) > 5):
#		print("Trade!")
#		Trade = routeTrade(Route.profit,Route.tradeRoute)

