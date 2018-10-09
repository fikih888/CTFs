### InCTF 2018

##### Challenge: Evilcrypter

##### Category: Forensics / Stegano

##### Points: 996

##### Solves: 4/306

##### Description: A harmful ransomware script encrypted my precious text and hid it somewhere. I was going through some old photos when this incident happened. Luckily I was able to dump the memory as soon as I noticed something suspicious. Can you retrieve my data?

In this challenge we received a memory dump and had to find the flag within it.

Analyzing the dump with volatily (“*volatility imageinfo -f challenge.data*”) we identified that it came from a Windows 7 32 bits, so we used the profile “Win7SP0x86”for further analysis.

Playing a bit, we identified that the main user was “hello”, that “notepad.exe” was running at that time with the files “vip.txt” and “evilscript.py” (thanks to “*volatility --profile=Win7SP0x86 -f challenge.data dlllist*”) and also that the user had an image file called “suspision1.jpg” on his desktop (“*volatility --profile=Win7SP0x86 -f challenge.data filescan*”). 

![evilcrypter1](https://user-images.githubusercontent.com/38633962/46692797-76383580-cc08-11e8-92e8-aa271fbd9dd1.png)

We extracted them with “*volatility --profile=Win7SP0x86 -f challenge.data dumpfile -D ./ -Q 0x3e727e50*”, “*volatility --profile=Win7SP0x86 -f challenge.data dumpfile -D ./ -Q 0x3de1b5f0*” and “*volatility --profile=Win7SP0x86 -f challenge.data dumpfile -D ./ -Q 0x0x04f34148*”.

The python script was the following:

```python
import sys
import string

def xor(s):
	a = ''.join(chr(ord(i)^3) for i in s)
	return a

def encoder(x):

	return x.encode("base64")

if __name__ == "__main__":
	f = open("C:\\Users\\hello\\Desktop\\vip.txt", "w")
	arr = sys.argv[1]
	arr = encoder(xor(arr))
	f.write(arr)
	f.close()
```

This code made some XOR operations and encoded the result with base64 from a string and saved the result on the file “vip.txt”. So our next step was to obtain the string of “vip.txt” and reverse the process using the the same XOR function and decoding the base64.

The result of this was the string “inctf{0n3_h4lf”, what seemed to be the first part of the flag. So we still needed to find the second one.

After long time trying different things and some stego techniques on the “suspision1.jpg” file, we ended up getting the second part of the flag (“_1s_n0t_3n0ugh}”) using “steghide” over the image and using the first part of the flag as a password.

So, concatenating both parts we obtained the complete flag:

```
inctf{0n3_h4lf_1s_n0t_3n0ugh} 
```


