
const initialState = () => ({
    selectedJob: null,
    selectedActive: null,
});

const state = initialState();

const getters = {
    selectedJob(){
        return state.selectedJob
    },
    selectedActive(){
        return state.selectedActive
    }
}

const mutations = {
    updateSelectedJob(state, payload){
        state.selectedJob = payload.job
    },
    updateSelectedActive(state, payload){
        state.selectedActive = payload.id
    },
}

const actions = {
    setSelectedJob({ commit }, payload){
        commit('updateSelectedJob', payload)
    },
    setSelectedActive({ commit }, payload){
        commit('updateSelectedActive', payload)
    },
}


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
