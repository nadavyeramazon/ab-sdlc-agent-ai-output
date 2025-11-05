// Test backend connection
document.getElementById('testBackendBtn').addEventListener('click', async () => {
    const responseDiv = document.getElementById('backendResponse');
    responseDiv.textContent = 'Connecting to backend...';
    responseDiv.className = 'response show';
    
    try {
        const response = await fetch('/api/backend-data');
        const data = await response.json();
        
        if (data.success) {
            responseDiv.className = 'response show success';
            responseDiv.innerHTML = `
                <h3>✅ Connection Successful!</h3>
                <p><strong>Backend Message:</strong> ${data.backendResponse.message}</p>
                <p><strong>Backend Status:</strong> ${data.backendResponse.status}</p>
                <p><strong>Frontend Message:</strong> ${data.frontendMessage}</p>
            `;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        responseDiv.className = 'response show error';
        responseDiv.innerHTML = `
            <h3>❌ Connection Failed</h3>
            <p><strong>Error:</strong> ${error.message}</p>
            <p>Make sure both services are running via docker-compose.</p>
        `;
    }
});

// Get custom greeting
document.getElementById('getGreetingBtn').addEventListener('click', async () => {
    const nameInput = document.getElementById('nameInput');
    const responseDiv = document.getElementById('greetingResponse');
    const name = nameInput.value.trim() || 'World';
    
    responseDiv.textContent = 'Fetching greeting...';
    responseDiv.className = 'response show';
    
    try {
        const response = await fetch(`/api/greeting?name=${encodeURIComponent(name)}`);
        const data = await response.json();
        
        if (data.success) {
            responseDiv.className = 'response show success';
            responseDiv.innerHTML = `
                <h3>💬 ${data.data.greeting}</h3>
                <p><strong>From:</strong> ${data.data.from}</p>
            `;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        responseDiv.className = 'response show error';
        responseDiv.innerHTML = `
            <h3>❌ Error</h3>
            <p><strong>Error:</strong> ${error.message}</p>
        `;
    }
});

// Allow Enter key in name input
document.getElementById('nameInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('getGreetingBtn').click();
    }
});
