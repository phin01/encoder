import pandas as pd
from cryptography.fernet import Fernet
import base64



class EncoDeco():

    def __init__(self):
        self._fernet_key = '7AbQpZWYYi96g1nmNTcYxFxg04Qi5Rfmd7drVqhL1t8='
        self._vigenere_key = 'knrStW0PJDgn3e1PaQw3QXxq5oqAzCKJ7XwrnHLWkcihd_7'


    # ------------------------------------------------
    # Handle CSV files
    # ------------------------------------------------
    def load_csv(self, filename: str, separator: str) -> pd.DataFrame :
        try:
            df = pd.read_csv(filename, sep=separator, header=None)
        except:
            df = None
        return df

    def store_csv(self, df: pd.DataFrame, filename:str, separator: str) -> bool:
        try:
            df.to_csv(filename, sep=separator, header=None, index=None)
            return True
        except:
            return False
        

    # ------------------------------------------------
    # Encode/Decode functions
    # ------------------------------------------------
    def encode(self, df: pd.DataFrame, method="base64") -> pd.DataFrame :
        df['concat'] = ['|'.join(row) for row in df[df.columns[0:]].astype(str).values]
        if method == "fernet":
            df['fernet'] = [self._fernet_encode(row.encode('utf-8')) for row in df['concat'].values]
        if method == "vigenere":
            df['vigenere'] = [self._vigenere_encode(row) for row in df['concat'].values]
        if method == "base64":
            df['base64'] = [self._scramble64(row) for row in df['concat'].values]
        df = df.drop(columns=['concat'])
        return df

    def decode(self, df: pd.DataFrame, method="base64") -> pd.DataFrame :
        print('oxe')
        if method == "fernet":
            df['converted'] = [str(self._fernet_decode(row)) for row in df[0].values]
        if method == "vigenere":
            df['converted'] = [str(self._vigenere_decode(row)) for row in df[0].values]
        if method == "base64":
            df['converted'] = [str(self._unscramble64(row)) for row in df[0].values]

        df_split = df['converted'].str.split('|', expand=True)
        df_split['encoded'] = df[0] 

        return df_split


    # ------------------------------------------------
    # Fernet encode/decode helper functions
    # ------------------------------------------------
    def _fernet_encode(self, message: bytes) -> bytes:
        return Fernet(self._fernet_key).encrypt(message)

    def _fernet_decode(self, token: bytes) -> bytes:
        return Fernet(self._fernet_key).decrypt(token)
    

    # ------------------------------------------------
    # Vigenere encode/decode helper functions
    # https://gist.github.com/gowhari/fea9c559f08a310e5cfd62978bc86a1a
    # ------------------------------------------------
    def _vigenere_encode(self, string: str) -> str:
        key = self._vigenere_key
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return encoded_string

    def _vigenere_decode(self, string: str) -> str:
        key = self._vigenere_key
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        decoded_string = ''.join(encoded_chars)
        return decoded_string
        

    # ------------------------------------------------
    # Personal Base64 encoding
    #   String is initially encoded using base64
    #   Each char will be scrambled based on its unicode number incremented by an offset factor
    #        Offset factor is the remainder of the string's length divided by 8, added 1 (so it falls between a 1-8 range)
    #        Offset factor is reversed every other char
    # ------------------------------------------------
    def _scramble64(self, string: str) -> str:
        try:
            scrambled = ''
            b64 = base64.b64encode(string.encode('utf-8'))
            b64_string = str(b64)[2:-1]
            offset = len(b64_string) % 8 + 1
            for x in range(0, len(b64_string)):
                delta = offset * -1 if x % 2 == 0 else offset
                char = chr(ord(b64_string[x]) - delta)
                scrambled += str(char)
            return str(offset) + scrambled
        except:
            return ''

    def _unscramble64(self, string: str) -> str:
        # try:
        unscrambled = ''
        offset = int(string[0])
        string = string[1:]
        for x in range(0, len(string)):
            delta = offset * -1 if x % 2 == 0 else offset
            char = chr(ord(string[x]) + delta)
            unscrambled += str(char)
        return str(base64.b64decode(unscrambled.encode('utf-8')))[2:-1]
        # except:
        #     return ''
    
