function drawCateChart(labels, data) {
    const ctx = document.getElementById('cateStats');

    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Số lượng',
          data: data,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}

function drawRevenueChart(data, labels) {
  const ctx = document.getElementById('revenueChart');

  new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: '# Doanh thu',
          data: data,
          borderWidth: 1,
          backgroundColor: ['#9BD0F5', '#FFCCFF', '#99FFFF', '#669900',
                            '#FFFF99', '#99FF99', '#FFCC99	', '#CC99FF	',
                            '#FF6666', '#FF9933', '#00FF00', '#99CCFF']
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}

function drawfrequencyChart(data, labels) {
  const ctx = document.getElementById('frequencyChart');

  new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Số lượng',
          data: data,
          borderWidth: 1,
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}