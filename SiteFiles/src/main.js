
let start = '{"favColor":{"first":"green","second":"blue"},"favState":"Texas"}';

let myObject = JSON.parse(start);

console.log(myObject);

document.getElementById('display').innerHTML = myObject.favState;
document.getElementById('display2').innerHTML = myObject.favColor.first;