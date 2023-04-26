#!/usr/bin/env python3

# pip install pyjwt
import jwt
# pip install requests
import requests
import time
import json


def createASCToken(p8KeyPath, kid, iss):
	try:
		header = {
			"alg": "ES256",
			"typ": "JWT",
			"kid": kid
		}
		payload = {
			"iss": iss,
			"aud": "appstoreconnect-v1",
			"iat": int(time.time()),
			"exp": int(round(time.time() + (20.0 * 60.0))) # 20 minutes timestamp
		}
		file = open(p8KeyPath)
		key_data = file.read()
		file.close()
		token = jwt.encode(headers=header, payload=payload, key=key_data, algorithm="ES256")
		return token
	except Exception as e:
		print(e)
		return ""

	
# ---- TODO: 配置你的参数！ ----
	
p8 = "xxxxxx.p8"
kid = "xxxxxx"
iss = "xxxxxx"
token = createASCToken(p8, kid, iss)

header = {
	"Authorization": f"Bearer {token}"
}

def get(url):
	rs1 = requests.get(url, headers=header)
	print(rs1.status_code)
	print(rs1.text)
	#	data = json.loads(rs1.text)
	#	print(data)
	if rs1.status_code != 200:
		print(url)

def post(url, body):
	rs1 = requests.post(url, headers=header, json=body)
	print(rs1.status_code)
	print(rs1.text)
	

def patch(url, body):
	rs1 = requests.patch(url, headers=header, json=body)
	print(rs1.status_code)
	print(rs1.text)
	
	
def delete(url):
	rs1 = requests.delete(url, headers=header)
	print(rs1.status_code)
	print(rs1.text)


# ---- IAP 删除 ----

# 1. 全部 app
def apps():
	url = "https://api.appstoreconnect.apple.com/v1/apps" 
	get(url)

#apps()


# 2. 某个 app 信息
def app_versions(app_id):
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appStoreVersions'
	get(url)


# ---- TODO: 填写要清空的 app id ----

app_id = "xxxxxx"
#app_versions(app_id)



# 3. app 内购列表
def app_inAppPurchases_list(app_id):
	# List All In-App Purchases for an App
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}/inAppPurchasesV2?limit=200' #'?limit=50&offset=1'
	#url = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}/inAppPurchasesV2?cursor=Mg.ANrqDAc&limit=50'
	return get(url)


## 4. 删除内购商品信息
def app_iap_delete(app_iap_id):
	id = app_iap_id
	#Delete an In-App Purchase
	url = f'https://api.appstoreconnect.apple.com/v2/inAppPurchases/{id}'
	delete(url)


## 5. Delete All IAP
def delete_all_iap(data):
	iaps = data["data"]
	for iap in iaps:
		id = iap["id"]
		print(id)
		app_iap_delete(id)


data = app_inAppPurchases_list(app_id)
delete_all_iap(data)


## 6. 获取所有订阅组
def app_subscriptionGroups(app_id):
	id = app_id
	# List All Subscription Groups for an App
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/subscriptionGroups'
	return get(url)


## 7. 获取订阅组下所有内购商品
def app_subscriptionGroups_subscriptions(app_iap_grop_id):
	id = app_iap_grop_id
	# List All Subscriptions for a Subscription Group
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptionGroups/{id}/subscriptions'
	return get(url)


## 8. 删除订阅商品
def app_iap_subscriptions_delete(app_iap_id):
	id = app_iap_id
	#Delete a Review Screenshot for an In-App Purchase
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptions/{id}'
	delete(url)


## 9. 删除订阅组
def app_iap_subscriptionGroups_delete(app_iap_grop_id):
	id = app_iap_grop_id
	#Delete a Subscription Group
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptionGroups/{id}'
	delete(url)

	
## 10. Get All Subscription
def all_subscription(groups):
	app_subscriptions = []
	for group in groups.get("data", []):
		app_iap_grop_id = group.get("id", "")
		subscriptions = app_subscriptionGroups_subscriptions(app_iap_grop_id)
		app_subscriptions += subscriptions.get("data", [])	
	return app_subscriptions


## 11. Delete All Subscription
def delete_all_subs(subscriptions):
	for subs in subscriptions:
		app_iap_id = subs.get("id", "")
		print(app_iap_id)
		app_iap_subscriptions_delete(app_iap_id)


## 12. Delete All Subscription Group
def delete_all_groups(groups):
	for group in groups.get("data", []):
		app_iap_grop_id = group.get("id", "")
		print(app_iap_grop_id)
		app_iap_subscriptionGroups_delete(app_iap_grop_id)


groups = app_subscriptionGroups(app_id)
subscriptions = all_subscription(groups)
delete_all_subs(subscriptions)
delete_all_groups(groups)

