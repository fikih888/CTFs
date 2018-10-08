### InCTF 2018

##### Challenge: Biz44re

##### Category: Stego / Forensics

##### Points: 856

##### Solves: 19

##### Description: Kevin sent me a file with some hidden message. Help me recover this secret from this bizzare network.



In this challenge received a pcap file (“bizz.pcap”) and had to find the flag in it.

After analyzing the capture, we saw strange bytes after some ICMP packets.

![inctf2018_bizarre2](https://user-images.githubusercontent.com/38633962/46627259-2b4fec80-cb3a-11e8-91f5-3449d076a68e.png)

Extracting these values and concatenating all together as HEX values we got a zip file with a PNG file on it showing the flag: inctf{_s0meTim3s_u_h4v3_t0_lOOk_3v3ryWh3r3_cl0s3r_T0_G3T_th3_wh0l3!}

![inctf2018_bizarre3](https://user-images.githubusercontent.com/38633962/46627285-415dad00-cb3a-11e8-905a-442687194d09.png)

