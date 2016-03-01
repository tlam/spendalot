angular.module('spendalot-app').controller('CategoryCtrl', function($scope, $http, $attrs) {
  $http.get('/categories/' + $attrs.slug + '.json').success(function(data) {
    var category = data.category;
    var monthlyData = data.monthly.Amount;
    var yearlyData = data.yearly.Amount;

    $scope.monthlyMean = category.monthly_mean;
    $scope.sum = category.sum;
    $scope.yearlyMean = category.yearly_mean;

    var monthOptions = {
      animation: false
    };
    var yearOptions = {
      barValueSpacing: 10,
      animation: false
    };
    var monthData = {
      labels: [],
      datasets: [
        {
          label: 'Month',
          fillColor: 'rgba(151,187,205,0.5)',
          strokeColor: 'rgba(rgba(151,187,205,0.8))',
          highlightFill: 'rgba(151,187,205,0.75)',
          highlightStroke: 'rgba(151,187,205,1)',
          data: []
        }
      ]
    };
    var yearData = {
      labels: [],
      datasets: [
        {
          label: 'Year',
          fillColor: 'rgba(220,220,220,0.5)',
          strokeColor: 'rgba(220,220,220,0.8)',
          highlightFill: 'rgba(220,220,220,0.75)',
          highlightStroke: 'rgba(220,220,220,1)',
          data: []
        }
      ]
    };

    var ctx = $('#monthly-chart').get(0).getContext('2d');
    var monthBarChart = new Chart(ctx).Bar(monthData, monthOptions);

    var ctx = $('#yearly-chart').get(0).getContext('2d');
    var yearBarChart = new Chart(ctx).Bar(yearData, yearOptions);

    var i = 0;
    $.each(monthlyData, function(month, sum) {
      var monthLabel = '';
      // Show label for every 4 months
      if (i % 4 == 0) {
        monthLabel = month;
      }
      monthBarChart.addData([parseFloat(sum)], monthLabel);
      ++i;
    });

    $.each(yearlyData, function(year, sum) {
      yearBarChart.addData([parseFloat(sum)], year);
    });
  });
});
