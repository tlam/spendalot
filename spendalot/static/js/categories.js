Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function drawCategory() {
  var categoryId = $("#category-id").val();
  var categoryName = $("#category-name").val();
  var categorySlug = $("#category-slug").val();

  if (categoryId == undefined || categoryName == undefined || categorySlug == undefined) {
    return 0;
  }

  // Create and populate the data table.
  var data = new google.visualization.DataTable();
        
  data.addColumn("string", categoryName);
  data.addColumn("number", categoryName); 
       
  $.getJSON("/categories/" + categorySlug + ".json", function(monthly_data) {
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
       {title: categoryName + " spending by month", 
        width:800, height:400,
        hAxis: {title: "Month"},
        vAxis: {title: "Amount"}}
      );
  });
}
google.setOnLoadCallback(drawCategory);
