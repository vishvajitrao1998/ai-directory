// AI Directory - Forms JavaScript

class FormHandler {
    constructor() {
        this.init();
    }

    init() {
        this.setupDarkMode();
        // this.setupFormValidation();
        this.setupCharacterCounters();
        this.setupFormSubmissions();
    }

    // Dark mode functionality (shared with main app)
    setupDarkMode() {
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme) {
            this.setTheme(savedTheme);
        } else if (systemPrefersDark) {
            this.setTheme('dark');
        }

        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', () => {
                this.toggleDarkMode();
            });
        }
    }

    toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        const darkModeIcon = document.getElementById('darkModeIcon');
        if (darkModeIcon) {
            darkModeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    // Form validation setup Not in use
    setupFormValidation() {
        // Bootstrap form validation
        const forms = document.querySelectorAll('.needs-validation, form[novalidate]');
        
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });

        // Custom validation rules
        this.setupCustomValidation();
    }

    setupCustomValidation() {
        // URL validation
        const urlInputs = document.querySelectorAll('input[type="url"]');
        urlInputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateURL(input);
            });
        });

        // Email validation
        const emailInputs = document.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateEmail(input);
            });
        });

        // Required field validation
        const requiredInputs = document.querySelectorAll('input[required], select[required], textarea[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateRequired(input);
            });
        });
    }

    validateURL(input) {
        const urlPattern = /^https?:\/\/.+\..+/;
        const isValid = urlPattern.test(input.value) || input.value === '';
        
        if (!isValid && input.value !== '') {
            input.setCustomValidity('Please enter a valid URL starting with http:// or https://');
        } else {
            input.setCustomValidity('');
        }
    }

    validateEmail(input) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailPattern.test(input.value) || input.value === '';
        
        if (!isValid && input.value !== '') {
            input.setCustomValidity('Please enter a valid email addhgkgkghress');
        } else {
            input.setCustomValidity('');
        }
    }

    validateRequired(input) {
        if (input.type === 'checkbox') {
            if (!input.checked) {
                input.setCustomValidity('This field is required');
            } else {
                input.setCustomValidity('');
            }
        } else {
            if (input.value.trim() === '') {
                input.setCustomValidity('This field is required');
            } else {
                input.setCustomValidity('');
            }
        }
    }

    // Close 


    // Character counters
    setupCharacterCounters() {
        const descriptionTextarea = document.getElementById('toolDescription');
        const descriptionCounter = document.getElementById('descriptionCount');
        if (descriptionTextarea && descriptionCounter) {
            descriptionTextarea.addEventListener('input', () => {
                const count = descriptionTextarea.value.length;
                descriptionCounter.textContent = count;
                
                if (count > 400) {
                    descriptionCounter.classList.add('text-danger');
                    descriptionTextarea.classList.add('is-invalid');
                } else {
                    descriptionCounter.classList.remove('text-danger');
                    descriptionTextarea.classList.remove('is-invalid');
                }
            });
        }
    }

    // Form submissions
    setupFormSubmissions() {
        // contact us form description
        const contactUSForm = document.getElementById('contactUSForm');
        if (contactUSForm) {
            contactUSForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleContactSubmit(contactUSForm);
            });
        }
    }

    async handleContactSubmit(form) {
        console.log(form.checkValidity())
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            // this.showAlert('Please fill in all required fields correctly.', 'danger');
            return;
        }

        const formData = new FormData(form);
        const contactlData = this.formDataToObject(formData);
        console.log(contactlData)
        // Show confirmation modal
        // const confirmed = await this.showConfirmationModal(
        //     'Confirm Tool Removal',
        //     'Are you sure you want to request removal of this tool? This action cannot be undone.',
        //     'Remove Tool',
        //     'btn-danger'
        // );

        // if (!confirmed) return;

        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

        try {
            // Simulate API call (replace with actual API endpoint)
            await this.simulateAPICall(contactlData, 'contact');
            this.showSubscribeAlert();
            
            form.reset();
            form.classList.remove('was-validated');
            
        } catch (error) {
            console.error('Removal error:', error);
            this.showAlert('There was an error processing your removal request. Please try again later.', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }

    // Utility functions
    formDataToObject(formData) {
        const obj = {};
        for (let [key, value] of formData.entries()) {
            obj[key] = value;
        }
        return obj;
    }

    async simulateAPICall(data, action) {
        try {
            let endpoint, method;
            console.log(action)
            console.log(data)
            if (action === 'submit') {
                endpoint = '/api/submit/';
                method = 'POST';
            } else if (action === 'remove') {
                endpoint = '/api/remove/';
                method = 'POST';
            } else if (action === 'contact') {
                endpoint = '/api/contact/';
                method = 'POST';
            }
            else {
                throw new Error('Invalid action');
            }
            
            const response = await fetch(endpoint, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (!response.ok || !result.success) {
                throw new Error(result.error || 'API request failed');
            }
            
            return result;
            
        } catch (error) {
            console.error(`${action} API error:`, error);
            throw error;
        }
    }


    // Not in use
    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert-dynamic');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-dynamic`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of main content
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        }
    }

    showSuccessModal(title, message) {
        // Create modal if it doesn't exist
        let modal = document.getElementById('successModal');
        if (!modal) {
            modal = this.createSuccessModal();
            document.body.appendChild(modal);
        }

        // Update content
        modal.querySelector('.modal-title').textContent = title;
        modal.querySelector('.modal-body p').textContent = message;

        // Show modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    createSuccessModal() {
        const modalDiv = document.createElement('div');
        modalDiv.className = 'modal fade';
        modalDiv.id = 'successModal';
        modalDiv.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">Success</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <i class="fas fa-check-circle text-success display-4 mb-3"></i>
                        <p>Success message</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal">OK</button>
                    </div>
                </div>
            </div>
        `;
        return modalDiv;
    }

    showConfirmationModal(title, message, confirmText = 'Confirm', confirmClass = 'btn-primary') {
        return new Promise((resolve) => {
            // Create modal if it doesn't exist
            let modal = document.getElementById('confirmationModal');
            if (!modal) {
                modal = this.createConfirmationModal();
                document.body.appendChild(modal);
            }

            // Update content
            modal.querySelector('.modal-title').textContent = title;
            modal.querySelector('.modal-body p').textContent = message;
            const confirmBtn = modal.querySelector('.btn-confirm');
            confirmBtn.textContent = confirmText;
            confirmBtn.className = `btn ${confirmClass}`;

            // Setup event listeners
            const handleConfirm = () => {
                resolve(true);
                bsModal.hide();
            };

            const handleCancel = () => {
                resolve(false);
                bsModal.hide();
            };

            // Remove existing listeners
            const existingConfirmBtn = modal.querySelector('.btn-confirm');
            const existingCancelBtn = modal.querySelector('.btn-cancel');
            existingConfirmBtn.replaceWith(existingConfirmBtn.cloneNode(true));
            existingCancelBtn.replaceWith(existingCancelBtn.cloneNode(true));

            // Add new listeners
            modal.querySelector('.btn-confirm').addEventListener('click', handleConfirm);
            modal.querySelector('.btn-cancel').addEventListener('click', handleCancel);

            // Show modal
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        });
    }

    createConfirmationModal() {
        const modalDiv = document.createElement('div');
        modalDiv.className = 'modal fade';
        modalDiv.id = 'confirmationModal';
        modalDiv.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirm Action</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <i class="fas fa-question-circle text-warning display-4 mb-3"></i>
                        <p>Confirmation message</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-cancel" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary btn-confirm">Confirm</button>
                    </div>
                </div>
            </div>
        `;
        return modalDiv;
    }

    // Close 

    // Function to show success or failure alert
    showSubscribeAlert(plan='Obtain.AI') {
        // Create toast element
        const toastEl = document.createElement('div');
        toastEl.className = 'toast';
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="toast-header bg-primary text-white">
                <strong class="me-auto">Obtain.AI</strong>
                <button type="button" class="btn-close btn-close-white shadow-none" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                <p>Thank you for subscribing to our <strong>${plan}</strong> plan!</p>
                <p class="mb-0">Our team will contact you shortly with next steps.</p>
            </div>
        `;
        
        // Add toast to container
        const toastContainer = document.querySelector('.toast-container');
        toastContainer.appendChild(toastEl);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
        toast.show();
        
        // Remove toast from DOM after it's hidden
        toastEl.addEventListener('hidden.bs.toast', function() {
            toastEl.remove();
        });
    }
    // close
}

// Initialize form handler when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FormHandler();
});

// Additional form enhancements
document.addEventListener('DOMContentLoaded', () => {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Form field animations
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        control.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if field has value on load
        if (control.value) {
            control.parentElement.classList.add('focused');
        }
    });

    // Smooth scrolling for form navigation
    const formSections = document.querySelectorAll('h4');
    formSections.forEach(section => {
        section.style.cursor = 'pointer';
        section.addEventListener('click', () => {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
});

