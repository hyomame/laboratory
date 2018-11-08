# -*- coding: utf-8 -*-

import time
import communication
import processing

def init():
    times = 1
    while True:
        client = communication.CommunicationToServer()
        action = processing.ProcessingMessage()
        client.connect_to_server()
        print("episodes:" + str(times))

        play(client, action)

        times += 1
        time.sleep(1)

def play(client, action):
    loop_flag = True
    while loop_flag:
        receive_file = client.receive_message()
        for rmessage in receive_file:
            print('[rec] ' + rmessage)

            smessage = action.analyze(rmessage)
            if smessage != '000 NOTPLAY':
                print('[send] ' + smessage)
                client.send_message(smessage)
            if smessage == '203 EXIT':
                loop_flag = False

if __name__ == '__main__':
    init()