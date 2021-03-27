#!/usr/bin/env python3
from argparse import ArgumentParser
from getpass import getpass
import urllib.request
from urllib.error import HTTPError
import ssl
import json
import os


def request(method, host, endpoint, headers=None, data=None, proxy=None, verify=None):
    request_ = urllib.request.Request('https://' + host + endpoint)
    request_.method = method
    request_.add_header('accept', 'application/json')
    request_.add_header('content-type', 'application/json')
    context = ''
    if headers:
        for key, value in headers.items():
            request_.add_header(key, value)
    if data:
        request_.data = json.dumps(data).encode()
    if proxy:
        request_.set_proxy(proxy, 'https')
    if verify is False:
        context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(request_, context=context)
        return response
    except HTTPError as error:
        print('\nERROR: HTTP ' + str(error.code))
        print(error.reason)


class TenableIO:
    def __init__(self, username=None, password=None, proxy=None, verify=True):
        self.host = 'cloud.tenable.com'
        self.username = username
        self.password = password
        self.proxy = proxy
        self.verify = verify

        # Create authentication headers
        auth = self._login()
        self.headers = {"x-cookie": "token=" + auth['token']}

    def request(self, method, endpoint, data=None):
        response = request(method, self.host, endpoint, self.headers, data, self.proxy, self.verify)
        return response

    def _login(self):
        response = request('POST', self.host, '/session', data={"username": self.username, "password": self.password},
                           proxy=self.proxy, verify=self.verify)
        return json.load(response)

    def logout(self):
        response = self.request('DELETE', '/session')
        return response


def menu(data):
    os.system('clear')
    print('Update authentication methods for which user group?')
    for index, key in enumerate(data):
        print(str(index) + '. ' + str(key['name']))
    selection = prompt('number', 'Enter number: ', range(len(data)))
    user_group = data[selection]
    return user_group


def prompt(type_, message, selections):
    error_msg = 'ERROR: Invalid entry'
    while True:
        try:
            if type_ == 'number':
                selection = int(input(message).strip())
            elif type_ == 'yn':
                selection = input(message).strip()
        except ValueError:
            print(error_msg)
            continue
        if selection not in selections:
            print(error_msg)
            continue
        else:
            break
    if type(selection) is int:
        return selection
    elif selection == 'y':
        return True
    elif selection == 'n':
        return False
    else:
        print(error_msg)
        tio.logout()
        quit()


# Gather arguments. Proxy and ssl verification arguments are not required.
arguments = ArgumentParser(description='Tool to update Tenable.IO user authentication methods')
arguments.add_argument(
    '-p',
    '--proxy',
    metavar='127.0.0.1:8080',
    default='',
    dest='proxy',
    help='HTTPS proxy'
)
arguments.add_argument(
    '-i',
    '--insecure',
    action='store_false',
    dest='verify',
    default=True,
    help='Disable SSL verification'
)
arguments = arguments.parse_args()

username = input('Username: ')
password = getpass()
proxy = arguments.proxy
verify = arguments.verify

tio = TenableIO(username=username, password=password, proxy=proxy, verify=verify)

if json.load(tio.request('GET', '/session'))['permissions'] != 64:
    print('ERROR: User is not an Administrator')
    tio.logout()
    quit()

user_group = menu(json.load(tio.request('GET', '/groups'))['groups'])

auth_api = prompt('yn', 'API authentication permitted [y/n]: ', ['y', 'n'])
auth_password = prompt('yn', 'Tenable.IO local authentication permitted [y/n]: ', ['y', 'n'])
auth_saml = prompt('yn', 'SAML authentication permitted [y/n]: ', ['y', 'n'])

if auth_api is False and auth_password is False and auth_saml is False:
    print('ERROR: You must have at least one authentication method enabled')
    tio.logout()
    quit()

users = json.load(tio.request('GET', '/groups/' + str(user_group['id']) + '/users'))

os.system('clear')
print('********** WARNING **********\nYou are about to update authentication methods to:')
print('API authentication permitted: ' + str(auth_api))
print('Tenable.IO local authentication permitted: ' + str(auth_password))
print('SAML authentication permitted: ' + str(auth_saml))
print('\n')
print('For the following users:')
for user in users['users']:
    print(user['username'])
print('\n')

proceed = prompt('yn', 'Proceed with authentication updates? [y/n]: ', ['y', 'n'])
if proceed is False:
    print('INFO: No changes were made')
elif proceed is True:
    for user in users['users']:
        tio.request(
            'PUT',
            '/users/' + str(user['id']) + '/authorizations',
            data={
                "api_permitted": auth_api,
                "password_permitted": auth_password,
                "saml_permitted": auth_saml
            }
        )
    for user in users['users']:
        auths = json.load(tio.request('GET', '/users/' + str(user['id']) + '/authorizations'))
        if (auths['api_permitted'] is not auth_api or auths['password_permitted'] is not auth_password or
                auths['saml_permitted'] is not auth_saml):
            print('WARNING: Failed to update authentication methods for user ' + user['username'])
    print('INFO: Process complete')

tio.logout()
