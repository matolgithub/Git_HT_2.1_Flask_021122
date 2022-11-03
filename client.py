import requests

# data = requests.post("http://127.0.0.1:5000/ads/",
#                      json={
#                          "title": "Продам дом.",
#                          "description": "Очень престижный район, кирпичный, 3 этажа.",
#                          "owner": "Пользователь_1"
#                      })

# data = requests.post("http://127.0.0.1:5000/ads/",
#                      json={
#                          "title": "Продам дачу.",
#                          "description": "Рядом лес, река, пруд.",
#                          "owner": "Пользователь_2"
#                      })

# data = requests.post("http://127.0.0.1:5000/ads/",
#                      json={
#                          "title": "Продам машину.",
#                          "description": "Форд-Транзит, 2015г..",
#                          "owner": "Пользователь_3"
#                      })

# data = requests.post("http://127.0.0.1:5000/ads/",
#                      json={
#                          "title": "Куплю дом.",
#                          "description": "В М.О., 30-50км МКАД, 100м.кв..",
#                          "owner": "Пользователь_4"
#                      })

# data = requests.get("http://127.0.0.1:5000/ads/1")

# data = requests.get("http://127.0.0.1:5000/ads/2")

# data = requests.delete("http://127.0.0.1:5000/ads/6")
# 404
# {"message":"Ads not found.","status":"error"}

# Try to delete ads with id=3
data = requests.delete("http://127.0.0.1:5000/ads/3")
# The result:
# 200
# {"status":"successfully deleted"}

# data = requests.get("http://127.0.0.1:5000/ads/3")
# 404
# {"message":"There are not ads with id: 3.","status":"error"}

print(data.status_code)
print(data.text)
