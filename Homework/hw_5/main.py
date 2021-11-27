import hashlib
import base64
from typing import Literal
import random


class PasswordHandler:

    def __init__(self, hashAlgorithm: str, numberBase: Literal[16, 32, 64], paper=""):
        self.h = hashlib.new(hashAlgorithm)
        self.numberBase = numberBase
        self.paper = paper

    def convertBaseOfHash(self, hashBytes: bytes, base: int) -> str:
        convertedHash = str()
        if base == 16:
            convertedHash = base64.b16encode(hashBytes).decode("utf-8")
        elif base == 32:
            convertedHash = base64.b16encode(hashBytes).decode("utf-8")
        else:
            convertedHash = base64.b64encode(hashBytes).decode("utf-8")

        return convertedHash

    def hash_password_raw(self, password: str) -> str:
        h = self.h.copy()
        h.update(f'{password}'.encode())
        hashed = h.digest()
        return self.convertBaseOfHash(hashed, self.numberBase)

    def hash_password(self, password: str) -> str:
        salt = self.get_salt()
        return self.hash_password_raw(password + salt + self.paper) + ":" + salt

    def verify_password(self, password: str, compared_hash: str) -> bool:
        raw_hash, hash_salt = compared_hash.split(':', 2)
        hashed_input_password = self.hash_password_raw(password + hash_salt + self.paper)
        if(raw_hash == hashed_input_password):
            return True
        return False

    def get_salt(self) -> str:
        salt_number = random.randint(0, 2 ** 256 - 1)
        return base64.b64encode(salt_number.to_bytes(32, "little")).decode("utf-8")


hashPassword = PasswordHandler('sha256', 32, paper="somelonglongpapper")

password = input()

hashed_password = hashPassword.hash_password(password)

while True:
    passw = input("write saved password: ")
    if(hashPassword.verify_password(passw, hashed_password)):
        print("Password okey")
        break
    print("Wrong password")
