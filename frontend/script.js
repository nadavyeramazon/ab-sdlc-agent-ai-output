// Simple Frontend JavaScript - Item Manager
// This script handles interaction with the FastAPI backend

class ItemManager {
    constructor() {
        this.baseURL = 'http://localhost:8000/api';
        this.items = [];
        this.currentEditId = null;
        
        this.initializeElements();
        this.bindEvents();
        this.checkBackendConnection();
        this.loadItems();
    }

    initializeElements() {
        // Form elements
        this.addItemForm = document.getElementById('addItemForm');
        this.editItemForm = document.getElementById('editItemForm');
        
        // Input elements
        this.itemNameInput = document.getElementById('itemName');
        this.itemDescriptionInput = document.getElementById('itemDescription');
        this.editItemNameInput = document.getElementById('editItemName');
        this.editItemDescriptionInput = document.getElementById('editItemDescription');
        
        // Display elements
        this.itemsList = document.getElementById('itemsList');
        this.statusElement = document.getElementById('status');
        this.itemCountElement = document.getElementById('itemCount');
        
        // Buttons and controls
        this.refreshBtn = document.getElementById('refreshBtn');
        this.editModal = document.getElementById('editModal');
        this.closeModalBtn = document.querySelector('.close');
        this.cancelEditBtn = document.getElementById('cancelEdit');
    }

    bindEvents() {
        // Form submissions
        this.addItemForm.addEventListener('submit', (e) => this.handleAddItem(e));
        this.editItemForm.addEventListener('submit', (e) => this.handleEditItem(e));
        
        // Button clicks
        this.refreshBtn.addEventListener('click', () => this.loadItems());
        this.closeModalBtn.addEventListener('click', () => this.closeEditModal());
        this.cancelEditBtn.addEventListener('click', () => this.closeEditModal());
        
        // Modal outside click
        this.editModal.addEventListener('click', (e) => {
            if (e.target === this.editModal) {
                this.closeEditModal();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.editModal.style.display === 'block') {
                this.closeEditModal();
            }
        });
    }

    async checkBackendConnection() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api', '')}/health`);
            if (response.ok) {
                this.updateStatus(true, 'Connected to backend');
            } else {
                throw new Error('Backend not responding');
            }
        } catch (error) {
            this.updateStatus(false, 'Backend offline');
            console.error('Backend connection failed:', error);
        }
    }

    updateStatus(isOnline, message) {
        const statusText = this.statusElement.querySelector('.status-text');
        statusText.textContent = message;
        
        if (isOnline) {
            this.statusElement.className = 'status-indicator online';
        } else {
            this.statusElement.className = 'status-indicator offline';
        }
    }

    async loadItems() {
        try {
            this.showLoading();
            const response = await fetch(`${this.baseURL}/items`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.items = await response.json();
            this.renderItems();
            this.updateItemCount();
            
        } catch (error) {
            console.error('Error loading items:', error);
            this.showError('Failed to load items. Please check if the backend is running.');
        }
    }

    async handleAddItem(event) {
        event.preventDefault();
        
        const formData = new FormData(this.addItemForm);
        const itemData = {
            name: formData.get('name').trim(),
            description: formData.get('description').trim()
        };
        
        if (!itemData.name || !itemData.description) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.baseURL}/items`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const newItem = await response.json();
            this.items.push(newItem);
            this.renderItems();
            this.updateItemCount();
            this.addItemForm.reset();
            this.showNotification('Item added successfully!', 'success');
            
        } catch (error) {
            console.error('Error adding item:', error);
            this.showNotification('Failed to add item', 'error');
        }
    }

    async handleEditItem(event) {
        event.preventDefault();
        
        if (!this.currentEditId) return;
        
        const formData = new FormData(this.editItemForm);
        const itemData = {
            name: formData.get('name').trim(),
            description: formData.get('description').trim()
        };
        
        if (!itemData.name || !itemData.description) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.baseURL}/items/${this.currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const updatedItem = await response.json();
            const index = this.items.findIndex(item => item.id === this.currentEditId);
            if (index !== -1) {
                this.items[index] = updatedItem;
                this.renderItems();
            }
            
            this.closeEditModal();
            this.showNotification('Item updated successfully!', 'success');
            
        } catch (error) {
            console.error('Error updating item:', error);
            this.showNotification('Failed to update item', 'error');
        }
    }

    async deleteItem(itemId) {
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }
        
        try {
            const response = await fetch(`${this.baseURL}/items/${itemId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.items = this.items.filter(item => item.id !== itemId);
            this.renderItems();
            this.updateItemCount();
            this.showNotification('Item deleted successfully!', 'success');
            
        } catch (error) {
            console.error('Error deleting item:', error);
            this.showNotification('Failed to delete item', 'error');
        }
    }

    openEditModal(itemId) {
        const item = this.items.find(item => item.id === itemId);
        if (!item) return;
        
        this.currentEditId = itemId;
        this.editItemNameInput.value = item.name;
        this.editItemDescriptionInput.value = item.description;
        this.editModal.style.display = 'block';
        this.editItemNameInput.focus();
    }

    closeEditModal() {
        this.editModal.style.display = 'none';
        this.currentEditId = null;
        this.editItemForm.reset();
    }

    renderItems() {
        if (this.items.length === 0) {
            this.itemsList.innerHTML = `
                <div class="empty-state">
                    <h3>📋 No items found</h3>
                    <p>Add your first item using the form on the left!</p>
                </div>
            `;
            return;
        }
        
        const itemsHTML = this.items.map(item => `
            <div class="item-card">
                <div class="item-header">
                    <span class="item-title">${this.escapeHtml(item.name)}</span>
                    <span class="item-id">#${item.id}</span>
                </div>
                <div class="item-description">${this.escapeHtml(item.description)}</div>
                <div class="item-actions">
                    <button class="btn btn-edit" onclick="itemManager.openEditModal(${item.id})">
                        ✏️ Edit
                    </button>
                    <button class="btn btn-danger" onclick="itemManager.deleteItem(${item.id})">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `).join('');
        
        this.itemsList.innerHTML = itemsHTML;
    }

    updateItemCount() {
        const count = this.items.length;
        this.itemCountElement.textContent = `${count} item${count !== 1 ? 's' : ''}`;
    }

    showLoading() {
        this.itemsList.innerHTML = '<div class="loading">🔄 Loading items...</div>';
    }

    showError(message) {
        this.itemsList.innerHTML = `
            <div class="empty-state" style="border-color: #f44336; background-color: #ffebee;">
                <h3>❌ Error</h3>
                <p>${message}</p>
                <button class="btn btn-secondary" onclick="itemManager.loadItems()">🔄 Retry</button>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">&times;</button>
        `;
        
        // Add styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 20px;
                    border-radius: 8px;
                    color: white;
                    font-weight: 600;
                    z-index: 1001;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    animation: slideInRight 0.3s ease-out;
                    max-width: 400px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                }
                .notification-success { background-color: #4caf50; }
                .notification-error { background-color: #f44336; }
                .notification-info { background-color: #2196f3; }
                .notification button {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 3000);
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.itemManager = new ItemManager();
});

// Handle page visibility changes to check connection
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.itemManager) {
        window.itemManager.checkBackendConnection();
    }
});
