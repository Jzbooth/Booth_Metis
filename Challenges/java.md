### Make a function that adds 3 to any input.

function addthree(x) { return x + 3; }

### Make a function that divides any input by three.

function divthree(x) {return x/3; }

### Make a function that takes an array and returns an array with only those elements that are less than 4.

function less4(ar) {return ar.filter( function(x) {return x < 4;});};

### Make a function that takes an array of numbers and returns their sum. (Google "reduce")

function sumarray(ar) {return ar.reduce(function(total, num) {return total + num;} ); };
