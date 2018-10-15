### InCTF 2018

##### Challenge: Mag1cal Radio

##### Category: Stegano

##### Points: 1000

##### Solves: 1/306

##### Description: A number station in Russia broadcasted a series of encoded messages to one of it's intelligence agency. We have been able to get a piece of that message along with a picture hidden by one of the spy. Decode the transmitted data and be a hero!!
Link : https://goo.gl/JQTKXA



In this challenge we had a PNG file of 40,8MB (“index.png”) and an audio file (“new.mp3”).


Opening the mp3 file with audacity we realize that it was a message transmitted in Morse.

![magical1](https://user-images.githubusercontent.com/38633962/46976829-cad92600-d0ca-11e8-8114-ae20a34e4aa7.png)

After decode it, we got the following message:

```
FLAGISNOTH3R3
```

So we had to find the flag in other place...


After playing a bit with both files, we detected the numbers “1517” in the LSB colors of the image "index.png":

![magical2](https://user-images.githubusercontent.com/38633962/46976845-d4628e00-d0ca-11e8-931c-8511d613d328.jpeg)

Here we were stuck a long time, trying different things with no success, until that, thanks to the name of the challenge, we found a stego tool called “StegoMagic” (https://tech2copycat.wordpress.com/2012/02/06/how-to-hide-data-in-image-audio-video-files-steganography/#more-30).

After using “StegoMagic_BIN.exe” over the mp3 file with the password “1517” we extracted a PNG file with a QR code:

![magical3](https://user-images.githubusercontent.com/38633962/46976855-dc223280-d0ca-11e8-9508-ffd2cd53d664.png)

This QR Code gave us the URL “http://qrs.ly/ai7bsyn” whose content was:
```
Ob>(FfBIDELM1nJQ56TtP:XxTU\]^YZ"\cdefgK*dkfg/iSkr4nXp8rsz{|w~!zB|%&hG#*%&-op0P,-4/w189Y5}=]9@;<C'?eAHIJKFGmIPKLSTUPQXS=zV]X_ZaE$^H`gh*delmniS2lVn6pqxyt^|>x!"{|%g'(H$l,-M)*+2t4T078zY5<=8"@ABb>EFG+hDKLGH23pLMTUVQwSZ[\@^~Z[bcde`gK*dklgnipT3mtupwxy]<v}~!"#eD~!"j*+K'./01stS/67834|[78?:A%b>EF*BIJjFM1nJ45STtPWXYT[VW^B`"\]d_I(bcjkfP/ijkrm5ovwxyt{=w~yz#$fE!()*+m'M)*+,R./0723{5[7>?@AB='d@GBC-ELlHO34qM7UVWXxT[\]A~Z[\cdefJK*dklgnipT3mtuYqx])^OP>!d{$VE4F6l%nLo<O+,@v5gV89|Y<!K9_;`'D 
```

After losing a huge amount of time with this string, we guessed that it was a reversed string of a  “Malbolge” program, an esoteric programming language...  (http://www.malbolge.doleczek.pl/)

After reversing the string and running the program we got the flag:

![magical4](https://user-images.githubusercontent.com/38633962/46976863-e5130400-d0ca-11e8-8bc5-b9659041b631.png)

```
inctf{M1xiNg_uP_4udio_Qr_4nD_A_W3ird_L4ngu4ge_1s_So_L0vely}
```

Note: During the CTF we run out of time and got the flag 20 minutes after its ending, so we could not get the 1000 points for the chall... :( 
