var app = angular.module('spendalot-app', []);
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

function getRandomColour() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

angular.module('spendalot-app').controller('ChartCtrl', function($scope, $http) {
  $http.get('/categories/categories.json').success(function(data) {
    var ctx = $('#categories-chart').get(0).getContext('2d');
    var options = {
      legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
    };
    var pieChart = new Chart(ctx).Pie([], options);

    $.each(data, function(category, sum) {
      var colour = getRandomColour();
      pieChart.addData({
        value: parseFloat(sum),
        color: colour,
        highlight: colour,
        label: category,
        labelColor: 'white',
        labelFontSize: '16'
      });
    });

    $('#legend').html(pieChart.generateLegend());

  });
});

$(function() {
  $('#id_date').datepicker();

  $('#id_description').autocomplete({
    source: '/expenses/descriptions.json',
    minLength: 2,
    select: function(event, ui) {
    }
  });

  $('#id_description').focusout(function() {
    $.getJSON('/expenses/category.json', {"description": $(this).val()}, function(data) {
      if (data.category_id) {
        $('#id_category').val(data.category_id);
      }
    });
  });
});
