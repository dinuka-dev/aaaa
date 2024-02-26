import requests
from bs4 import BeautifulSoup
import concurrent.futures

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getArtists(first_two):

    cookies = {
        'osano_consentmanager_uuid': '0eae5c2d-d0f4-4eb6-9ff3-94ce3b8f5134',
        'osano_consentmanager': 'fVmG_Y7dwv2npaDYVtUXTpFZQVYRGD6FqDAawLV-myiwuhFKVgZBciwXCVXK7pzTF41NdMJzAn8AiPc2nCi4q08q46VZ3ZGolbYDwdx4hzuAn4h-BBiDHMF4M8kOinDsA_YOhODJLHMf0kGjaF05DUHDN8wTPQOY_I-gke6gck15FbXjV3jMzkhw_3ELschrXlqnKJOAd_fejJlKc0efPoe7JNHoS4j_Jv63AZ0_1z3Zrq0QchxILIbu8tACy2UBLfCihjBn3aKvOA-H1lUHDU429yi8Vk1qeU6Dgg==',
        '_hjSessionUser_3094063': 'eyJpZCI6IjY2MjU5NmE4LTZhZTYtNTNlYy05MjAyLTUxZTRlZTlkMTlkMyIsImNyZWF0ZWQiOjE3MDg1Njg2NDg4MDUsImV4aXN0aW5nIjp0cnVlfQ==',
        '__cf_bm': 'HJ_mddXkLfSe0B3jPiZV_H1uNAYdbl8TxMsHJdjK6kI-1708752740-1.0-AWMGobyGHvIlCJtfy75mNnmIKkEkYODEWTERgpLgchIXSNGtINk0ZJKlZjz4Bbavy21wYxlm2yUojgbWYWdPZJQ=',
        '_ga_CS131LSFZC': 'GS1.1.1708752740.3.0.1708752740.60.0.0',
        '_ga': 'GA1.2.1779780398.1708568648',
        '_gid': 'GA1.2.292641689.1708752741',
        '_hjSession_3094063': 'eyJpZCI6ImZiYzYzYjEzLTQyNjYtNDRjMS1iNTg3LWZkODQzZDNiNjkzYSIsImMiOjE3MDg3NTI3NDE2NjMsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    }

    headers = {
        'authority': 'www.soundexchange.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.soundexchange.com',
        'referer': 'https://www.soundexchange.com/what-we-do/for-artists-labels-and-producers/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'ulists_get_query',
        'ul_cate': 'UP',
        'ul_search': first_two,
        'ul_type': '',
    }

    try:
        response = requests.post('https://www.soundexchange.com/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)

        html_part = find_between( response.text, '.<hr><br>', '"}')
        html_part = html_part.replace('\/', '/').replace('class=\\"uli-search-item\\"', 'class="uli-search-item"')
        soup = BeautifulSoup(html_part, 'html.parser')
        items = soup.find_all(name="div", class_="uli-search-item")
        file_path = f"output/{first_two}.txt"

        for item in items:
            name = item.text
            decoded_name = bytes(name, "utf-8").decode("unicode_escape")
            print(decoded_name)
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(decoded_name + '\n')

    except:
        with open('failed.txt', 'a', encoding='utf-8') as file:
            file.write(first_two + '\n')
        return

def ProcessDataList(data_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(getArtists, data_list))
        return results

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

result_list = []
for first_letter in alphabet:
    for second_letter in alphabet:
        for third_letter in alphabet:
            result_list.append(first_letter + second_letter + third_letter)

print(len(result_list))
ProcessDataList(result_list)
