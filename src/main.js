import Vue from 'vue'
import Vuex from 'vuex'
import 'normalize.css/normalize.css' // A modern alternative to CSS resets
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import VueInputAutowidth from 'vue-input-autowidth'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 *
 * if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}
 */

// set ElementUI lang to EN
Vue.use(ElementUI, { locale })
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueInputAutowidth)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
