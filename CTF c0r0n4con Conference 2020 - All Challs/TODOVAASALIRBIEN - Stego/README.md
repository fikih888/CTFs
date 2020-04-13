### c0r0n4CON CTF 2020

##### Challenge: TODOVAASALIRBIEN

##### Category: Stegano

##### Points: 100

##### Solves: 148/362

##### Description: Everything will be OK, really. The rainbow told me!

En este reto se nos da el PDF "EL-4RCOIRIS-TODO-VA-A-SALIR-BIEN-.pdf" y abriéndolo con un visor vemos que tiene un archivo adjunto llamado "sin_barreras.txt".

Este archivo contiene un base64 que al decodificarlo nos devuelve una imagen en PNG que contiene el siguiente código de barras:

![stego100_2_barcode](https://user-images.githubusercontent.com/38633962/79116137-f6a09f00-7d87-11ea-89f0-e36593dd5fe5.png)

Decodificando este código (utilizando por ejemplo https://online-barcode-reader.inliteresearch.com") obtenemos el flag:
```
flag{r3sistir3_abril}
```

