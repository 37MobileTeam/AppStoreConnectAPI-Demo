#!/usr/bin/env python3

# pip install pyjwt
import jwt
import time
import requests
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

# ---- 统一请求方法 ----
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
	if rs1.status_code != 200:
		print(url)

def patch(url, body):
	rs1 = requests.patch(url, headers=header, json=body)
	print(rs1.status_code)
	print(rs1.text)
	if rs1.status_code != 200:
		print(url)
	
def delete(url):
	rs1 = requests.delete(url, headers=header)
	print(rs1.status_code)
	print(rs1.text)
	if rs1.status_code != 200:
		print(url)


# ---- API 使用方法 ----

# 1. 全部 app
def apps():
	url = "https://api.appstoreconnect.apple.com/v1/apps" 
	get(url)

#apps()


# 2. 某个 app 信息
def app_versions(app_id):
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appStoreVersions'
	get(url)

app_id = "1240856775"
#app_versions(app_id)


# 3. app 某个版本 id
def app_version_localizations(app_version_id):
	# app 某个版本 id
	id = app_version_id
	# List All App Store Version Localizations for an App Store Version
	url = f'https://api.appstoreconnect.apple.com/v1/appStoreVersions/{id}/appStoreVersionLocalizations'
	get(url)
	
app_version_id = "6ac74d39-4005-8286-e053-c43a210a859b" #appStoreVersions
#app_version_localizations(app_version_id)


# 4. app 版本多语言，某个语言的商店图片
def app_version_localization_appScreenshotSets(app_version_local_id):
	id = app_version_local_id
	# List All App Screenshot Sets for an App Store Version Localization
	url = f'https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{id}/appScreenshotSets'
	get(url)
	
app_version_local_id = "27859c43-50d0-4636-abb6-1b6b72a3504b" #ko
app_version_local_id = "920ea101-e021-4893-892a-d8977aad6f7b" #ja
app_version_local_id = "5d1fe96d-94ff-d976-3486-371a90ee529c" #zh-Hans
#app_version_localization_appScreenshotSets(app_version_local_id)



# 5. 获取所有有效的国家或地区
# List Territories：https://developer.apple.com/documentation/appstoreconnectapi/list_territories
def list_territories():
	url = f'https://api.appstoreconnect.apple.com/v1/territories?limit=200'
	get(url)
	
list_territories()
	

# 6. 获取 App 的价格点（900个价格点）
# List all price points for an app：https://developer.apple.com/documentation/appstoreconnectapi/list_all_price_points_for_an_app
def app_price_points(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints'
	# 带查询参数
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints' + '?limit=200&fields[appPricePoints]=app,customerPrice,equalizations,proceeds,territory&fields[territories]=currency&filter[territory]=USA'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints' + '?limit=200&fields[appPricePoints]=app,customerPrice,equalizations,proceeds,territory&fields[territories]=currency&filter[territory]=CHN,JPN'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints' + '?limit=200&fields[appPricePoints]=app,customerPrice,equalizations,proceeds,territory&fields[territories]=currency&filter[territory]=JPN&include=territory'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints?filter[territory]=USA,HKG&include=territory&limit=200'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPricePoints?filter[territory]=CHN&include=territory&limit=200'
	get(url)

#app_price_points(app_id)


# 7. 获取某个 app 的价格点的信息
# Read app price point information：https://developer.apple.com/documentation/appstoreconnectapi/read_app_price_point_information-eg1
def app_price_points_info(app_point_id):
	id = app_point_id
	url = f'https://api.appstoreconnect.apple.com/v3/appPricePoints/{id}'
	url = f'https://api.appstoreconnect.apple.com/v3/appPricePoints/{id}' + '?include=app,territory'
	get(url)


app_point_id = 'eyJzIjoiMTI0MDg1Njc3NSIsInQiOiJDSE4iLCJwIjoiMTAwMDEifQ'
#app_price_points_info(app_point_id)


# 8. 某个价格点对应的174个国家或地区的均衡价格
# List app price point equalizations：https://developer.apple.com/documentation/appstoreconnectapi/list_app_price_point_equalizations
def app_price_points_equalizations(app_point_id):
	id = app_point_id
	url = f'https://api.appstoreconnect.apple.com/v3/appPricePoints/{id}/equalizations'
	url = f'https://api.appstoreconnect.apple.com/v3/appPricePoints/{id}/equalizations' + '?include=app,territory'
	get(url)
	
	
#app_price_points_equalizations(app_point_id)



# 9. app 内购列表
# List All In-App Purchases for an App: https://developer.apple.com/documentation/appstoreconnectapi/list_all_in-app_purchases_for_an_app
def app_inAppPurchases_list(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/inAppPurchasesV2' #'?limit=5'
	get(url)
	
#app_inAppPurchases_list(app_id)



# 10. 获取 内购IAP 的价格点（900个价格点）
# List all price points for an in-app purchase：https://developer.apple.com/documentation/appstoreconnectapi/list_all_price_points_for_an_in-app_purchase
def iap_price_points(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v2/inAppPurchases/{id}/pricePoints'
	# 带查询参数
	url = f'https://api.appstoreconnect.apple.com/v2/inAppPurchases/{id}/pricePoints' + '?limit=200&fields[inAppPurchasePricePoints]=customerPrice,inAppPurchaseV2,priceTier,proceeds,territory&fields[territories]=currency&filter[territory]=USA'
	url =f'https://api.appstoreconnect.apple.com/v2/inAppPurchases/{id}/pricePoints?filter[territory]=CHN&include=territory&limit=200'
	get(url)


app_iap_id = '6444653105'
#iap_price_points(app_iap_id)



# 11. 获取某个 app 的价格时间表（App 级别）
# Read price schedule information for an app：https://developer.apple.com/documentation/appstoreconnectapi/read_price_schedule_information_for_an_app
def app_appPriceSchedule(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPriceSchedule'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appPriceSchedule' + '?include=app,automaticPrices,baseTerritory,manualPrices'
	get(url)

#app_appPriceSchedule(app_id)




# 12. 获取某个 app 的详细价格时间表（App 级别）
# Read an app's price schedule information：https://developer.apple.com/documentation/appstoreconnectapi/read_an_app_s_price_schedule_information
def app_appPriceSchedules_info(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}'
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}' + '?include=app,automaticPrices,baseTerritory,manualPrices'
	get(url)
	
#app_appPriceSchedules_info(app_id)



# 13. 获取某个 app 的全球均衡价格时间表（App 级别）
# List automatically generated prices for an app：https://developer.apple.com/documentation/appstoreconnectapi/list_automatically_generated_prices_for_an_app
def app_appPriceSchedules_automaticPrices(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}/automaticPrices'
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}/automaticPrices' + '?include=appPricePoint,territory&limit=200'
	get(url)
	

#app_appPriceSchedules_automaticPrices(app_id)



# 14. 获取某个 app 的自定价格时间表（App 级别）
# List manually chosen prices for an app：https://developer.apple.com/documentation/appstoreconnectapi/list_manually_chosen_prices_for_an_app
def app_appPriceSchedules_manualPrices(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}/manualPrices'
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}/manualPrices' + '?include=appPricePoint,territory&limit=200'
	get(url)
	
	
#app_appPriceSchedules_manualPrices(app_id)




# 15. 获取某个 app 的基准国家（App 级别）
# Read the base territory for an app's price schedule：https://developer.apple.com/documentation/appstoreconnectapi/read_the_base_territory_for_an_app_s_price_schedule
def app_appPriceSchedules_baseTerritory(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appPriceSchedules/{id}/baseTerritory'
	get(url)
	
	
#app_appPriceSchedules_baseTerritory(app_id)


# 16. 设定某个 app 的价格调整（App 级别）
# Add a scheduled price change to an app：https://developer.apple.com/documentation/appstoreconnectapi/add_a_scheduled_price_change_to_an_app
def app_appPriceSchedules_create(body):
	url = 'https://api.appstoreconnect.apple.com/v1/appPriceSchedules'
	post(url, body)



base_territory_id = "CHN"
base_territory_id = "HKG"
manual_prices_id = "eyJzIjoiMTI0MDg1Njc3NSIsInQiOiJDSE4iLCJwIjoiMTAwMDEifQ"
manual_prices_id2 = "eyJzIjoiMTI0MDg1Njc3NSIsInQiOiJDSE4iLCJwIjoiMTAwMTUifQ"
iap_price_point_id = "eyJzIjoiNjQ0NDY1MzEwNSIsInQiOiJDSE4iLCJwIjoiMTAwMDUifQ" # CNY￥ 2.50

body = {
	'data': {
		'relationships': {
			'app': {
				'data': {
					'id': f"{app_id}",
					'type': 'apps'
				}
			},
			'baseTerritory': {
				'data': {
					'id': f"{base_territory_id}",
					'type': 'territories'
				}
			},
			'manualPrices': {
				'data': [
					{
						'id': f"{manual_prices_id}",
						'type': 'appPrices'
					}
				]
			}
		},
		'type': 'appPriceSchedules'
	},
	'included': [
		{
			'id': f'{base_territory_id}',
			'type': 'territories',
		},
		{
			'id': f'{manual_prices_id}',
			'type': 'appPrices',
			'attributes': {
				'startDate': None, # '2023-04-14',
				'endDate': None
			},
			'relationships': {
				'appPricePoint': {
					'data': {
						'id': f"{manual_prices_id}",
						'type': 'appPricePoints'
					}
				}
			}
		}
	]
}

app_appPriceSchedules_create(body)


'''

TODO: 不清楚那里的错误！！！

```
409
{
  "errors" : [ {
    "id" : "94ac817a-2fed-43a0-b746-69105714d6a3",
    "status" : "409",
    "code" : "ENTITY_ERROR.RELATIONSHIP.REQUIRED",
    "title" : "The provided entity is missing a required relationship",
    "detail" : "You must provide a value for the relationship 'appPricePoint' with this request",
    "source" : {
      "pointer" : "/included/0/relationships/appPricePoint"
    }
  } ]
}
```

'''



# 17. 获取某个 IAP 的价格时间表（IAP 级别）
# Read price information for an in-app purchase price schedule：https://developer.apple.com/documentation/appstoreconnectapi/read_price_information_for_an_in-app_purchase_price_schedule
def iap_appPriceSchedule(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}/manualPrices'
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}/manualPrices' + '?include=inAppPurchasePricePoint,territory'
	get(url)
	
#iap_appPriceSchedule(app_iap_id)
	
	
	
	
# 18. 获取某个 IAP 的详细价格时间表（IAP 级别）
# Read in-app purchase price schedule information：https://developer.apple.com/documentation/appstoreconnectapi/read_in-app_purchase_price_schedule_information
def iap_appPriceSchedules_info(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}'
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}' + '?include=automaticPrices,baseTerritory,manualPrices'
	get(url)
	
#iap_appPriceSchedules_info(app_iap_id)
	
	
	
	
	
# 19. 获取某个 IAP 的全球均衡价格时间表（IAP 级别）
# List automatically generated prices for an in-app purchase price：https://developer.apple.com/documentation/appstoreconnectapi/list_automatically_generated_prices_for_an_in-app_purchase_price
def iap_appPriceSchedules_automaticPrices(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}/automaticPrices'
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}/automaticPrices' + '?include=inAppPurchasePricePoint,territory&limit=200'
	get(url)
	
	
#iap_appPriceSchedules_automaticPrices(app_iap_id)
	
	



# 20. 获取某个 IAP 的基准国家（IAP 级别）
# Read the selected base territory for an in-app purchase price schedule：https://developer.apple.com/documentation/appstoreconnectapi/read_the_selected_base_territory_for_an_in-app_purchase_price_schedule
def iap_appPriceSchedules_baseTerritory(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules/{id}/baseTerritory'
	get(url)
	
	
#iap_appPriceSchedules_baseTerritory(app_iap_id)
	


# 21. 设定某个 IAP 的价格调整（IAP 级别）
# Add a scheduled price change to an in-app purchase：https://developer.apple.com/documentation/appstoreconnectapi/add_a_scheduled_price_change_to_an_in-app_purchase
def iap_appPriceSchedules_create(body):
	url = 'https://api.appstoreconnect.apple.com/v1/inAppPurchasePriceSchedules'
	post(url, body)


#基准国家
base_territory_id = "CHN"
base_territory_id2 = "HKG"

iap_price_id = "随意名字，用于区别一个价格计划"
# 全球均衡价格
iap_price_point_id = "eyJzIjoiNjQ0NDY1MzEwNSIsInQiOiJDSE4iLCJwIjoiMTAwMDEifQ" # CNY￥ 1.00
iap_price_point_id2 = "eyJzIjoiNjQ0NDY1MzEwNSIsInQiOiJDSE4iLCJwIjoiMTAwMDUifQ" # CNY￥ 2.50
# 自定价格
iap_price_point_id3 = "eyJzIjoiNjQ0NDY1MzEwNSIsInQiOiJIS0ciLCJwIjoiMTAwMTUifQ" # HKD $16.00

body = {
	'data': {
		'relationships': {
			'inAppPurchase': {
				'data': {
					'id': f"{app_iap_id}",
					'type': 'inAppPurchases'
				}
			},
			'baseTerritory': {
				'data': {
					'id': f"{base_territory_id}",
					'type': 'territories'
				}
			},
			'manualPrices': {
				'data': [
					{
						'id': f'{iap_price_id}',
						'type': 'inAppPurchasePrices'
					},
					{
						'id': f"{iap_price_id}2",
						'type': 'inAppPurchasePrices'
					},
					{
						'id': f"{iap_price_id}3",
						'type': 'inAppPurchasePrices'
					}
				]
			}
		},
		'type': 'inAppPurchasePriceSchedules'
	},
	'included': [
		{
			'id': f'{iap_price_id}',
			'type': 'inAppPurchasePrices',
			'attributes': {
				'startDate': '2023-04-25',
				'endDate': None
			},
			'relationships': {
				'inAppPurchasePricePoint': {
					'data': {
						'id': f"{iap_price_point_id}",
						'type': 'inAppPurchasePricePoints'
					}
				},
				'inAppPurchaseV2': {
					'data': {
						'id': f"{app_iap_id}",
						'type': 'inAppPurchases'
					}
				}
			}
		},
		{
			'id': f'{iap_price_id}2',
			'type': 'inAppPurchasePrices',
			'attributes': {
				'startDate': None,
				'endDate': '2023-04-25'
			},
			'relationships': {
				'inAppPurchasePricePoint': {
					'data': {
						'id': f"{iap_price_point_id2}",
						'type': 'inAppPurchasePricePoints'
					}
				},
				'inAppPurchaseV2': {
					'data': {
						'id': f"{app_iap_id}",
						'type': 'inAppPurchases'
					}
				}
			}
		},
		{
			'id': f'{iap_price_id}3',
			'type': 'inAppPurchasePrices',
			'attributes': {
				'startDate': None,
				'endDate': None
			},
			'relationships': {
				'inAppPurchasePricePoint': {
					'data': {
						'id': f"{iap_price_point_id3}",
						'type': 'inAppPurchasePricePoints'
					}
				},
				'inAppPurchaseV2': {
					'data': {
						'id': f"{app_iap_id}",
						'type': 'inAppPurchases'
					}
				}
			}
		}
	]
}

#iap_appPriceSchedules_create(body)



# 22. 获取某个 app 的销售范围（App 级别）
# List availability for an app：https://developer.apple.com/documentation/appstoreconnectapi/list_availability_for_an_app
def app_availability(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appAvailability'
	url = f'https://api.appstoreconnect.apple.com/v1/apps/{id}/appAvailability' + '?include=app,availableTerritories'
	get(url)
	
	
#app_availability(app_id)


# 23. 获取某个 app 的销售范围信息（App 级别）
# Read the availability for an app：https://developer.apple.com/documentation/appstoreconnectapi/read_the_availability_for_an_app
def app_availability_info(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appAvailabilities/{id}'
	url = f'https://api.appstoreconnect.apple.com/v1/appAvailabilities/{id}' + '?include=app,availableTerritories'
	get(url)
	
	
#app_availability_info(app_id)



# 24. 获取某个 app 的销售范围列表（App 级别）
# List territory availability for an app：https://developer.apple.com/documentation/appstoreconnectapi/list_territory_availability_for_an_app
def app_availability_availableTerritories(app_id):
	id = app_id
	url = f'https://api.appstoreconnect.apple.com/v1/appAvailabilities/{id}/availableTerritories'
	get(url)
	
	
#app_availability_availableTerritories(app_id)
	
	

# 25. 修改某个 app 的销售范围（App 级别）
# Modify territory availability for an app：https://developer.apple.com/documentation/appstoreconnectapi/modify_territory_availability_for_an_app
def app_availability_territories_modify(body):
	url = 'https://api.appstoreconnect.apple.com/v1/appAvailabilities'
	post(url, body)
	

body = {
	"data": {
		"type": "appAvailabilities",
		"attributes": {
			"availableInNewTerritories": True
		},
		"relationships": {
			"app": {
				"data": {
					"type": "apps",
					"id": f"{app_id}"
				}
			},
			"availableTerritories": {
				"data": [
					{
						"type": "territories",
						"id": "USA"
					},
					{
						"type": "territories",
						"id": "HKG"
					},
					{
						"type": "territories",
						"id": "CHN"
					}
				]
			}
		}
	}
}

#app_availability_territories_modify(body)




# 26. 获取某个 IAP 的销售范围（IAP 级别）
# List the territory availablity of an in-app purchase：https://developer.apple.com/documentation/appstoreconnectapi/list_the_territory_availablity_of_an_in-app_purchase
def iap_availability(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchaseAvailabilities/{id}/availableTerritories'
	get(url)
	
	
#iap_availability(app_iap_id)
	


# 27. 获取某个 IAP 的销售范围信息（IAP 级别）
#Read the availablity of an in-app purchase：https://developer.apple.com/documentation/appstoreconnectapi/read_the_availablity_of_an_in-app_purchase
def iap_availability_info(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchaseAvailabilities/{id}'
	url = f'https://api.appstoreconnect.apple.com/v1/inAppPurchaseAvailabilities/{id}' + '?include=availableTerritories'
	get(url)
	
	
#iap_availability_info(app_iap_id)
	
	
	
# 28. 修改某个 IAP 的销售范围（IAP 级别）
#Modify the territory availablity of an in-app purchase：https://developer.apple.com/documentation/appstoreconnectapi/modify_the_territory_availablity_of_an_in-app_purchase

def iap_availability_territories_modify(body):
	url = 'https://api.appstoreconnect.apple.com/v1/inAppPurchaseAvailabilities'
	post(url, body)
	
	
body = {
	"data": {
		"type": "inAppPurchaseAvailabilities",
		"attributes": {
			"availableInNewTerritories": True
		},
		"relationships": {
			"availableTerritories": {
				"data": [
					{
						"type": "territories",
						"id": "USA"
					},
					{
						"type": "territories",
						"id": "CHN"
					},
					{
						"type": "territories",
						"id": "ISL"
					}
				]
			},
			"inAppPurchase": {
				"data": {
					"id": f"{app_iap_id}",
					"type": "inAppPurchases"
				}
			}
		}
	}
}

#iap_availability_territories_modify(body)




# 29. 获取某个 subscription IAP 的销售范围（IAP 级别）
#List the territory availability of a subscription：https://developer.apple.com/documentation/appstoreconnectapi/list_the_territory_availability_of_a_subscription
def subscription_availability(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptionAvailabilities/{id}/availableTerritories'
	get(url)
	
	
#subscription_availability(app_iap_id)
	
	
	
# 30. 获取某个 subscription IAP 的销售范围信息（IAP 级别）
#Read the availability of a subscription：https://developer.apple.com/documentation/appstoreconnectapi/read_the_availability_of_a_subscription
def subscription_availability_info(app_iap_id):
	id = app_iap_id
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptionAvailabilities/{id}'
	url = f'https://api.appstoreconnect.apple.com/v1/subscriptionAvailabilities/{id}' + '?include=availableTerritories,subscription'
	get(url)
	
	
#subscription_availability_info(app_iap_id)
	

	

# 31. 修改某个 subscription IAP 的销售范围（IAP 级别）
#Modify the territory availability of a subscription：https://developer.apple.com/documentation/appstoreconnectapi/modify_the_territory_availability_of_a_subscription	
def subscription_availability_territories_modify(body):
	url = 'https://api.appstoreconnect.apple.com/v1/subscriptionAvailabilities'
	post(url, body)
	
	
body = {
	"data": {
		"type": "subscriptionAvailabilities",
		"attributes": {
			"availableInNewTerritories": True
		},
		"relationships": {
			"availableTerritories": {
				"data": [
					{
						"type": "territories",
						"id": "USA"
					},
					{
						"type": "territories",
						"id": "CHN"
					},
					{
						"type": "territories",
						"id": "ISL"
					}
				]
			},
			"subscription": {
				"data": {
					"id": f"{app_iap_id}",
					"type": "subscriptions"
				}
			}
		}
	}
}

#iap_availability_territories_modify(body)



			