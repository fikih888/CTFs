### c0r0n4con CTF 2020

##### Challenge: Welcome

##### Category: Web - SanityFlag

##### Points: 1

##### Solves: 330/362

##### Description: Welcome to Fwhibbit CTF!

![sanity1](https://user-images.githubusercontent.com/38633962/79115906-64989680-7d87-11ea-9d14-a09dde37ba94.png)

En este reto teníamos una página web nos decía que teníamos que llegar a la función "welcome()" y nos mostraba su código fuente:
```php
 <!DOCTYPE HTML>
<?php
  require("flag.php");

  if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
  }

  if (isset($_GET['hole'])) {

    $rabbit = $_GET['hole'];
    $boomer = 'boomerrabbit';
    $holly = preg_replace(
            "/$boomer/", '', $rabbit);

    if ($holly === $boomer) {
      welcome();
    }
  }
?>

<html>
  <head>
    <title>Welcome</title>
  </head>
  <body>
    <h1>Welcome to Fwhibbit MiniCTF Quarantine Edition 2020</h1>
    <p>Try to reach <code>welcome()</code></p>
    <a target="_blank" href="?source">View source code</a>

  </body>
</html>
```

Tras analizar el código fuente, vemos que tenemos que pasar a la variable GET "hole" algo para que despúes de eliminar "boomerrabit" el resultado sea "boomerrabit".

Pasando por ejemplo "hole=boomerrboomerrabbitabbit", nos saltamos esta comprobación y se nos muestra el flag:
```
flag{welcome_b00mer_to_rabbit_hutch!}
```
