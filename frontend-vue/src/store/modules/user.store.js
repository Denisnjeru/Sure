import Utils from '../../utils/Cookies';


const initialState = () => ({
    userLoadStatus: 0, // 1 - Loading, 2 - Successful, 3 - unsuccesful, 4 - uncaught error
    userMessage: null,
    // userData: !!Cookies.get('userData') && Cookies.get('userData'),
    userData: null,
    userProfile: null,
    userType: 'supplier'
});

const state = initialState();

const getters = {
    userLoadStatus(state) {
        return state.userLoadStatus
    },
    userMessage(state) {
        return state.userMessage
    },
    userData(state) {
        // return JSON.parse(state.userData)
        return state.userData
    },
    userProfile(state) {
        return state.userProfile
    },
    userType(state) {
        return state.userType
    },   


}

const mutations = {
    userRequest(state) {
        state.userLoadStatus = 1
        state.userMessage = null
    },

    userSuccess(state, response) {
        state.userLoadStatus = 2
        state.userMessage = 'User data loaded successfully!'
        // state.userData = Cookies.set('userData', JSON.stringify(response.data))
        state.userData = response
    },

    userError(state, response) {
        state.userLoadStatus = 3
        state.userMessage = response.data
    },

    userExec(state, error) {
        state.userLoadStatus = 4
        state.userMessage = error.response
    },
    updateUserType (state, payload) {
        state.userType = payload.userType
    },
    userLogout(state){
        state.userData = null
        state.userProfile = null
        state.userType = 'supplier'
    },
    updateUserPermissions(state, payload) {
        state.userData.permissions = payload.permissions
    },
    // Reset
    reset(state) {
        const newState = initialState()
        Object.keys(newState).forEach(key => {
            state[key] = newState[key]
        })
    }

    
}

const actions = {
    async getUser({ commit }) {
        return new Promise(() => {
            const userData = Utils.authTokenExists() && Utils.decodeAuthToken()
            const userId = userData.user_id;

            if (userId) {
                commit('userRequest');
                // success
                commit('userSuccess', userData)
                let userType = 'supplier'
                commit('updateUserType', { userType })
            } 
        });
    },
    setUserType ({ commit }, payload) {
        commit('updateUserType', payload)
    },
    setUserPermissions ({ commit }, payload) {
        commit('updateUserPermissions', payload)
    },
    logout({ commit }){
        commit('reset')
    },

}


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
