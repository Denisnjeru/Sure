<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Supplier Contracts
            </span>
            <div class="page__head--links">
                <router-link :to="'/buyer/contracts/supplier/categories/'+$route.params.categoryId+'/suppliers'">
                    <a class="page__head--link button button-link">
                        Upload New Contract
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       <span v-if="selectedCategory !== null">{{selectedCategory.name}} -</span> Currently available contracts
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="supplierContracts" :options="options" class="hasRowNo hasNoWrap">
                    <p class="row-no" v-if="supplierContracts.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p slot="supplier" slot-scope="{row}">
                        {{row.name}}
                    </p>

                    <p  class="capitalize" slot="approval" slot-scope="{row}">
                        {{row.approval_status}}
                    </p>

                    <p  class="capitalize" slot="status" slot-scope="{row}">
                        {{row.status}}
                    </p>

                    <span class="view" slot="contract">
                        <font-awesome-icon class="view__icon" icon="eye" />
                        <span> View Contract</span>
                    </span>
                    
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/buyer/contracts/supplier/contract/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
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
import contracts from '@/services/company/contracts'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'supplier', 'contact_person', 'phone_number', 'contract', 'status', 'approval', 'start_date', 'end_date', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            data: [
                {
                    supplier: 'ABC Stationers Limited',
                    contact_person: 'Emmanuel',
                    phone_number: '072222222',
                    status: 'In-Complete',
                    start_date: 'April 26, 2022',
                    end_date: 'June 11, 2022'
                },
            ],
            supplierContracts: []
        }
    },
    computed: {
        ...mapGetters('Contracts',['selectedCategory',]),
    },
    mounted() {
        this.getContracts()
    },
    methods: {
        async getContracts() {
            try {
                const response = await contracts.supplierContracts(this.$route.params.categoryId)
                this.dataCount = response.data.count
                this.supplierContracts = response.data.results
            } catch (err) {
                console.log(err)
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
