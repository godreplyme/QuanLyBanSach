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
        alert("Vui lòng đăng nhập để thêm vào giỏ hàng!");
    });
}

// Hàm thu thập sản phẩm đã chọn

function collectSelectedProducts() {
    const selectedProducts = [];

    // Lặp qua các checkbox đã chọn
    document.querySelectorAll(".product-checkbox:checked").forEach(function (checkbox) {
        const rows = document.querySelectorAll('.table tr');
        const row = checkbox.closest("tr"); // Tìm thẻ <tr> chứa checkbox
        // Lấy productId từ data-product-id của thẻ <tr>
        const productId = row.getAttribute('data-product-id');
        // lấy tên
        const ten = row.getAttribute('data-ten');
        // lấy đơn giá
        const donGia = row.getAttribute('data-donGia');
        // Lấy số lượng từ input type="number" trong dòng
        const soLuong = row.querySelector("input[type='number']").value;
        // Lấy phương thức thanh toán từ radio buttons
        let paymentMethod = '';
        document.querySelectorAll("input[name='optradio']").forEach(function (radio) {
            if (radio.checked) {
                paymentMethod = radio.value; // lấy giá trị luôn
            }
        });

        // Thêm sản phẩm vào danh sách
        selectedProducts.push({
            id: productId,
            ten: ten,
            donGia: donGia,
            quantity: soLuong, // Số lượng mặc định là 1 nếu không hợp lệ
            paymentMethod: paymentMethod
        });
    });
    localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
    return selectedProducts;
}

// Hàm gửi yêu cầu thanh toán
function processPayment() {
    const products = JSON.parse(localStorage.getItem("selectedProducts")); // Parse thành đối tượng JSON

    // Thu thập danh sách sản phẩm đã chọn

    if (products.length === 0) {
        alert("Vui lòng chọn sản phẩm trước khi thanh toán!");
        return;
    }

    // Gửi yêu cầu POST đến server
    fetch('/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ products: products }) // Gửi danh sách sản phẩm dưới dạng JSON
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/payment"; // Điều hướng đến trang thanh toán
        } else {
            console.error("Failed to process payment:", response.status);
            alert("Có lỗi xảy ra khi thanh toán. Vui lòng thử lại!");
        }
    })
    .catch(err => {
        console.error("Lỗi khi gửi request:", err);
        alert("Không thể kết nối đến server. Vui lòng thử lại!");
    });
}
// Lấy thông tin giỏ hàng từ localStorage
const cartData = JSON.parse(localStorage.getItem("selectedProducts"));
console.log(cartData);
if (cartData && cartData.length > 0) {
    // Hàm lấy thông tin sản phẩm từ API
    const fetchProductById = (id) => {
        // Tìm sản phẩm trong selectedProducts
        const product = cartData.find(item => item.id === id);
        if (product) {
            return {
                id: product.id,
                name: product.ten,
                price: product.donGia
            };
        } else {
            console.error(`Product with ID ${id} not found.`);
            return null;
        }
    };


    const displayProducts = () => {
        const productList = document.getElementById("productList");

        document.addEventListener('DOMContentLoaded', function() {
            for (const cartItem of cartData) {
                const product = fetchProductById(cartItem.id);
                const quantity = parseInt(cartItem.quantity, 10) || 0;
                const totalPrice = product.price * quantity;

                // Tạo một hàng mới trong bảng
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.price.toLocaleString()} VND</td>
                    <td>${quantity}</td>
                    <td>${totalPrice.toLocaleString()} VND</td>
                `;
                productList.appendChild(row);
            }
        });
    }
    // Gọi hàm hiển thị
    displayProducts();
} else {
    // Hiển thị thông báo nếu giỏ hàng trống
    document.getElementById("productList").innerHTML = `
        <tr>
            <td colspan="4" class="text-center">Không có sản phẩm trong giỏ hàng</td>
        </tr>
    `;
}
//// hàm mua ngay sản phẩm
//function paymentNow(sachId, ten, donGia) {
//    const selectedProduct ;
//    // Lấy số lượng từ input
//    const quantity = document.getElementById("quantity").value;
//    // Kiểm tra nếu `quantity` không hợp lệ
//    if (!quantity || isNaN(quantity) || quantity <= 0) {
//        alert("Vui lòng nhập số lượng hợp lệ.");
//        return;
//    }
//    // Thêm sản phẩm vào danh sách
//    selectedProduct.push({
//        id: sachId,
//        ten: ten,
//        donGia: donGia,
//        quantity: quantity, // Số lượng mặc định là 1 nếu không hợp lệ
//        paymentMethod: paymentMethod
//    });
//    localStorage.setItem("selectedProduct", JSON.stringify(selectedProducts));
//    return selectedProduct;
//}

