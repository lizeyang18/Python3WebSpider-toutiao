import requests
import os
from hashlib import md5
from urllib.parse import urlencode

def get_page(offset):
   params={
       'offset':offset,
       'format':'json',
       'keyword':'街拍',
       'autoload':'true',
       'count':'20',
       'cur_tab':'3'
   }
   url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
   try:
       response = requests.get(url)
       if response.status_code == 200:
           return response.json()
   except requests.ConnectionError:
       return None

def get_images(json):
     if json.get('data'):
         for item in json.get('data'):
             title = item.get('title')
             images = item.get('image_list')
             for image in images:
                 yield {
                     'image':image.get('url'),
                     'title':title
                 }

def save_image(item):
     if not os.path.exists(item.get('title')):   #新建文件夹
         os.mkdir(item.get('title'))
     try:
         response = requests.get("http:" + item.get('image'))
         if response.status_code == 200:
             file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
             if not os.path.exists(file_path):
                 with open(file_path,'wb') as f:
                     f.write(response.content)
             else:
                 print('Already Download',file_path)
     except requests.ConnectionError:
         print('Failed to save Image!')

if __name__ == '__main__':
     for offset in range(1,3):
         json = get_page(offset*20)
         for item in get_images(json):
               print(item)
               save_image(item)