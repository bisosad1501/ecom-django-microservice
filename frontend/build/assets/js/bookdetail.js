// utils.js - Các hàm tiện ích dùng chung
const utils = {
    showLoading() {
        const existingOverlay = document.getElementById('loading-overlay');
        if (existingOverlay) return;

        const loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
            </div>
        `;
        loadingOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        document.body.appendChild(loadingOverlay);
    },

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        loadingOverlay?.remove();
    },

    showErrorMessage(message, type = 'danger') {
        const existingAlerts = document.querySelectorAll('.api-error-alert');
        existingAlerts.forEach(alert => alert.remove());

        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} position-fixed top-0 start-0 end-0 text-center api-error-alert`;
        alertContainer.style.zIndex = '9999';
        alertContainer.textContent = message;
        document.body.appendChild(alertContainer);

        setTimeout(() => alertContainer.remove(), 3000);
    },

    escapeHtml(unsafe) {
        return unsafe
            ?.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;") || '';
    },

    formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount || 0);
    },

    parseDimensions(dimensionsString) {
        try {
            // Kiểm tra nếu chuỗi rỗng hoặc không hợp lệ
            if (!dimensionsString) {
                return { length: 0, width: 0, height: 0 };
            }

            // Tách các giá trị
            const matches = dimensionsString.match(/\('(\w+)',\s*(\d+(?:\.\d+)?)\)/g);

            const dimensions = {
                length: 0,
                width: 0,
                height: 0
            };

            if (matches) {
                matches.forEach(match => {
                    const [, key, value] = match.match(/\('(\w+)',\s*(\d+(?:\.\d+)?)\)/);
                    dimensions[key] = parseFloat(value);
                });
            }

            return dimensions;
        } catch (error) {
            console.error('Lỗi phân tích kích thước:', error);
            return { length: 0, width: 0, height: 0 };
        }
    },

    renderStarRating(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;

        return `
            ${'<i class="bi bi-star-fill text-warning"></i>'.repeat(fullStars)}
            ${halfStar ? '<i class="bi bi-star-half text-warning"></i>' : ''}
            ${'<i class="bi bi-star text-warning"></i>'.repeat(emptyStars)}
        `;
    }
};

// ui.js - Đối tượng quản lý giao diện
const ui = {
    updateTextContent(elementId, text, fallbackText = 'Chưa cung cấp') {
        const element = document.getElementById(elementId);
        element && (element.textContent = text || fallbackText);
    },

    updateImageSource(elementId, src, alt = '') {
        const element = document.getElementById(elementId);
        if (element) {
            element.src = utils.escapeHtml(src);
            element.alt = utils.escapeHtml(alt);
        }
    },

    renderAdditionalImages(images) {
    const container = document.getElementById('additional-images');
    if (!container) return;

    // Kiểm tra nếu không có ảnh
    if (!images || images.length === 0) {
        container.style.display = 'none';
        return;
    }

    // Hiển thị container
    container.style.display = 'block';

    // Render thumbnails
    container.innerHTML = images.map((img, index) => `
        <div class="thumbnail-item" onclick="selectThumbnail(this, ${index})">
            <img src="${utils.escapeHtml(img)}" 
                 class="img-thumbnail me-2" 
                 style="width: 80px; height: 80px; object-fit: cover;" 
                 alt="Ảnh phụ ${index + 1}">
        </div>
    `).join('');
},

    setAddToCartButtonState(book, addToCartCallback) {
        const addToCartButton = document.getElementById('add-to-cart-btn');
        if (addToCartButton) {
            addToCartButton.disabled = book.stock_quantity <= 0;
            addToCartButton.textContent = book.stock_quantity > 0 ? 'Thêm vào giỏ hàng' : 'Hết hàng';
            addToCartButton.onclick = () => addToCartCallback(book._id);
        }
    }
};

// book.js - Xử lý logic cho book detail
class BookDetail {
    constructor() {
        this.API_BASE_URL = this.getBaseUrl();
    }

    getBaseUrl() {
        const hostname = window.location.hostname;
        return hostname === 'localhost' || hostname === '127.0.0.1'
            ? 'http://localhost:8002/books/'
            : '/books/';
    }

    async fetchBookDetails(bookId) {
        try {
            utils.showLoading();
            const response = await fetch(`${this.API_BASE_URL}detail/${bookId}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error(`Không thể tải chi tiết sách: ${response.status}`);

            const book = await response.json();
            this.renderBookDetails(book);
        } catch (error) {
            console.error('Lỗi tải chi tiết sách:', error);
            utils.showErrorMessage(error.message);
        } finally {
            utils.hideLoading();
        }
    }

    renderBookDetails(book) {
        // Cập nhật các trường thông tin
        const fieldsMapping = {
            'book-title': book.title,
            'book-subtitle': book.subtitle,
            'book-author': book.author,
            'book-isbn': book.isbn,
            'book-publisher': book.publisher,
            'book-publication-date': book.publication_date,
            'book-description': book.description,
            'book-category': book.category,
            'book-language': book.language,
            'book-pages': book.pages,
            'book-sku': book.sku,
            'book-stock': book.stock_quantity,
            'book-rating': book.rating?.toFixed(1),
            'book-total-reviews': book.total_reviews
        };

        Object.entries(fieldsMapping).forEach(([elementId, value]) =>
            ui.updateTextContent(elementId, value)
        );

        // Xử lý giá
        const priceElement = document.getElementById('book-price');
        const salePriceElement = document.getElementById('book-sale-price');
        if (priceElement && salePriceElement) {
            if (book.sale_price) {
                priceElement.textContent = utils.formatCurrency(book.sale_price);
                salePriceElement.textContent = utils.formatCurrency(book.price);
                salePriceElement.style.display = 'inline';
            } else {
                priceElement.textContent = utils.formatCurrency(book.price);
                salePriceElement.style.display = 'none';
            }
        }

        // Xử lý kích thước
        const dimensions = utils.parseDimensions(book.dimensions);
        ui.updateTextContent('book-dimensions',
            `Dài ${dimensions.length}cm x Rộng ${dimensions.width}cm x Cao ${dimensions.height}cm`
        );

        // Xử lý ảnh
        ui.updateImageSource('cover-image', book.cover_image, book.title);

        // Xử lý ảnh phụ
        let additionalImages = [];
    try {
        // Kiểm tra và parse ảnh phụ
        if (book.additional_images) {
            // Nếu đã là mảng thì giữ nguyên
            if (Array.isArray(book.additional_images)) {
                additionalImages = book.additional_images;
            }
            // Nếu là chuỗi JSON
            else if (typeof book.additional_images === 'string') {
                // Thử parse JSON, thay thế nháy đơn bằng nháy kép
                additionalImages = JSON.parse(
                    book.additional_images
                        .replace(/'/g, '"')
                        .replace(/\\/g, '')
                );
            }
        }
    } catch (error) {
        console.error('Lỗi parse ảnh phụ:', error);
        additionalImages = [];
    }

    // Render ảnh phụ
    ui.renderAdditionalImages(additionalImages);


        // Xử lý đánh giá
        const ratingElement = document.querySelector('.rating');
        if (ratingElement) {
            ratingElement.innerHTML = utils.renderStarRating(book.rating);
        }

        // Trạng thái nút thêm vào giỏ hàng
        ui.setAddToCartButtonState(book, this.addToCart);
    }

    async addToCart(bookId) {
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
                    book_id: bookId,
                    quantity: 1
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Không thể thêm vào giỏ hàng");
            }

            Swal.fire({
                icon: 'success',
                title: 'Thành công!',
                text: 'Đã thêm sách vào giỏ hàng',
                timer: 1500
            });
        } catch (error) {
            console.error("Lỗi:", error);
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: error.message
            });
        }
    }
}

// main.js - Khởi tạo và xử lý chung
document.addEventListener('DOMContentLoaded', function () {
    const bookDetail = new BookDetail();

    function initPage() {
        const urlParams = new URLSearchParams(window.location.search);
        const bookId = urlParams.get('id');

        if (bookId) {
            bookDetail.fetchBookDetails(bookId);
        } else {
            const container = document.getElementById('book-detail-container');
            container && (container.innerHTML = `
                <div class="alert alert-warning text-center mt-5">
                    Không tìm thấy thông tin sách
                </div>
            `);
        }
    }

    // Gán hàm addToCart vào window để có thể gọi từ HTML
    window.addToCart = bookDetail.addToCart.bind(bookDetail);

    initPage();
});
