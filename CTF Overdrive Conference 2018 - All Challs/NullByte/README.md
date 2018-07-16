### NullByte - 130 Points
#### Come one guys, y'all already know this, we do this every f*cking year. (proof.txt)

##### Category: Hacking 
##### Solves: 8 

Esta máquina consistía en una máquina virtual vulnerable conocida que puede descargarse de “http://ly0n.me/nullbyte/NullByte.ova.zip”.

Puesto que en Internet hay varios writeups para conseguir el flag en esta máquina, he decidido hacer algo diferente para conseguirlo. En este caso, al tratarse de una maquina virtual que descargamos en nuestro equipo, simularemos que tenemos acceso físico a dicho sistema para su explotación.

Una de las configuraciones que existen en algunos sistemas linux, y que quizás mucha gente no es consciente, es la de modificación del arranque del sistema (GRUB), la cual puede permitir arrancar un equipo linux como root sin necesidad de introducir contraseña, así que a ello vamos:

Una vez arrancamos la máquina, en el menu del GRUB pulsaremos “e” para ir a la edición del mismo y añadiremos “init /bin/bash” en la línea de arranque del kernel deseado:

![null1](https://user-images.githubusercontent.com/38633962/42778365-24a06e1c-893d-11e8-9f7d-81b1fd9c89ff.png)

Tras esta modificación, presionaremos F10 para continuar con el arranque y obtendremos una shell con el usuario root :)

![null2](https://user-images.githubusercontent.com/38633962/42778408-45812036-893d-11e8-8032-09b8041338d7.png)

En este punto, únicamente nos queda mostrar el archivo “proof.txt” para obtener el flag:

![null3](https://user-images.githubusercontent.com/38633962/42778431-53f5d8f0-893d-11e8-819f-fa5299e6c1ff.png)
