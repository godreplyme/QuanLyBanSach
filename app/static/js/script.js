// Hàm thêm vào giỏ hàng
function addToCart() {
    // Lấy số lượng từ input
    const quantity = document.getElementById("quantity").value;

    // Lấy sachId từ URL (ví dụ: /products/3)
    const urlParts = window.location.pathname.split('/');
    const sachId = urlParts[urlParts.length - 1]; // Lấy phần cuối của URL, giả sử là ID sách

    // Kiểm tra nếu `quantity` không hợp lệ
    if (!quantity || isNaN(quantity) || quantity <= 0) {
        alert("Vui lòng nhập số lượng hợp lệ.");
        return;
    }

    // Gửi yêu cầu POST đến Flask server
    fetch(`/products/${sachId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: parseInt(quantity, 10) }) // Gửi dữ liệu dưới dạng JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log("Phản hồi từ server:", data);
        // Có thể cập nhật UI, ví dụ như hiển thị thông báo giỏ hàng đã cập nhật
        alert("Sản phẩm đã được thêm vào giỏ hàng!");
    })
    .catch(err => {
        console.error("Lỗi khi gửi request:", err);
        alert("Đã có lỗi xảy ra. Vui lòng thử lại.");
    });
}
