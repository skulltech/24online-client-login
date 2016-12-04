import requests
import time
from lxml import html
from configparser import ConfigParser



config = ConfigParser()
config.read('config.ini')

username = config['CREDENTIALS']['USERNAME']
password = config['CREDENTIALS']['PASSWORD']
mac = config['CREDENTIALS']['MAC']
server_IP = config['CREDENTIALS']['24ONLINE_IP']

login_form = {
    'mode': '191',
    'mac': mac,
    'servername': '192.168.200.50',
    'username': username,
    'password': password}

logout_form = {'logout': 'Logout', 'password': '12121', 'username': username, 'loggedinuser': username,
               'servername': '192.168.200.50', 'mac': mac, 'mode': '193'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
    'Origin': 'http://{24online_IP}'.format(server_IP), 'Referer': 'http://{24online_IP}/24online/webpages/client.jsp'.format(server_IP)}


def login():
    login_request = requests.post('http://{24online_IP}/24online/servlet/E24onlineHTTPClient'.format(server_IP), data=login_form,
                                  headers=headers)
    return login_request.status_code


def logout():
    logout_request = requests.post('http://{24online_IP}/24online/servlet/E24onlineHTTPClient'.format(server_IP), data=logout_form,
                                   headers=headers)
    return logout_request.status_code

def check_connection():
    try:
        r = requests.get('http://www.google.com')

        tree = html.fromstring(r.content)
        title = tree.xpath('//title/text()')[0]
        if not (title=='Google'):
            return False

    except (requests.exceptions.ConnectionError, IndexError):
        return False
    else:
        return True


def main():

    while True:
        if not check_connection():
            logout()
            print ('[*] Logging in to PMPL Broadband... ', end = '')
            login()
            print('Done.')

        time.sleep(10)

if __name__=='__main__':
    main()