function payment() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        const cartItems = [];
        $("#productList tr").each(function () {
            const productId = $(this).data("id");
            const quantity = parseInt($(this).data("so-luong"));
            cartItems.push({
                product_id: productId,
                quantity: quantity,
            });
        });
        // Dữ liệu giả định gửi lên server
        const data = {
            amount: document.getElementById("total").dataset.amount,
            order_desc: "Thanh toán đơn hàng",
            chi_tiet_don_hang: cartItems
        };

        fetch('/api/pay', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 200) {
                // Điều hướng tới URL thanh toán
                window.location.href = data.payment_url;
            } else {
                alert("Có lỗi xảy ra: " + (data.message || "Không rõ nguyên nhân"));
            }
        })
        .catch(err => {
            console.error(err);
            alert("Không thể kết nối tới server. Vui lòng thử lại sau!");
        });
    }
}