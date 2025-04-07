document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.container');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');

    registerBtn.addEventListener('click', () => {
        container.classList.add('active');
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');
    });

    // Đăng ký tài khoản
    document.getElementById("registerForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (!username || !email || !password) {
            Swal.fire("Lỗi", "Vui lòng điền đầy đủ thông tin!", "warning");
            return;
        }

        if (password !== confirmPassword) {
            Swal.fire("Lỗi", "Mật khẩu không khớp!", "error");
            return;
        }

        Swal.fire({
            title: "Đang xử lý...",
            html: "Vui lòng chờ",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        fetch("http://localhost/user/register/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        })
        .then(response => {
            if (response.status === 201) return response.json();
            throw new Error("Đăng ký không thành công");
        })
        .then(() => {
            Swal.fire({
                icon: "success",
                title: "Thành công!",
                text: "Tài khoản đã được tạo!",
                showConfirmButton: false,
                timer: 1000
            }).then(() => {
                container.classList.remove("active"); // Chuyển về form đăng nhập
            });
        })
        .catch(error => Swal.fire("Lỗi", error.message, "error"));
    });

    // Đăng nhập tài khoản
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const username = document.getElementById("loginUsername").value.trim();
        const password = document.getElementById("loginPassword").value;

        if (!username || !password) {
            Swal.fire("Lỗi", "Vui lòng nhập đầy đủ thông tin!", "warning");
            return;
        }

        Swal.fire({
            title: "Đang xác thực...",
            html: "Vui lòng chờ",
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        fetch("http://localhost/user/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (!response.ok) return response.text().then(text => { throw new Error(text) });
            return response.json();
        })
        .then(data => {
            localStorage.setItem("accessToken", data.access);
            localStorage.setItem("refreshToken", data.refresh);
            localStorage.setItem("userName", username);
            localStorage.setItem("userId", data.user_id);

            Swal.fire({
                icon: "success",
                title: "Thành công!",
                text: "Đăng nhập thành công!",
                showConfirmButton: false,
                timer: 1000
            }).then(() => {
                window.location.href = "index.html";
            });
        })
        .catch(error => Swal.fire("Lỗi", error.message || "Không thể đăng nhập", "error"));
    });
});

function setupPasswordToggle() {
    document.querySelectorAll('input[type="password"]').forEach(passwordInput => {
        // Kiểm tra xem đã thêm toggle chưa
        if (!passwordInput.parentNode.querySelector('.password-toggle')) {
            // Tạo nút toggle
            const toggleBtn = document.createElement('span');
            toggleBtn.innerHTML = '<i class="bx bx-show-alt"></i>';
            toggleBtn.classList.add('password-toggle');
            toggleBtn.style.display = 'none'; // Ẩn ban đầu
            
            // Chèn nút vào parent của input
            passwordInput.parentNode.appendChild(toggleBtn);
            
            // Sự kiện input để kiểm soát hiển thị nút
            passwordInput.addEventListener('input', function() {
                const toggleBtn = this.parentNode.querySelector('.password-toggle');
                if (this.value.length > 0) {
                    toggleBtn.style.display = 'block';
                } else {
                    toggleBtn.style.display = 'none';
                }
            });
            
            // Sự kiện click để toggle
            toggleBtn.addEventListener('click', function() {
                const icon = this.querySelector('i');
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.remove('bx-show-alt');
                    icon.classList.add('bx-hide');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.remove('bx-hide');
                    icon.classList.add('bx-show-alt');
                }
            });

            // Xử lý khi xóa hết nội dung
            passwordInput.addEventListener('change', function() {
                const toggleBtn = this.parentNode.querySelector('.password-toggle');
                if (this.value.length === 0) {
                    toggleBtn.style.display = 'none';
                }
            });
        }
    });
}
// Gọi hàm setup khi trang tải
setupPasswordToggle();
