<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Live Jobs > Supply of Laptops
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        Categories
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="categories" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="categories.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p class="link" slot="category_name" slot-scope="{row}">
                        {{ row.name }}
                    </p>

                    <p slot="code" slot-scope="{row}">
                        {{ row.unique_reference }}
                    </p>

                    <p slot="status" slot-scope="{row}">
                        <span v-if="row.is_open === false">
                            Closed
                        </span>
                        <span v-else>
                            Open
                        </span>
                    </p>
                    
                    <span class="actions" slot="actions" slot-scope="{row}">                        
                        <router-link :to="'/buyer/livejobs/categories/' + row.id + '/participants'" class="actions__button button">
                            Participants List
                        </router-link>
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
import prequal from '@/services/company/prequal'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'category_name', 'code', 'status', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            categories: []
        }
    },
    computed: {
        ...mapGetters('Contracts',['selectedJob',]),
    },
    mounted() {
        this.getCategories()
    },
    methods: {
        selectCategory: function() {
        },
        async getCategories() {
            if (this.$route.params.sourcing_activity === 'prequalification') {
                try {
                    const response = await prequal.categories(this.$route.params.jobId)
                    this.dataCount = response.data.count
                    this.categories = response.data.results
                } catch (err) {
                    console.log(err)
                }
            } else {
                this.categories = []
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
