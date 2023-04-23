import requests

# cookies = {
#     '_ga': 'GA1.1.255225930.1681806410',
#     'rmbUserInfo': '{%22account%22:%22hao001%22%2C%22password%22:%22104|97|111|48|48|49%22}',
#     'locale': 'zh',
#     '_ga_1WBG941YJG': 'GS1.1.1682211042.8.0.1682211042.0.0.0',
#     'CONFIRM_COUNTRY_FLAG': 'true',
# }

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',

}

json_data = {
    'account': 'hao001',
    'password': '9e174ce146833842138a704582890571',
    'language': 'zh',
}

response = requests.post(
    'http://test.tracksolidpro.com/new/homepage/login',
    headers=headers,
    json=json_data,
    verify=False,
).text


print(response)

