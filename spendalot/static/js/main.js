var app = new Vue({
  delimiters: ['<%', '%>'],
  el: '#vue-app',
  data: {
    message: 'Hello Vue!',
    output: []
  }/*,
  mounted: function() {
    this.$http.get('/categories/clothing.json').then(response => {
      console.log(response.data);
      this.output = response;
    }, response => {

    });
  }*/
});

