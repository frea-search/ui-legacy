# SPDX-License-Identifier: AGPL-3.0-or-later

'''
Frea Search is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Frea Search is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Frea Search. If not, see < http://www.gnu.org/licenses/ >.

(C) 2022  Frea Search, Ablaze
                   nexryai <gnomer@tuta.io>
'''

import sys
import os
import datetime
from zoneinfo import ZoneInfo
import requests
import json
import ast
import socket
import urllib
import dbm
import pygeonlp.api

socket_dir = '/var/frea/tmp/org.freasearch.intelligence-engine'
socket_path = '/var/frea/tmp/org.freasearch.intelligence-engine/weather.sock'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
header = {
	'User-Agent': user_agent
}

pygeonlp.api.init()

if not os.path.exists(socket_dir):
    os.makedirs(socket_dir)

db = dbm.open('/var/frea/tmp/weather_cache', 'c')


class Server:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def start(self):
        s = self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(self.socket_path)
        s.listen(1)
        try:
            while True:
                connection, address = s.accept()
                sys.stdout.write("connected\n")
                self.accepted(connection, address)
        finally:
            os.remove(self.socket_path)
            db.close()

    def accepted(self, connection, address):
        data = connection.recv(1024)
        sys.stdout.write("receive from client: {}\n".format(data.decode()))
        
        get_location = pygeonlp.api.geoparse(format(data.decode()))

        try:
            get_location[0]['geometry']['coordinates']
        except:
            connection.send(b'NO_DATA')
            return
        
        lon = get_location[0]['geometry']['coordinates'][0]
        lat = get_location[0]['geometry']['coordinates'][1]
        cache_key = str(lat) + '_' +  str(lon)
        
        get_date = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
        now_date = get_date.strftime('%Y%m%d%H')

        # check cache
        try: 
            cache_date = db[cache_key + '.date'].decode('utf-8')
        except:
            cache_date = 'unavailable'

        if cache_date == now_date:
            # use cache
            sys.stdout.write('Use cache!  data:' + str(now_date) + ' cache_date:' + str(cache_date) +'\n')
            cache_content = db[cache_key + '.content'].decode('utf-8')
            weather_json = ast.literal_eval(cache_content)
        else:
            # get weather data from met norway
            met_api_request_url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=" + str(lat) + "&lon=" + str(lon)
            met_api_response = requests.get (met_api_request_url,  headers=header)
            weather_json = met_api_response.json()

            # make cache
            sys.stdout.write('Save cache!\n')
            db[cache_key + '.content'] = str(weather_json)
            db[cache_key + '.date'] = str(now_date)

        get_d2_date = datetime.timedelta(days = 1)
        get_d3_date = datetime.timedelta(days = 2)

        date_year = get_date.year
        date_month = get_date.month
        date_day = get_date.day
        date_hour = get_date.hour

        date_d2_month = (get_date + get_d2_date).month
        date_d2_day = (get_date + get_d2_date).day
        date_d3_month = (get_date + get_d3_date).month
        date_d3_day = (get_date + get_d3_date).day

        # 翌日9時までの時間(h)
        d2_key =  24 + 9 - date_hour
        d3_key =  48 + 9 - date_hour

        weather = weather_json['properties']['timeseries'][0]['data']['next_12_hours']['summary']['symbol_code']
        temp_now = weather_json['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']

        weather_d2 = weather_json['properties']['timeseries'][d2_key]['data']['next_12_hours']['summary']['symbol_code']
        weather_d3 = weather_json['properties']['timeseries'][d3_key]['data']['next_12_hours']['summary']['symbol_code']

        def get_max_temp(day):
            max_temp = -99999
            for i in range(7):
                day_index = i + (24 * day - date_hour)
                i_temp = weather_json['properties']['timeseries'][day_index]['data']['instant']['details']['air_temperature']
                if max_temp < i_temp:
                    max_temp = i_temp

            return max_temp

        def get_min_temp(day):
            min_temp = 99999
            for i in range(7):
                day_index = i + (24 * day - date_hour)
                i_temp = weather_json['properties']['timeseries'][day_index]['data']['instant']['details']['air_temperature']
                if min_temp > i_temp:
                    min_temp = i_temp
            
            return min_temp

        maxtemp_d2 = get_max_temp(1)
        mintemp_d2 = get_min_temp(1)
        maxtemp_d3 = get_max_temp(2)
        mintemp_d3 = get_min_temp(2)

        response = {'debug': date_hour, 'weather': weather, 'temp_now': temp_now, 'weather_d2': weather_d2, 'weather_d3': weather_d3, 'maxtemp_d2': maxtemp_d2, 'mintemp_d2': mintemp_d2, 'maxtemp_d3': maxtemp_d3, 'mintemp_d3': mintemp_d3, 'd2_disp':  str(date_d2_month) + '/' + str(date_d2_day), 'd3_disp':  str(date_d3_month) + '/' + str(date_d3_day)} 
    
        connection.send(str(response).encode())
        return


def main():
    server = Server(socket_path)
    server.start()

if __name__ == '__main__':
    main()
