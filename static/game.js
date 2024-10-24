document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('map');
    const phaseInfoElement = document.getElementById('phase-info');
    const nextPhaseButton = document.getElementById('next-phase-btn');

    // Function to update the game UI
    function updateGameUI(gameState) {
        mapElement.innerHTML = '';  // Clear the map
        Object.values(gameState.world.countries).forEach(country => {
            const countryElement = document.createElement('div');
            countryElement.classList.add('country');
            countryElement.style.width = '50px';
            countryElement.style.height = '50px';
            countryElement.style.left = `${country.center.x}px`;
            countryElement.style.top = `${country.center.y}px`;
            countryElement.style.backgroundColor = `rgb(${country.color[0]}, ${country.color[1]}, ${country.color[2]})`;
            countryElement.textContent = country.units;
            mapElement.appendChild(countryElement);

            // Handle country click (for placing units, moving, attacking)
            countryElement.addEventListener('click', () => {
                handleCountryClick(country.name);
            });
        });

        // Update the phase information using drawText
        phaseInfoElement.innerHTML = ''; // Clear the phase info
        drawText('phase-info', `Current Phase: ${gameState.phase}`, 'black', 10, 10, false, 24);
    }

    // Function to render single-line text
    function drawText(containerId, text, color, x, y, center = false, size = 20) {
        const container = document.getElementById(containerId);
        const textElement = document.createElement('span');
        textElement.style.position = 'absolute';
        textElement.style.color = color;
        textElement.style.fontSize = `${size}px`;
        textElement.style.whiteSpace = 'nowrap';  // Prevent text from wrapping
        textElement.textContent = text;

        // Position the text element
        if (center) {
            textElement.style.transform = 'translate(-50%, -50%)';  // Center both horizontally and vertically
            textElement.style.left = `${x}px`;
            textElement.style.top = `${y}px`;
        } else {
            textElement.style.left = `${x}px`;
            textElement.style.top = `${y}px`;
        }

        container.appendChild(textElement);  // Append the text to the container
    }

    // Function to render multi-line text
    function drawMultilineText(containerId, textLines, color, x, y, center = false, size = 20) {
        const container = document.getElementById(containerId);
        textLines.forEach((line, index) => {
            const lineElement = document.createElement('span');
            lineElement.style.position = 'absolute';
            lineElement.style.color = color;
            lineElement.style.fontSize = `${size}px`;
            lineElement.textContent = line;

            const lineHeight = size + 5;  // Set line height with padding
            if (center) {
                lineElement.style.transform = 'translate(-50%, -50%)';
                lineElement.style.left = `${x}px`;
                lineElement.style.top = `${y + index * lineHeight}px`;  // Position each line below the previous one
            } else {
                lineElement.style.left = `${x}px`;
                lineElement.style.top = `${y + index * lineHeight}px`;
            }

            container.appendChild(lineElement);
        });
    }

    // Fetch the game state from the Flask API
    function fetchGameState() {
        fetch('/api/game')
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Log the game state data to ensure it's loading
                updateGameUI(data);
            });    
    }

    // Handle placing units (or other interactions based on phase)
    function handleCountryClick(countryName) {
        const units = parseInt(prompt('Enter units to place:'), 10);
        fetch('/api/player/place_units', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ country: countryName, units: units }),
        }).then(() => fetchGameState());
    }

    // Handle next phase button click
    nextPhaseButton.addEventListener('click', () => {
        fetch('/api/game/next_phase', {
            method: 'POST'
        }).then(() => fetchGameState());
    });

    // Initial fetch of the game state
    fetchGameState();
});
