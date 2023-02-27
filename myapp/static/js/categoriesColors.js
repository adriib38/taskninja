const backgroundColors = [
    '#FFB3BA',
    '#FFDFBA',
    '#FFFFBA',
    '#BAFFC9',
    '#BAE1FF',
    '#D0BAFF',
    '#FFB3F4',
];

let categories = document.querySelectorAll('.task-category');
let nameCategories = [];
categories.forEach(category => {
    nameCategories.push(category.innerHTML);
});

categories.forEach(category => {
    let firstLetter = category.innerHTML[0];
    
    //Asignar un color a cada categoria segun la primera letra
    let color = backgroundColors[firstLetter.charCodeAt(0) % backgroundColors.length];
    category.style.backgroundColor = color;
});
