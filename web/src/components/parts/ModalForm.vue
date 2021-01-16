<template>
  <b-modal v-model="isShown" :noCloseOnBackdrop="true" :no-stacking="true">
    <template #modal-title>{{ title }}</template>
    <template #default>
      <b-container fluid>
        <b-row>
          <b-col cols="1" v-show="isLoading"><b-spinner label="Spinning"></b-spinner></b-col>
          <b-col>{{ content }}</b-col>
        </b-row>
      </b-container>
    </template>
    <template #modal-footer>
      <b-button :variant="okInfo.color" v-show="okInfo.isShown" @click="okInfo.cb">{{ okInfo.label }}</b-button>
    </template>
  </b-modal>
</template>

<script>
export default {
  name: 'ModalForm',
  data: function () {
    return {
      title: '',
      isLoading: false,
      isShown: false,
      content: '',
      okInfo: {
        isShown: false,
        color: 'secondary',
        label: '閉じる',
        cb: this.hideModal
      }
    }
  },
  methods: {
    showModal (title, content, isLoading, okInfo) {
      this.title = title
      this.content = content
      this.isLoading = isLoading

      this.okInfo.isShown = false
      if (typeof (okInfo) !== 'undefined') {
        this.okInfo.isShown = true
        this.okInfo.color = ('color' in okInfo ? okInfo.color : 'secondary')
        this.okInfo.label = ('label' in okInfo ? okInfo.label : '')
        this.okInfo.cb = ('cb' in okInfo ? okInfo.cb : this.hideModal)
      }

      this.isShown = true
    },
    hideModal () { this.isShown = false },
    setContent (content) { this.content = content }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
