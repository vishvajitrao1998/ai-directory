// AI Directory - Main JavaScript Application

class AIDirectory {
    constructor() {
        console.log(this)
        this.tools = [];
        this.filteredTools = [];
        this.currentPage = 1;
        this.toolsPerPage = 9;
        this.searchTerm = '';
        this.filters = {
            category: '',
            pricing: '',
            listingType: ''
        };
        this.sortBy = 'name';
        
        this.init();
    }

    async init() {
        await this.loadTools();
        this.setupEventListeners();
        this.setupDarkMode();
        this.renderTools();
        this.updateStats();
    }

    // Load tools data from API
    async loadTools() {
        try {
            const response = await fetch('/api/tools/');
            const data = await response.json();
            console.log(data.response)
            if (data.success) {
                this.tools = data.tools;
                console.log(this.tools)
                this.filteredTools = [...this.tools];
            } else {
                console.error('API Error:', data.error);
                this.tools = [];
                this.filteredTools = [];
            }
        } catch (error) {
            console.log('Error loading tools:', error);
            // Fallback to empty array if API fails
            this.tools = [];
            this.filteredTools = [];
        }
    }

    // Setup all event listeners
    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.searchTerm = e.target.value.toLowerCase();
                this.applyFilters();
            }, 300));
        }

        // Filter controls
        const categoryFilter = document.getElementById('categoryFilter');
        const pricingFilter = document.getElementById('pricingFilter');
        const listingTypeFilter = document.getElementById('listingTypeFilter');
        const sortBy = document.getElementById('sortBy');
        const clearFilters = document.getElementById('clearFilters');

        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.filters.category = e.target.value;
                this.applyFilters();
            });
        }

        if (pricingFilter) {
            pricingFilter.addEventListener('change', (e) => {
                this.filters.pricing = e.target.value;
                this.applyFilters();
            });
        }

        if (listingTypeFilter) {
            listingTypeFilter.addEventListener('change', (e) => {
                this.filters.listingType = e.target.value;
                this.applyFilters();
            });
        }

        if (sortBy) {
            sortBy.addEventListener('change', (e) => {
                this.sortBy = e.target.value;
                this.sortTools();
                this.renderTools();
            });
        }

        if (clearFilters) {
            clearFilters.addEventListener('click', () => {
                this.clearAllFilters();
            });
        }

        // Dark mode toggle
        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', () => {
                this.toggleDarkMode();
            });
        }

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Dark mode functionality
    setupDarkMode() {
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme) {
            this.setTheme(savedTheme);
        } else if (systemPrefersDark) {
            this.setTheme('dark');
        }
    }

    toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        // if (currentTheme == 'light')
        // {
        //     const elements = document.getElementsByClassName('nav-link');
        //     Array.from(elements).forEach(element => {
        //     // element.style.color = 'green';
        //     });

        // }
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

    // Apply all filters and search
    applyFilters() {
        this.filteredTools = this.tools.filter(tool => {
            // Search filter
            const matchesSearch = !this.searchTerm || 
                tool.name.toLowerCase().includes(this.searchTerm) ||
                tool.description.toLowerCase().includes(this.searchTerm) ||
                tool.category.toLowerCase().includes(this.searchTerm) ||
                tool.tags.some(tag => tag.toLowerCase().includes(this.searchTerm));

            // Category filter
            const matchesCategory = !this.filters.category || 
                tool.category === this.filters.category;

            // Pricing filter
            const matchesPricing = !this.filters.pricing || 
                tool.pricing === this.filters.pricing;

            // Listing type filter
            const matchesListingType = !this.filters.listingType || 
                tool.listing_type === this.filters.listingType;

            return matchesSearch && matchesCategory && matchesPricing && matchesListingType;
        });

        this.currentPage = 1;
        this.sortTools();
        this.renderTools();
        this.updateResultsInfo();
    }

    // Sort tools based on selected criteria
    sortTools() {
        this.filteredTools.sort((a, b) => {
            switch (this.sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'date':
                    return new Date(b.date_added) - new Date(a.date_added);
                case 'rating':
                    return b.rating - a.rating;
                case 'category':
                    return a.category.localeCompare(b.category);
                default:
                    return 0;
            }
        });
    }

    // Clear all filters
    clearAllFilters() {
        this.searchTerm = '';
        this.filters = {
            category: '',
            pricing: '',
            listingType: ''
        };

        // Reset form controls
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const pricingFilter = document.getElementById('pricingFilter');
        const listingTypeFilter = document.getElementById('listingTypeFilter');

        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = '';
        if (pricingFilter) pricingFilter.value = '';
        if (listingTypeFilter) listingTypeFilter.value = '';

        this.applyFilters();
    }

    // Render tools grid
    renderTools() {
        const toolsGrid = document.getElementById('toolsGrid');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const noResults = document.getElementById('noResults');

        if (!toolsGrid) return;

        // Show loading
        if (loadingSpinner) loadingSpinner.style.display = 'block';
        toolsGrid.innerHTML = '';

        // Calculate pagination
        const startIndex = (this.currentPage - 1) * this.toolsPerPage;
        const endIndex = startIndex + this.toolsPerPage;
        const toolsToShow = this.filteredTools.slice(startIndex, endIndex);

        // Hide loading
        setTimeout(() => {
            if (loadingSpinner) loadingSpinner.style.display = 'none';

            if (toolsToShow.length === 0) {
                if (noResults) noResults.style.display = 'block';
                return;
            }

            if (noResults) noResults.style.display = 'none';

            // Render tool cards
            toolsToShow.forEach((tool, index) => {
                const toolCard = this.createToolCard(tool);
                toolCard.style.animationDelay = `${index * 0.1}s`;
                toolCard.classList.add('fade-in-up');
                toolsGrid.appendChild(toolCard);
            });

            this.renderPagination();
        }, 500);
    }

    // Create individual tool card
    createToolCard(tool) {
        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6 mb-4';

        const pricingBadgeClass = this.getPricingBadgeClass(tool.pricing);
        const listingIndicator = this.getListingIndicator(tool.listing_type);
        const ratingStars = this.generateRatingStars(tool.rating);

        col.innerHTML = `
            <div class="card tool-card h-100">
                <div class="tool-card-header">
                    ${listingIndicator}
                    <div class="d-flex align-items-center mb-3">
                        <div class="tool-logo me-3">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div>
                            <h5 class="card-title mb-1">${tool.name}</h5>
                            <span class="badge badge-category">${this.formatCategory(tool.category)}</span>
                        </div>
                    </div>
                </div>
                <div class="tool-card-body">
                    <p class="card-text text-muted mb-3">${tool.description}</p>
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <span class="badge badge-pricing ${pricingBadgeClass}">${this.formatPricing(tool.pricing)}</span>
                        <div class="rating-stars">
                            ${ratingStars}
                            <span class="ms-1">${tool.rating}</span>
                        </div>
                    </div>
                    <div class="mt-auto">
                        <div class="d-flex flex-wrap gap-1 mb-3">
                            ${tool.tags.slice(0, 3).map(tag => 
                                `<span class="badge bg-light text-dark">${tag}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
                <div class="tool-card-footer">
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-primary btn-sm flex-fill" onclick="aiDirectory.showToolDetails('${tool.id}')">
                            <i class="fas fa-info-circle me-1"></i>
                            View Details
                        </button>
                        <a href="${tool.website_url}" target="_blank" class="btn btn-primary btn-sm flex-fill">
                            <i class="fas fa-external-link-alt me-1"></i>
                            Visit
                        </a>
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    // Get pricing badge CSS class
    getPricingBadgeClass(pricing) {
        const classes = {
            'free': 'badge-free',
            'paid': 'badge-paid',
            'freemium': 'badge-freemium',
            'open_source': 'badge-open-source'
        };
        return classes[pricing] || 'badge-free';
    }

    // Get listing type indicator
    getListingIndicator(listingType) {
        if (listingType === 'verified') {
            return '<div class="listing-indicator listing-verified"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-patch-check-fill" viewBox="0 0 16 16"><path d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01zm.287 5.984-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7 8.793l2.646-2.647a.5.5 0 0 1 .708.708"/></svg></div>';
        } else if (listingType === 'featured') {
            return '<div class="listing-indicator listing-featured"><i class="fas fa-star" title="Featured"></i></div>';
        }
        return '';
    }

    // Generate rating stars
    generateRatingStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let stars = '';

        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }

        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }

        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star"></i>';
        }

        return stars;
    }

    // Format category for display
    formatCategory(category) {
        return category.split('-').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    // Format pricing for display
    formatPricing(pricing) {
        const formats = {
            'free': 'Free',
            'paid': 'Paid',
            'freemium': 'Freemium',
            'open_source': 'Open Source'
        };
        return formats[pricing] || 'Free';
    }

    // Show tool details in modal
    showToolDetails(toolId) {
        console.log(this.tools)
        const tool = this.tools.find(t => t.id == toolId);
        console.log(tool)
        if (!tool) return;

        const modal = document.getElementById('toolDetailModal');
        const modalTitle = document.getElementById('toolDetailModalLabel');
        const modalContent = document.getElementById('toolDetailContent');
        const visitBtn = document.getElementById('visitToolBtn');

        if (modalTitle) modalTitle.textContent = tool.name;
        if (visitBtn) visitBtn.href = tool.website_url;

        if (modalContent) {
            const listingIndicator = this.getListingIndicator(tool.listing_type);
            const ratingStars = this.generateRatingStars(tool.rating);
            const pricingBadgeClass = this.getPricingBadgeClass(tool.pricing);

            modalContent.innerHTML = `
                <div class="tool-detail-header">
                    <div class="tool-detail-logo">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div>
                        <h4 class="mb-1">${tool.name} ${listingIndicator}</h4>
                        <div class="d-flex align-items-center gap-3 mb-2">
                            <span class="badge badge-category">${this.formatCategory(tool.category)}</span>
                            <span class="badge badge-pricing ${pricingBadgeClass}">${this.formatPricing(tool.pricing)}</span>
                            <div class="rating-stars">
                                ${ratingStars}
                                <span class="ms-1">${tool.rating}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mb-4">
                    <h6>Description</h6>
                    <p>${tool.detailed_description}</p>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <h6>Features</h6>
                        <ul class="tool-features">
                            ${tool.features.map(feature => `<li>${feature}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="col-md-6 mb-3">
                        <h6>Tags</h6>
                        <div class="d-flex flex-wrap gap-1">
                            ${tool.tags.map(tag => 
                                `<span class="badge bg-light text-dark">${tag}</span>`
                            ).join('')}
                        </div>
                        
                        <h6 class="mt-3">Added</h6>
                        <p class="text-muted">${new Date(tool.date_added).toLocaleDateString()}</p>
                    </div>
                </div>
            `;
        }

        // Show modal
        console.log(modal)
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    // Render pagination
    renderPagination() {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;
        const totalPages = Math.ceil(this.filteredTools.length / this.toolsPerPage);

        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '';

        // Previous button
        paginationHTML += `
            <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#tools" onclick="aiDirectory.goToPage(${this.currentPage - 1})">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
        `;

        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        if (startPage > 1) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#tools" onclick="aiDirectory.goToPage(1)">1</a>
                </li>
            `;
            if (startPage > 2) {
                paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            paginationHTML += `
                <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                    <a class="page-link" href="#tools" onclick="aiDirectory.goToPage(${i})">${i}</a>
                </li>
            `;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#tools" onclick="aiDirectory.goToPage(${totalPages})">${totalPages}</a>
                </li>
            `;
        }

        // Next button
        paginationHTML += `
            <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="aiDirectory.goToPage(${this.currentPage + 1})">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        `;

        console.log(paginationHTML)


        pagination.innerHTML = paginationHTML;
    }

    // Go to specific page
    goToPage(page) {
        const totalPages = Math.ceil(this.filteredTools.length / this.toolsPerPage);
        if (page < 1 || page > totalPages) return;
        
        this.currentPage = page;
        this.renderTools();
        
        // Scroll to tools section
        const toolsSection = document.getElementById('tools');
        if (toolsSection) {
            toolsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Update results info
    updateResultsInfo() {
        const resultsCount = document.getElementById('resultsCount');
        if (resultsCount) {
            resultsCount.textContent = this.filteredTools.length;
        }
    }

    // Update stats in hero section
    updateStats() {
        const totalTools = document.getElementById('totalTools');
        const totalCategories = document.getElementById('totalCategories');
        const freeTools = document.getElementById('freeTools');

        if (totalTools) {
            totalTools.textContent = `${this.tools.length}+`;
        }

        if (totalCategories) {
            const categories = [...new Set(this.tools.map(tool => tool.category))];
            totalCategories.textContent = `${categories.length}+`;
        }

        if (freeTools) {
            const free = this.tools.filter(tool => 
                tool.pricing === 'free' || tool.pricing === 'open_source'
            );
            freeTools.textContent = `${free.length}+`;
        }
    }

    // Debounce function for search
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
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiDirectory = new AIDirectory();
});

// Handle form submissions (placeholder for now)
document.addEventListener('DOMContentLoaded', () => {
    const submitToolForm = document.getElementById('submitToolForm');
    if (submitToolForm) {
        submitToolForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Tool submission form will be implemented in the next phase!');
        });
    }
});

// Add some additional interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.card, .stat-item').forEach(el => {
        observer.observe(el);
    });

    // Add loading state to buttons
    document.addEventListener('click', (e) => {
        if (e.target.matches('.btn-primary, .btn-outline-primary')) {
            const btn = e.target;
            const originalText = btn.innerHTML;
            
            if (!btn.disabled) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                
                setTimeout(() => {
                    btn.disabled = false;
                    btn.innerHTML = originalText;
                }, 1000);
            }
        }
    });
});

