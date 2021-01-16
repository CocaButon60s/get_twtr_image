<template>
  <b-row class="m-5">
      <b-col class="text-center">
          <b-button variant="primary" @click="click">
            <slot/>
          </b-button>
      </b-col>
  </b-row>
</template>

<script>
export default {
  name: 'InputForm',
  methods: { click () { this.$emit('callback') } }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
