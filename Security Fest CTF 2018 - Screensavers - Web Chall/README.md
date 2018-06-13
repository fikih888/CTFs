### Security Fest CTF 2018

##### Challenge: Screensavers

##### Category: Web



In this challenge we had a web application that was able to create and download screensavers after login into the application.

In the “robots.txt” file, we identified the file “admin” but when we tried to access to it, we received a message saying that our IP was not allowed to see this file. So, we had to find a way to access to it “locally”.

After some time playing with the application, we identified a “File Inclusion Vuln” in the parameter “url” of the resource “/download”, but the access to “http://localhost:2999/admin” and the string “../” was filtered, so we had to bypass it with “ http://localhost:2999/user/.%0a./admin” to be able to see the flag: SCTF{y00_kn0w_KuNg_Fu!!!}


![securityfestctf2018_post1](https://user-images.githubusercontent.com/38633962/41380635-e77352ac-6f65-11e8-84ef-b559902f1240.png)
![securityfestctf2018_flag1](https://user-images.githubusercontent.com/38633962/41380753-3f8ee424-6f66-11e8-91f6-37191eb116ea.png)
