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
    
    // Initialize Bootstrap components
    initializeBootstrapComponents();
});

// Initialize Bootstrap modals and tooltips
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

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

// Advanced Features Functions

// Show batch processing modal
function showBatchModal() {
    const batchModal = new bootstrap.Modal(document.getElementById('batchModal'));
    batchModal.show();
    
    // Reset modal state
    document.getElementById('batchResults').style.display = 'none';
    document.getElementById('exportCsvBtn').disabled = true;
    document.getElementById('exportJsonBtn').disabled = true;
    
    // Refresh feather icons
    setTimeout(() => feather.replace(), 100);
}

// Load sample data for batch processing
function loadSampleData() {
    const sampleIPs = `# Sample IP addresses for testing
8.8.8.8
1.1.1.1
208.67.222.222
139.191.0.0/24
# Google DNS
8.8.4.4
# Cloudflare DNS
1.0.0.1`;
    
    document.getElementById('ipListInput').value = sampleIPs;
}

// Process batch IP addresses
async function processBatch() {
    const ipListText = document.getElementById('ipListInput').value.trim();
    
    if (!ipListText) {
        showTemporaryMessage('Please enter IP addresses to process', 'error');
        return;
    }
    
    // Show progress
    const resultsDiv = document.getElementById('batchResults');
    resultsDiv.style.display = 'block';
    
    const processedCount = document.getElementById('processedCount');
    const errorCount = document.getElementById('errorCount');
    const totalCount = document.getElementById('totalCount');
    const progressBar = document.getElementById('progressBar');
    const resultsList = document.getElementById('batchResultsList');
    
    // Reset counters
    processedCount.textContent = '0';
    errorCount.textContent = '0';
    totalCount.textContent = '0';
    progressBar.style.width = '0%';
    resultsList.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p>Processing batch...</p></div>';
    
    try {
        const response = await fetch('/batch_lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `ip_list=${encodeURIComponent(ipListText)}`
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Update counters
            processedCount.textContent = result.total_processed;
            errorCount.textContent = result.total_errors;
            totalCount.textContent = result.total_processed + result.total_errors;
            
            // Update progress bar
            const percentage = result.total_processed > 0 ? 
                (result.total_processed / (result.total_processed + result.total_errors)) * 100 : 0;
            progressBar.style.width = percentage + '%';
            
            // Display results
            displayBatchResults(result.results, result.has_more);
            
            // Enable export buttons
            document.getElementById('exportCsvBtn').disabled = false;
            document.getElementById('exportJsonBtn').disabled = false;
            
        } else {
            resultsList.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
        }
        
    } catch (error) {
        console.error('Batch processing error:', error);
        resultsList.innerHTML = `<div class="alert alert-danger">Batch processing failed: ${error.message}</div>`;
    }
}

// Display batch results
function displayBatchResults(results, hasMore) {
    const resultsList = document.getElementById('batchResultsList');
    
    if (!results || results.length === 0) {
        resultsList.innerHTML = '<div class="text-muted text-center">No results to display</div>';
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-sm table-dark"><thead><tr>';
    html += '<th>IP</th><th>RIR</th><th>Organization</th><th>Country</th><th>ASN</th>';
    html += '</tr></thead><tbody>';
    
    results.forEach(result => {
        const rdap = result.rdap || {};
        const geo = result.geolocation || {};
        const asn = result.asn || {};
        
        html += `<tr>
            <td><code>${result.ip}</code></td>
            <td><span class="badge bg-primary">${rdap.rir || 'Unknown'}</span></td>
            <td class="text-truncate" style="max-width: 150px;" title="${rdap.organization || 'Unknown'}">${rdap.organization || 'Unknown'}</td>
            <td>${geo.country_name || geo.country || 'Unknown'}</td>
            <td>${asn.asn_number || 'Unknown'}</td>
        </tr>`;
    });
    
    html += '</tbody></table></div>';
    
    if (hasMore) {
        html += '<div class="alert alert-info">Showing first 50 results. Export for complete data.</div>';
    }
    
    resultsList.innerHTML = html;
}

// Export batch results
function exportResults(format) {
    window.open(`/export/${format}`, '_blank');
}

// Show analytics page
function showAnalytics() {
    window.open('/analytics', '_blank');
}

// Show API documentation
function showApiDocs() {
    const docsContent = `
        <div class="modal fade" id="apiDocsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content bg-dark">
                    <div class="modal-header border-secondary">
                        <h5 class="modal-title">
                            <i data-feather="code" class="me-2"></i> RIPEScanner API Documentation
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6>Available Endpoints:</h6>
                        <div class="bg-secondary p-3 rounded mb-3">
                            <code>GET /geolocation/&lt;ip&gt;</code><br>
                            <small class="text-muted">Get geolocation data for IP address</small>
                        </div>
                        <div class="bg-secondary p-3 rounded mb-3">
                            <code>GET /asn/&lt;ip&gt;</code><br>
                            <small class="text-muted">Get ASN information for IP address</small>
                        </div>
                        <div class="bg-secondary p-3 rounded mb-3">
                            <code>POST /enhanced_lookup</code><br>
                            <small class="text-muted">Enhanced lookup with RDAP, geo, and ASN data</small>
                        </div>
                        <div class="bg-secondary p-3 rounded mb-3">
                            <code>GET /api/stats</code><br>
                            <small class="text-muted">Get usage statistics</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create and show modal
    document.body.insertAdjacentHTML('beforeend', docsContent);
    const modal = new bootstrap.Modal(document.getElementById('apiDocsModal'));
    modal.show();
    
    // Refresh feather icons in modal
    setTimeout(() => feather.replace(), 100);
    
    // Clean up when modal closes
    document.getElementById('apiDocsModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Show temporary message helper
function showTemporaryMessage(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
    alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 3000);
}
