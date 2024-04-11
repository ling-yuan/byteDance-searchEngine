# from Crypto.Cipher import AES
# import base64
# import re
# import random

# import execjs

# def decrypt_aes(encryptedStr):
#     key = "SjXbYTJb7zXoUToSicUL3A=="
#     iv = "OekMLjghRg8vlX/PemLc+Q=="
#     formatedKey = base64.b64decode(key)
#     formatedIv = base64.b64decode(iv)
#     decryptedData = AES.new(formatedKey, AES.MODE_CBC,
#                             formatedIv).decrypt(base64.b64decode(encryptedStr))
#     return re.sub(r"\f|[\x00-\x1F\x7F-\x9F]", "",
#                   decryptedData.decode("utf-8"))

# def get_ms_token(randomlength=107):
#     """
#     根据传入长度产生随机字符串
#     """
#     random_str = ''
#     base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
#     length = len(base_str) - 1
#     for _ in range(randomlength):
#         random_str += base_str[random.randint(0, length)]
#     return random_str

# def get_xb_data():
#     with open("douyin.js") as f:
#         js_data = f.read()

#     js_compile = execjs.compile(js_data)
#     xb_data = js_compile.call("window.xiaoc", )
#     print(xb_data)

# get_xb_data()

# var t = new XMLHttpRequest;
# tmp_url = "https://trendinsight.oceanengine.com/api/v2/index/get_relation_word";
# t.open('POST',tmp_url,true);
# t.setRequestHeader('accept', 'application/json, text/plain, */*');  
# t.setRequestHeader('accept-language', 'zh-CN,zh;q=0.9');
# t.setRequestHeader('content-type', 'application/json;charset=UTF-8');
# t.send('{"param":{"app_name": "aweme", "end_date":"20240317","keyword":"新能源汽车","start_date":"20240311"}}');  