document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validation cơ bản
    if (!username || !email || !password) {
        Swal.fire({
            icon: 'warning',
            title: 'Lỗi',
            text: 'Vui lòng điền đầy đủ thông tin'
        });
        return;
    }

    if (password !== confirmPassword) {
        Swal.fire({
            icon: 'error',
            title: 'Lỗi',
            text: 'Mật khẩu không khớp'
        });
        return;
    }

    // Hiển thị loading
    Swal.fire({
        title: 'Đang xử lý...',
        html: 'Vui lòng chờ',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading()
        }
    });

    // Log dữ liệu gửi đi để kiểm tra
    console.log('Sending registration data:', {
        username,
        email,
        password
    });

    fetch('http://localhost/user/register/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: username,
        email: email,
        password: password
    })
})
.then(response => {
    // Kiểm tra status code
    if (response.status === 201) {
        // Đăng ký thành công
        return response.json();
    } else {
        // Xử lý các status code khác
        throw new Error('Đăng ký không thành công');
    }
})
.then(data => {
    // Hiển thị thông báo đăng ký thành công
    Swal.fire({
        icon: 'success',
        title: 'Đăng Ký Thành Công',
        text: 'Tài khoản của bạn đã được tạo',
        timer: 2000,
        showConfirmButton: false
    }).then(() => {
        // Chuyển đến trang đăng nhập
        window.location.href = 'login.html';
    });
})
.catch(error => {
    // Xử lý lỗi
    Swal.fire({
        icon: 'error',
        title: 'Lỗi',
        text: error.message
    });
});
});
