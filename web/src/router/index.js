import Vue from 'vue'
import Router from 'vue-router'
import GetImage from '@/components/pages/GetImage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GetImage',
      props: true,
      component: GetImage
    }
  ]
})
