# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
import socket
import ast
import chardet

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
        client = Client('/var/frea/tmp/org.freasearch.intelligence-engine/weather.sock')
        api_result = client.request(search.search_query.query)
        result = ast.literal_eval(api_result)
        #print(chardet.detect(result))
        message="現在の天気: " + result['weather']

        search.result_container.answers['weather'] = {'answer': message, 
                                                                                                       'weather': 'MET Norway', 
                                                                                                       'hide_icon': 'true',
                                                                                                       'weather_icon': result['weather'],
                                                                                                       'weather_temp': result['temp_now'],
                                                                                                       'weather_icon_2d': result['weather_d2'],
                                                                                                       'weather_temp_2d': result['maxtemp_d2'],
                                                                                                       'weather_icon_3d': result['weather_d3'],
                                                                                                       'weather_temp_3d': result['maxtemp_d3'],
                                                                                                       'd2_disp': result['d2_disp'],
                                                                                                       'd3_disp': result['d3_disp']}
        
    return True

if __name__ == '__main__':
    client = Client('/var/frea/tmp/org.freasearch.intelligence-engine/weather.sock')
    print(client.request('東京　天気'))