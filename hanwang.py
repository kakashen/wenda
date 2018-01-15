import requests, base64, json, os, time,config
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(config.driver_location)
# 访问百度
driver.get('http://www.baidu.com')

key = 'adb3db14-a7b1-4f49-9514-703ae951d756'
url='http://api.hanvon.com/rt/ws/v1/ocr/text/recg?key=%s&code=74e51a88-41ec-413e-b162-bd031fe0407e' % key

print(url)
exit(123)

count = 0
screenpath = config.image_directory
while True:
  text = input('按下回车发起搜索')

  start = time.time()
  count = count+1
  imagepath = "D:\\screenshots\\1.jpg"
  region_path = config.image_directory+"region" + str(count) +".png"

  im = Image.open(imagepath)
  img_size = im.size
  w = im.size[0]
  h = im.size[1]


  region = im.crop((config.left, config.top, w - config.right, h-config.bottom))  # 裁剪的区域
  region.save(region_path)

  f = open(region_path, 'rb')
  ls_f = base64.b64encode(f.read())
  f.close()
  image_byte = bytes.decode(ls_f)


  url = 'http://api.hanvon.com/rt/ws/v1/ocr/text/recg?key=adb3db14-a7b1-4f49-9514-703ae951d756&code=74e51a88-41ec-413e-b162-bd031fe0407e'

  data = {"uid": "118.12.0.12", "lang": "chns", "color": "color",
          'image': image_byte}

  headers = {"Content-Type": "application/json; charset=UTF-8",
             "Accept-Content-Type": "application/octet-stream",
             "Authorization": "APPCODE " + config.appcode
             }
  res = requests.post(url, data=json.dumps(data), headers=headers)
  content = res.text
  if res.status_code != 200:
    print("orc识别错误")
    break

  json_data = json.loads(content)['textResult']
  keyword = str(json_data).strip().rstrip().lstrip().replace("\r", "").replace("\n","").replace(" ","")
  print("OCR识别内容: " + keyword)

  driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'a')
  driver.find_element_by_id('kw').send_keys(Keys.BACK_SPACE)
  driver.find_element_by_id('kw').send_keys(keyword)
  driver.find_element_by_id('su').send_keys(Keys.ENTER)

  end = time.time()
  print('程序用时：' + str(end - start) + '秒')
