import requests
import json


api_key = '6104cdf2aa594a6a6fce642b03fd63f2'
get_number_url = f'https://onlinesim.ru/api/getNum.php?apikey=' \
    f'{api_key}&service=wildberries&number=1'

get_number = requests.get(get_number_url)
get_number = json.loads(get_number.text)
my_number = get_number['number']
my_number = my_number[2:]
my_tzid = get_number['tzid']



get_code_url = f'https://onlinesim.ru/api/getState.php?apikey' \
    f'={api_key}'
params = {
    'tzid': my_tzid,
    'message_to_code': '1'
}
get_code_req = requests.get(get_code_url, params=params)
get_code = json.loads(get_code_req.text)
get_code = get_code[0]
try:
    code = get_code['msg']
except Exception:
    print('Смс не пришло')
