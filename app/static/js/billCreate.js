  $(document).ready(function() {

      $('#addRow').click(function() {
          var id = $('#id').val();
          $.get(`/billCreate`, {
              id: id
          }, function(data) {
              if (data.error) {
                  alert(data.error);
              } else {
                  let isExisting = false;
                  $("#danh_sach_san_pham tr").each(function() {
                      let row = $(this);
                      let existingId = parseInt(row.find("td[name='id']").text());

                      if (existingId === data[0].id) {
                          let quantityInput = row.find("input[name='quantity']");
                          let currentQuantity = parseInt(quantityInput.val());
                          quantityInput.val(currentQuantity + 1);
                          isExisting = true;
                      }
                  });

                  if (!isExisting) {
                      var row = `
                    <tr>
                        <td name="id" class="text-center">${data[0].id}</td>
                        <td name="name" class="text-center">${data[0].ten}</td>
                        <td name="category" class="text-center">${data[0].theLoai}</td>
                        <td name="price" class="text-center">${data[0].donGia}</td>
                        <td class="text-center"><input type="number" name="quantity" class="form-control" value="1"></td>
                        <td class="text-center"><button type="button" class="btn btn-danger deleteRow mb-0">Xóa</button></td>
                    </tr>
                `;
                      $('#danh_sach_san_pham').append(row);
                  }
              }
          }).fail(function() {
              alert("Có lỗi khi lấy thông tin sách");
          });
      });


      $(document).on("click", ".deleteRow", function() {
          $(this).closest("tr").remove();
      });

      $("#cancelBill").click(function() {
          window.location.href = "{{ url_for('billCreate') }}";
      });


      $("#hoadonForm").on("submit", function(e) {
          e.preventDefault();

          let isValid = true;
          let errorMessage = "";
          let sachList = [];
          $("#danh_sach_san_pham tr").each(function() {
              let row = $(this);
              let id_sach = parseInt(row.find("[name='id']").text());
              let so_luong = parseInt(row.find("input[name='quantity']").val());

              if (id_sach) {
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
              alert("Vui lòng thêm ít nhất một sản phẩm vào danh sách hóa đơn.");
              return;
          }
          if (!isValid) {
              alert(errorMessage);
              return;
          }

          let payload = {
              ngayDatHang: $("#ngay_lap_hoa_don").val(),
              sachList: sachList,
          };
          $.ajax({
              url: "/billCreate",
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
      $("#export").click(function() {
          let sachList = [];
          $("#danh_sach_san_pham tr").each(function() {
              let row = $(this);
              let id_sach = parseInt(row.find("[name='id']").text());
              let so_luong = parseInt(row.find("input[name='quantity']").val());

              if (id_sach) {
                  sachList.push({
                      id_Sach: id_sach,
                      soLuong: so_luong
                  });
              }
          });

          if (sachList.length === 0) {
              alert("Vui lòng thêm ít nhất một sản phẩm vào danh sách hóa đơn.");
              return;
          }

          let payload = {
              ten_kh: $("#ten_kh").val(),
              ngayDatHang: $("#ngay_lap_hoa_don").val(),
              sachList: sachList,
          };

          $.ajax({
              url: "/billExport",
              method: "POST",
              contentType: "application/json",
              data: JSON.stringify(payload),
              success: function(response) {
                  if (response.success) {
                      window.location.href = response.download_url; // Tải file
                  } else {
                      alert("Không thể xuất hóa đơn. Vui lòng thử lại.");
                  }
              },
              error: function() {
                  alert("Đã xảy ra lỗi khi tạo file hóa đơn.");
              },
          });
      });
      $(".load-detail").click(function() {
          const id = $(this).data("id"); // Lấy ID từ nút bấm

          $.ajax({
              url: "/bill",
              type: "POST",
              contentType: "application/json", // Header Content-Type
              data: JSON.stringify({
                  id_Bill: id
              }), // Dữ liệu JSON
              success: function(response) {
                  if (response.success) {
                      $("#detail-title").text(`Chi tiết đơn hàng ${response.ngay_dat_hang}:`);
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