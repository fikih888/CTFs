### InCTF 2018

##### Challenge: Winter Sport

##### Category: Stegano

##### Points: 996

##### Solves: 4/306

##### Description: I have a friend named Jake.We were watching a football tournament on one fine chilly morning. Meanwhile Jake's sister Susan did something mischievous which cause Jake to lose some really important data. We could only find this piece of evidence, can you recover it for him?

In this challenge we only had a PDF file with the sentence “Welcome to inctf. Hope you solve this challenge the fastest.”

After opening it with “*peepdf*” to analyze it, we saw an embedded file in the stream 8, so we decided to extract it with “*rawstream 8 > omg.7z*”

![winter0](https://user-images.githubusercontent.com/38633962/46700460-3760aa80-cc1d-11e8-9e48-3636ff81c3eb.png) 

Once it was extracted, we identified it as a “7z” file with another PDF file inside called "omg.pdf”.

This PDF showed different things depending which PDF viewer was used. In one we had white letters over a white background and in other we had different symbols in black.

![winter2](https://user-images.githubusercontent.com/38633962/46700495-45aec680-cc1d-11e8-922c-fc72008bbd55.png)

![winter1](https://user-images.githubusercontent.com/38633962/46700517-4e9f9800-cc1d-11e8-8011-63276485ed50.png)


When we converted the pdf to txt with “*pdftotext omg.pdf omg.txt*”, we obtained the next text:

```
What	is	Steganography	?Steganography	is	an	amaz	?S
g
```

After analyzing this PDF with *peepdf*, we did not detected anything special excepting the use of spaces of different length between some of the words and data.


![winter3](https://user-images.githubusercontent.com/38633962/46700664-b950d380-cc1d-11e8-9382-f10c32b0fae3.png)

With this in mind, we decided to use “SNOW”, a stegano tool for text files that uses spaces to hide the information (http://www.darkside.com.au/snow/).

In this case, we run “*snow.exe -C omg.pdf outfile.txt*” and obtainted a txt file with the flag:
```
inctf{w3lcom3_t0_7h3_w0rld_0f_whit3sp4c3}
```

