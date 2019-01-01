import requests

def sentLine(msg):
	token = "" #Line token
	url = "https://notify-api.line.me/api/notify"
	headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
	
	r=requests.post(url,headers = headers ,data = {'message':msg})
	#print(r.text)
