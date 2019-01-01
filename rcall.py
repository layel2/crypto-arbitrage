from RouteCk import *
import time
from lineMsg import *
i = 0
while  True:
	print("Start")
	RouteCkLine()
	i = i + 1
	if(i==12):
		sentLine("Status Checked")
		i = 0
	time.sleep(300)