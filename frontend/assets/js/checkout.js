document.addEventListener("DOMContentLoaded", function () {
    const baseURL = "http://localhost:8003";
    const userId = localStorage.getItem('userId');
    const accessToken = localStorage.getItem('accessToken');

    // Track selected shipping and payment methods
    let selectedShippingMethod = null;
    let selectedPaymentMethod = null;

    // Function to load the cart summary
    function loadCartSummary() {
        if (!userId) {
            showLoginRequiredMessage();
            return;
        }

        fetch(`${baseURL}/cart/get/${userId}/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        })
            .then(response => response.json())
            .then(cartData => {
                const cartItems = cartData.items || [];
                let subtotal = cartData.total_cart_value || 0;
                const originalTotal = cartData.total_original_value || 0;
                const totalSavings = cartData.total_savings || 0;

                // Calculate shipping fee based on selected method
                const shippingFee = calculateShippingFee(subtotal, selectedShippingMethod);
                const discount = 0; // Discount example
                const total = subtotal + shippingFee - discount;

                // Render cart items in summary section
                renderCartItems(cartItems);

                // Update summary totals
                document.getElementById("subtotal").textContent = formatCurrency(subtotal);
                document.getElementById("shipping-fee").textContent = formatCurrency(shippingFee);
                document.getElementById("discount").textContent = "-" + formatCurrency(discount);
                document.getElementById("total").textContent = formatCurrency(total);

                // Show original price and savings if applicable
                if (totalSavings > 0) {
                    document.getElementById("original-price").textContent = formatCurrency(originalTotal);
                    document.getElementById("total-savings").textContent = formatCurrency(totalSavings);
                    document.getElementById("savings-section").classList.remove("d-none");
                } else {
                    document.getElementById("savings-section").classList.add("d-none");
                }
            })
            .catch(error => {
                console.error("Error loading cart summary:", error);
            });
    }

    // Calculate shipping fee based on selected method and order value
    function calculateShippingFee(subtotal, shippingMethod) {
        if (!shippingMethod) return 20000; // Default fee

        switch(shippingMethod) {
            case 'standard':
                return subtotal > 500000 ? 0 : 20000; // Free shipping for orders over 500,000₫
            case 'express':
                return 35000;
            case 'same-day':
                return 50000;
            default:
                return 20000;
        }
    }

    // Initialize shipping methods
    function initializeShippingMethods() {
        const shippingContainer = document.querySelector(".shipping-methods-container");
        if (!shippingContainer) return;

        const methods = [
            { id: 'standard', name: 'Giao hàng tiêu chuẩn', fee: '20.000₫', time: '3-5 ngày', icon: 'fa-truck' },
            { id: 'express', name: 'Giao hàng nhanh', fee: '35.000₫', time: '1-2 ngày', icon: 'fa-shipping-fast' },
            { id: 'same-day', name: 'Giao trong ngày', fee: '50.000₫', time: 'Trong ngày', icon: 'fa-truck-loading' }
        ];

        shippingContainer.innerHTML = methods.map(method => `
            <div class="form-check shipping-method mb-2 border rounded p-3">
                <input class="form-check-input" type="radio" name="shipping-method" 
                       id="shipping-${method.id}" value="${method.id}">
                <label class="form-check-label d-flex justify-content-between align-items-center" for="shipping-${method.id}">
                    <div>
                        <i class="fas ${method.icon} me-2 text-primary"></i>
                        <span class="fw-medium">${method.name}</span>
                        <small class="d-block text-muted">Thời gian: ${method.time}</small>
                    </div>
                    <span class="fee">${method.fee}</span>
                </label>
            </div>
        `).join('');

        // Add event listeners for shipping method selection
        document.querySelectorAll('input[name="shipping-method"]').forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    selectedShippingMethod = this.value;
                    loadCartSummary(); // Recalculate totals
                }
            });
        });
    }

    // Initialize payment methods
    function initializePaymentMethods() {
        const paymentContainer = document.querySelector(".payment-methods-container");
        if (!paymentContainer) return;

        const methods = [
            { id: 'cod', name: 'Thanh toán khi nhận hàng (COD)', icon: 'fa-money-bill-wave' },
            { id: 'transfer', name: 'Chuyển khoản ngân hàng', icon: 'fa-university' },
            { id: 'credit', name: 'Thẻ tín dụng / Ghi nợ', icon: 'fa-credit-card' },
            { id: 'momo', name: 'Ví MoMo', icon: 'fa-wallet' }
        ];

        paymentContainer.innerHTML = methods.map(method => `
            <div class="form-check payment-method mb-2 border rounded p-3">
                <input class="form-check-input" type="radio" name="payment-method" 
                       id="payment-${method.id}" value="${method.id}">
                <label class="form-check-label d-flex align-items-center" for="payment-${method.id}">
                    <i class="fas ${method.icon} me-2 text-primary"></i>
                    <span>${method.name}</span>
                </label>
            </div>
        `).join('');

        // Add event listeners for payment method selection
        document.querySelectorAll('input[name="payment-method"]').forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    // ... (continuing from existing code)
                    selectedPaymentMethod = this.value;
                }
            });
        });
    }

    // Render cart items in the order summary section with detailed info
    function renderCartItems(items) {
        const container = document.querySelector(".order-items");
        if (!container) return;

        container.innerHTML = '';

        if (items.length === 0) {
            container.innerHTML = '<div class="alert alert-info text-center">Giỏ hàng của bạn đang trống</div>';
            return;
        }

        items.forEach(item => {
            container.insertAdjacentHTML('beforeend', `
                <div class="card mb-3" data-book-id="${item.product_id}">
                    <div class="card-body p-2">
                        <div class="d-flex align-items-center">
                            <img src="" class="cart-item-image me-2 book-image" style="width: 60px; height: 60px; object-fit: cover;" alt="${item.product_name}">
                            <div class="flex-grow-1">
                                <h6 class="mb-1">${item.product_name}</h6>
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <span class="badge bg-primary me-1">${item.quantity}</span>
                                        <span class="text-muted ${item.original_price && item.original_price > item.sale_price ? 'text-decoration-line-through' : ''}">
                                            ${formatCurrency(item.original_price || item.sale_price)}
                                        </span>
                                        ${item.original_price && item.original_price > item.sale_price ? 
                                            `<span class="text-danger ms-1">${formatCurrency(item.sale_price)}</span>` : ''}
                                    </div>
                                    <span class="fw-bold">${formatCurrency(item.quantity * item.sale_price)}</span>
                                </div>
                                ${item.discount_percentage ? `<small class="text-success">Giảm ${item.discount_percentage}%</small>` : ''}
                            </div>
                        </div>
                    </div>
                </div>
            `);
        });

        // Fetch book images like in cart.js
        fetchBookImages(items);
    }

    // Fetch book images from book service
    function fetchBookImages(items) {
        items.forEach(item => {
            fetch(`http://localhost:8002/books/detail/${item.product_id}/`)
                .then(response => response.json())
                .then(book => {
                    const bookElement = document.querySelector(`[data-book-id="${item.product_id}"]`);
                    if (bookElement) {
                        bookElement.querySelector('.book-image').src = book.cover_image || '';
                    }
                })
                .catch(error => console.error('Error fetching book image:', error));
        });
    }

    // Format currency in VND
    function formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount || 0);
    }

    // Show login required message
    function showLoginRequiredMessage() {
        Swal.fire({
            icon: 'warning',
            title: 'Thông báo',
            text: 'Bạn cần đăng nhập để thanh toán',
            confirmButtonText: 'Đăng nhập',
            showCancelButton: true,
            cancelButtonText: 'Hủy'
        }).then(result => {
            if (result.isConfirmed) window.location.href = '/login.html';
        });
    }

    // Initialize form field autocomplete from user data
    function initializeFormFields() {
        if (!userId) return;

        fetch(`http://localhost:8001/users/${userId}/`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        })
            .then(response => response.json())
            .then(user => {
                if (document.getElementById('fullName'))
                    document.getElementById('fullName').value = user.name || '';
                if (document.getElementById('email'))
                    document.getElementById('email').value = user.email || '';
                if (document.getElementById('phone'))
                    document.getElementById('phone').value = user.phone || '';
                if (document.getElementById('address'))
                    document.getElementById('address').value = user.address || '';
            })
            .catch(error => console.error('Error loading user data:', error));
    }

    // Apply coupon code
    const applyCouponBtn = document.getElementById("apply-coupon");
    if (applyCouponBtn) {
        applyCouponBtn.addEventListener("click", function() {
            const couponCode = document.getElementById("coupon-code").value;
            if (!couponCode.trim()) {
                Swal.fire("Lỗi", "Vui lòng nhập mã giảm giá", "error");
                return;
            }

            Swal.fire("Thông báo", "Chức năng đang được phát triển", "info");
        });
    }

    // Load Vietnam locations for address selection
function initializeLocationSelectors() {
    const provinceSelect = document.getElementById('province');
    const districtSelect = document.getElementById('district');
    const wardSelect = document.getElementById('ward');

    // Disable cascading selects initially
    districtSelect.disabled = true;
    wardSelect.disabled = true;

    // Fetch provinces from Vietnam API
    fetch('https://provinces.open-api.vn/api/p/')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(provinces => {
            provinceSelect.innerHTML = '<option value="">Chọn tỉnh/thành phố</option>';
            provinces.forEach(province => {
                provinceSelect.innerHTML += `<option value="${province.code}">${province.name}</option>`;
            });
        })
        .catch(error => {
            console.error('Error loading provinces:', error);
            loadFallbackProvinces();
        });

    // Handle province change
    provinceSelect.addEventListener('change', function() {
        const provinceCode = this.value;
        districtSelect.innerHTML = '<option value="">Chọn quận/huyện</option>';
        wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';
        wardSelect.disabled = true;

        if (!provinceCode) {
            districtSelect.disabled = true;
            return;
        }

        districtSelect.disabled = false;

        // Show loading indicator
        districtSelect.innerHTML = '<option value="">Đang tải...</option>';

        // Fetch districts for selected province
        fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(provinceData => {
                districtSelect.innerHTML = '<option value="">Chọn quận/huyện</option>';
                const districts = provinceData.districts;
                districts.forEach(district => {
                    districtSelect.innerHTML += `<option value="${district.code}">${district.name}</option>`;
                });
            })
            .catch(error => {
                console.error('Error loading districts:', error);
                districtSelect.innerHTML = '<option value="">Lỗi tải dữ liệu</option>';
            });
    });

    // Handle district change
    districtSelect.addEventListener('change', function() {
        const districtCode = this.value;
        wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';

        if (!districtCode) {
            wardSelect.disabled = true;
            return;
        }

        wardSelect.disabled = false;

        // Show loading indicator
        wardSelect.innerHTML = '<option value="">Đang tải...</option>';

        // Fetch wards for selected district
        fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(districtData => {
                wardSelect.innerHTML = '<option value="">Chọn phường/xã</option>';
                const wards = districtData.wards;
                wards.forEach(ward => {
                    wardSelect.innerHTML += `<option value="${ward.code}">${ward.name}</option>`;
                });
            })
            .catch(error => {
                console.error('Error loading wards:', error);
                wardSelect.innerHTML = '<option value="">Lỗi tải dữ liệu</option>';
            });
    });
}

// Fallback data if API fails
function loadFallbackProvinces() {
    const commonProvinces = [
        {code: "01", name: "Hà Nội"},
        {code: "79", name: "TP. Hồ Chí Minh"},
        {code: "48", name: "Đà Nẵng"},
        {code: "92", name: "Cần Thơ"},
        {code: "31", name: "Hải Phòng"},
        {code: "75", name: "Đồng Nai"},
        {code: "77", name: "Bà Rịa - Vũng Tàu"},
        {code: "74", name: "Bình Dương"}
    ];

    const provinceSelect = document.getElementById('province');
    provinceSelect.innerHTML = '<option value="">Chọn tỉnh/thành phố</option>';
    commonProvinces.forEach(province => {
        provinceSelect.innerHTML += `<option value="${province.code}">${province.name}</option>`;
    });
}

    // Initialize the checkout page components
    function initializeCheckoutPage() {
        loadCartSummary();
        initializeFormFields();
        initializeShippingMethods();
        initializeLocationSelectors();
        initializePaymentMethods();
    }

    // Load all checkout components on page load
    initializeCheckoutPage();

    // Place order button click
    const placeOrderBtn = document.getElementById("place-order-btn");
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener("click", function (event) {
            event.preventDefault();

            if (!userId) {
                showLoginRequiredMessage();
                return;
            }

            // Validate shipping information
            const form = document.getElementById("checkout-form");
            if (form && !form.checkValidity()) {
                form.reportValidity();
                return;
            }

            // Validate shipping and payment methods
            if (!selectedShippingMethod) {
                Swal.fire("Lỗi", "Vui lòng chọn phương thức vận chuyển", "error");
                return;
            }

            if (!selectedPaymentMethod) {
                Swal.fire("Lỗi", "Vui lòng chọn phương thức thanh toán", "error");
                return;
            }

            const fullName = document.getElementById("fullName").value;
            const email = document.getElementById("email").value;
            const phone = document.getElementById("phone").value;
            const address = document.getElementById("address").value;
            const provinceElement = document.getElementById("province");
            const districtElement = document.getElementById("district");
            const wardElement = document.getElementById("ward");

            const province = provinceElement.options[provinceElement.selectedIndex].text;
            const district = districtElement.options[districtElement.selectedIndex].text;
            const ward = wardElement.options[wardElement.selectedIndex].text;

            const shippingAddress = `${address}, ${ward}, ${district}, ${province}`;

            const orderData = {
                user_id: userId,
                shipping_address: shippingAddress,
                contact_name: fullName,
                contact_email: email,
                contact_phone: phone,
                shipping_method: selectedShippingMethod,
                payment_method: selectedPaymentMethod
            };
            console.log("Sending order data:", JSON.stringify(orderData));


            fetch(`${baseURL}/orders/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify(orderData)
            })
                .then(response => response.json().then(data => ({ status: response.status, data })))
                .then(result => {
                    if (result.status === 201) {
                        Swal.fire("Thành công", "Đặt hàng thành công!", "success")
                            .then(() => {
                                window.location.href = `/order-confirmation.html?id=${result.data.order_id}`;
                            });
                    } else {
                        const errorMsg = result.data.error || "Đặt hàng thất bại.";
                        Swal.fire("Lỗi", errorMsg, "error");
                    }
                })
                .catch(error => {
                    Swal.fire("Lỗi", error.message, "error");
                });
        });
    }
});