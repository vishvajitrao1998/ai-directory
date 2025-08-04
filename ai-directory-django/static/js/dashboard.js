// Dashboard JavaScript Enhancements

class Dashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupKeyboardShortcuts();
    }

    setupEventListeners() {
        // Real-time search functionality
        const searchInputs = document.querySelectorAll('[data-search]');
        searchInputs.forEach(input => {
            input.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
        });

        // Auto-save form data
        const forms = document.querySelectorAll('[data-autosave]');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('change', this.autoSave.bind(this));
            });
        });

        // Infinite scroll for tables
        const scrollContainers = document.querySelectorAll('[data-infinite-scroll]');
        scrollContainers.forEach(container => {
            container.addEventListener('scroll', this.handleInfiniteScroll.bind(this));
        });
    }

    initializeComponents() {
        this.initTooltips();
        this.initCharts();
        this.initNotifications();
        this.setupThemeToggle();
    }

    initTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initCharts() {
        // Initialize any charts that need dynamic data
        const chartElements = document.querySelectorAll('[data-chart]');
        chartElements.forEach(element => {
            this.loadChartData(element);
        });
    }

    initNotifications() {
        // Check for new notifications periodically
        setInterval(() => {
            this.checkNotifications();
        }, 30000); // Check every 30 seconds
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', this.toggleTheme.bind(this));
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.focusSearch();
            }

            // Ctrl/Cmd + N for new tool
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                window.location.href = '/dashboard/tools/submit/';
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeModals();
            }
        });
    }

    handleSearch(event) {
        const query = event.target.value.toLowerCase();
        const searchTarget = event.target.dataset.search;
        const items = document.querySelectorAll(`[data-searchable="${searchTarget}"]`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            const isVisible = text.includes(query);
            item.style.display = isVisible ? '' : 'none';
        });

        // Update search results count
        const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
        this.updateSearchResults(visibleItems.length, items.length);
    }

    updateSearchResults(visible, total) {
        const resultElement = document.querySelector('[data-search-results]');
        if (resultElement) {
            resultElement.textContent = `Showing ${visible} of ${total} results`;
        }
    }

    autoSave(event) {
        const form = event.target.closest('form');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Save to localStorage
        localStorage.setItem(`autosave_${form.id}`, JSON.stringify(data));

        // Show auto-save indicator
        this.showAutoSaveIndicator();
    }

    showAutoSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator';
        indicator.innerHTML = '<i class="fas fa-check text-success"></i> Auto-saved';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 8px 16px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        document.body.appendChild(indicator);
        
        setTimeout(() => indicator.style.opacity = '1', 100);
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => indicator.remove(), 300);
        }, 2000);
    }

    handleInfiniteScroll(event) {
        const container = event.target;
        const { scrollTop, scrollHeight, clientHeight } = container;

        if (scrollTop + clientHeight >= scrollHeight - 5) {
            this.loadMoreContent(container);
        }
    }

    loadMoreContent(container) {
        if (container.dataset.loading === 'true') return;

        container.dataset.loading = 'true';
        const page = parseInt(container.dataset.page || '1') + 1;

        // Show loading indicator
        this.showLoadingIndicator(container);

        // Simulate API call
        setTimeout(() => {
            this.appendContent(container, page);
            container.dataset.page = page;
            container.dataset.loading = 'false';
            this.hideLoadingIndicator(container);
        }, 1000);
    }

    showLoadingIndicator(container) {
        const loader = document.createElement('div');
        loader.className = 'loading-indicator text-center p-3';
        loader.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
        container.appendChild(loader);
    }

    hideLoadingIndicator(container) {
        const loader = container.querySelector('.loading-indicator');
        if (loader) loader.remove();
    }

    appendContent(container, page) {
        // This would typically fetch real data from an API
        const mockContent = this.generateMockContent(page);
        container.insertAdjacentHTML('beforeend', mockContent);
    }

    generateMockContent(page) {
        return `
            <tr>
                <td>Mock Tool ${page}</td>
                <td><span class="badge bg-success">Approved</span></td>
                <td>AI Writing</td>
                <td>1,234</td>
                <td>Just now</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary">Edit</button>
                </td>
            </tr>
        `;
    }

    loadChartData(element) {
        const chartType = element.dataset.chart;
        // Load chart data based on type
        // This would typically fetch from an API
    }

    checkNotifications() {
        // Check for new notifications
        fetch('/dashboard/api/notifications/')
            .then(response => response.json())
            .then(data => {
                if (data.new_notifications > 0) {
                    this.showNotificationBadge(data.new_notifications);
                }
            })
            .catch(error => console.log('Notification check failed:', error));
    }

    showNotificationBadge(count) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'block' : 'none';
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }

    focusSearch() {
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) modalInstance.hide();
        });
    }

    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Show success notification
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    // Show error notification
    showError(message) {
        this.showNotification(message, 'error');
    }

    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});

// Export for use in other scripts
window.Dashboard = Dashboard;

