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
    tsunami_client = Client('/var/frea/tmp/org.freasearch.intelligence-engine/tsunami.sock')
    tsunami_info = tsunami_client.request(search.search_query.query)
    tsunami = ast.literal_eval(tsunami_info)

    if tsunami["no_tsunami"] != "true":
        message = "警告: 現在、一部の沿岸地域に" + tsunami["grade"] + "が発表されています。"
        search.result_container.answers['tsunami'] = {'message': message, 'tsunami': 'true', 'hide_icon': 'true'}
        return True

    if search.search_query.pageno > 1:
        return True
    if '天気' in search.search_query.query:
        weather_client = Client('/var/frea/tmp/org.freasearch.intelligence-engine/weather.sock')
        api_result = weather_client.request(search.search_query.query)
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