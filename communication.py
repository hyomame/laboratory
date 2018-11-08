# -*- coding: utf-8 -*-

import socket

class CommunicationToServer:
    def __init__(self):
        self.default_IP = socket.gethostbyname(socket.gethostname())
        self.default_port = 18420

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.default_IP, self.default_port))

    def receive_message(self):
        socket_file = self.client_socket.makefile()
        return socket_file
    
    def send_message(self, text):
        self.client_socket.send((text + '\r\n').encode())