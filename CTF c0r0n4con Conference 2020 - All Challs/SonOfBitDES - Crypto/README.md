### c0r0n4con CTF 2020

##### Challenge: SonOfBitDES

##### Category: Crypto

##### Points: 250

##### Solves: 76/362

##### Description: We have found a hidden message in our old servers. It really seems old and broken.


En este reto se nos facilita el archivo cifrado "ciphertext.txt" y el código utilizado para cifrarlo "cipher.py".

En este código vemos que se utiliza DES-OFB con un vector IV fijo ("13371337"), así que podemos utilizar el siguiente script para obtener el texto en claro basandonos en las "Weak keys" de DES (https://en.wikipedia.org/wiki/Weak_key).

```python
from Crypto.Cipher import DES

IV = '13371337'

f = open('ciphertext', 'r')
ciphertext = f.read()
f.close()


KEY=b'\x00\x00\x00\x00\x00\x00\x00\x00'
a = DES.new(KEY, DES.MODE_OFB, IV)
plainkey1 = a.decrypt(ciphertext)
f = open("plainkey1", "w+")
f.write(plainkey1)
f.close()

KEY=b'\x1E\x1E\x1E\x1E\x0F\x0F\x0F\x0F'
a = DES.new(KEY, DES.MODE_OFB, IV)
plainkey2 = a.decrypt(ciphertext)
f = open("plainkey2", "w+")
f.write(plainkey2)
f.close()

KEY="\xE1\xE1\xE1\xE1\xF0\xF0\xF0\xF0"
a = DES.new(KEY, DES.MODE_OFB, IV)
plainkey3 = a.decrypt(ciphertext)
f = open("plainkey3", "w+")
f.write(plainkey3)
f.close()

KEY="\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
a = DES.new(KEY, DES.MODE_OFB, IV)
plainkey4 = a.decrypt(ciphertext)
f = open("plainkey4", "w+")
f.write(plainkey4)
f.close()
```

Tras ejecutarlo, vemos que con la clave 4 obtenemos un texto donde en el final aparece nuestra flag:
```
flag{The_Mentor_de_fresa}
```


