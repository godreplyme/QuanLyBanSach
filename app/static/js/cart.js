function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") == true) {
        // Nếu thanh toán onl thành công thì ghi nhận đơn hàng này
        fetch("/api/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert("Có lỗi xảy ra!")    
        })
    }    
}
