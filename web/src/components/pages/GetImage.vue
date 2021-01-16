<template>
  <b-container fluid class="form-group">
    <input-form :contents.sync="id">Twitter ID:</input-form>
    <button-form @callback="get_image">取得</button-form>
  </b-container>
</template>

<script>
import InputForm from '@/components/parts/InputForm'
import ButtonForm from '@/components/parts/ButtonForm'
export default {
  name: 'GetImage',
  data: function () {
    return {
      id: '',
      timer_interval: null,
      timer_timeout: null
    }
  },
  props: ['modal'],
  methods: {
    async get_image () {
      // パラメータチェック
      if (this.id === '') {
        this.modal.showModal('IDエラー', '画像を取得するユーザーのIDを入力してください', false, {color: 'secondary', label: '閉じる'})
        return
      }
      this.modal.showModal('画像取得中', '取得中', true, {color: 'danger', label: '中止', cb: this.cancel})
      // 画像取得
      await eel.py_set_target(this.id)()
      this.timer_interval = null
      this.timer_timeout = null
      this.get_image_loop()
    },
    async get_image_loop () {
      var result = await eel.py_get_image()()
      if (!isNaN(result)) {
        this.modal.setContent('取得中 ...' + result.toString())
        setTimeout(this.get_image_loop, 0)
      }

      if (result === 'RATE_LIMIT_ERROR') {
        var remainingTime = 15
        this.modal.showModal('利用制限', '利用制限がかかりました。' + remainingTime.toString() + '分後に処理を再開します', true, {color: 'danger', label: '中止', cb: this.cancel})
        this.timer_interval = setInterval(() => {
          remainingTime--
          this.modal.setContent('利用制限がかかりました。' + remainingTime.toString() + '分後に処理を再開します')
        }, 1000 * 60)
        this.timer_timeout = setTimeout(() => {
          clearInterval(this.timer_interval)
          this.modal.showModal('画像取得中', '取得中', true, {color: 'danger', label: '中止', cb: this.cancel})
          setTimeout(this.get_image_loop, 0)
        }, 1000 * 60 * 15)
      }

      if (result === 'NON_EXIST_USERID') this.modal.showModal('IDエラー', '指定したユーザーは存在しません', false, {color: 'secondary', label: '閉じる'})

      if (result === 'SUCCESS') this.modal.showModal('画像取得成功', 'imagesフォルダ内を確認してください', false, {color: 'secondary', label: '閉じる'})

      if (result === 'CANCEL') {
        if (this.timer_interval != null) clearInterval(this.timer_interval)
        if (this.timer_timeout != null) clearTimeout(this.timer_timeout)
        this.modal.showModal('画像取得中止', '画像取得を中止しました', false, {color: 'secondary', label: '閉じる'})
      }

      if (result === 'ERR') {
        if (this.timer_interval != null) clearInterval(this.timer_interval)
        if (this.timer_timeout != null) clearTimeout(this.timer_timeout)
        this.modal.showModal('画像取得失敗', 'アプリ製作者に連絡してください', false, {color: 'secondary', label: '閉じる'})
      }
    },
    async cancel () {
      this.modal.showModal('画像取得中止中', '画像取得を中止します', true)
      var isEnd = false
      if (this.timer_interval != null) {
        clearInterval(this.timer_interval)
        isEnd = true
      }
      if (this.timer_timeout != null) {
        clearTimeout(this.timer_timeout)
        isEnd = true
      }
      if (isEnd) this.modal.showModal('画像取得中止', '画像取得を中止しました', false, {color: 'secondary', label: '閉じる'})
      await eel.py_cancel()()
    }
  },
  components: {InputForm, ButtonForm}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
