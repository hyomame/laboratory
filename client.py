# -*- coding: utf-8 -*-

import time
import communication
import processing

def main():
    loop_count = 200
    client = communication.CommunicationToServer()
    action = processing.ProcessingMessage()
    client.connect_to_server()

    for i in range (loop_count+1):
        print("episodes:" + str(i+1))

        if i != 0:
            action.reset_board()

        play(client, action)
    
    exit(0)

def play(client, action):
    loop_flag = True

    while loop_flag:
        receive_file = client.receive_message()

        for rmessage in receive_file:
            print('[rec] ' + rmessage)

            smessage = action.analyze(rmessage)
            if smessage == None:
                print('None error.')
                client.disconnect_to_server()
                exit(1)
            if smessage == '003 DISCONNECT':
                client.disconnect_to_server()
                exit(1)
            elif smessage == '001 NEXT':
                loop_flag = False
                break
            elif smessage != '000 NOTPLAY':
                print('[send] ' + smessage)
                client.send_message(smessage)

if __name__ == '__main__':
    main()