Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function CategoryCtrl($scope, $attrs) {
  $scope.drawChart = function() {
    // Create and populate the data table.
    var data = new google.visualization.DataTable();
            
    data.addColumn("string", $attrs.category);
    data.addColumn("number", $attrs.category); 
           
    $.getJSON("/categories/" + $attrs.slug + ".json", function(monthly_data) {
      var amountData = monthly_data['Amount'];
      data.addRows(Object.size(amountData));

      var j = 0;
      $.each(amountData, function(month, sum) {
        data.setValue(j, 0, month);
        data.setValue(j, 1, parseFloat(sum));
        ++j;
      });

      // Create and draw the visualization.
      new google.visualization.ColumnChart(document.getElementById('category')).
        draw(data,
         {title: $attrs.category + " spending by month", 
          width:800, height:400,
          hAxis: {title: "Month"},
          vAxis: {title: "Amount"}}
        );
    });
  }
  $scope.drawChart();
}
