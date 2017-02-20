var app = new Vue({
  delimiters: ['<%', '%>'],
  el: '#vue-app',
  data: {
    message: 'Hello Vue!',
    output: []
  },
  mounted: function() {
    this.$http.get('/categories/clothing.json').then(response => {
      console.log(response);
      console.log(response.data);
      console.log(response.body);
      this.output = response;
    }, response => {

    });
  }
});
