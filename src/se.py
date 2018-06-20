import os
import binascii
import hashlib
import sys
import json
import timeit

#PyCrypto package libraries
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16

words = []
index = {}
inverted_index = {}

# Padding for encryption and decryption. The value we encrypt must be a multiple of BLOCK_SIZE.
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def main(argv):
	# program enters the following segment if the enc command is used.
	if(argv[1] == "keygen"):
		r_key = binascii.hexlify(os.urandom(32)) # generating a random 32 bytes or 256 bit key
		key = hashlib.sha256(r_key.encode('utf-8')).hexdigest() #saving it in hex
		print(key)
		# write the generated key into a file (AES key)
		f = open(argv[3], 'w')
		f.write(key)
		f.close()
		# using SHA256 for PRF so no key is required. Writing nothing to the file.
		f = open(argv[2], 'w')
		f.write("")
		f.close()

		iv = Random.new().read(AES.block_size) # generating IV randomly
		f = open('../data/iv.txt', 'w') # saving IV to a file
		f.write(binascii.hexlify(iv))
		f.close()

	elif(argv[1] == "enc"):
		#loading AES key
		f = open(argv[3], 'r')
		key = f.read()
		key = binascii.unhexlify(key)
		f.close()

		f = open('../data/iv.txt', 'r')
		iv = f.read()
		iv = binascii.unhexlify(iv)
		f.close()
		#loading the files
		start = timeit.default_timer()
		for filename in os.listdir(argv[5]):
			f = open(argv[5]+"/"+filename, 'r')
			content = f.read()
			words_list = content.split(" ")
			f.close()

			for k in words_list:
				words.append(k)
			index["{}".format(filename)] = words_list

			padded_file_content = pad(content) #padding plaintext
			cipher = AES.new(key, AES.MODE_CBC, iv)
			ciphered_file_content = binascii.hexlify(iv + cipher.encrypt(padded_file_content)) # getting encrypted message in hex

			f = open(argv[6]+"/c{}.txt".format(filename[1:-4]), 'w') # saving the ciphered text in hex to a file
			f.write(ciphered_file_content)
			f.close()
			words_list = []

		unique_words = set(words)
		unique_words = list(unique_words)
		temp_list = []
		for x in unique_words:
			cx = hashlib.sha256(x.encode('utf-8')).hexdigest()
			for y in index:
				for z in range(len(index[y])):
					if(index[y][z] == x):
						temp_list.append("c{}".format(y[1:]))
			#print temp_list

			inverted_index["{}".format(cx)] = temp_list
			temp_list = []

		stop = timeit.default_timer()
		print("Encryption and build time:" + "{}".format(stop - start))

		print(inverted_index)

		with open(argv[4], 'w') as outfile:
			json.dump(inverted_index, outfile)

	elif(argv[1] == "token"):
		w = argv[2]
		token = hashlib.sha256(w.encode('utf-8')).hexdigest()
		print(token)

		f = open(argv[4], 'w')
		f.write(token)
		f.close()

	elif(argv[1] == "search"):
		str1 = ""
		str2 = ""
		f = open(argv[3], 'r')
		token = f.read()
		f.close()

		c_index = dict(json.load(open(argv[2])))

		start = timeit.default_timer()
		for x in c_index:
			if(x == token):
				for y in c_index[x]:
					str1 = str1 + y + " "
				print str1
				for y in c_index[x]:
					f = open(argv[4]+"/"+str(y), 'r')
					content = f.read()
					f.close()
					# load the key file
					f = open(argv[5], 'r')
					key = f.read()
					key = binascii.unhexlify(key)
					f.close()
					# load the iv file
					f = open('../data/iv.txt', 'r')
					iv = f.read()
					iv = binascii.unhexlify(iv)
					f.close()

					decoded_content = binascii.unhexlify(content) # decoding from hex
					dec_file_content = AES.new(key, AES.MODE_CBC, iv )
					unpadded_file_content = unpad(dec_file_content.decrypt(decoded_content[16:])).decode('utf-8') #unpadding the deciphered messaged (the first 16 bytes contain IV so the data after first 16 is to be decrypted)
					print(y+" "+unpadded_file_content)
					str2 = str2 + y + " " + unpadded_file_content + "\n"

		stop = timeit.default_timer()
		print("Search and decrypt time:" + "{}".format(stop - start))
		f = open('../data/result.txt', 'w')
		f.write(str1+"\n"+str2)
		f.close()

	else:
		print("Error: Invalid arguments")

main(sys.argv)