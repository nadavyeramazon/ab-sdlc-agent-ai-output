document.addEventListener('DOMContentLoaded', () => {
    const fetchButton = document.getElementById('fetchButton');
    const responseBox = document.getElementById('response');

    fetchButton.addEventListener('click', async () => {
        responseBox.innerHTML = '<div style="color: #ffd93d;">⏳ Fetching data from backend...</div>';
        fetchButton.disabled = true;

        try {
            const response = await fetch('/api/message');
            const data = await response.json();

            if (response.ok) {
                responseBox.innerHTML = `
                    <div class="success">✅ Successfully communicated with backend!</div>
                    <br>
                    <strong>Frontend Message:</strong>
                    <div>${data.frontend}</div>
                    <br>
                    <strong>Backend Response:</strong>
                    <div>${JSON.stringify(data.backend, null, 2)}</div>
                    <br>
                    <strong>Timestamp:</strong> ${data.timestamp}
                `;
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        } catch (error) {
            responseBox.innerHTML = `
                <div class="error">❌ Error: ${error.message}</div>
                <br>
                <div>Make sure both services are running with Docker Compose.</div>
            `;
        } finally {
            fetchButton.disabled = false;
        }
    });

    // Display initial message
    responseBox.innerHTML = '<div style="color: #e1bee7;">👆 Click the button above to fetch data from the backend service!</div>';
});
