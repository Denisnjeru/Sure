<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                New User
            </span>
            <div class="page__head--links">
            </div>
        </div>
        <form class="form" v-on:submit.prevent="createUser()">
        <div class="page__content columns is-centered is-multiline">
            <div class="column is-8 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Add New User</p>
                    <p class="column-details__head--desc">Fill in the required details.</p>
                </div>
                <div class="column-details__content">                    
                    <div class="field">
                        <label class="label">Email Address (Username) <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="user.email" class="input" type="text">
                        </div>
                    </div>  
                    <div class="field">
                        <label class="label">First Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="user.first_name" class="input" type="text">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Last Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="user.last_name" class="input" type="text">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Role<span class="required">*</span></label>
                        <div class="select">
                            <select v-model="user.buyer_role">
                                <option>Select role</option>
                                <option v-for="role in roles" :key="role.id" :value="role.id">{{role.name}}</option>
                            </select>
                        </div>                                    
                    </div>
                </div>
                <div class="column-details__content is-centered additions form-submit">     
                    <input type="submit" class="button button-submit" value="Create user">
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
               <!-- <input type="submit" class="button button-submit" value="Create role"> -->
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import system_management from '@/services/company/system_management'

export default {
    name: 'Dashboard',
    data() {
        return {
            user: {},
            role: []
        }
    },
    mounted() {
        this.getRoles()
    },
    methods: {
        async search() {
            console.log('search');
        },
        async getRoles() {
            try {
                const response = await system_management.roles()
                this.roles = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async createUser(){
            try {
                const response = await system_management.createUser(this.user)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.first_name + ' created successfully'
                })
                this.$router.push('/buyer/user/users')
            } catch (err) {
                console.log(err.response)      
            } 
        },

    }
}
</script>

<style lang="scss" scoped>
@include page;
@include form;

.page__content {
    padding: $line-height $line-height;
    margin-top: $line-height;

}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

</style>
