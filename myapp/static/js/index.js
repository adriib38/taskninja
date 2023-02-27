
//numero random del 1 al 3
var numero = Math.floor(Math.random() * 5) + 1;

//selecciona la imagen
var imagen = document.getElementById("img-index");

//cambia la imagen
imagen.src = "static/imgs/ninja" + numero + ".png";
