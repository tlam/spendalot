<template>
<div class="categories list-group">
  <a v-for="category in categories" :href="category.url" class="list-group-item" v-bind:class="{active : category.slug === selectedCategory }">{{ category.name }}</a>
</div>
</template>

<script>
var data = {
  categories: []
}

export default {
  name: 'category-list',
  data: function() {
    return data;
  },
  props: ['selectedCategory'],
  mounted: function() {
    this.$http.get('/categories/categories.json').then(response => {
      data.categories = response.data.categories;
    }, response => {

    });
  }
}
</script>
