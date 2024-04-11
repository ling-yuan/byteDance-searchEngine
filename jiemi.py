# aes-cbc解密
from Crypto.Cipher import AES
import base64
import re


def decrypt_aes(encryptedStr):
    key = "SjXbYTJb7zXoUToSicUL3A=="
    iv = "OekMLjghRg8vlX/PemLc+Q=="
    formatedKey = base64.b64decode(key)
    formatedIv = base64.b64decode(iv)
    decryptedData = AES.new(formatedKey, AES.MODE_CBC,
                            formatedIv).decrypt(base64.b64decode(encryptedStr))
    return re.sub(r"\f|[\x00-\x1F\x7F-\x9F]", "",
                  decryptedData.decode("utf-8"))


if __name__ == '__main__':
    encryptedStr = ""

    ans = decrypt_aes(encryptedStr)
    # with open("decrypted.json", "w", encoding='utf-8') as f:
    #     f.write(ans)
    print(ans)
