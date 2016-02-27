// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

angular.module('spendalot-app').controller('ChartCtrl', function($scope, $http) {
  $scope.toppings = [
    ['Mushrooms', 3],
    ['Onions', 1],
    ['Olives', 1],
    ['Zucchini', 1],
    ['Pepperoni', 2]
  ];
    
  $scope.drawChart = function() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Slices');
    data.addRows($scope.toppings);
 
    var options = {'title':'How Much Pizza I Ate Last Night',
                   'width':400,
                   'height':300};
 
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('pie'));
    chart.draw(data, options);
  }
  $scope.drawChart();
});
