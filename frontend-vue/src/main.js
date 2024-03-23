import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import webSocketsService from './services/websockets/websocketclient'

// font-awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faGlobe, faEye, faEyeSlash, faTimes, faChevronRight, faChartArea, faFileUpload, faChartBar, faGavel, faFileContract, faUserCog, faFileInvoice, faBox, faUsers, faPlayCircle,
   faArrowCircleUp, faChevronDown, faShoppingBasket, faBell, faFolderPlus, faFolderMinus, faDotCircle, faSearch, faFileSignature, faPen, faTrashAlt, faPenAlt, faUser, faCaretSquareRight,
   faSort, faSortDown, faSortUp, faPencilAlt, faInbox, faFileAlt, faCheck, faShieldAlt, faHammer, faAngleDown,
   faArrowLeft, faChevronLeft, faFileDownload, faPrint, faDownload, faUserAlt, faUserCircle, faCircle, faCartPlus, faChevronUp,
   faBook, faReceipt, faLock, faCircleNotch, faSpinner, faClock, faCalendar, faPlus
  } from '@fortawesome/free-solid-svg-icons'
  import { faLine } from '@fortawesome/free-brands-svg-icons'
import {  } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faGlobe, faEye, faEyeSlash, faTimes, faChevronRight, faChartArea, faFileUpload, faChartBar, faGavel, faFileContract, faUserCog, faFileInvoice, faBox, faUsers, faPlayCircle,
  faArrowCircleUp, faChevronDown, faShoppingBasket, faBell, faFolderPlus, faFolderMinus, faDotCircle, faSearch, faFileSignature, faPen, faTrashAlt, faPenAlt, faUser, faCaretSquareRight,
  faSort, faSortDown, faSortUp, faPencilAlt, faInbox, faFileAlt, faCheck, faShieldAlt, faHammer, faAngleDown,
  faArrowLeft, faChevronLeft, faFileDownload, faPrint, faDownload, faUserAlt, faUserCircle, faCircle, faCartPlus,
  faChevronUp, faBook, faReceipt, faLock, faCircleNotch, faSpinner, faLine, faClock, faCalendar, faPlus)

Vue.component('font-awesome-icon', FontAwesomeIcon)

// vue table
import {ClientTable, ServerTable} from 'vue-tables-3';
Vue.use(ClientTable);
Vue.use(ServerTable);

// Vue Pagination
import Pagination from 'vue-pagination-2';
Vue.component('pagination', Pagination);

// Vue axios
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

// Vue form wizard
import VueFormWizard from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'
Vue.use(VueFormWizard)

// Vue sweet alert
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
Vue.use(VueSweetalert2);

// Vue country select
import vueCountryRegionSelect from 'vue-country-region-select'
Vue.use(vueCountryRegionSelect)

// Vue  TinyMCE
import Editor from '@tinymce/tinymce-vue';
// var Editor = require('@tinymce/tinymce-vue').default;
Vue.component('editor', Editor)

// Vue Draggable
import draggable from 'vuedraggable'
Vue.component('draggable', draggable)

// Vue Apex Charts
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

// toast
import Swal from 'sweetalert2'
const toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
  });
window.toast = toast;


// Vue Select
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';
Vue.component('v-select', vSelect)

// Vue Charts
import VueCharts from 'vue-chartjs'
Vue.use(VueCharts);

// Vue tab component
import {Tabs, Tab} from 'vue-tabs-component';
Vue.component('tabs', Tabs);
Vue.component('tab', Tab);

// Timeago
import VueTimeago from 'vue-timeago'
Vue.use(VueTimeago, {
  name: 'Timeago', // Component name, `Timeago` by default
  locale: 'en', // Default locale
  // We use `date-fns` under the hood
  // So you can use all locales from it
  locales: {
    'zh-CN': require('date-fns/locale/zh_cn'),
    ja: require('date-fns/locale/ja')
  }
})


//ClickOutside
import vClickOutside from 'v-click-outside'
Vue.use(vClickOutside)

// Vue slick carousel
import VueSlickCarousel from 'vue-slick-carousel'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
// optional style for arrows & dots
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'
Vue.component('VueSlickCarousel', VueSlickCarousel);

// Vue count down
import vueAwesomeCountdown from 'vue-awesome-countdown'
Vue.use(vueAwesomeCountdown, 'vac')

// Vue translation
import VueI18n from 'vue-i18n';
Vue.use(VueI18n);

import VueLazyload from 'vue-lazyload'
Vue.use(VueLazyload)

import VueUploadMultipleImage from 'vue-upload-multiple-image'
Vue.component('vue-upload-multiple-image', VueUploadMultipleImage);

const messages = {
  en: {
    message: {
      value: 'Login'
    }
  },
  be: {
    message: {
      value: 'Гэта прыклад перакладу змесціва.'
    }
  },
  da: {
    message: {
      value: 'Dette er et eksempel på oversættelse af indhold.'
    }
  },
  hr: {
    message: {
      value: 'Ovo je primjer prevođenja sadržaja.'
    }
  },
  fr: {
    message: {
      value: 'Connexion'
    }
  }
};
const i18n = new VueI18n({
  locale: 'en',
  silentTranslationWarn: true,
  messages
});

// Prevent parent from scrolling
Vue.use(require('vue-prevent-parent-scroll'))

// Format currency
Vue.filter('toCurrency', function (value, currency) {
  // if (typeof value !== "number") {
  //     return value;
  // }
  var formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2
  });
  return formatter.format(value);
});

// Format Date
import moment from 'moment'
Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MMMM Do YYYY')
  }
});

Vue.filter('formatDateTime', function(value) {
  if (value) {
    return moment(String(value)).format('MMMM Do YYYY, h:mm a')
  }
});

// Time left
Vue.filter('timeLeft', function(value) {
  if (value) {
    let duration = moment.duration(value * 1000);
    let timeLeft = ''
    if (duration.asDays() > 0) { timeLeft = timeLeft + Math.floor(duration.asDays()) + ' days ' }
    if (duration.asHours() > 0) { timeLeft = timeLeft + Math.floor(duration.asHours()) % 24 + ' hours ' }
    if (duration.asMinutes() > 0) { timeLeft = timeLeft + Math.floor(duration.asMinutes()) % 60 + ' mins ' }
    if (duration.asSeconds() > 0) { timeLeft = timeLeft + Math.floor(duration.asSeconds()) % 60 + ' secs ' }
    return timeLeft
  }
});

// Format values by rounding off
Vue.filter('round', function (value) {
  if (!value) {
    value = 0
  }

  let decimals = 2

  value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
  return value
})

// Format values to percentage
Vue.filter('percentage', function (value) {
  if (!value) {
    value = 0
  }

  let decimals = 2

  value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
  value = value + '%'
  return value
})

Vue.filter('nameInRoute', function (value, name) {
  if (value === null) {
    return false
  }
  value = value.toLowerCase();
  let result = value.includes(name);
  return result
})

Vue.filter('truncate', function(data,num){
  return data.split("").slice(0, num).join("");
})

// vue-nprogress
import NProgress from 'vue-nprogress'
Vue.use(NProgress)
const nprogress = new NProgress()

Vue.use(webSocketsService, {
  store,
  url: process.env.VUE_APP_WS_API_URL
})

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
  i18n
}).$mount('#app')
