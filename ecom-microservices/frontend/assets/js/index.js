document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo Flash Sale Countdown
    initFlashSaleCountdown();

    // Khởi tạo Product Carousel
    initProductCarousels();

    // Khởi tạo Wishlist Handling
    initWishlistHandling();

    // Khởi tạo Category Tabs
    initCategoryTabs();

    // Khởi tạo Lazy Loading cho hình ảnh
    initLazyLoadingImages();

    // Khởi tạo danh sách sản phẩm
    initializeProductList();
});

// Flash Sale Countdown
function initFlashSaleCountdown() {
    const endTime = new Date();
    endTime.setHours(endTime.getHours() + 2); // Set countdown 2 giờ từ bây giờ

    function updateCountdown() {
        const now = new Date();
        const timeDiff = endTime - now;

        if (timeDiff <= 0) {
            const flashSaleElem = document.querySelector('.flash-sale');
            if (flashSaleElem) {
                flashSaleElem.style.display = 'none';
            }
            return;
        }

        const hours = Math.floor(timeDiff / (1000 * 60 * 60));
        const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

        const timeBoxes = document.querySelectorAll('.time-box');
        if (timeBoxes.length >= 5) {
            timeBoxes[0].textContent = hours.toString().padStart(2, '0');
            timeBoxes[2].textContent = minutes.toString().padStart(2, '0');
            timeBoxes[4].textContent = seconds.toString().padStart(2, '0');
        }
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Product Carousels
function initProductCarousels() {
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
            const productCard = this.closest('.product-card');
            if (!productCard) return;
            const productId = productCard.dataset.productId;
            toggleWishlist(productId, this);
        });

        const productCard = icon.closest('.product-card');
        if (productCard) {
            const productId = productCard.dataset.productId;
            updateWishlistIcon(productId, icon);
        }
    });
}

function toggleWishlist(productId, icon) {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlistItems')) || [];
    const index = wishlistItems.indexOf(productId);

    if (index === -1) {
        wishlistItems.push(productId);
        const iElem = icon.querySelector('i');
        if (iElem) {
            iElem.classList.remove('far');
            iElem.classList.add('fas');
            iElem.style.color = '#dc3545';
        }
    } else {
        wishlistItems.splice(index, 1);
        const iElem = icon.querySelector('i');
        if (iElem) {
            iElem.classList.remove('fas');
            iElem.classList.add('far');
            iElem.style.color = '';
        }
    }

    localStorage.setItem('wishlistItems', JSON.stringify(wishlistItems));
    updateWishlistCount();
}

function updateWishlistIcon(productId, icon) {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlistItems')) || [];
    if (wishlistItems.includes(productId)) {
        const iElem = icon.querySelector('i');
        if (iElem) {
            iElem.classList.remove('far');
            iElem.classList.add('fas');
            iElem.style.color = '#dc3545';
        }
    }
}

// Category Tabs
function initCategoryTabs() {
    const categoryTabs = document.querySelectorAll('.category-tabs .btn');
    const productCards = document.querySelectorAll('.product-card');

    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            categoryTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const category = this.textContent.toLowerCase();

            productCards.forEach(card => {
                if (category === 'tất cả') {
                    card.style.display = '';
                } else {
                    const productCategory = card.dataset.category ? card.dataset.category.toLowerCase() : '';
                    card.style.display = productCategory === category ? '' : 'none';
                }
            });
        });
    });
}

// Async Add to Cart Handling with API Call
async function addToCart(productId) {
    const userId = localStorage.getItem('userId');
    const accessToken = localStorage.getItem('accessToken');

    if (!userId || !accessToken) {
        Swal.fire({
            icon: 'error',
            title: 'Lỗi',
            text: 'Bạn cần đăng nhập để thêm vào giỏ hàng'
        });
        return;
    }

    try {
        const response = await fetch("http://localhost:8003/cart/add-item/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                user_id: userId,
                product_id: productId,
                quantity: 1
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Không thể thêm vào giỏ hàng");
        }

        // Show success notification
        Swal.fire({
            icon: 'success',
            title: 'Thành công!',
            text: 'Đã thêm sản phẩm vào giỏ hàng',
            timer: 1500
        });

        // Immediately update the cart count using the global base function
        window.updateCartCount();
    } catch (error) {
        console.error("Lỗi:", error);
        Swal.fire({
            icon: 'error',
            title: 'Lỗi',
            text: error.message
        });
    }
}

// Toast Notification (still available for other notifications)
function showToast(message) {
    const toast = document.createElement('div');
    toast.classList.add('toast-notification');
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Lazy Loading for Images
function initLazyLoadingImages() {
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
}

// Constants
const DEFAULT_PRODUCT_IMAGE = '/assets/images/product-default.png';
const API_URL = 'http://localhost:8005/products/';

// Product List Handling
function initializeProductList() {
    const productListContainer = document.getElementById("dynamicProductList");
    if (!productListContainer) return;
    fetchAndRenderProducts(productListContainer);
}

async function fetchAndRenderProducts(container) {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const products = await response.json();
        renderProducts(products, container);
    } catch (error) {
        console.error("Error loading products:", error);
        showErrorMessage(container);
    }
}

function renderProducts(products, container) {
    container.innerHTML = "";
    products.forEach(product => {
        const productElement = createProductElement(product);
        container.insertAdjacentHTML('beforeend', productElement);
    });
    initializeProductEventListeners();
}

function createProductElement(product) {
    const discountPercentage = calculateDiscount(product.sale_price, product.base_price);
    const ratingStars = createRatingStars(product.rating);
    
    return `
        <div class="col-6 col-md-3">
            <div class="product-card" data-product-id="${product._id}" data-category="${product.category || ''}">
                ${createDiscountBadge(discountPercentage)}
                <div class="wishlist-icon position-absolute top-0 end-0 m-2">
                    <i class="far fa-heart"></i>
                </div>
                <img 
                    src="${product.primary_image || DEFAULT_PRODUCT_IMAGE}" 
                    class="card-img-top" 
                    alt="${product.name}"
                    onerror="this.onerror=null; this.src='${DEFAULT_PRODUCT_IMAGE}';"
                >
                <div class="card-body p-2">
                    <h6 class="card-title text-truncate">
                        <a href="product-detail.html?id=${product._id}" class="product-link">
                            ${product.name}
                        </a>
                    </h6>
                    <div class="rating mb-1">
                        ${ratingStars}
                        <span class="rating-count">(${product.review_count || 0})</span>
                    </div>
                    ${createPriceBox(product)}
                    <div class="mt-2 d-flex justify-content-between align-items-center">
                        <small class="text-muted">Đã bán ${product.total_sold || 0}</small>
                        <small class="text-primary">${product.brand || 'No Brand'}</small>
                    </div>
                    <button class="btn btn-primary btn-sm w-100 mt-2 add-to-cart" 
                            data-product-id="${product._id}">
                        <i class="fas fa-shopping-cart me-1"></i>Thêm vào giỏ
                    </button>
                </div>
            </div>
        </div>
    `;
}

function calculateDiscount(salePrice, basePrice) {
    return salePrice ? Math.round((1 - salePrice / basePrice) * 100) : 0;
}

function createDiscountBadge(discount) {
    return discount > 0 ? 
        `<div class="badge bg-danger position-absolute top-0 start-0 m-2">-${discount}%</div>` 
        : '';
}

function createRatingStars(rating) {
    const fullStars = Math.floor(rating || 0);
    const hasHalfStar = (rating || 0) % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < 5; i++) {
        if (i < fullStars) {
            stars += '<i class="fas fa-star text-warning"></i>';
        } else if (i === fullStars && hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        } else {
            stars += '<i class="far fa-star text-warning"></i>';
        }
    }
    return stars;
}

function createPriceBox(product) {
    const currentPrice = formatPrice(product.sale_price || product.base_price);
    const oldPrice = product.sale_price ? 
        `<span class="old-price">${formatPrice(product.base_price)}₫</span>` : '';
    
    return `
        <div class="price-box">
            <span class="new-price">${currentPrice}₫</span>
            ${oldPrice}
        </div>
    `;
}

function formatPrice(price) {
    return (price || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function showErrorMessage(container) {
    container.innerHTML = `
        <div class="col-12 text-center">
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Không thể tải danh sách sản phẩm. Vui lòng thử lại sau.
            </div>
        </div>
    `;
}

function initializeProductEventListeners() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (e) => {
            const productId = e.currentTarget.dataset.productId;
            // Call the async addToCart function with the product id
            addToCart(productId);
        });
    });

    document.querySelectorAll('.wishlist-icon').forEach(icon => {
        icon.addEventListener('click', (e) => {
            const productCard = e.currentTarget.closest('.product-card');
            if (!productCard) return;
            const productId = productCard.dataset.productId;
            toggleWishlist(productId, icon);
        });
    });
}

function updateWishlistCount() {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlistItems')) || [];
    const wishlistCountElem = document.getElementById('wishlistCount');
    if (wishlistCountElem) {
        wishlistCountElem.textContent = wishlistItems.length;
    }
}