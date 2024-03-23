
const initialState = () => ({
    activeUser: null,
});

const state = initialState();

const getters = {
    activeUser (state) {
        return state.activeUser
    },
}

const mutations = {
    updateActiveUser (state, payload) {
        state.activeUser = payload.activeUser
    },
}

const actions = {
    setActiveUser ({ commit }, payload) {
        commit('updateActiveUser', payload)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
