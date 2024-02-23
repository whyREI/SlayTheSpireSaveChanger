import base64


class SaveFileObfuscator:
    def __init__(self, key="key"):
        self.key = key.encode()

    def encode(self, s):
        encoded_data = self.xor_with_key(s.encode())
        return self.base64_encode(encoded_data)

    def decode(self, s):
        decoded_data = self.base64_decode(s)
        return self.xor_with_key(decoded_data).decode()

    def xor_with_key(self, data):
        key_length = len(self.key)
        out = bytearray(len(data))
        for i in range(len(data)):
            out[i] = data[i] ^ self.key[i % key_length]
        return out

    @staticmethod
    def base64_decode(s):
        return base64.b64decode(s)

    @staticmethod
    def base64_encode(b):
        return base64.b64encode(b).decode()

    @staticmethod
    def is_obfuscated(data):
        return "{" not in data and "}" not in data
