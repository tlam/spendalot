// Load the Visualization API and the piechart package.
//google.charts.load('current', {packages: ['corechart']});

angular.module('spendalot-app').controller('ChartCtrl', function($scope, $http) {
  $http.get('/categories/categories.json').success(function(data) {
    var pieData = [];
    for (var category in data) {
      pieData.push([category, Math.ceil(data[category])]);
    }

    $scope.drawChart = function() {
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
    google.charts.setOnLoadCallback($scope.drawChart);
  });
});
