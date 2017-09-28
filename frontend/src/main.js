// The following line loads the standalone build of Vue instead of the runtime-only build,
// so you don't have to do: import Vue from 'vue/dist/vue'
// This is done with the browser options. For the config, see package.json
import axios from 'axios'
import bootstrap from 'bootstrap'
import Vue from 'vue'
import PieChart from './components/PieChart.vue'
import CategoryList from './components/CategoryList.vue'
import CategoryBarCharts from './components/CategoryBarCharts.vue'

/*
new Vue({ // eslint-disable-line no-new
  el: '#vue-app',
  render: (h) => h(App)
})
*/

Vue.prototype.$http = axios;

new Vue({
  components: {
    PieChart,
    CategoryList,
    CategoryBarCharts
  },
  //delimiters: ['<%', '%>'],
  el: '#vue-app',
  data: {
    message: 'Hello Vue!',
    output: []
  }
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
