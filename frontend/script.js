document.addEventListener('DOMContentLoaded', () => {
    const nameInput = document.getElementById('nameInput');
    const greetButton = document.getElementById('greetButton');
    const greeting = document.getElementById('greeting');

    greetButton.addEventListener('click', async () => {
        const name = nameInput.value.trim();
        if (name) {
            try {
                const response = await fetch(`http://localhost:8000/greet/${name}`);
                const data = await response.json();
                greeting.textContent = data.message;
            } catch (error) {
                console.error('Error:', error);
                greeting.textContent = 'An error occurred while fetching the greeting.';
            }
        } else {
            greeting.textContent = 'Please enter a name.';
        }
    });
});
