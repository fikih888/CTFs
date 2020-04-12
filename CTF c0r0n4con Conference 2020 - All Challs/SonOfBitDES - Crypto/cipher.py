from Crypto.Cipher import DES

def do_encrypt():
	keyfile = raw_input("Enter key file: ")
	f = open(keyfile, 'r')
	key_hex = f.readline() # discard newline
	f.close()

	KEY = key_hex.decode("hex")

	# I can't be entering this all day xD
	#ivfile = raw_input("Enter IV file: ")
	#i = open(ivfile, 'r')
	#IV = i.readline()
	#i.close()
	IV = "13371337"

	a = DES.new(KEY, DES.MODE_OFB, IV)

	plainfile = raw_input("Enter plain text file: ")
	p = open(plainfile, 'r')
	plaintext = p.read()
	p.close()

	ciphertext = a.encrypt(plaintext)

	cipherfile = raw_input("Enter cipher output file: ")
	c = open(cipherfile, 'w')
	c.write(ciphertext)
	c.close()

if __name__ == '__main__':
	do_encrypt()
