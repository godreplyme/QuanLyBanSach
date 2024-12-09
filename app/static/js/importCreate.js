  $(document).ready(function () {
       // Tìm kiếm sách
       $("#searchSach").on("input", function () {
        let query = $(this).val();
        if (query.length < 2) {
            $("#searchResults").empty();
            return;
        }
        $.get("/importCreate", { q: query }, function (data) {
            $("#searchResults").empty();
            data.forEach((item) => {
                $("#searchResults").append(`
                    <a href="#" class="list-group-item list-group-item-action" data-id="${item.id}" data-ten="${item.ten}" data-tacgia="${item.tacGia}" data-theloai="${item.theLoai}" data-soluong="${item.soLuongTonKho}">
                        ${item.ten} - ${item.tacGia}
                    </a>
                `);
            });
        });
    });

        // Chọn sách từ danh sách gợi ý
        $("#searchResults").on("click", ".list-group-item", function () {
            let id = $(this).data("id");
            let ten = $(this).data("ten");
            let tacgia = $(this).data("tacgia");
            let theloai = $(this).data("theloai");
            let soluong = $(this).data("soluong");

            $("#selectedSachTable").html(`
                <tr>
                    <td>${id}</td>
                    <td>${ten}</td>
                    <td>${theloai}</td>
                    <td>${tacgia}</td>
                    <td>${soluong}</td>
                </tr>
            `);
            $("#searchResults").empty();
            $("#searchSach").val("");
        });

        // Thêm dòng nhập sách mới
        $("#addRow").on("click", function () {
            $("#nhapSachTable").append(`
                <tr>
                    <td name="id_sach"></td>
                    <td><input type="text" class="form-control" name="ten_sach"></td>
                    <td name="the_loai"></td>
                    <td name="tac_gia"></td>
                    <td><input type="number" class="form-control" name="so_luong"></td>
                    <td><button type="button" class="btn btn-danger removeRow">Xóa</button></td>
                </tr>
            `);
        });

        // Xóa dòng nhập sách
        $("#nhapSachTable").on("click", ".removeRow", function () {
            $(this).closest("tr").remove();
        });

        // Xác nhận nhập sách
        $("#nhapSachForm").on("submit", function (e) {
            e.preventDefault();
            let sachList = [];
            $("#nhapSachTable tr").each(function () {
                let row = $(this);
                let id_sach = row.find("input[name='id_sach']").val();
                let so_luong = row.find("input[name='so_luong']").val();
                if (id_sach && so_luong) {
                    sachList.push({ id_Sach: id_sach, soLuong: parseInt(so_luong) });
                }
            });

            let payload = {
                ngayNhap: $("#ngayNhap").val(),
                sachList: sachList,
            };

            $.ajax({
                url: "/nhap-sach",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(payload),
                success: function (response) {
                    if (response.success) {
                        alert("Nhập sách thành công!");
                        location.reload();
                    }
                },
            });
        });

        $("#searchSach").on("blur", function () {
            setTimeout(function() {
                $("#searchResults").empty();
            }, 200); // Đợi một chút để người dùng chọn gợi ý
        });

    });