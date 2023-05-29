
//random number 1 -  3
var numero = Math.floor(Math.random() * 5) + 1;

//select a image box
var imagen = document.getElementById("img-index");

//set a image
imagen.src = "static/imgs/ninja" + numero + ".png";
