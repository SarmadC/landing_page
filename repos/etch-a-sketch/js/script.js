const mainContainer = document.createElement('div');
mainContainer.classList.add("main-container");
document.body.appendChild(mainContainer);


const container = document.createElement("div");
container.classList.add("container");

mainContainer.appendChild(container);

const button = document.getElementById("btn")
button.addEventListener("click", () => {
    gridSize();
})

function rgb(){
    return `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
}

function darken(squareDiv) {
    let currentOpacity = parseFloat(squareDiv.getAttribute('data-opacity'));

    if (currentOpacity > 0) {
        currentOpacity -= 0.1;
        squareDiv.style.opacity = currentOpacity;
        squareDiv.setAttribute('data-opacity', currentOpacity);
    }
}

function gridSize(){
    container.textContent = "";
    const size = prompt("Select grid size");


    if (size <= 100){
        // Set both width and height dynamically
        const gridWidth = size * 25;
        container.style.width = `${gridWidth}px`;
        container.style.height = `${gridWidth}px`;

        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const squareDiv = document.createElement("div");
                squareDiv.classList.add("square");
                container.appendChild(squareDiv);

                squareDiv.setAttribute('data-opacity', 1.0)

                squareDiv.addEventListener("mouseover", () => {
                    squareDiv.style.opacity = darken(squareDiv);
                    squareDiv.style.backgroundColor = rgb();
                });

            }
        }
    }
    else{
        alert("Please enter a valid size less than 100");
    }
}