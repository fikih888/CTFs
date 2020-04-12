### c0r0n4con CTF 2020

##### Challenge: Paperroling

##### Category: Stegano

##### Points: 50

##### Solves: 116/362

##### Description: Sometimes information is hidden in plain sight. Some other times, you will have to go get it.

En este reto se nos facilitaba un archivo .GIF ("paperrolling.gif") en el cual tras extraer cada frame (por ejemplo con "*convert paperrolling.gif frames.png*") podíamos ver el siguiente enlace a la wikipedia "https://es.wikipedia.org/wiki/COVID-19" en uno de ellos.

Por otro lado, al analizar el archivo con un editor hexadecimal, se observó que al final del mismo había un fichero ZIP concatenado con el fichero "flag.txt", así que se pasó "binwalk" para extraerlo:
```
binwalk --dd=".*" paperrolling.gif
```
Tras abrir el archivo ZIP, éste solicitaba contraseña, así que se creó un diccionario con el link de wikipedia para ver si el el pass era alguna palabra existente en el enlace que se había visto en el GIF. Para ello se utilizó la siguiente instrucción:
```
cewl -d 0 -w covid1.txt https://es.wikipedia.org/wiki/COVID-19
```
Tras obtener el diccionario, se utilizó "fcrackzip" para probar las palabras obtenidas y se pudo extrar el archivo con la contraseña "cuarentenas". 
```
fcrackzip -u -v -D -p "covid1.txt" zip1.zip
```
Obteniendo así el flag "flag{maXirolltopap3r}".

