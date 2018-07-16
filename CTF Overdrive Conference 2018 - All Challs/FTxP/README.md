### FTxP - 90 Points
#### Find the FTxP box and manually craft an exploit for it's main service. Then look for the flag.txt file in the file-system.

##### Category: Hacking 
##### Solves: 5 

En este reto se nos daba una máquina (192.168.0.11) con diversos puertos abiertos, entre los que nos llamó la atención el puerto 21 (FTP), ya que fue posible acceder al servidor FTP con el usuario anonymous (user: anonymous, pass: anonymous) y se podía acceder a todo el contenido del sistema. Así que llegados a este punto tan solo faltaba encontrar el archivo “flag.txt”.

![ftp1](https://user-images.githubusercontent.com/38633962/42778211-a6f6a1b6-893c-11e8-9de4-d385ee4a6559.png)

Tras buscar por el sistema y directorios comunes (carpetas personales, de sistema, etc.) no se encontró nada relevante. Lo único que se identificó fue un acceso directo de Windows que apuntaba a “flag.txt”, pero parecía ser que era la ubicación antigua del archivo y que ahora se encontraba en otra ubicación, ya que ahora ya no estaba en “C:\Documents and Settings\UdG\Desktop\”.

![ftp2](https://user-images.githubusercontent.com/38633962/42778225-b4c6ec6a-893c-11e8-8fb7-188713cdb34e.png)

Durante la búsqueda se identificaron los archivos de instalación del servidor FTP (“Free Float FTP Server”) el cual contenía una vulnerabilidad de buffer overflow con exploit público que permitía la ejecución remota de código (https://www.rapid7.com/db/modules/exploit/windows/ftp/freefloatftp_user). Así que nos propusimos a explotar dicha vulnerabilidad utilizando el módulo de metasploit ya creado para ello (windows/ftp/freefloatftp_user).

Una vez explotada la vulnerabilidad, cargamos una sesión de meterpreter para localizar el archivo “flag.txt” con la función “search” (search -f file.txt) y descubrimos que el flag se encontraba en “C:\Windows\Help\flag,txt”, por lo que solo bastaba con mostrar su contenido y obtener el flag deseado:

![ftp3](https://user-images.githubusercontent.com/38633962/42778237-c08d05fc-893c-11e8-8772-5eee44f8591c.png)

![ftp4](https://user-images.githubusercontent.com/38633962/42778259-d0838d14-893c-11e8-8b51-5d264701b816.png)
