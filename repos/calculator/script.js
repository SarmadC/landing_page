function add(a,b){
    return a + b;
}

function subtract(a,b){
    return a - b;
}

function multiply(a,b){
    return a * b;
}

function divide(a,b){
    return a / b;
}

let firstValue = '';
let operator = '';
let secondValue = '';

function operate(firstValue, secondValue, operator){
    firstValue = parseFloat(firstValue);
    secondValue = parseFloat(secondValue);
    switch(operator){
        case '+':
            return add(firstValue, secondValue);
        case '-':
            return subtract(firstValue, secondValue);
        case '*':
            return multiply(firstValue, secondValue);
        case '/':
            return divide(firstValue, secondValue);
    }
}t display = '123' 

le

