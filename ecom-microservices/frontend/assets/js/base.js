document.addEventListener('DOMContentLoaded', function() {
    const authButtons = document.getElementById('authButtons');
    const userProfile = document.getElementById('userProfile');
    const userNameDisplay = document.getElementById('userNameDisplay');
    const logoutBtn = document.getElementById('logoutBtn');

    // Kiểm tra trạng thái đăng nhập
    function checkLoginStatus(redirectIfNotLoggedIn = false) {
    const accessToken = localStorage.getItem('accessToken');
    const userName = localStorage.getItem('userName');
    const userId = localStorage.getItem('userId'); // Lấy userId từ localStorage
        console.log('User ID:', userId);


    if (accessToken) {
        // Đã đăng nhập
        authButtons?.classList.add('d-none');
        userProfile?.classList.remove('d-none');

        // Hiển thị tên người dùng
        if (userNameDisplay) {
            userNameDisplay.textContent = userName
                ? `Xin chào, ${userName}`
                : 'Xin chào';
        }
    } else {
        // Chưa đăng nhập
        authButtons?.classList.remove('d-none');
        userProfile?.classList.add('d-none');

        if (redirectIfNotLoggedIn) {
            window.location.href = 'login.html';
        }
    }
}


    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();

            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                }
            }).catch(error => console.error('Lỗi đăng xuất:', error));

            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('userName');

            window.location.href = 'login.html';
        });
    }

    // Lắng nghe sự kiện thay đổi localStorage
    window.addEventListener('storage', function(event) {
        if (event.key === 'accessToken') {
            checkLoginStatus();
        }
    });

    // Xử lý submenu dropdown
    function setupSubmenus() {
        const dropdownSubmenus = document.querySelectorAll('.dropdown-submenu');

        dropdownSubmenus.forEach(submenu => {
            const dropdownToggle = submenu.querySelector('.dropdown-toggle');

            dropdownToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // Đóng các submenu khác
                dropdownSubmenus.forEach(otherSubmenu => {
                    if (otherSubmenu !== submenu) {
                        otherSubmenu.querySelector('.dropdown-menu').classList.remove('show');
                    }
                });

                // Toggle submenu hiện tại
                this.nextElementSibling.classList.toggle('show');
            });
        });

        // Đóng submenu khi click ra ngoài
        document.addEventListener('click', function() {
            dropdownSubmenus.forEach(submenu => {
                submenu.querySelector('.dropdown-menu').classList.remove('show');
            });
        });
    }

    // Xử lý chuyển hướng danh mục
    function setupCategoryNavigation() {
        const categoryCards = document.querySelectorAll('.category-card');

        categoryCards.forEach(card => {
            card.addEventListener('click', function() {
                const categoryName = this.querySelector('.card-title').textContent.toLowerCase();
                window.location.href = `category.html?cat=${encodeURIComponent(categoryName)}`;
            });
        });
    }

    function setupBookLink() {
        const bookLink = document.querySelector('a[href="booklist.html"]');
        if (bookLink) {
            bookLink.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = 'booklist.html';
            });
        }
    }

    // Khởi tạo các chức năng
    checkLoginStatus();
    setupSubmenus();
    setupCategoryNavigation();
    setupBookLink();
});

async function updateCartCount() {
    const userId = localStorage.getItem('userId');
    const accessToken = localStorage.getItem('accessToken');
    const cartBadge = document.getElementById('cart-badge');

    if (!userId || !cartBadge) return; // Nếu không có user hoặc không tìm thấy badge, thoát

    try {
        const response = await fetch(`http://localhost:8003/cart/get/${userId}/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (!response.ok) throw new Error('Không thể lấy dữ liệu giỏ hàng');

        const data = await response.json();
        const itemCount = data.total_items_count || 0;

        // Cập nhật số lượng trên icon giỏ hàng
        cartBadge.textContent = itemCount;
        cartBadge.style.display = itemCount > 0 ? 'inline-block' : 'none'; // Ẩn nếu giỏ rỗng

    } catch (error) {
        console.error('Lỗi cập nhật số lượng giỏ hàng:', error);
    }
}

// Gọi hàm này mỗi khi trang load
document.addEventListener('DOMContentLoaded', updateCartCount);