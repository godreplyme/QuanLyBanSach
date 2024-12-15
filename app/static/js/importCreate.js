  $(document).ready(function() {
      $("#searchSach").on("input", function() {
          let query = $(this).val();
          if (query.length < 2) {
              $("#searchResults").empty();
              return;
          }
          $.get("/importCreate", {
              q: query
          }, function(data) {
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


      $("#searchResults").on("click", ".list-group-item", function() {
          let id = $(this).data("id");
          let ten = $(this).data("ten");
          let tacgia = $(this).data("tacgia");
          let theloai = $(this).data("theloai");
          let soluong = $(this).data("soluong");

          $("#selectedSachTable").html(`
                <tr class="p-2">
                    <td class=" text-center">${id}</td>
                    <td class=" text-center">${ten}</td>
                    <td class=" text-center">${theloai}</td>
                    <td class=" text-center">${tacgia}</td>
                    <td class=" text-center">${soluong}</td>
                </tr>
            `);
          $("#searchResults").empty();
          $("#searchSach").val("");
      });


      $("#nhapSachTable").on("input", "input[id='searchSach2']", function() {
          let query = $(this).val();
          let searchResults = $(this).siblings("#searchResults2");
          if (query.length < 2) {
              searchResults.empty();
              return;
          }
          $.get("/importCreate", {
              q: query
          }, function(data) {
              searchResults.empty();
              data.forEach((item) => {
                  searchResults.append(`
                        <a href="#" class="list-group-item list-group-item-action" data-id="${item.id}" data-ten="${item.ten}" data-tacgia="${item.tacGia}" data-theloai="${item.theLoai}" data-soluong="${item.soLuongTonKho}">
                            ${item.ten} - ${item.tacGia}
                        </a>
                    `);
              });
          });
      });


      $("#addRow").on("click", function() {
          $("#nhapSachTable").append(`
                <tr>
                    <td name="id_sach" class="text-center"></td>
                    <td>
                        <div class="position-relative">
                            <input type="text" class="form-control" name="q" id="searchSach2">
                            <div class="list-group" id="searchResults2" ></div>
                        </div>
                    </td>
                    <td name="the_loai" class="text-center"></td>
                    <td name="tac_gia" class="text-center"></td>
                    <td><input type="number" class="form-control" name="so_luong"></td>
                    <td><button type="button" class="btn btn-danger removeRow">Xóa</button></td>
                </tr>
            `);
      });

      $("#nhapSachTable").on("click", ".list-group-item", function() {
          let row = $(this).closest("tr");
          let id = $(this).data("id");
          let ten = $(this).data("ten");
          let tacgia = $(this).data("tacgia");
          let theloai = $(this).data("theloai");
          let soluong = $(this).data("soluong");

          row.find("input[id='searchSach2']").val(ten);
          row.find("[name='id_sach']").html(id);
          row.find("[name='the_loai']").html(theloai);
          row.find("input[name='so_luong']").val(150);
          row.find("[name='tac_gia']").html(tacgia);

          row.append(`<input type="hidden" name="so_luong_ton_kho" value="${soluong}" />`);

          $(this).closest(".list-group").empty();
      });

      $("#nhapSachTable").on("click", ".removeRow", function() {
          $(this).closest("tr").remove();
      });

      $("#nhapSachForm").on("submit", function(e) {
          e.preventDefault();

          let isValid = true;
          let errorMessage = "";
          let sachList = [];
          let so_luong_nhap_toi_thieu = $(document).find("input[name='so_luong_nhap_toi_thieu']").val();
          let gioi_han_nhap = $(document).find("input[name='gioi_han_nhap']").val();
          $("#nhapSachTable tr").each(function() {
              let row = $(this);
              let id_sach = parseInt(row.find("[name='id_sach']").text());
              let so_luong = parseInt(row.find("input[name='so_luong']").val());
              let so_luong_ton_kho = parseInt(row.find("input[name='so_luong_ton_kho']").val());
              if (!so_luong) {
                  isValid = false;
                  errorMessage = `Vui lòng nhập số lượng cho sách.`;
                  return false;
              }

              if (id_sach && so_luong) {
                  if (so_luong < so_luong_nhap_toi_thieu) {
                      isValid = false;
                      errorMessage = `Số lượng nhập cho sách có mã ${id_sach} phải ít nhất là ${so_luong_nhap_toi_thieu}.`;
                  } else if (so_luong_ton_kho + so_luong > gioi_han_nhap) {
                      isValid = false;
                      errorMessage = `Sách có mã ${id_sach} sẽ vượt quá ${gioi_han_nhap} cuốn trong kho nếu nhập thêm ${so_luong} cuốn.`;
                  }

                  if (isValid) {
                      sachList.push({
                          id_Sach: id_sach,
                          soLuong: so_luong
                      });
                  } else {
                      return false;
                  }
              }
          });

          if (sachList.length === 0) {
              alert("Vui lòng thêm ít nhất một sản phẩm vào danh sách sản phẩm.");
              return;
          }

          if (!isValid) {
              alert(errorMessage);
              return;
          }

          let payload = {
              ngayNhap: $("#ngayNhap").val(),
              sachList: sachList,
          };

          $.ajax({
              url: "/importCreate",
              method: "POST",
              contentType: "application/json",
              data: JSON.stringify(payload),
              success: function(response) {
                  if (response.success) {
                      alert("Nhập sách thành công!");
                      location.reload();
                  }
              },
              error: function() {
                  alert("Đã xảy ra lỗi khi gửi dữ liệu. Vui lòng thử lại.");
              },
          });
      });
      $("#searchSach").on("blur", function() {
          setTimeout(function() {
              $("#searchResults").empty();
          }, 200);
      });
      $(".load-detail").click(function() {
          const id = $(this).data("id"); // Lấy ID từ nút bấm

          $.ajax({
              url: "/import",
              type: "POST",
              contentType: "application/json", // Header Content-Type
              data: JSON.stringify({
                  id_Import: id
              }), // Dữ liệu JSON
              success: function(response) {
                  if (response.success) {
                      $("#detail-title").text(`Chi tiết phiếu nhập ${response.ngay_nhap}:`);
                      const tbody = $("#detail-table tbody");
                      tbody.empty();
                      response.details.forEach((detail, index) => {
                          tbody.append(`
                    <tr>
                        <td>${index + 1}</td>
                        <td>${detail.ten_sach}</td>
                        <td>${detail.ten_the_loai}</td>
                        <td>${detail.tac_gia}</td>
                        <td class="text-center">${detail.soLuong}</td>
                    </tr>
                `);
                      });
                  } else {
                      alert("Không thể tải chi tiết phiếu nhập!");
                  }
              },
              error: function() {
                  alert("Đã xảy ra lỗi khi tải chi tiết phiếu nhập!");
              }
          });
      });
  });