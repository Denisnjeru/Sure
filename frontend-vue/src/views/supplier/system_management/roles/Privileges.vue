<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Roles
                <span class="page__head--sub_page">
                    <span class="sub_page__icon">
                        <font-awesome-icon class="sub_page__icon--icon" icon="chevron-right" />
                    </span>
                    <span class="sub_page__name">
                        Privileges
                    </span>
                </span>
            </span>
            <div class="page__head--links">
                
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Role Name: {{role.name}}
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="privileges" :options="options">    
                    <span slot="privilege_name" slot-scope="{row}">
                        {{row.title}}
                    </span>

                    <span slot="created" slot-scope="{row}">
                        {{row.created_at | formatDateTime}}
                    </span>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <span class="action actions__delete" v-if="row.has_privilege === true" @click="confirmDenyPrivilege(row)">
                            Deny Privilege
                        </span>
                        <span class="action actions__edit" v-else @click="assignRolePrivilege(row)">
                            Assign Privilege
                        </span>
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
import system_management from '@/services/supplier/system_management'

export default {
    name: 'SupplierSystemUserUsers',
    data() {
        return {
            columns: ['privilege_name', 'description', 'actions'],
            options: {
                sortable: ['privilege_name', 'created_at'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            role: {},
            privileges: [
            ]
        }
    },
    computed: {
        
    },
    mounted() {
        this.getRolePrivileges()
        this.getRole()
    },
    methods: {
        async getRole() {
            try {
                const response = await system_management.role(this.$route.params.id)
                this.role = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getRolePrivileges() {
            try {
                const response = await system_management.rolePrivileges(this.$route.params.id)
                this.dataCount = response.data.count
                this.privileges = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async assignRolePrivilege(privilege){
            console.log(privilege)
            try {
                let payload = {
                    "supplier_role": this.$route.params.id,
                    "supplier_privilege": privilege.id
                }
                await system_management.assignRolePrivilege(this.$route.params.id, payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Privilege assigned to ' + this.role.name
                })
                this.getRolePrivileges()
            } catch (err) {
                console.log(err.response)      
            } 
        },
        confirmDenyPrivilege: function(privilege) {
            this.$swal({
                text: 'Remove ' + privilege.title + ' privilege from role ' + this.role.name,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.denyPrivilege(privilege)    
                }
            });
        },
        async denyPrivilege(privilege) {           
            try {
                await system_management.deleteRolePrivilege(this.$route.params.id, privilege.id)                
            } catch (err) {
                window.toast.fire({
                    icon: 'success',
                    title: privilege.title + ' has been removed from role ' + this.role.name 
                })
                this.getRolePrivileges()
            }
        },
        async search() {
            console.log('search');
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
