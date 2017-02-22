Vue.component('pie-chart', {
  template: '<div id="pie"></div>',
  mounted: function() {
    this.$http.get('/categories/categories.json').then(response => {
      var data = response.data;
      var pieData = [];
      for (var category in data) {
        pieData.push([category, Math.ceil(data[category])]);
      }

      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Category');
        data.addColumn('number', 'Total');
        data.addRows(pieData);
 
        var options = {
          'title':'Category Expenses',
          'width':400,
          'height':300
        };
 
        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('pie'));
        chart.draw(data, options);
      }
      google.charts.setOnLoadCallback(drawChart);
    }, response => {

    });
  }
});

var app = new Vue({
  delimiters: ['<%', '%>'],
  el: '#vue-app',
  data: {
    message: 'Hello Vue!',
    output: []
  },
  mounted: function() {
    this.$http.get('/categories/clothing.json').then(response => {
      console.log(response.data);
      this.output = response;
    }, response => {

    });
  }
});

