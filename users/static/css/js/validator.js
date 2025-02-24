document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    // Validation patterns
    const patterns = {
        username: /^[a-zA-Z0-9_]{3,20}$/,
        email: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
        password: /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
    };

    // Error messages
    const errorMessages = {
        username: 'Username must be 3-20 characters long and can only contain letters, numbers, and underscores',
        email: 'Please enter a valid email address',
        password: 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character',
        password2: 'Passwords do not match'
    };

    // Add error display div after each input
    function addErrorDisplay() {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.id = `${input.id}-error`;
            input.parentNode.insertBefore(errorDiv, input.nextSibling);
        });
    }

    // Show error message
    function showError(input, message) {
        const errorDiv = document.getElementById(`${input.id}-error`);
        errorDiv.textContent = message;
        input.classList.add('error');
    }

    // Clear error message
    function clearError(input) {
        const errorDiv = document.getElementById(`${input.id}-error`);
        errorDiv.textContent = '';
        input.classList.remove('error');
    }

    // Validate individual fields
    function validateField(input) {
        const value = input.value.trim();
        
        switch(input.id) {
            case 'username':
                if (!patterns.username.test(value)) {
                    showError(input, errorMessages.username);
                    return false;
                }
                break;
            case 'email':
                if (!patterns.email.test(value)) {
                    showError(input, errorMessages.email);
                    return false;
                }
                break;
            case 'password1':
                if (!patterns.password.test(value)) {
                    showError(input, errorMessages.password);
                    return false;
                }
                break;
            case 'password2':
                const password1 = document.getElementById('password1').value;
                if (value !== password1) {
                    showError(input, errorMessages.password2);
                    return false;
                }
                break;
        }
        clearError(input);
        return true;
    }

    // Initialize error displays
    addErrorDisplay();

    // Add input event listeners for real-time validation
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', () => validateField(input));
    });

    // Form submission handler
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate all fields
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    });
});