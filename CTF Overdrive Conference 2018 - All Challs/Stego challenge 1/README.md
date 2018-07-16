### Stego challenge #1 - 60 Points
#### Pepe is back! Discover the secret he is trying to hide.

##### Category: Stego 
##### Solves: 7 

Tras abrir la imagen que se nos daba en el reto con un editor hexadecimal, fue posible ver que contenía datos después del EOF del formato JPG (valores “0xFFD9”). Concretamente se podía observar un string en formato base64 (“MV9jR1BMTzhkb3M=”) y un archivo ZIP.

![stego1_hex1](https://user-images.githubusercontent.com/38633962/42777533-acbc3c5c-893a-11e8-8b68-a7b13dd1f712.png)

Una vez extraído el archivo ZIP con “binwalk” (por ejemplo), se solicitaba una contraseña para poder abrirlo, por lo que decidimos investigar un poco sobre el string identificado anteriormente (ya que muy posiblemente tendría algo que ver con la contraseña).

El string en base64 se correspondía a “1_cGPLO8dos”, y tras buscarlo en google, nos dirigió al siguiente vídeo de Youtube “https://www.youtube.com/watch?v=1_cGPLO8dos”, cuyo título es “Frogs - The Thin Green Line (Documentary Full Length)”. Así que tras probar la palabra “frogs” como contraseña, fue posible abrir el ZIP y acceder al archivo “3.txt” que había en su interior, el cual contenía la cadena “iodj{s3s3_1v_vw1oo_4o1y3}”.

![stego1_zip1](https://user-images.githubusercontent.com/38633962/42777564-c0b0a266-893a-11e8-8a8f-40de5569e05a.png)

Puesto que el formato del flag esperado era “flag{...}”, se observó rápidamente que se había utilizado el cifrado Cesar para cifrarlo (utilizando un desplazamiento de 3). Así que haciendo la conversión se obtenía el flag de este reto:

      iodj{s3s3_1v_vw1oo_4o1y3} → flag{p3p3_1s_st1ll_4l1v3}
