
// RIPEScanner Production JavaScript
(function() {
    'use strict';
    
    // Main JavaScript for RDAP application

document.addEventListener('DOMContentLoaded', function() {
    const ipInput = document.getElementById('ip_address');
    const validationFeedback = document.getElementById('validation-feedback');
    const lookupForm = document.getElementById('lookupForm');
    const lookupBtn = document.getElementById('lookupBtn');
    
    // Real-time IP validation
    if (ipInput) {
        let validationTimeout;
        
        ipInput.addEventListener('input', function() {
            clearTimeout(validationTimeout);
            validationTimeout = setTimeout(() => {
                validateIPAddress(this.value.trim());
            }, 300);
        });
    }
    
    // Form submission handling
    if (lookupForm) {
        lookupForm.addEventListener('submit', function(e) {
            const ipValue = ipInput.value.trim();
            if (!ipValue) {
                e.preventDefault();
                showValidationMessage('Please enter an IP address or network', 'error');
                return;
            }
            
            // Show loading state
            showLoadingState(true);
        });
    }
    
    // Initialize feather icons when content changes
    const observer = new MutationObserver(function() {
        feather.replace();
    });
    observer.observe(document.body, { childList: true, subtree: true });
});

// Validate IP address via AJAX
async function validateIPAddress(ipValue) {
    const validationFeedback = document.getElementById('validation-feedback');
    const ipInput = document.getElementById('ip_address');
    
    if (!ipValue) {
        clearValidation();
        return;
    }
    
    try {
        const response = await fetch('/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip_address: ipValue })
        });
        
        const result = await response.json();
        
        if (result.valid) {
            showValidationMessage(result.message, 'success');
            ipInput.classList.remove('is-invalid-custom');
            ipInput.classList.add('is-valid-custom');
        } else {
            showValidationMessage(result.message, 'error');
            ipInput.classList.remove('is-valid-custom');
            ipInput.classList.add('is-invalid-custom');
        }
    } catch (error) {
        console.error('Validation error:', error);
        showValidationMessage('Unable to validate IP address', 'error');
    }
}

// Show validation message
function showValidationMessage(message, type) {
    const validationFeedback = document.getElementById('validation-feedback');
    if (validationFeedback) {
        validationFeedback.textContent = message;
        validationFeedback.className = `form-text ${type === 'success' ? 'valid-feedback-custom' : 'invalid-feedback-custom'}`;
    }
}

// Clear validation
function clearValidation() {
    const validationFeedback = document.getElementById('validation-feedback');
    const ipInput = document.getElementById('ip_address');
    
    if (validationFeedback) {
        validationFeedback.textContent = '';
        validationFeedback.className = 'form-text';
    }
    
    if (ipInput) {
        ipInput.classList.remove('is-valid-custom', 'is-invalid-custom');
    }
}

// Show/hide loading state
function showLoadingState(loading) {
    const lookupBtn = document.getElementById('lookupBtn');
    const lookupForm = document.getElementById('lookupForm');
    
    if (loading) {
        if (lookupBtn) {
            lookupBtn.disabled = true;
            lookupBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Scanning...';
        }
        if (lookupForm) {
            lookupForm.classList.add('loading');
        }
    } else {
        if (lookupBtn) {
            lookupBtn.disabled = false;
            lookupBtn.innerHTML = '<i data-feather="search" class="me-2"></i>Scan IP Registry';
        }
        if (lookupForm) {
            lookupForm.classList.remove('loading');
        }
        feather.replace();
    }
}

// Copy results to clipboard
async function copyResults() {
    if (!window.rdapResult) {
        alert('No results to copy');
        return;
    }
    
    try {
        const textToCopy = JSON.stringify(window.rdapResult, null, 2);
        await navigator.clipboard.writeText(textToCopy);
        
        // Show success feedback
        const copyBtn = document.querySelector('[onclick="copyResults()"]');
        if (copyBtn) {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i data-feather="check" class="me-1"></i>Copied!';
            copyBtn.classList.add('copy-success');
            
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.classList.remove('copy-success');
                feather.replace();
            }, 2000);
        }
    } catch (error) {
        console.error('Failed to copy:', error);
        alert('Failed to copy results to clipboard');
    }
}

// Handle browser back/forward
window.addEventListener('popstate', function() {
    showLoadingState(false);
});

// Auto-focus on IP input when page loads
window.addEventListener('load', function() {
    const ipInput = document.getElementById('ip_address');
    if (ipInput && !ipInput.value) {
        ipInput.focus();
    }
    showLoadingState(false);
});

    
    // Production error handling
    window.addEventListener('error', function(e) {
        console.error('RIPEScanner Error:', e.error);
    });
    
    // Service worker registration for PWA capabilities
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js').then(function(registration) {
                console.log('SW registered: ', registration);
            }).catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
        });
    }
})();
