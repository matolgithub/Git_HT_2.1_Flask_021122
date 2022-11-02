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

data = requests.post("http://127.0.0.1:5000/ads/",
                     json={
                         "title": "Продам машину.",
                         "description": "Форд-Транзит, 2015г..",
                         "owner": "Пользователь_3"
                     })

print(data.status_code)
print(data.text)
