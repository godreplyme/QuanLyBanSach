//function switchForm(formType) {
//    // Tabs
//    const loginTab = document.getElementById('login-tab');
//    const registerTab = document.getElementById('register-tab');
//
//    // Forms
//    const loginForm = document.getElementById('login-form');
//    const registerForm = document.getElementById('register-form');
//
//    if (formType === 'login') {
//        // Hiển thị form đăng nhập, ẩn form đăng ký
//        loginForm.classList.remove('d-none');
//        registerForm.classList.add('d-none');
//
//        // Kích hoạt tab đăng nhập, bỏ kích hoạt tab đăng ký
//        loginTab.classList.add('active');
//        registerTab.classList.remove('active');
//    } else if (formType === 'register') {
//        // Hiển thị form đăng ký, ẩn form đăng nhập
//        registerForm.classList.remove('d-none');
//        loginForm.classList.add('d-none');
//
//        // Kích hoạt tab đăng ký, bỏ kích hoạt tab đăng nhập
//        registerTab.classList.add('active');
//        loginTab.classList.remove('active');
//    }
//}
// Hàm đọc tham số từ URL
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    console.log(urlParams);
    return urlParams.get(param);
}

// Hàm khởi tạo form dựa trên URL
function initializeForm() {
    const tab = getQueryParam('tab'); // Lấy giá trị tab từ URL
    if (tab === 'register') {
        switchForm('register'); // Hiển thị form đăng ký
    } else {
        switchForm('login'); // Mặc định hiển thị form đăng nhập
    }
}

// Hàm chuyển đổi form
function switchForm(formType) {
    // Tabs
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');

    // Forms
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (formType === 'login') {
        // Hiển thị form đăng nhập, ẩn form đăng ký
        loginForm.classList.remove('d-none');
        registerForm.classList.add('d-none');

        // Kích hoạt tab đăng nhập, bỏ kích hoạt tab đăng ký
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
    } else if (formType === 'register') {
        // Hiển thị form đăng ký, ẩn form đăng nhập
        registerForm.classList.remove('d-none');
        loginForm.classList.add('d-none');

        // Kích hoạt tab đăng ký, bỏ kích hoạt tab đăng nhập
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
    }
}
