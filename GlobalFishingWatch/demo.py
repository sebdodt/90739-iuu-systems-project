import requests

url = "https://gateway.api.globalfishingwatch.org/v2/vessels/search?query=224224000&datasets=public-global-support-vessels:latest,public-global-carrier-vessels:latest,public-global-fishing-vessels:latest&limit=10&offset=0"

params = {'H':'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJJVVVQcm9qZWN0IiwidXNlcklkIjoyMDUwMCwiYXBwbGljYXRpb25OYW1lIjoiSVVVUHJvamVjdCIsImlkIjoxODQsInR5cGUiOiJ1c2VyLWFwcGxpY2F0aW9uIn0sImlhdCI6MTY2MzExNjY4MiwiZXhwIjoxOTc4NDc2NjgyLCJhdWQiOiJnZnciLCJpc3MiOiJnZncifQ.bvgbI7Hgl7AdfsfZOtsGd8aevNxRQcYqXLuLxRZZqbf49ztzwi190FmkqYsHVclvFDpfV0eizrvzaCBVXO2TI3KT_3CAoiYOBboTA5tp034p7QDSHR76c2w_0fX3E-H6lXXnK7ny3PppulDZrKovyH-KY8Efk031wXrFrPxK-HyAIZStVOMAySxh4IOQu1v-IAz6jLg0hHxmJl6jfGViWdB_MPN6K-wNY1e3JTbcJh-KpjSyqPa0NAmHMBW75_5MEA196dZ6E9CqILd3qezuklrn168qt9gKrKf3qe316cYd3BM24n4VH1nJWqOqLFcYOLsCWXaTgoK-Ozqm7c8zRqKTCfgVJV-YXRtM4K-FDZ7-jfVTTS3-QqzMGAEaJkLwfLrEUzToieS8bjvXeuwtW5-BBJTRs_xeQRfPmOSEfRshy6O1hchzDLe64ZnhOAycbk61LFMxuZc59siLzgxKMu-8H7KyDxLDb7wsCdycfM_plJhlFawk2TZ_b5j7EePF'}

r = requests.get(url=url, headers=params)

data = r.json()

print(data)


import requests

url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
payload = open("request.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=payload, headers=headers)