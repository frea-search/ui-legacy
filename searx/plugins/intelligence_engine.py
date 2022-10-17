# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
import socket
import json

name = "Intelligence Engine"
description = "Displays useful informations."
default_on = True

class Client:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def request(self, query):
        s = self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)
        message = query
        s.send(message.encode())
        data = s.recv(1024)
        return(format(data.decode()))
        s.close()
    

def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if '天気' in search.search_query.query:
        client = Client('/tmp/org.freasearch.intelligence-engine/weather.sock')
        api_result = client.request(search.search_query.query)
        result = json.load(api_result)
        message="現在の天気: " + api_result['next_1_hours']['summary']['symbol_code']

        search.result_container.answers['weather'] = {'answer': result}
        
    return True

if __name__ == '__main__':
    client = Client('/tmp/org.freasearch.intelligence-engine/weather.sock')
    print(client.request('東京　天気'))