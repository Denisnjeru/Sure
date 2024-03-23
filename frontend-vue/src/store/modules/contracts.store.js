
const initialState = () => ({
    selectedJob: null,
    selectedCategory: null,
    selectedSupplier: null,
    selectedBuyer: null,
});

const state = initialState();

const getters = {
    selectedJob (state) {
        return state.selectedJob
    },
    selectedCategory (state) {
        return state.selectedCategory
    },
    selectedSupplier (state) {
        return state.selectedSupplier
    },
    selectedBuyer (state) {
        return state.selectedBuyer
    },
}

const mutations = {
    updateSelectedJob (state, payload) {
        state.selectedJob = payload.job
    },
    updateSelectedCategory (state, payload) {
        state.selectedCategory = payload.category
    },
    updateSelectedSupplier (state, payload) {
        state.selectedSupplier = payload.supplier
    },
    updateSelectedBuyer (state, payload) {
        state.selectedBuyer = payload.buyer
    },
}

const actions = {
    setSelectedJob ({ commit }, payload) {
        commit('updateSelectedJob', payload)
    },
    setSelectedCategory ({ commit }, payload) {
        commit('updateSelectedCategory', payload)
    },
    setSelectedSupplier ({ commit }, payload) {
        commit('updateSelectedSupplier', payload)
    },
    setSelectedBuyer ({ commit }, payload) {
        commit('updateSelectedBuyer', payload)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
