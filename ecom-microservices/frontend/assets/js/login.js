document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        console.error('Không tìm thấy form đăng nhập');
        return;
    }

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        // Validate input
        if (!validateInput(username, password)) return;

        // Hiển thị loading
        Swal.fire({
            title: 'Đang xác thực...',
            html: 'Vui lòng chờ giây lát',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading()
            }
        });

        // Gửi request đăng nhập
        fetch('http://localhost/user/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(async (response) => {
            console.log('Response Status:', response.status);

            // Kiểm tra status code
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Lỗi HTTP: ${response.status} - ${errorText}`);
            }

            // Parse JSON
            return response.json();
        })
        .then(data => {
            if (data.access && data.refresh) {
                // Lưu tokens
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);

                localStorage.setItem('userName', username);
                localStorage.setItem('userId', data.user_id);

                console.log('user_id:', data.user_id);


                Swal.fire({
                    icon: 'success',
                    title: 'Đăng nhập thành công!',
                    text: 'Chuyển đến trang chủ',
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    window.location.href = 'index.html';
                });
            }
        })
        .catch(error => {
            console.error('Lỗi đăng nhập chi tiết:', error);

            // Hiển thị thông báo lỗi cụ thể
            Swal.fire({
                icon: 'error',
                title: 'Đăng Nhập Thất Bại',
                text: error.message || 'Không thể đăng nhập. Vui lòng thử lại.',
                footer: 'Kiểm tra lại thông tin đăng nhập'
            });
        });
    });
});

// Hàm validate input
function validateInput(username, password) {
    if (!username) {
        Swal.fire({
            icon: 'warning',
            title: 'Lỗi',
            text: 'Vui lòng nhập tên đăng nhập'
        });
        return false;
    }

    if (!password) {
        Swal.fire({
            icon: 'warning',
            title: 'Lỗi',
            text: 'Vui lòng nhập mật khẩu'
        });
        return false;
    }

    if (password.length < 6) {
        Swal.fire({
            icon: 'warning',
            title: 'Lỗi',
            text: 'Mật khẩu phải có ít nhất 6 ký tự'
        });
        return false;
    }

    return true;
}