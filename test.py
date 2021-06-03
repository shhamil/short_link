import requests
response_api = requests.post('http://127.0.0.1:8000/api/url_api', headers={'Authorization': 'Token ' + 'ank52w-0a393c15825668b88f559cd1cb1edbb4'}, data={'url_for_shorting': 'https://progi.pro/oshibka-cs0433-tip-zadacha-sushestvuet-kak-v-systemthreading-tak-i-v-mscorlib-6706374'})
response_url_json = response_api.json()
print(response_url_json['short_link'])
