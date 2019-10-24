#coding=utf-8
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
# AES CBC PKCS5Padding

class PrpCrypt(object):

    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC

    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad.encode("utf-8")* amount_to_pad
    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'1269571569321021')
        text = self.__pad(text)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'1269571569321021')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    pc = PrpCrypt('hqtw-15600000004')  # 初始化密钥
    e = pc.encrypt("a1234567")  # 加密
    d = pc.decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)