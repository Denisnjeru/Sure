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
import user_management from '@/services/qed/user_management'

export default {
    name: 'QedUserManagementRolesCreate',
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
                const response = await user_management.createRole(this.role)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.name + ' role created successfully'
                })
                this.$router.push('/qed/user/roles')
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
    margin-top: 0;
}

.page__head {
    padding-left: $line-height/2;

    &--title {
        margin-left: -$line-height*6;
    }
}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

.column-details__content {
    margin-bottom: $line-height/3 !important;
}


// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

</style>
