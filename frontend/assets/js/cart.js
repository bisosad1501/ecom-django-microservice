class CartManager {
    constructor() {
        this.BASE_URL = 'http://localhost:8003/cart/';
        this.userId = localStorage.getItem('userId');
        this.accessToken = localStorage.getItem('accessToken');
        this.deleteItemId = null;
        this.initEventListeners();
    }

    initEventListeners() {
        document.addEventListener('DOMContentLoaded', () => this.loadCart());
        document.addEventListener('cartUpdated', () => this.updateCartCount());

        const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', () => this.removeItemFromCart(this.deleteItemId));
        }
    }

    async updateCartCount() {
        try {
            const response = await fetch(`${this.BASE_URL}get/${this.userId}/`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${this.accessToken}` }
            });

            const data = await response.json();
            document.querySelectorAll('.cart-badge').forEach(badge => {
                badge.textContent = data.total_items_count || 0;
            });
        } catch (error) {
            console.error('Lỗi cập nhật số lượng giỏ hàng:', error);
        }
    }

    showLoading() {
        Swal.fire({ title: 'Đang tải...', didOpen: () => Swal.showLoading() });
    }

    hideLoading() {
        Swal.close();
    }

    async loadCart() {
        if (!this.userId) {
            this.showLoginRequiredMessage();
            return;
        }

        try {
            this.showLoading();
            const response = await fetch(`${this.BASE_URL}get/${this.userId}/`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${this.accessToken}` }
            });

            const data = await response.json();
            this.renderCartItems(data.items);
            this.renderCartSummary(data);
            document.dispatchEvent(new Event('cartUpdated'));
        } catch (error) {
            console.error('Lỗi tải giỏ hàng:', error);
            this.showErrorMessage('Không thể tải giỏ hàng');
        } finally {
            this.hideLoading();
        }
    }

    renderCartItems(items) {
        const container = document.getElementById('cart-items-container');
        container.innerHTML = '';

        if (items.length === 0) {
            container.innerHTML = `<div class="alert alert-info text-center">Giỏ hàng của bạn đang trống</div>`;
            return;
        }

        items.forEach(item => {
            container.insertAdjacentHTML('beforeend', `
                <div class="card mb-3" data-book-id="${item.product_id}">
                    <div class="card-body d-flex align-items-center">
                        <img src="" class="cart-item-image me-3 book-image" alt="${item.product_name}">
                        <div class="flex-grow-1">
                            <h5 class="card-title">${item.product_name}</h5>
                            <p class="card-text">
                                <span class="text-muted ${item.original_price ? 'text-decoration-line-through' : ''}">
                                    ${this.formatCurrency(item.original_price || item.sale_price)}
                                </span>
                                ${item.original_price ? `<span class="text-danger ms-2">${this.formatCurrency(item.sale_price)}</span>` : ''}
                            </p>
                            <div class="d-flex align-items-center">
                                <button class="btn btn-sm btn-outline-secondary decrease-qty">-</button>
                                <input type="number" class="form-control form-control-sm mx-2 quantity-control" value="${item.quantity}" min="1">
                                <button class="btn btn-sm btn-outline-secondary increase-qty">+</button>
                            </div>
                            ${item.discount_percentage ? `<small class="text-success">Giảm ${item.discount_percentage}%</small>` : ''}
                        </div>
                        <button class="btn btn-danger btn-sm remove-item"><i class="bi bi-trash"></i></button>
                    </div>
                </div>
            `);
        });

        this.addCartItemEventListeners();
        this.fetchBookImages(items);
    }

    renderCartSummary(cartData) {
        document.getElementById('total-quantity').textContent = cartData.total_items_count || 0;
        document.getElementById('total-price').textContent = this.formatCurrency(cartData.total_cart_value || 0);

        if (cartData.total_original_value && cartData.total_savings) {
            document.getElementById('original-price').textContent = this.formatCurrency(cartData.total_original_value);
            document.getElementById('total-savings').textContent = this.formatCurrency(cartData.total_savings);
            document.getElementById('savings-section').classList.remove('d-none');
        } else {
            document.getElementById('savings-section').classList.add('d-none');
        }

        document.getElementById('checkout-btn').disabled = cartData.total_items_count === 0;
    }

    fetchBookImages(items) {
        items.forEach(item => {
            fetch(`http://localhost:8002/books/detail/${item.product_id}/`)
                .then(response => response.json())
                .then(book => {
                    const bookElement = document.querySelector(`[data-book-id="${item.product_id}"]`);
                    if (bookElement) {
                        bookElement.querySelector('.book-image').src = book.cover_image || '';
                    }
                });
        });
    }

    addCartItemEventListeners() {
        document.querySelectorAll('.increase-qty').forEach(btn => {
            btn.addEventListener('click', e => {
                const input = e.target.previousElementSibling;
                input.value = parseInt(input.value) + 1;
                this.updateItemQuantity(input);
            });
        });

        document.querySelectorAll('.decrease-qty').forEach(btn => {
            btn.addEventListener('click', e => {
                const input = e.target.nextElementSibling;
                if (parseInt(input.value) > 1) {
                    input.value = parseInt(input.value) - 1;
                    this.updateItemQuantity(input);
                }
            });
        });

        document.querySelectorAll('.quantity-control').forEach(input => {
            input.addEventListener('change', e => this.updateItemQuantity(e.target));
        });

        document.querySelectorAll('.remove-item').forEach(btn => {
            btn.addEventListener('click', e => {
                this.deleteItemId = e.target.closest('[data-book-id]').dataset.bookId;
                new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
            });
        });
    }

    async updateItemQuantity(inputElement) {
        const bookId = inputElement.closest('[data-book-id]').dataset.bookId;
        const quantity = parseInt(inputElement.value);

        if (isNaN(quantity) || quantity < 1) {
            inputElement.value = 1;
            return;
        }

        try {
            const response = await fetch(`${this.BASE_URL}update-item/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${this.accessToken}` },
                body: JSON.stringify({ user_id: this.userId, book_id: bookId, quantity })
            });

            if (!response.ok) throw new Error('Cập nhật số lượng thất bại');
            this.loadCart();
        } catch (error) {
            console.error('Lỗi:', error);
            this.showErrorMessage('Không thể cập nhật số lượng');
        }
    }

    async removeItemFromCart(bookId) {
        try {
            const response = await fetch(`${this.BASE_URL}remove-item/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${this.accessToken}` },
                body: JSON.stringify({ user_id: this.userId, book_id: bookId })
            });

            if (!response.ok) throw new Error('Xóa sản phẩm thất bại');

            bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal')).hide();
            this.loadCart();
        } catch (error) {
            console.error('Lỗi:', error);
            this.showErrorMessage('Không thể xóa sản phẩm');
        }
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount || 0);
    }

    showLoginRequiredMessage() {
        Swal.fire({
            icon: 'warning',
            title: 'Thông báo',
            text: 'Bạn cần đăng nhập để xem giỏ hàng',
            confirmButtonText: 'Đăng nhập',
            showCancelButton: true,
            cancelButtonText: 'Hủy'
        }).then(result => {
            if (result.isConfirmed) window.location.href = '/login';
        });
    }

    showErrorMessage(message) {
        Swal.fire({ icon: 'error', title: 'Lỗi', text: message });
    }
}

const cartManager = new CartManager();