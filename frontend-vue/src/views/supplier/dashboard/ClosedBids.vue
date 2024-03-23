<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Closed Bids
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        Categories
                    </p>
                    <div class="table-search__search">
                        <form v-on:submit.prevent="getCategories()">
                            <font-awesome-icon @click="getCategories()" class="table-search__search--icon" icon="search" />
                            <input @keyup.enter="getCategories()" v-model="searchQuery" class="table-search__search--input" type="text" placeholder="Search here">
                        </form>
                    </div>
                </div>
                <v-client-table :columns="columns" :data="categories" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="categories.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p class="link" slot="category_name" slot-scope="{row}">
                        <router-link to="/supplier/tender/ordered/categories/" v-if="row.target === 'tender'">
                            {{ row.name }}
                        </router-link>
                        <router-link :to="'/supplier/prequal/category/instructions/' + row.id" v-if="row.target === 'prequal'">
                            {{ row.name }}
                        </router-link>
                    </p>

                    <p slot="closing_date" slot-scope="{row}">
                        {{ row.closing_date | formatDateTime }}
                    </p> 

                    <p class="actions" slot="actions" slot-scope="{row}">                            
                        <router-link to="/supplier/tender/ordered/categories/" v-if="row.target === 'tender'">
                            <a class="actions__cart-icon actions__icon">
                                <font-awesome-icon icon="eye" />
                            </a>
                        </router-link>
                        <router-link :to="'/supplier/prequal/category/instructions/' + row.id" v-if="row.target === 'prequal'">
                            <a class="actions__cart-icon actions__icon">
                                <font-awesome-icon icon="eye" />
                            </a>
                        </router-link>
                    </p>    
                    
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="categories.length !== 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getCategories()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import dashboard from '@/services/supplier/dashboard'

export default {
    name: 'SupplierDashboardClosedBids',
    data() {
        return {
            columns: ['#','category_name',  'company', 'job', 'closing_date', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            categories: [],
            searchQuery: ''
        }
    },
    computed: {
        
    },
    mounted() {
        this.getCategories()
    },
    methods: {
        async getCategories() {
            try {
                if (this.searchQuery === '') {
                    const response = await dashboard.closedBids(this.page, this.dataPerPage)
                    this.categories = response.data.results
                    this.dataCount = response.data.count
                } else {
                    const response = await dashboard.closedBids(this.page, this.dataPerPage, this.searchQuery)
                    this.categories = response.data.results
                    this.dataCount = response.data.count
                }
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
