import Vue from 'vue';
// geolocation testing
import VueGeoLocation from 'vue-browser-geolocation';
import * as VueGoogleMaps from 'vue2-google-maps';

import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;

// geolocation testing
Vue.use(VueGeoLocation);

// geolocation testing
Vue.use(VueGoogleMaps, {
  load: {
    key: '',
  },
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
