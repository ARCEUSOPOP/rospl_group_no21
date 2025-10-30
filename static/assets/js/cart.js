// Initialize cart as empty object if it doesn't exist in localStorage
if (!localStorage.getItem('cart')) {
    localStorage.setItem('cart', JSON.stringify({}));
}

// Add click event listeners to all cart buttons
document.addEventListener('DOMContentLoaded', function() {
    const cartButtons = document.querySelectorAll('.cart');
    cartButtons.forEach(button => {
        button.addEventListener('click', function() {
            addToCart(this.id);
        });
    });

    updateCartPopover();
});

// Function to add items to cart
function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart'));
    
    // Initialize if product is not in cart
    if (!(productId in cart)) {
        cart[productId] = 1;
    } else {
        cart[productId] += 1;
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartPopover();
    showCartNotification();
}

// Function to update cart display
function updateCartPopover() {
    const cart = JSON.parse(localStorage.getItem('cart'));
    let totalItems = Object.values(cart).reduce((a, b) => a + b, 0);
    
    document.getElementById('cartCount').textContent = totalItems;
}

// Function to show notification when item is added
function showCartNotification() {
    const notification = document.getElementById('cartNotification');
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 2000);
}

// Function to clear cart
function clearCart() {
    localStorage.setItem('cart', JSON.stringify({}));
    updateCartPopover();
}