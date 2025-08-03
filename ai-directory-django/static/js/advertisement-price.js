
document.addEventListener('DOMContentLoaded', function () {
    // Currency data with flags (SVG format for better quality)
    // const currencies = [
    //     { code: 'USD', name: 'US Dollar', flag: createFlagSVG('us') },
    //     { code: 'EUR', name: 'Euro', flag: createFlagSVG('eu') },
    //     { code: 'GBP', name: 'British Pound', flag: createFlagSVG('gb') },
    //     { code: 'JPY', name: 'Japanese Yen', flag: createFlagSVG('jp') },
    //     { code: 'AUD', name: 'Australian Dollar', flag: createFlagSVG('au') },
    //     { code: 'CAD', name: 'Canadian Dollar', flag: createFlagSVG('ca') },
    //     { code: 'CHF', name: 'Swiss Franc', flag: createFlagSVG('ch') },
    //     { code: 'CNY', name: 'Chinese Yuan', flag: createFlagSVG('cn') },
    //     { code: 'INR', name: 'Indian Rupee', flag: createFlagSVG('in') },
    //     { code: 'SGD', name: 'Singapore Dollar', flag: createFlagSVG('sg') },
    //     { code: 'NZD', name: 'New Zealand Dollar', flag: createFlagSVG('nz') },
    //     { code: 'MXN', name: 'Mexican Peso', flag: createFlagSVG('mx') },
    //     { code: 'BRL', name: 'Brazilian Real', flag: createFlagSVG('br') },
    //     { code: 'ZAR', name: 'South African Rand', flag: createFlagSVG('za') }
    // ];

    // Function to create simple flag SVGs
    function createFlagSVG(countryCode) {
        //     const flagMap = {
        //         'us': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#fff"/><rect width="24" height="1.38" fill="#b22234" y="0"/><rect width="24" height="1.38" fill="#b22234" y="2.77"/><rect width="24" height="1.38" fill="#b22234" y="5.54"/><rect width="24" height="1.38" fill="#b22234" y="8.31"/><rect width="24" height="1.38" fill="#b22234" y="11.08"/><rect width="24" height="1.38" fill="#b22234" y="13.85"/><rect width="24" height="1.38" fill="#b22234" y="16.62"/><rect width="9.6" height="9.69" fill="#3c3b6e"/></svg>`,
        //         'eu': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#039"/><circle cx="12" cy="9" r="6" fill="none" stroke="#fc0" stroke-width="1"/><path d="M12,3 L12.76,6.57 L16.5,6.57 L13.47,8.93 L14.23,12.5 L12,10.14 L9.77,12.5 L10.53,8.93 L7.5,6.57 L11.24,6.57 Z" fill="#fc0"/></svg>`,
        //         'gb': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#012169"/><path d="M0,0 L24,18 M24,0 L0,18" stroke="#fff" stroke-width="3"/><path d="M12,0 L12,18 M0,9 L24,9" stroke="#fff" stroke-width="5"/><path d="M12,0 L12,18 M0,9 L24,9" stroke="#c8102e" stroke-width="3"/><path d="M0,0 L24,18 M24,0 L0,18" stroke="#c8102e" stroke-width="1"/></svg>`,
        //         'jp': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#fff"/><circle cx="12" cy="9" r="5" fill="#bc002d"/></svg>`,
        //         'au': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#00008B"/><path d="M0,0 L12,9 L0,18" fill="#00008B"/><path d="M0,0 L10,7.5 L0,15" fill="#00008B" stroke="#fff" stroke-width="2"/><path d="M0,0 L12,9 L0,18" stroke="#f00" stroke-width="1"/><circle cx="16" cy="4.5" r="1" fill="#fff"/><circle cx="16" cy="13.5" r="1" fill="#fff"/><circle cx="20" cy="9" r="1" fill="#fff"/><circle cx="12" cy="9" r="1" fill="#fff"/></svg>`,
        //         'ca': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#fff"/><rect width="6" height="18" fill="#f00"/><rect width="6" height="18" x="18" fill="#f00"/><path d="M12,5 L13,8 L16,8 L14,10 L15,13 L12,11 L9,13 L10,10 L8,8 L11,8 Z" fill="#f00"/></svg>`,
        //         'ch': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#f00"/><rect x="6" y="6" width="12" height="6" fill="#fff"/><rect x="9" y="3" width="6" height="12" fill="#fff"/></svg>`,
        //         'cn': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#de2910"/><path d="M2,2 L3,5 L6,5 L3.5,7 L4.5,10 L2,8 L-0.5,10 L0.5,7 L-2,5 L1,5 Z" fill="#ffde00" transform="translate(5,3) scale(0.8)"/><path d="M2,2 L3,5 L6,5 L3.5,7 L4.5,10 L2,8 L-0.5,10 L0.5,7 L-2,5 L1,5 Z" fill="#ffde00" transform="translate(10,1) scale(0.4)"/><path d="M2,2 L3,5 L6,5 L3.5,7 L4.5,10 L2,8 L-0.5,10 L0.5,7 L-2,5 L1,5 Z" fill="#ffde00" transform="translate(12,3) scale(0.4)"/><path d="M2,2 L3,5 L6,5 L3.5,7 L4.5,10 L2,8 L-0.5,10 L0.5,7 L-2,5 L1,5 Z" fill="#ffde00" transform="translate(10,5) scale(0.4)"/><path d="M2,2 L3,5 L6,5 L3.5,7 L4.5,10 L2,8 L-0.5,10 L0.5,7 L-2,5 L1,5 Z" fill="#ffde00" transform="translate(8,3) scale(0.4)"/></svg>`,
        //         'in': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="6" fill="#f93"/><rect width="24" height="6" y="6" fill="#fff"/><rect width="24" height="6" y="12" fill="#128807"/><circle cx="12" cy="9" r="1.8" fill="#008"/><circle cx="12" cy="9" r="1.6" fill="#fff"/><circle cx="12" cy="9" r="0.4" fill="#008"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(15,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(30,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(45,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(60,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(75,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(90,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(105,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(120,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(135,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(150,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(165,12,9)"/><path d="M12,7.5 L12,10.5" stroke="#008" stroke-width="0.2" transform="rotate(180,12,9)"/></svg>`,
        //         'sg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#fff"/><rect width="24" height="9" fill="#ed2939"/><circle cx="6" cy="4.5" r="3" fill="#fff"/><path d="M4.5,3 L5,2 L5.5,3 L6.5,2.5 L6,3.5 L7,4 L6,4.5 L6.5,5.5 L5.5,5 L5,6 L4.5,5 L3.5,5.5 L4,4.5 L3,4 L4,3.5 Z" fill="#ed2939"/></svg>`,
        //         'nz': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#00247d"/><path d="M0,0 L12,9 L0,18" fill="#00247d"/><path d="M0,0 L10,7.5 L0,15" fill="#00247d" stroke="#fff" stroke-width="2"/><path d="M0,0 L12,9 L0,18" stroke="#cc142b" stroke-width="1"/><path d="M18,4 L19,6 L21,6.5 L19,7 L18,9 L17,7 L15,6.5 L17,6 Z" fill="#cc142b"/><path d="M18,11 L18.5,12 L19.5,12.2 L18.5,12.4 L18,13.5 L17.5,12.4 L16.5,12.2 L17.5,12 Z" fill="#cc142b"/><path d="M21,10 L21.5,11 L22.5,11.2 L21.5,11.4 L21,12.5 L20.5,11.4 L19.5,11.2 L20.5,11 Z" fill="#cc142b"/><path d="M15,13 L15.5,14 L16.5,14.2 L15.5,14.4 L15,15.5 L14.5,14.4 L13.5,14.2 L14.5,14 Z" fill="#cc142b"/></svg>`,
        //         'mx': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="8" height="18" fill="#006847"/><rect width="8" height="18" x="8" fill="#fff"/><rect width="8" height="18" x="16" fill="#ce1126"/><circle cx="12" cy="9" r="2.5" fill="#f1c40f"/></svg>`,
        //         'br': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#009b3a"/><path d="M2,9 L12,2 L22,9 L12,16 Z" fill="#fedf00"/><circle cx="12" cy="9" r="4" fill="#002776"/><path d="M8,9 A4,4 0 0 1 16,9" fill="#fff"/></svg>`,
        //         'za': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" fill="#002395"/><path d="M0,3 L24,3 L24,15 L0,15 Z" fill="#de3831"/><path d="M0,5 L24,5 L24,13 L0,13 Z" fill="#fff"/><path d="M0,6 L24,6 L24,12 L0,12 Z" fill="#007a4d"/><path d="M0,0 L12,9 L0,18 Z" fill="#000"/><path d="M0,1.5 L9,9 L0,16.5 Z" fill="#ffb612"/><path d="M0,3 L6,9 L0,15 Z" fill="#007a4d"/></svg>`
        //     };

        //     return flagMap[countryCode] || '';
    }

    // API Call to Get Available currencies

    let currencies = null;
    fetch("/api/currencies/").then(response => response.json()).then(data => {
        currencies = data.currencies;
        populateCurrencyOptions();
    }).catch(error => {
        console.error("Failed to load currency list:", error);
    });

    // console.log(currencies)

    const selectedCurrencyDisplay = document.getElementById('selectedCurrencyDisplay');
    const currencyDropdown = document.getElementById('currencyDropdown');
    const currencyOptions = document.getElementById('currencyOptions');
    const checkRateBtn = document.getElementById('checkRate');
    const resultContainer = document.getElementById('resultContainer');
    const resultText = document.getElementById('resultText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const searchInput = document.getElementById('searchCurrency');

    let selectedCurrency = 'INR';

    // Populate currency options
    function populateCurrencyOptions(filterText = '') {
        currencyOptions.innerHTML = '';
        const filteredCurrencies = currencies.filter(currency =>
            currency.code.toLowerCase().includes(filterText.toLowerCase()) ||
            currency.name.toLowerCase().includes(filterText.toLowerCase())
        );

        filteredCurrencies.forEach(currency => {
            const option = document.createElement('div');
            option.className = 'dropdown-item';
            option.dataset.code = currency.code;
            option.innerHTML = `
                        <div class="flag d-flex align-items-center justify-content-center">${currency.flag}</div>
                        <span class="currency-code d-flex align-items-center justify-content-center">${currency.code}</span>
                    `;

            option.addEventListener('click', () => {
                selectCurrency(currency);
                currencyDropdown.style.display = 'none';
            });

            currencyOptions.appendChild(option);
        });

        if (filteredCurrencies.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'dropdown-item';
            noResults.textContent = 'No currencies found';
            currencyOptions.appendChild(noResults);
        }
    }

    // Assign value to plan based on the plan type
    function assign_value_to_plan(element, class_name) {
        let elms = document.getElementsByClassName(class_name);
        for (let i = 0; i < elms.length; i++) {

            // Access each element using its index
            const elmt = elms[i];
            // Assign a value to the element (e.g., for input fields)
            elmt.innerText = element.formated_price;
        }
    }

    // Select a currency and display into main input box
    function selectCurrency(currency) {
        selectedCurrency = currency;
        selectedCurrencyDisplay.innerHTML = `
                    <div class="selected-currency">
                        <div class="selected-flag d-flex align-items-center justify-content-center">${currency.flag}</div>
                        <span class="currency-code d-flex align-items-center justify-content-center">${currency.code}</span>
                    </div>
                `;

        // Changing pricing based on the currency selected
        fetch(`/api/advertise/prices?currency=${currency.id}`)
            .then(response => response.json())
            .then(data => {
                data.prices.forEach(element => {
                    if (element.plan_name == 'Basic Boost') {
                        assign_value_to_plan(element, "simple-listing-price")
                    }
                    else if (element.plan_name == 'Pro Spotlight') {
                        assign_value_to_plan(element, "verified-listing-price")
                    }
                    if (element.plan_name == 'Ultimate Promo') {
                        assign_value_to_plan(element, "featured-listing-price")
                    }
                });
            }).catch(error => console.error("Error fetching prices:", error));
    }

    // Toggle dropdown - Intial Toggle Dropdown
    selectedCurrencyDisplay.addEventListener('click', () => {
        const isVisible = currencyDropdown.style.display === 'block';
        currencyDropdown.style.display = isVisible ? 'none' : 'block';
        if (!isVisible) {
            searchInput.focus();
            searchInput.value = '';
            populateCurrencyOptions();
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
        if (!selectedCurrencyDisplay.contains(event.target) &&
            !currencyDropdown.contains(event.target)) {
            currencyDropdown.style.display = 'none';
        }
    });

    // Search functionality
    searchInput.addEventListener('input', (e) => {
        populateCurrencyOptions(e.target.value);
    });

    // Check rate button click
    // checkRateBtn.addEventListener('click', function () {
    //     if (!selectedCurrency) {
    //         alert('Please select a currency first');
    //         return;
    //     }

    //     // Show the result container with loading state
    //     resultContainer.style.display = 'block';
    //     loadingSpinner.style.display = 'inline-block';

    //     // Simulate API call with setTimeout
    //     setTimeout(function () {
    //         // Hide loading spinner
    //         loadingSpinner.style.display = 'none';

    //         // In a real app, this would be an actual API call
    //         // For now, just show an alert and update the result text
    //         alert(`You selected: ${selectedCurrency.code} (${selectedCurrency.name})`);

    //         // Update the result container with fake data
    //         resultText.innerHTML = `
    //                     <div class="d-flex align-items-center mb-3">
    //                         <div class="flag me-2" style="width: 32px; height: 24px;">${selectedCurrency.flag}</div>
    //                         <h5 class="mb-0">Exchange Rate for ${selectedCurrency.code}</h5>
    //                     </div>
    //                     <p class="mb-1">1 ${selectedCurrency.code} = ${(Math.random() * 80 + 20).toFixed(4)} Base Currency</p>
    //                     <p class="text-muted small">Last updated: ${new Date().toLocaleString()}</p>
    //                 `;

    //         /* 
    //         // This is how you would make an actual API call
    //         fetch('/api/currency-rate/' + selectedCurrency.code)
    //             .then(response => response.json())
    //             .then(data => {
    //                 loadingSpinner.style.display = 'none';
    //                 resultText.innerHTML = `
    //                     <div class="d-flex align-items-center mb-3">
    //                         <div class="flag me-2" style="width: 32px; height: 24px;">${selectedCurrency.flag}</div>
    //                         <h5 class="mb-0">Exchange Rate for ${data.currency}</h5>
    //                     </div>
    //                     <p class="mb-1">1 ${data.currency} = ${data.rate} Base Currency</p>
    //                     <p class="text-muted small">Last updated: ${data.lastUpdated}</p>
    //                 `;
    //             })
    //             .catch(error => {
    //                 loadingSpinner.style.display = 'none';
    //                 resultText.textContent = 'Error fetching exchange rate. Please try again.';
    //                 console.error('Error:', error);
    //             });
    //         */

    //     }, 1000);
    // });

    // Initialize dropdown options
    const c_object = {
        "code": "INR",
        "name": "Indian Rupee",
        "flag": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 18\"><rect width=\"24\" height=\"6\" fill=\"#f93\"/><rect width=\"24\" height=\"6\" y=\"6\" fill=\"#fff\"/><rect width=\"24\" height=\"6\" y=\"12\" fill=\"#128807\"/><circle cx=\"12\" cy=\"9\" r=\"1.8\" fill=\"#008\"/><circle cx=\"12\" cy=\"9\" r=\"1.6\" fill=\"#fff\"/><circle cx=\"12\" cy=\"9\" r=\"0.4\" fill=\"#008\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(15,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(30,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(45,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(60,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(75,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(90,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(105,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(120,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(135,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(150,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(165,12,9)\"/><path d=\"M12,7.5 L12,10.5\" stroke=\"#008\" stroke-width=\"0.2\" transform=\"rotate(180,12,9)\"/></svg>",
        id: 5
    };
    selectCurrency(c_object);
});
