document.addEventListener('DOMContentLoaded', function() {
    if (!window.location.pathname.includes('/booklist.html')) return;

    const API_BASE_URL = 'http://localhost:8002/books/'; // Luôn gọi API từ localhost

    function showLoading() {
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
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.7); display: flex;
            justify-content: center; align-items: center; z-index: 9999;
        `;
        document.body.appendChild(loadingOverlay);
    }

    function hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) loadingOverlay.remove();
    }

    function showErrorMessage(message) {
        const alertContainer = document.createElement('div');
        alertContainer.className = 'alert alert-danger position-fixed top-0 start-0 end-0 text-center api-error-alert';
        alertContainer.style.zIndex = '9999';
        alertContainer.textContent = message;
        document.body.appendChild(alertContainer);

        setTimeout(() => alertContainer.remove(), 3000);
    }

    function formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency', currency: 'VND'
        }).format(amount);
    }

    async function fetchBookList(params = {}) {
        try {
            showLoading();
            const queryParams = new URLSearchParams(params).toString();
            const response = await fetch(`${API_BASE_URL}?${queryParams}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error(`Lỗi: ${response.status}`);
            }

            const data = await response.json();
            renderBookList(data.books || data.results || data);
            hideLoading();
        } catch (error) {
            showErrorMessage(`Không thể tải danh sách sách: ${error.message}`);
            hideLoading();
        }
    }

    function renderBookList(books) {
        const bookListContainer = document.getElementById('book-list-container');
        const template = document.querySelector('.book-card-template');

        if (!Array.isArray(books) || books.length === 0) {
            bookListContainer.innerHTML = `
                <div class="alert alert-info text-center">Không có sách nào được tìm thấy.</div>
            `;
            return;
        }

        bookListContainer.innerHTML = "";

        books.forEach(book => {
            const bookCard = template.cloneNode(true);
            bookCard.classList.remove('d-none', 'book-card-template');

            const discountPercentage = book.sale_price && book.price
                ? Math.round(((parseFloat(book.price) - parseFloat(book.sale_price)) / parseFloat(book.price)) * 100)
                : 0;

            bookCard.querySelector('.book-cover').src = book.cover_image;
            bookCard.querySelector('.book-cover').alt = book.title;
            bookCard.querySelector('.book-title').textContent = book.title;
            bookCard.querySelector('.book-author').textContent = book.author;
            bookCard.querySelector('.book-category').textContent = book.category;

            if (discountPercentage > 0) {
                bookCard.querySelector('.discount-badge').textContent = `-${discountPercentage}%`;
                bookCard.querySelector('.discount-badge').classList.remove('d-none');
            }

            bookCard.querySelector('.book-sale-price').textContent = book.sale_price
                ? formatCurrency(book.sale_price)
                : "";
            bookCard.querySelector('.book-price').textContent = book.sale_price
                ? formatCurrency(book.price)
                : formatCurrency(book.price);

            bookCard.querySelector('.book-rating').innerHTML = renderStarRating(book.rating);

            bookCard.querySelector('.book-detail-btn').onclick = () =>
                window.location.href = `/bookdetail.html?id=${encodeURIComponent(book._id)}`;

            bookListContainer.appendChild(bookCard);
        });
    }

    function renderStarRating(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;

        return `${'★'.repeat(fullStars)}${halfStar ? '☆' : ''}${'☆'.repeat(emptyStars)}`;
    }

    fetchBookList();
});