Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function CategoryCtrl($scope, $http, $attrs) {

  $http.get('/categories/' + $attrs.slug + '.json').success(function(data) {
    // Create and populate the data table.
    var monthlyDataTable = new google.visualization.DataTable();
    var yearlyDataTable = new google.visualization.DataTable();
    var category = data.category;
    var name = category.name;
    var monthlyData = data.monthly.Amount;
    var yearlyData = data.yearly.Amount;

    $scope.monthlyMean = category.monthly_mean;
    $scope.sum = category.sum;
    $scope.yearlyMean = category.yearly_mean;

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
    new google.visualization.ColumnChart(document.getElementById('monthly-category')).
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

    new google.visualization.ColumnChart(document.getElementById('yearly-category')).
      draw(yearlyDataTable,
       {title: name + ' spending by year',
        width: 800, height: 400,
        hAxis: {title: 'Year'},
        vAxis: {title: 'Amount'}}
    );
  });
}
