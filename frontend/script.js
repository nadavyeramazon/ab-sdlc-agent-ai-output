document.getElementById('greetingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const name = document.getElementById('nameInput').value;
    try {
        const response = await fetch(`http://localhost:8000/greet/${name}`);
        const data = await response.json();
        document.getElementById('greeting').textContent = data.message;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('greeting').textContent = 'An error occurred. Please try again.';
    }
});