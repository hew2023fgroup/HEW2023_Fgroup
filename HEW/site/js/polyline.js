<script>
  var ctx = document.getElementById("chart");
  var myLineChart = new Chart(ctx, {
    // グラフの種類：折れ線グラフを指定
    type: 'line',
    data: {
      // x軸の各メモリ
      labels: ['8月9日', '8月10日', '8月11日', '8月12日', '8月13日', '8月14日', '8月15日'],
      datasets: [
        {
          label: '最高気温(度）',
          data: [27, 26, 31, 25, 30, 22, 27, 26],
          borderColor: "#ec4343",
          backgroundColor: "#00000000"
        },
        {
          label: '最低気温(度）',
          data: [18, 21, 24, 22, 21, 19, 18, 20],
          borderColor: "#2260ea",
          backgroundColor: "#00000000"
        }
      ],
    },
    options: {
      title: {
        display: true,
        text: '札幌の気温（8月9日～8月15日）'
      },
      scales: {
        yAxes: [{
          ticks: {
            suggestedMax: 40,
            suggestedMin: 15,
            stepSize: 10,  // 縦メモリのステップ数
            callback: function(value, index, values){
              return  value +  '度'  // 各メモリのステップごとの表記（valueは各ステップの値）
            }
          }
        }]
      },
    }
  });