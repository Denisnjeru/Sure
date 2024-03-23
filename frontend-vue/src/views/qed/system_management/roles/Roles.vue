<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Roles
            </span>
            <div class="page__head--links">
                <router-link :to="'/qed/user/roles/create'">
                    <a class="page__head--link button button-link">
                        Add Role
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Roles
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="roles" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="roles.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    
                    <span class="view" slot="role" slot-scope="{row}">
                        <router-link :to="'/qed/user/roles/' + row.id + '/update'">
                            <span>{{row.role}}</span>
                        </router-link>
                    </span>
                                        
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/qed/user/roles/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete" @click="confirmDeleteRole(row)">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                        <router-link :to="'/qed/user/roles/' + row.id + '/privileges'">
                            <span class="actions__edit">
                               Privileges
                            </span>
                        </router-link>
                    </span>

                    <span slot="created" slot-scope="{row}">
                        {{row.created_at | formatDateTime}}
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
import user_management from '@/services/qed/user_management'

export default {
    name: 'QedUserManagementRoles',
    data() {
        return {
            columns: ['#', 'name', 'description', 'actions'],
            options: {
                editableColumns:[],
                sortable: ['company', 'job'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            roles: [
               
            ]
        }
    },
    computed: {
        
    },
    mounted() {
        this.getRoles()
    },
    methods: {
        async getRoles() {
            try {
                const response = await user_management.roles(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.roles = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        confirmDeleteRole: function(role) {
            this.$swal({
                text: 'This role will be permanently deleted',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.deleteRole(role)    
                }
            });
        },
        async deleteRole(role) {           
            try {
                await user_management.deleteRole(role.id)                
            } catch (err) {
                window.toast.fire({
                    icon: 'success',
                    title: role.name + ' role deleted successfully'
                })
                this.getRoles()
            }
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
