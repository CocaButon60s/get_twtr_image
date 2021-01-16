<template>
  <b-row class="m-5">
    <b-col class="text-center">
      <label>
        <slot/>
        <b-form-input type="text" class="form-control" :value="contents" @change="update">
      </label>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: 'InputForm',
  props: ['contents'],
  methods: { update: function (e) { this.$emit('update:contents', e) } }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
