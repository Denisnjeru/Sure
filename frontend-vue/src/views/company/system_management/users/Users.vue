<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                User Management
            </span>
            <div class="page__head--links">
                <router-link :to="'/buyer/user/users/create/'">
                    <a class="page__head--link button button-link">
                        Add New User
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Users (Buyer Admins)
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="users" :options="options" class="hasNoWrap">

                    <p class="view" slot="name" slot-scope="{row}">
                        {{row.first_name}} {{row.last_name}}
                    </p>

                    <span class="actions" slot="status" slot-scope="{row}">
                        <span class="actions__edit action" v-if="row.is_active === false" @click="activate_user()">
                            Activate
                        </span>
                        <span class="actions__delete action" v-else @click="deactivate_user()">
                            Deactivate
                        </span>
                    </span>

                    <span class="view" slot="role" slot-scope="{row}">
                        <router-link :to="'buyer/system/roles/' + row.id + '/privileges'">
                            <span> {{row.buyer_role.name}}</span>
                        </router-link>
                    </span>

                    <span slot="last_login" slot-scope="{row}">
                        {{row.last_login}}
                    </span>

                    <span slot="invitation_email">
                        <span class="button table-button" @click="resend_email()">Resend</span>
                    </span>
                    
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/buyer/user/users/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>

                    <span class="view" slot="date_joined" slot-scope="{row}">
                        {{row.date_joined}}
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import system_management from '@/services/company/system_management'

export default {
    name: 'BuyerSystemUserUsers',
    data() {
        return {
            columns: ['name', 'email', 'status', 'role', 'last_login', 'invitation_email', 'actions', 'date_joined'],
            options: {
                sortable: ['name', 'email'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 0,
            dataPerPage: 20,
            users: []
        }
    },
    computed: {
        
    },
    mounted() {
        this.getUsers()
    },
    methods: {
        async getUsers() {
            try {
                const response = await system_management.users()
                this.dataCount = response.data.count
                this.users = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        async resend_email() {
            window.toast.fire({
                icon: 'success',
                title: 'If you are registered with that email address on this system an email containing a reset link will be sent to you shortly. Otherwise, no communication will be sent.'
            })
        },
        async activate_user() {
            window.toast.fire({
                icon: 'success',
                title: 'User account has been successfully activated!.'
            })
        },
        async deactivate_user() {
            window.toast.fire({
                icon: 'success',
                title: 'User account has been successfully deactivated!'
            })
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}

</style>
