<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                User logs
            </span>
            <div class="page__head--links">
                
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Logs
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="logs" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="logs.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <span slot="ip_address" slot-scope="{row}">
                        {{row.remote_addr}}
                    </span>

                    <span slot="activity" slot-scope="{row}">
                        {{row.url}}
                    </span>
                                        
                    <span slot="date" slot-scope="{row}">
                        {{row.created_at | formatDateTime}}
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="logs.length !== 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getRoles()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import auth from '@/services/authentication/auth'

export default {
    name: 'SupplierUserManagementLogs',
    data() {
        return {
            columns: ['ip_address', 'activity', 'date'],
            options: {
                sortable: ['ip_address', 'date'],
                perPageValues: [10], 
                pagination: {show: false, dropdown: false},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 10,
            logs: [
               
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
                const response = await auth.logs(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.logs = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        
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
