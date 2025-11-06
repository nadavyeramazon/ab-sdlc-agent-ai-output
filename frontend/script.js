const API_BASE_URL = 'http://localhost:8000';

// Utility functions for input validation
const validation = {
    validateName: (name) => {
        const errors = [];
        if (!name || name.trim().length === 0) {
            errors.push('Name is required');
        }
        if (name && name.length > 100) {
            errors.push('Name cannot exceed 100 characters');
        }
        if (name && /[<>"'\/]/.test(name)) {
            errors.push('Name contains invalid characters');
        }
        return errors;
    },
    
    validateDescription: (description) => {
        const errors = [];
        if (description && description.length > 500) {
            errors.push('Description cannot exceed 500 characters');
        }
        return errors;
    },
    
    validatePrice: (price) => {
        const errors = [];
        const numPrice = parseFloat(price);
        if (isNaN(numPrice)) {
            errors.push('Price must be a valid number');
        }
        if (numPrice < 0) {
            errors.push('Price cannot be negative');
        }
        if (numPrice > 999999.99) {
            errors.push('Price cannot exceed 999,999.99');
        }
        return errors;
    },
    
    validateCategory: (category) => {
        const errors = [];
        const allowedCategories = ['electronics', 'clothing', 'food', 'books', 'home', 'sports', 'other'];
        if (!category || !allowedCategories.includes(category.toLowerCase())) {
            errors.push('Please select a valid category');
        }
        return errors;
    }
};

// Error handling utility
class ErrorHandler {
    static showError(message, container = null) {
        console.error('Error:', message);
        
        // Remove existing error messages
        const existingErrors = document.querySelectorAll('.error-message');
        existingErrors.forEach(error => error.remove());
        
        // Create and show error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <div class="alert alert-error">
                <span class="error-icon">⚠️</span>
                <span class="error-text">${message}</span>
                <button class="close-error" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
        `;
        
        if (container) {
            container.insertBefore(errorDiv, container.firstChild);
        } else {
            document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.container').firstChild);
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
    
    static showSuccess(message, container = null) {
        console.log('Success:', message);
        
        // Remove existing success messages
        const existingSuccess = document.querySelectorAll('.success-message');
        existingSuccess.forEach(success => success.remove());
        
        // Create and show success message
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <div class="alert alert-success">
                <span class="success-icon">✅</span>
                <span class="success-text">${message}</span>
                <button class="close-success" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
        `;
        
        if (container) {
            container.insertBefore(successDiv, container.firstChild);
        } else {
            document.querySelector('.container').insertBefore(successDiv, document.querySelector('.container').firstChild);
        }
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 3000);
    }
    
    static handleApiError(error, operation) {
        let message = `Failed to ${operation}`;
        
        if (error.response) {
            // Server responded with error status
            const status = error.response.status;
            const data = error.response.data;
            
            if (status === 422 && data.detail) {
                // Validation error
                if (Array.isArray(data.detail)) {
                    const errors = data.detail.map(err => err.msg || err.message || 'Validation error').join(', ');
                    message = `Validation error: ${errors}`;
                } else {
                    message = `Validation error: ${data.detail}`;
                }
            } else if (status === 404) {
                message = data.detail || 'Item not found';
            } else if (status === 400) {
                message = data.detail || 'Bad request';
            } else if (status >= 500) {
                message = 'Server error. Please try again later.';
            } else {
                message = data.detail || `Failed to ${operation}`;
            }
        } else if (error.request) {
            // Network error
            message = 'Network error. Please check your connection and try again.';
        } else {
            // Other error
            message = error.message || `Failed to ${operation}`;
        }
        
        this.showError(message);
    }
}

// API functions with improved error handling
const api = {
    async fetchItems() {
        try {
            const response = await fetch(`${API_BASE_URL}/items`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            ErrorHandler.handleApiError(error, 'load items');
            throw error;
        }
    },
    
    async fetchItem(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/items/${id}`);
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Item not found');
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            ErrorHandler.handleApiError(error, 'load item');
            throw error;
        }
    },
    
    async createItem(itemData) {
        try {
            const response = await fetch(`${API_BASE_URL}/items`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData)
            });
            
            const responseData = await response.json();
            
            if (!response.ok) {
                const error = new Error('Create failed');
                error.response = { status: response.status, data: responseData };
                throw error;
            }
            
            return responseData;
        } catch (error) {
            ErrorHandler.handleApiError(error, 'create item');
            throw error;
        }
    },
    
    async updateItem(id, itemData) {
        try {
            const response = await fetch(`${API_BASE_URL}/items/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(itemData)
            });
            
            const responseData = await response.json();
            
            if (!response.ok) {
                const error = new Error('Update failed');
                error.response = { status: response.status, data: responseData };
                throw error;
            }
            
            return responseData;
        } catch (error) {
            ErrorHandler.handleApiError(error, 'update item');
            throw error;
        }
    },
    
    async deleteItem(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/items/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Item not found');
                }
                const responseData = await response.json();
                const error = new Error('Delete failed');
                error.response = { status: response.status, data: responseData };
                throw error;
            }
            
            return true;
        } catch (error) {
            ErrorHandler.handleApiError(error, 'delete item');
            throw error;
        }
    }
};

// Form validation
function validateForm(formData) {
    const errors = [];
    
    errors.push(...validation.validateName(formData.name));
    errors.push(...validation.validateDescription(formData.description));
    errors.push(...validation.validatePrice(formData.price));
    errors.push(...validation.validateCategory(formData.category));
    
    return errors;
}

// Display validation errors
function showValidationErrors(errors, form) {
    // Clear existing error displays
    const errorDisplays = form.querySelectorAll('.field-error');
    errorDisplays.forEach(error => error.remove());
    
    if (errors.length > 0) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.innerHTML = `
            <div class="validation-errors">
                <h4>Please fix the following errors:</h4>
                <ul>
                    ${errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            </div>
        `;
        form.insertBefore(errorDiv, form.firstChild);
        return false;
    }
    return true;
}

// UI functions
function showLoading(element, text = 'Loading...') {
    element.disabled = true;
    element.innerHTML = `<span class="loading-spinner"></span> ${text}`;
}

function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

function createItemCard(item) {
    return `
        <div class="item-card" data-id="${item.id}">
            <div class="item-header">
                <h3 class="item-name">${escapeHtml(item.name)}</h3>
                <span class="item-category">${escapeHtml(item.category)}</span>
            </div>
            <div class="item-body">
                <p class="item-description">${escapeHtml(item.description)}</p>
                <div class="item-price">$${parseFloat(item.price).toFixed(2)}</div>
            </div>
            <div class="item-actions">
                <button onclick="editItem(${item.id})" class="btn btn-edit">Edit</button>
                <button onclick="deleteItem(${item.id})" class="btn btn-delete">Delete</button>
            </div>
        </div>
    `;
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load and display items
async function loadItems() {
    try {
        const items = await api.fetchItems();
        const itemsContainer = document.getElementById('items-container');
        
        if (items.length === 0) {
            itemsContainer.innerHTML = '<p class="no-items">No items found. Create your first item!</p>';
        } else {
            itemsContainer.innerHTML = items.map(item => createItemCard(item)).join('');
        }
    } catch (error) {
        // Error already handled in api function
        const itemsContainer = document.getElementById('items-container');
        itemsContainer.innerHTML = '<p class="error-text">Failed to load items. Please refresh the page.</p>';
    }
}

// Add new item
async function addItem() {
    const form = document.getElementById('item-form');
    const submitBtn = document.getElementById('submit-btn');
    const originalBtnText = submitBtn.innerHTML;
    
    const formData = {
        name: document.getElementById('name').value.trim(),
        description: document.getElementById('description').value.trim(),
        price: parseFloat(document.getElementById('price').value),
        category: document.getElementById('category').value
    };
    
    // Validate form data
    const validationErrors = validateForm(formData);
    if (!showValidationErrors(validationErrors, form)) {
        return;
    }
    
    showLoading(submitBtn, 'Creating...');
    
    try {
        await api.createItem(formData);
        ErrorHandler.showSuccess('Item created successfully!');
        form.reset();
        loadItems();
    } catch (error) {
        // Error already handled in api function
    } finally {
        hideLoading(submitBtn, originalBtnText);
    }
}

// Edit item
async function editItem(id) {
    try {
        const item = await api.fetchItem(id);
        
        // Populate form with item data
        document.getElementById('name').value = item.name;
        document.getElementById('description').value = item.description;
        document.getElementById('price').value = item.price;
        document.getElementById('category').value = item.category;
        
        // Change form mode to edit
        const form = document.getElementById('item-form');
        const submitBtn = document.getElementById('submit-btn');
        const cancelBtn = document.getElementById('cancel-btn');
        
        form.dataset.mode = 'edit';
        form.dataset.editId = id;
        submitBtn.innerHTML = 'Update Item';
        cancelBtn.style.display = 'inline-block';
        
        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        // Error already handled in api function
    }
}

// Update item
async function updateItem() {
    const form = document.getElementById('item-form');
    const submitBtn = document.getElementById('submit-btn');
    const originalBtnText = submitBtn.innerHTML;
    const id = form.dataset.editId;
    
    const formData = {
        name: document.getElementById('name').value.trim(),
        description: document.getElementById('description').value.trim(),
        price: parseFloat(document.getElementById('price').value),
        category: document.getElementById('category').value
    };
    
    // Validate form data
    const validationErrors = validateForm(formData);
    if (!showValidationErrors(validationErrors, form)) {
        return;
    }
    
    showLoading(submitBtn, 'Updating...');
    
    try {
        await api.updateItem(id, formData);
        ErrorHandler.showSuccess('Item updated successfully!');
        cancelEdit();
        loadItems();
    } catch (error) {
        // Error already handled in api function
    } finally {
        hideLoading(submitBtn, originalBtnText);
    }
}

// Cancel edit mode
function cancelEdit() {
    const form = document.getElementById('item-form');
    const submitBtn = document.getElementById('submit-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    
    form.reset();
    form.dataset.mode = 'add';
    delete form.dataset.editId;
    submitBtn.innerHTML = 'Add Item';
    cancelBtn.style.display = 'none';
    
    // Clear validation errors
    const errorDisplays = form.querySelectorAll('.field-error');
    errorDisplays.forEach(error => error.remove());
}

// Delete item with confirmation
async function deleteItem(id) {
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    
    try {
        await api.deleteItem(id);
        ErrorHandler.showSuccess('Item deleted successfully!');
        loadItems();
    } catch (error) {
        // Error already handled in api function
    }
}

// Form submission handler
function handleFormSubmit() {
    const form = document.getElementById('item-form');
    const mode = form.dataset.mode || 'add';
    
    if (mode === 'edit') {
        updateItem();
    } else {
        addItem();
    }
}

// Initialize the app
function init() {
    // Load items on page load
    loadItems();
    
    // Add form submit event listener
    const form = document.getElementById('item-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit();
    });
    
    // Add real-time validation
    const nameInput = document.getElementById('name');
    const descriptionInput = document.getElementById('description');
    const priceInput = document.getElementById('price');
    const categorySelect = document.getElementById('category');
    
    nameInput.addEventListener('blur', () => {
        const errors = validation.validateName(nameInput.value);
        showFieldErrors(nameInput, errors);
    });
    
    descriptionInput.addEventListener('blur', () => {
        const errors = validation.validateDescription(descriptionInput.value);
        showFieldErrors(descriptionInput, errors);
    });
    
    priceInput.addEventListener('blur', () => {
        const errors = validation.validatePrice(priceInput.value);
        showFieldErrors(priceInput, errors);
    });
    
    categorySelect.addEventListener('change', () => {
        const errors = validation.validateCategory(categorySelect.value);
        showFieldErrors(categorySelect, errors);
    });
}

// Show field-specific errors
function showFieldErrors(field, errors) {
    // Remove existing field error
    const existingError = field.parentNode.querySelector('.field-error-inline');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error if there are any
    if (errors.length > 0) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error-inline';
        errorDiv.innerHTML = errors.join(', ');
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
        field.classList.add('error');
    } else {
        field.classList.remove('error');
    }
}

// Initialize app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}