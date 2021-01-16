<template>
  <div id="app">
    <!-- ヘッダ -->
    <div class="container-fluid mt-2">
      <div class="col text-center">
        <h1>Twitter 画像ゲッター</h1>
      </div>
    </div>
    <router-view :modal="modal" />
    <modal-form ref="modal"></modal-form>
  </div>
</template>

<script>
import ModalForm from '@/components/parts/ModalForm'
export default {
  name: 'App',
  data: function () { return { modal: '' } },
  mounted () { this.modal = this.$refs.modal },
  components: { ModalForm }
}
</script>

<style>
</style>
