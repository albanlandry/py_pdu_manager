import urllib.request
import json
import html
from pprint import pprint

class HttpRequest:
    '''
    [ Example Usage ]
    # Initialize the HttpRequest object with the URL
    http_request = HttpRequest('https://dummyjson.com/users')

    # Example GET request with optional headers
    get_headers = {'User-Agent': 'Mozilla/5.0'}
    response_get = http_request.get()
    print(f"GET Response: {response_get['total']}")

    # Example POST request with data and optional headers
    post_data = {'title': 'foo', 'body': 'bar', 'userId': 1}
    post_headers = {'Content-Type': 'application/json'}
    response_post = http_request.post(data=post_data, headers=post_headers)
    print("POST Response:", response_post)
    '''
    def __init__(self, url):
        self.url = url

    def get(self, headers=None):
        req = urllib.request.Request(self.url, headers=headers if headers else {})

        try:
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                # pprint(response_data)
                return json.loads(html.unescape(response_data))
        except urllib.error.HTTPError as errh:
            print("HTTP Error:", errh)
        except urllib.error.URLError as erru:
            print("URL Error:", erru)
        except Exception as err:
            print("An Error Occurred:", err)
    
    def post(self, data=None, headers=None):
        json_data = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(self.url, data=json_data, headers=headers if headers else {}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except urllib.error.HTTPError as errh:
            print("HTTP Error:", errh)
        except urllib.error.URLError as erru:
            print("URL Error:", erru)
        except Exception as err:
            print("An Error Occurred:", err)