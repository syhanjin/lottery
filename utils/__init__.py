from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class PrpCrypt(object):
    """
    AES 加密类
    """

    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_ECB


    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def add_to_16(self, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')

    def encrypt(self, text):
        cryptor = AES.new(
            self.key,
            self.mode,
        )
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        text = self.add_to_16(text)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        # print(self.ciphertext)
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode)
        plain_text = cryptor.decrypt(a2b_hex(text))
        # return plain_text.rstrip('\0')
        return bytes.decode(plain_text).rstrip('\0')


# ECB 加密方式
# 秘钥 16(AES-128) / 24(AES-192) / 32(AES-256) Bytes 长度
prpc = PrpCrypt('==lottery-2021==')
#               ^................^

from . import data