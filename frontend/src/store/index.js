import { createStore } from 'vuex'

import createPersistedState from "vuex-persistedstate";

export default createStore({
  plugins: [createPersistedState(
    {storage: window.sessionStorage}
  )],
  state: {
    userid: null,
    userrole: null,
    username:null
  },
  mutations:{
    reset(state){
      state.userid = null
      state.userrole =null
      state.username=null
    },
    setuserInfo(state, data) {     
      state.userid = data["userid"];
      state.userrole = data["userrole"];
      state.username = data["username"];
    },
  },
  actions: {
   

  },
  modules: {

  }
})
