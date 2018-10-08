### InCTF 2018

##### Challenge: WildCat

##### Category: Web

##### Points: 804

##### Solves: 22

##### Description: Your task is to read the flag containing file.




In this challenge we had a website with only a picture of a cat.

Analyzing the HTML code we saw “is_debug” commented, what give us a clue about what to do.

So after GETing the page again with the parameter “is_debug=1” we obtained the PHP source code:

```php
<?php
error_reporting(0);
include('flag.php');
$message = "<img src='cat.jpg' height=400><!-- is_debug -->";

if (isset($_GET['is_debug']))
{
	highlight_file(__FILE__) and die();
}
else
{
	$qs = $_SERVER['QUERY_STRING'];
	if(!(substr_count($qs, '_') > 0) && !(substr_count($qs, '%')> 1))
	{
	    $cmd = $_GET['c_m_d'];
	    if(!preg_match('/[a-z0-9]/is', $cmd)){
		system("/sandboxed_bin/".$cmd);
	    }else{
		echo $message;
		die();
	    }
	}
	echo $message;
	die();
}
?>
```

In this case, we see that we have a “system” call with the content of the parameter “c_m_d” but for landing on it we have to bypass some checks before. 

Concretely:
```php
$qs = $_SERVER['QUERY_STRING'];
if(!(substr_count($qs, '_') > 0) && !(substr_count($qs, '%')> 1))
```
and:

```php
$cmd = $_GET['c_m_d'];
if(!preg_match('/[a-z0-9]/is', $cmd)){
````


So, we cannot use any “_” in our query and we cannot use any “a-zA-Z0-9” values.

The firs step is to bypass the first check (no “_”). 

For this we can use the PHP functionality that converts “.” and spaces in “_”, using “c.m.d.” instead if “c_m_d”.

After that, we have to execute something to get the content of “flag.php” without using “ a-zA-Z0-9”.

In this case we can use some wildcards that are interpreted by bash to do what we need --> cat flag.php

As we cannot use letters, we use the character “?” to replace them.

In the first try, we tried “../../../../../../../../../../???/??? ????.???” for “../../../../../../../../../../bin/cat flag.php” but we did not get any result. As we where in a “sandboxed_bin”, we would have to use “??? ????.???” to match with “/sandboxed_bin/cat flag.php”.

So, putting all together, we created out request as “c.m.d=??? ????.???" and showed us the flag :)

![inctf2018_wildcat2](https://user-images.githubusercontent.com/38633962/46628916-6f91bb80-cb3f-11e8-8560-3a356c1677ae.png)




