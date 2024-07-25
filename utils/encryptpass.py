import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes as grb

def encrypt(key, src, encode=True, keyType = 'hex'):
	src = src.encode()
	if keyType == "hex":
		key = bytes(bytearray.fromhex(key))

	IV = grb(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, IV)
	padding = AES.block_size - len(src) % AES.block_size
	src += bytes([padding]) * padding
	encData = IV + cipher.encrypt(src)
	return base64.b64encode(encData).decode() if encode else encData


def decrypt(key, src, decode=True, keyType="hex"):
	# src = src.encode()
	if decode:
		src = base64.b64decode(src)

	if keyType == "hex":
		key = bytes(bytearray.fromhex(key))

	IV = src[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CBC, IV)
	decData = cipher.decrypt(src[AES.block_size:])
	padding = decData[-1]
	if decData[-padding:] != bytes([padding]) * padding:
		raise ValueError("Invalid padding...")
	return decData[:-padding]
