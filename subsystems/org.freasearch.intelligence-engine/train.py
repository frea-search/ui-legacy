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
import requests
import ast
import socket
import dbm
import feedparser

socket_dir = '/tmp/org.freasearch.intelligence-engine'
socket_path = '/tmp/org.freasearch.intelligence-engine/train.sock'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
header = {
	'User-Agent': user_agent
}

db = dbm.open('train_cache', 'c')


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
        
        query = format(data.decode())

        feed_data = feedparser.parse('http://api.tetsudo.com/traffic/atom.xml')

        for entry in feed_data.entries:
            train_name = entry.title
            info_url = entry.link

            if query in entry.title:
                result = entry.link
                break
            else:
                result = "NO_DATA"

        connection.send(result.encode())
        return


def main():
    if not os.path.exists(socket_dir):
        os.makedirs(socket_dir)
    
    server = Server(socket_path)
    server.start()

if __name__ == '__main__':
    main()
