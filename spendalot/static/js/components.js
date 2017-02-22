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

Vue.component('category-bar-charts', {
  template: '<div></div>',
  mounted: function() {
    this.$http.get('/categories/clothing.json').then(response => {
      var data = response.data;
      var category = data.category;

      function drawChart() {
        // Create and populate the data table.
        var monthlyDataTable = new google.visualization.DataTable();
        var yearlyDataTable = new google.visualization.DataTable();
        var name = category.name;
        var monthlyData = data.monthly.Amount;
        var yearlyData = data.yearly.Amount;

        monthlyDataTable.addColumn('string', name);
        monthlyDataTable.addColumn('number', name); 
        monthlyDataTable.addRows(Object.size(monthlyData));

        var j = 0;
        $.each(monthlyData, function(month, sum) {
          monthlyDataTable.setValue(j, 0, month);
          monthlyDataTable.setValue(j, 1, parseFloat(sum));
          ++j;
        });

        // Create and draw the visualization.
        new google.visualization.ColumnChart(document.getElementById('vmonthly-category')).
          draw(monthlyDataTable,
           {title: name + ' spending by month',
            width: 800, height: 400,
            hAxis: {title: 'Month'},
            vAxis: {title: 'Amount'}}
        );

        yearlyDataTable.addColumn('string', name);
        yearlyDataTable.addColumn('number', name); 
        yearlyDataTable.addRows(Object.size(yearlyData));

        var j = 0;
        $.each(yearlyData, function(month, sum) {
          yearlyDataTable.setValue(j, 0, month);
          yearlyDataTable.setValue(j, 1, parseFloat(sum));
          ++j;
        });

        new google.visualization.ColumnChart(document.getElementById('vannual-category')).
          draw(yearlyDataTable,
           {title: name + ' spending by year',
            width: 800, height: 400,
            hAxis: {title: 'Year'},
            vAxis: {title: 'Amount'}}
        );
      }
      google.charts.setOnLoadCallback(drawChart);
    }, response => {

    });
  }
});
