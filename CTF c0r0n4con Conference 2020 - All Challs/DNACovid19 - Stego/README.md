### c0r0n4con CTF 2020

##### Challenge: DNACovid19

##### Category: Stego

##### Points: 100

##### Solves: 68/362

##### Description: We have found a misterious message inside our biological lab server. Could it contain a cure?

En este reto se nos da la imagen "seqfragment.jpg", que contiene una cadena con las letras "ACGT".

A través del nombre del reto y debido a que únicamente se usan las letras "A", "G", "C" y "T" puede ser que se trate de una codificación utilizando cadenas de ADN.

Buscando tipos de codifaciones existentes (de las muchas que hay en papers y estudios), vimos que la siguiente codificación nos devuelve algo con sentido:

![stego_100_dna_codes](https://user-images.githubusercontent.com/38633962/79077595-29ed1a80-7d03-11ea-8f1e-74a127c7a34c.png)

Concretamente nos devuelve el string:
```
GY3DMYZWGE3DON3CGRSDONJVGI3DGNBZGY2TIYZWGE2DOMZQGVTDOMBUGE3GKNBXGZTDIYZTGE3GKN3E
```
El cual, haciendo un base32 del mismo y convirtiendo el resultado ("666c61677b4d75526349654c6147305f70416e476f4c316e7d") de hex a ASCII, nos devuelve el flag:
```
flag{MuRcIeLaG0_pAnGoL1n}
```

