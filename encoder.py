import pandas as pd
from cryptography.fernet import Fernet



class EncoderDecoder():

    def __init__(self):
        self._fernet_key = '7AbQpZWYYi96g1nmNTcYxFxg04Qi5Rfmd7drVqhL1t8='
        self._vigenere_key = 'knrStW0PJDgn3e1PaQw3QXxq5oqAzCKJ7XwrnHLWkcihd_7'


    # ------------------------------------------------
    # Handle CSV files
    # ------------------------------------------------
    def load_csv(self, filename: str, separator: str) -> pd.DataFrame :
        try:
            df = pd.read_csv(filename, sep=separator)
        except:
            df = None
        return df

    def store_csv(self, df: pd.DataFrame, filename:str, separator: str) -> bool:
        df.to_csv(filename, sep=separator)
        

    # ------------------------------------------------
    # Encode/Decode functions
    # ------------------------------------------------
    def encode(self, df: pd.DataFrame, fernet=True, vigenere=True) -> pd.DataFrame :
        df['concat'] = ['|'.join(row) for row in df[df.columns[0:]].astype(str).values]
        if fernet:
            df['fernet'] = [self._fernet_encode(row.encode('utf-8')) for row in df['concat'].values]
        if vigenere:
            df['vigenere'] = [self._vigenere_encode(row) for row in df['concat'].values]
        df = df.drop(columns=['concat'])
        df.to_csv('encoded.csv')
        return df


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
    def _vigenere_encode(self, string):
        key = self._vigenere_key
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return encoded_string

    def _vigenere_decode(self, string):
        key = self._vigenere_key
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        decoded_string = ''.join(encoded_chars)
        return decoded_string
        

eita = EncoderDecoder()
df = eita.load_csv('eita.csv', ';')
df = eita.encode(df)
print(df)