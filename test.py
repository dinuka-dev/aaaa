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
        '_gid': 'GA1.2.72723438.1708981075',
        '__cf_bm': 'Jag1gUtR.XTu1uSYwmSZoN4EB_FFArmTFk6iJJnTE1c-1709052926-1.0-AZdf5Wvyx6tHSKHQQn9oe7feUChHVQ1l8SfGouciZFI24pnHSQVikmTQU6RJpXXNrUf2dzLLuh5pJvVpttUijVc=',
        '_ga_CS131LSFZC': 'GS1.1.1709052926.5.0.1709052926.60.0.0',
        '_hjSession_3094063': 'eyJpZCI6IjgzOTRhMWIwLWM3MTUtNGZjMS04MGFiLTRkM2JiOTBjYWQ0YiIsImMiOjE3MDkwNTI5MjY4MjEsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_ga': 'GA1.2.1779780398.1708568648',
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
        'ul_cate': 'UA',
        'ul_search': first_two,
        'ul_type': '',
    }

    try:
        response = requests.post('https://www.soundexchange.com/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)
        if "No results found for this search." in response.text:
            print("No Results!")
            return
        
        jsonRes = response.json()
        html_string = jsonRes['html']
        soup = BeautifulSoup(html_string, 'html.parser')
        items = soup.find_all(name="div", class_="uli-search-item")
        file_path = f"output-ua/{first_two}.txt"
        for item in items:
            name = item.text
            decoded_name = bytes(name, "utf-8").decode("unicode_escape")
            print(decoded_name)
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(decoded_name + '\n')
    except:
        print("Failed!")
        with open('failed.txt', 'a', encoding='utf-8') as file:
            file.write(first_two + '\n')
        return

    if len(items) == 0:
        with open('your_file.txt', 'w', encoding='utf-8') as file:
            file.write(response.text + first_two)

def ProcessDataList(data_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        results = list(executor.map(getArtists, data_list))
        return results

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

result_list = []
# for first_letter in alphabet:
#     for second_letter in alphabet:
#         for third_letter in alphabet:
#             for fourth_letter in alphabet:
#                 result_list.append(first_letter + second_letter + third_letter + fourth_letter)

# Flag to indicate whether the current combination is after "KRSX"

found_krsx = False

for first_letter in alphabet:
    for second_letter in alphabet:
        for third_letter in alphabet:
            for fourth_letter in alphabet:
                current_combination = first_letter + second_letter + third_letter + fourth_letter
                result_list.append(current_combination)
                
                if found_krsx:
                    break
                
                # Check if the current combination is "KRSX"
                if current_combination == "KRSX":
                    found_krsx = True

print(len(result_list))
ProcessDataList(result_list)
