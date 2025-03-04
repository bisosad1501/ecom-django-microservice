document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo Flash Sale Countdown
    initFlashSaleCountdown();

    // Khởi tạo Product Carousel
    initProductCarousels();

    // Khởi tạo Wishlist Handling
    initWishlistHandling();

    // Khởi tạo Category Tabs
    initCategoryTabs();
});

// Flash Sale Countdown
function initFlashSaleCountdown() {
    const endTime = new Date();
    endTime.setHours(endTime.getHours() + 2); // Set countdown 2 hours from now

    function updateCountdown() {
        const now = new Date();
        const timeDiff = endTime - now;

        if (timeDiff <= 0) {
            // Reset countdown or hide flash sale section
            document.querySelector('.flash-sale').style.display = 'none';
            return;
        }

        const hours = Math.floor(timeDiff / (1000 * 60 * 60));
        const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

        // Update countdown display
        document.querySelector('.time-box:nth-child(1)').textContent = hours.toString().padStart(2, '0');
        document.querySelector('.time-box:nth-child(3)').textContent = minutes.toString().padStart(2, '0');
        document.querySelector('.time-box:nth-child(5)').textContent = seconds.toString().padStart(2, '0');
    }

    // Update countdown every second
    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Product Carousels
function initProductCarousels() {
    // Initialize Bootstrap carousel
    const mainBanner = document.getElementById('mainBanner');
    if (mainBanner) {
        new bootstrap.Carousel(mainBanner, {
            interval: 5000,
            wrap: true
        });
    }
}

// Wishlist Handling
function initWishlistHandling() {
    const wishlistIcons = document.querySelectorAll('.wishlist-icon');

    wishlistIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const productId = this.closest('.product-card').dataset.productId;
            toggleWishlist(productId, this);
        });

        // Check if product is in wishlist and update icon
        const productId = icon.closest('.product-card').dataset.productId;
        updateWishlistIcon(productId, icon);
    });
}

function toggleWishlist(productId, icon) {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlistItems')) || [];
    const index = wishlistItems.indexOf(productId);

    if (index === -1) {
        // Add to wishlist
        wishlistItems.push(productId);
        icon.querySelector('i').classList.remove('far');
        icon.querySelector('i').classList.add('fas');
        icon.querySelector('i').style.color = '#dc3545';
    } else {
        // Remove from wishlist
        wishlistItems.splice(index, 1);
        icon.querySelector('i').classList.remove('fas');
        icon.querySelector('i').classList.add('far');
        icon.querySelector('i').style.color = '';
    }

    localStorage.setItem('wishlistItems', JSON.stringify(wishlistItems));
    updateWishlistCount();
}

function updateWishlistIcon(productId, icon) {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlistItems')) || [];
    if (wishlistItems.includes(productId)) {
        icon.querySelector('i').classList.remove('far');
        icon.querySelector('i').classList.add('fas');
        icon.querySelector('i').style.color = '#dc3545';
    }
}

// Category Tabs
function initCategoryTabs() {
    const categoryTabs = document.querySelectorAll('.category-tabs .btn');
    const productCards = document.querySelectorAll('.product-card');

    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            categoryTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');

            const category = this.textContent.toLowerCase();

            // Filter products
            productCards.forEach(card => {
                if (category === 'tất cả') {
                    card.style.display = '';
                } else {
                    const productCategory = card.dataset.category.toLowerCase();
                    card.style.display = productCategory === category ? '' : 'none';
                }
            });
        });
    });
}

// Add to Cart Handling
function addToCart(productId) {
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    cartItems.push(productId);
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    updateCartCount();

    // Show success message
    showToast('Sản phẩm đã được thêm vào giỏ hàng');
}

// Toast Notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.classList.add('toast-notification');
    toast.textContent = message;
    document.body.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Lazy Loading for Images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});