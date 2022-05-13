import os
from time import sleep
import requests
import ffmpy
import json

def message_write(message):
    f = open('./python/result.txt', 'w+')
    f.write(str(message))
    f.close()

file_path = "../flv/"
url = "http://120.131.15.222:19971/classify_file"
# url = "http://172.20.15.136:19971/"
# url = "http://172.20.15.138:1985/api/v1/raw"

wait_file_count = 0
repost_count = 0
response_none_count = 0

while(True):
    # 
    message_write("")

    # Get sorted file name
    file_list = [f for f in os.listdir(file_path) if f.endswith('flv')]
    if(not file_list):
        wait_file_count += 1
        sleep(10)
        if(wait_file_count == 3):
            message_write("no_file_error")
            exit()
        continue
    wait_file_count = 0
    file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))

    # Transcode flv file to mp3 file
    for i in range(len(file_list)):
        ff = ffmpy.FFmpeg(inputs = {file_path + file_list[i] : '-y'}, 
                            outputs= {file_path + file_list[i].replace('flv', 'wav') : ['-loglevel', 'quiet']})
        ff.run()

    # Send flv file by POST
    for i in range(len(file_list)):
        payload={}
        files=[('file',(str(i)+'.wav',open(file_path + file_list[i].replace('flv', 'wav'),'rb')))]
        headers = {}    
        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=20)
        except:
            # Some post errors hapended and Repost this file
            i -= 1
            repost_count += 1
            if(repost_count == 3):
                message_write("post_error")
                exit()
            continue
        
        # Bad response
        if(response.status_code != 200):
            response_none_count += 1
            i -= 1
            if(response_none_count == 3):
                message_write("no_response_error")
                exit()
            continue

        # Get response from post
        os.remove(file_path + file_list[i])
        os.remove(file_path + file_list[i].replace('flv', 'wav'))
        
        repost_count = 0
        response_none_count = 0

        re_data = json.loads(response.text)
        re_code = re_data['code']

        if(re_code == 0):
            message_write("algorithm error!")
        elif(re_code == 1):
            message_write("")
        elif(re_code == 2):
            message_write("hunger")
        elif(re_code == 3):
            message_write("pain")
        elif(re_code == 4):
            message_write("physiological")
        elif(re_code == 5):
            message_write("awake")
        elif(re_code == 6):
            message_write("diaper")
        elif(re_code == 7):
            message_write("hug")
        elif(re_code == 8):
            message_write("sleepy")
        elif(re_code == 9):
            message_write("lonely")



