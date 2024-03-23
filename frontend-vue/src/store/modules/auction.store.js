const namespaced = true

const initialState = () =>({
    isConnected: 0, // 1 - Successful, 2 - Disconnected, 3 - Error
    auctionNotifications: [],
    auctionObject: null,
    itemBid: [],
    auctionItems: []
});


const state = initialState();

const getters = {
  socketStatus: state => {
    return state.isConnected
  },
  auctionNotifications: state =>{
    return state.auctionNotifications
  },
  auctionObject: state =>{
    return state.auctionObject
  },
  auctionItems: state =>{
    return state.auctionItems
  },
  itemBid: state =>{
   return state.itemBid
  }
}

const mutations = {
  updateSocket:(state, payload) =>{
    state.isConnected = payload
  }, 
  updateAuctionNotifications: (state, payload) => {
    state.auctionnotifications.push(payload)
  },
  updateAuctionObject: (state, payload) =>{
    state.auctionObject = payload
    state.auctionItems = payload.auction_items
  },
  updateBidItem: (state, payload) =>{
    state.itemBid.push(payload)
  },
  updateAuctionItem: (state, payload) =>{
    //Testing Purposes
    // console.log(state.auctionItems.length)
    // console.log(typeof(payload))
    // console.log(payload)
    // console.log(payload.length)
    // Option 1 commented was replacing the whole object
    // for(var i = 0, l = state.auctionItems.length; i < l; i++) {
    //   for(var j = 0, ll = payload.length; j < ll; j++) {
    //     if(state.auctionItems[i].id === payload[j].id) {
    //       state.auctionItems.splice(i, 1, payload[j]);
    //       break;
    //     }
    //   }
    // }
    let objIndex = state.auctionItems.findIndex((obj => obj.id == payload[0].id))
    console.log("Before update: ", state.auctionItems[objIndex])
    state.auctionItems[objIndex].best_bid_price = payload[0].best_bid_price
    // Todo add no of bids:
    console.log("After update: ", state.auctionItems[objIndex])
  },
  // Reset
  reset(state){
    const newState = initialState()
    Object.keys(newState).forEach(key =>{
        state[key] = newState[key]
    })
  }
}

const actions = {
  setReset: ({commit}) =>{
    commit('reset')
  },
  SOCKET_CONNECT_DISCONNECT: async({commit}, payload) => {
    commit('updateSocket', payload);
  },
  setNotifications: ({commit}, payload) => {
    commit('updateAuctionNotifications', payload)
  },
  setItemBid: ({commit}, payload) =>{
    commit('updateBidItem', payload)
  },
  setAuctionObject: ({commit}, payload) =>{
    commit('updateAuctionObject', payload)
  },
  setAuctionItem: ({commit}, payload) =>{
    commit('updateAuctionItem', payload)
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions
}