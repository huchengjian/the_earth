#!/bin/python
# -*- coding=utf-8 -*-

import os
import uuid
import urllib2
import cookielib
from PIL import Image

base_path = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/"
latest_json = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
save_path = "/data/earth_project/pictures/"
UNIT_SIZE = 550
TARGET_WIDTH = 550 *4
TARGET_HEIGHT = 550 *4

# base_name = "2016-01-11-071000_"

def joint_pics(today_path, store_filename_base):

    print "Joint Pics."

    target = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT))

    left_margin = 0
    top_margin = 0
    for i in range(4):
        for j in range(4):

            # print "Joint Picture: " + store_filename_base+str(i)+'_'+str(j)+'.png'

            curr_image = Image.open(today_path + store_filename_base+str(i)+'_'+str(j)+'.png')
            target.paste(curr_image, (left_margin, top_margin))
            top_margin += UNIT_SIZE

        left_margin += UNIT_SIZE
        top_margin = 0

    # save header image
    full_pic_path = save_path + store_filename_base[0:-1] + '.png'
    if not os.path.exists(full_pic_path):
        quality_value = 100
        target.save(full_pic_path, quality=quality_value)
    else:
        print full_pic_path + " file exists!"
    print 'done! save file: ' + full_pic_path
    return full_pic_path

def get_file(url):
    try:
        cj=cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req=urllib2.Request(url)
        operate=opener.open(req, timeout=30)
        data=operate.read()
        return data
    except BaseException, e:
        print e
        return None

def save_file(path, file_name, data):
    if data == None:
        return

    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()

def main():
    print "\nBegin new one \n"

    result = urllib2.urlopen(latest_json, timeout = 30)

    dic = []
    date = ""
    store_filename = ""
    for line in result:
        print "Get latest json: " + line
        dic = eval(line)
        date = dic["date"].replace('-', '/').replace(' ','/').replace(':', '')

    today_path = save_path + date[0:10].replace('/', '_') + '/'
    if not os.path.exists(today_path):
        print "make dir " + today_path
        os.mkdir(today_path)

    for i in range(4):
        for j in range(4):
            filename = date+'_'+str(i)+'_'+str(j)+'.png'
            store_filename = filename.replace('/', '_')

            if os.path.exists(today_path+store_filename):
                print "ERROR: file exits. Already downloaded." + today_path + store_filename
                return

            url = base_path+filename
            print "Download picture: " + url

            #重试5次
            for count in range(5):
                receive_data = get_file(url)
                if receive_data == None:
                   print "Network error, retry." + url
                   if count == 4:
                       print "Retry 5 times, shutdown download."
                       return
                else:
                    break

            save_file(today_path, store_filename, receive_data) #按天存储临时照片

    full_pic_path = joint_pics(today_path, store_filename[0:-7])

    #存储最新照片的文件名, 用于设置桌面
    save_file(save_path, "newest_file", full_pic_path)


if __name__ == '__main__':
    main()