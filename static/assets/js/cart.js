// Ensure a cart exists in localStorage
if (!localStorage.getItem('cart')) {
    localStorage.setItem('cart', JSON.stringify({}));
}

// Register click delegation immediately (works regardless of load timing)
document.addEventListener('click', function(evt) {
    const btn = evt.target.closest('.cart');
    if (!btn) return;
    evt.preventDefault();
    if (btn.id) addToCart(btn.id);
});

// Remove-from-cart delegation (used on checkout list)
document.addEventListener('click', function(evt) {
    const rm = evt.target.closest('.remove-from-cart');
    if (!rm) return;
    evt.preventDefault();
    const key = rm.dataset.key || '';
    const format = rm.dataset.format || 'map';
    removeFromCart(key, format);
});

// Initialize counters/rendering whether DOM is already loaded or not
(function initCartUI() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            updateCartCount();
            renderCheckoutIfPresent();
        });
    } else {
        updateCartCount();
        renderCheckoutIfPresent();
    }
})();

// Add or increment product in cart. Product id format: pr<ID>
function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    const numericId = productId.startsWith('pr') ? productId.slice(2) : productId;
    const nameElem = document.getElementById('namepr' + numericId);
    const priceElem = document.getElementById('pricepr' + numericId);
    const btnElem = document.getElementById(productId);

    // Prefer DOM elements, fallback to button data attributes
    let name = nameElem ? nameElem.innerText : '';
    let priceRaw = priceElem ? priceElem.innerText : '0';
    if (!name && btnElem && btnElem.dataset && btnElem.dataset.name) {
        name = btnElem.dataset.name;
    }
    if ((!priceRaw || priceRaw === '0') && btnElem && btnElem.dataset && btnElem.dataset.price) {
        priceRaw = btnElem.dataset.price;
    }
    const price = String(priceRaw).replace(/[^0-9.]/g, '');

    // If cart is legacy array format: [{ name, price, qty }]
    if (Array.isArray(cart)) {
        let found = false;
        for (let i = 0; i < cart.length; i++) {
            const it = cart[i];
            if (it && it.name === name) {
                it.qty = (it.qty || 0) + 1;
                found = true;
                break;
            }
        }
        if (!found) {
            cart.push({ name: name, price: parseFloat(price) || 0, qty: 1 });
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    } else {
        if (!cart[productId]) {
            // Store as [quantity, name, price]
            cart[productId] = [1, name, price];
        } else {
            cart[productId][0] = (cart[productId][0] || 0) + 1;
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    updateCartCount();
    renderCheckoutIfPresent();
}

function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    let totalItems = 0;
    if (Array.isArray(cart)) {
        for (const item of cart) {
            if (item && typeof item === 'object') {
                totalItems += Number(item.qty) || 0;
            }
        }
    } else {
        Object.values(cart).forEach(value => {
            // value is [qty, name, price]
            const qty = Array.isArray(value) ? (value[0] || 0) : (typeof value === 'number' ? value : 0);
            totalItems += qty;
        });
    }
    const counter = document.getElementById('cartCount');
    if (counter) counter.textContent = String(totalItems);
}

function clearCart() {
    localStorage.setItem('cart', JSON.stringify({}));
    updateCartCount();
    renderCheckoutIfPresent();
}

// If on checkout page, render the cart lines and totals, and populate hidden fields
function renderCheckoutIfPresent() {
    const itemsList = document.getElementById('items');
    if (!itemsList) return; // Not on checkout page

    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    itemsList.innerHTML = '';

    let totalItems = 0;
    let totalPrice = 0;

    if ((Array.isArray(cart) && cart.length === 0) || (!Array.isArray(cart) && Object.keys(cart).length === 0)) {
        itemsList.innerHTML = `<p>Your cart is empty, please add some items to your cart before checking out!</p>`;
    } else if (Array.isArray(cart)) {
        for (const it of cart) {
            const qty = Number(it.qty) || 0;
            const name = it.name || '';
            const numericPrice = parseFloat(it.price) || 0;
            totalItems += qty;
            totalPrice += qty * numericPrice;

            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${name}
                <div><b> Price : ${numericPrice}</b></div>
                <span class="badge badge-primary badge-pill">${qty}</span>
                <button class="btn btn-sm btn-danger remove-from-cart" data-format="array" data-key="${encodeURIComponent(name)}">Remove</button>
            `;
            itemsList.appendChild(li);
        }
    } else {
        for (const key in cart) {
            const [qty, name, price] = cart[key];
            const numericPrice = parseFloat(price) || 0;
            totalItems += qty;
            totalPrice += qty * numericPrice;

            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${name}
                <div><b> Price : ${numericPrice}</b></div>
                <span class="badge badge-primary badge-pill">${qty}</span>
                <button class="btn btn-sm btn-danger remove-from-cart" data-format="map" data-key="${encodeURIComponent(key)}">Remove</button>
            `;
            itemsList.appendChild(li);
        }
    }

    const totalPriceEl = document.getElementById('totalprice');
    if (totalPriceEl) totalPriceEl.innerHTML = String(totalPrice);

    const amountHidden = document.getElementById('amt');
    if (amountHidden) amountHidden.value = String(totalPrice);

    const itemsJsonHidden = document.getElementById('itemsJson');
    if (itemsJsonHidden) itemsJsonHidden.value = JSON.stringify(cart);
}

// Remove an item from cart entirely (by key for map format, by name for array format)
function removeFromCart(key, format) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    if (Array.isArray(cart) || format === 'array') {
        const name = decodeURIComponent(key);
        if (Array.isArray(cart)) {
            cart = cart.filter(it => !(it && it.name === name));
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    } else {
        const mapKey = decodeURIComponent(key);
        if (cart[mapKey]) {
            delete cart[mapKey];
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    updateCartCount();
    renderCheckoutIfPresent();
}