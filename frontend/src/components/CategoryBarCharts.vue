<template>
<div class="row">
  <div class="col-md-8">
    <div id="vmonthly-category"></div>
    <div id="vannual-category"></div>
  </div>

  <div id="category-stats" class="col-md-2">
    <div>
      <b>Monthly mean:</b> {{ monthlyMean }}
    </div>
    <div>
      <b>Annual mean:</b> {{ annualMean }}
    </div>
    <div>
      <b>Sum:</b> {{ sum }}
    </div>

    <category-list :selectedCategory="category"></category-list>
  </div>
</div>
</template>

<script>
Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

var componentData = {
  annualMean: 0,
  monthlyMean: 0,
  sum: 0
};

export default {
  name: 'category-bar-charts',
  components: {
    'category-list': require('./CategoryList.vue')
  },
  data: function() {
    return componentData;
  },
  props: ['category'],
  mounted: function() {
    this.$http.get('/categories/' + this.category + '.json').then(response => {
      var data = response.data;
      var category = data.category;
      componentData.annualMean = category.yearly_mean;
      componentData.monthlyMean = category.monthly_mean;
      componentData.sum = category.sum;

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
}
</script>
