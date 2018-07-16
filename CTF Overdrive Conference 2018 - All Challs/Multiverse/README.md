### multiverse - 140 Points
#### Look for the multiverse box in the network. Get root. Cat flag.txt

##### Category: Hacking + Exploiting
##### Solves: 1

Tras realizar un escaneo de puertos en esta máquina (191.168.0.12), nos centramos en la aplicación web que había tras el puerto 80 y lanzamos dirb para identificar potenciales directorios y archivos que pudieran aportarnos información para ampliar nuestros vectores de ataque.

Gracias a dirb, identificamos la aplicación “Gallarific” (ubicada en “/gallery/gallery/”), la cual es una aplicación que te permite subir fotos a la web para poder visualizarlas posteriormente.

Tras navegar por la aplicación e identificar las distintas funcionalidades de la misma, se identificó que la aplicación era vulnerable a SQL injection en el parámetreo “id” del recurso “gallery.php” (https://www.exploit-db.com/exploits/15891/). Así que tras su explotación se consiguieron las credenciales de acceso a la misma (admin/g2c7t0z7) como administrador con la petición:

http://191.168.0.12/gallery/gallery/gallery.php?id=null+and+1=2+union+select+1,(select+group_concat(userid,0x3A,username,0x3A,password),3,4,5,6+from+gallarific_users--

Una vez se consiguió acceso a la aplicación como usuario autenticado, se intentó obtener una shell o ejecución remota de comandos a través de la subida de imágenes y a través del propio SQLi, pero no hubo éxito. Así que tras analizar las distintas bases de datos que existían en el servidor SQL (y que nuestro usuario tenía acceso) se identificaron la base de datos “information_schema”, “mysql”, “os”, “performance_schema”, “sf” y “users”:

![multiverse_sqli1](https://user-images.githubusercontent.com/38633962/42779400-9d01a18e-8940-11e8-80c1-ac81b1e20653.png)

Analizando el contenido de la base de datos “users” vimos que contenía una tabla llamada “admins” con las columnas “id”, “user” y “pass”, así que nos propusimos obtener su contenido:

![multiverse_sqli2](https://user-images.githubusercontent.com/38633962/42779424-b0310ff6-8940-11e8-9164-39da6cffde32.png)

Obteniendo así un usuario llamado “juan” y un hash MD5 de su contraseña, el cual se correspondía a la palabra “elite”.

![multiverse_hash1](https://user-images.githubusercontent.com/38633962/42779468-d212eb1c-8940-11e8-9a5c-3c752e123ec6.png)

Con estas credenciales fue posible acceder al sistema a través de SSH y conseguir una shell en la máquina, eso sí, sin privilegios de administrador. Por lo que aún nos quedaría escalar privilegios para conseguir el flag.

![multiverse_ssh1](https://user-images.githubusercontent.com/38633962/42779495-ea314a7c-8940-11e8-8c78-ff04e50d9535.png)

Tras analizar el sistema para intentar escalar privilegios, se observó que era muy posible que el exploit utilizado en “Ubuntu Goat” funcionase, así que siguiendo el mismo procedimiento (compilando todo en local para un sistema de 32 bits y subiendo los archivos necesarios al servidor) se consiguió explotar la vulnerabilidad de overlayfs, convertirnos en root y obtener el flag :)

![multiverse_root1](https://user-images.githubusercontent.com/38633962/42779515-f9717cdc-8940-11e8-8367-7d6837bb52a3.png)
