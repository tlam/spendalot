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
