import os
from time import sleep
import requests
import ffmpy
import json
import time

def message_write(message):
    f = open('./python/result.txt', 'w')
    f.write(str(message))
    f.close()

file_path = "../flv/"
url = "http://120.131.15.222:19971/classify_file"
# url = "http://172.20.15.136:19971/"
# url = "http://172.20.15.138:1985/api/v1/raw"

wait_file_count = 0
repost_count = 0
response_none_count = 0

message_dict = {0:"algorithm error!",
                1:"",
                2:"hunger",
                3:"pain",
                4:"physiological",
                5:"awake",
                6:"diaper",
                7:"hug",
                8:"sleepy",
                9:"lonely"}

delay_cry_ST = 0
DELAY_INTERVAL = 5

while(True):
    # Reset result file
    message_write("")

    # Get sorted flv file name
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

    # Transcode flv file to wav file
    for i in range(len(file_list)):
        ff = ffmpy.FFmpeg(inputs = {file_path + file_list[i] : '-y'}, 
                            outputs= {file_path + file_list[i].replace('flv', 'wav') : ['-loglevel', 'quiet', '-ar', '22050', '-ac',  '1']})
        ff.run()

    # Send wav file to algorithm by POST
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
        print(re_code)

        if re_code == 0 or re_code == 1:
            keep_time = time.time()-delay_cry_ST
            if keep_time<=DELAY_INTERVAL:
                pass
            else:
                message_write(message_dict[re_code])
        else: #cry
            delay_cry_ST = time.time()
            message_write(message_dict[re_code])




