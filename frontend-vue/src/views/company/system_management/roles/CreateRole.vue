<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                New Role
            </span>
            <div class="page__head--links">
            </div>
        </div>
        <form class="form" v-on:submit.prevent="createRole()">
        <div class="page__content columns is-centered is-multiline">
            <div class="column is-8 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Add New Role</p>
                    <p class="column-details__head--desc">Fill in the required details.</p>
                </div>
                <div class="column-details__content">                    
                    <div class="field">
                        <label class="label">Role Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="role.name" required class="input" type="text">
                        </div>
                    </div>  
                    <div class="field">
                        <label class="label">Description <span class="required">*</span></label>
                        <div class="control">
                            <textarea class="textarea" required v-model="role.description" placeholder="Add role description"></textarea>
                        </div>
                    </div> 
                </div>
                <div class="column-details__content is-centered additions form-submit">     
                    <input type="submit" class="button button-submit" value="Create role">
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
            role: {}
        }
    },
    methods: {
        async search() {
            console.log('search');
        },
        async createRole(){
            try {
                const response = await system_management.createRole(this.role)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.name + ' created successfully'
                })
                this.$router.push('/buyer/user/roles')
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


// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

</style>
