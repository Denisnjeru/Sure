<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive > Job >  Categories
            </span>

            <div class="page__head--links">
                <span class="page__head--link button button-link">
                    QED Contract &nbsp;&nbsp; <font-awesome-icon icon="download" />
                </span>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        <span v-if="selectedJob !== null">{{selectedJob.title}}</span>&nbsp;>&nbsp;Categories
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

                    <p slot="category_name" slot-scope="{row}">
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

                    <p class="centered" slot="suppliers" slot-scope="{row}">
                        {{ row.participants }}
                    </p>
                    
                    <span class="actions" slot="actions" slot-scope="{row}">                        
                        <span class="actions__select" @click="selectCategory(row)">
                            <font-awesome-icon icon="eye"/>&nbsp;Suppliers
                        </span>
                        |
                        <span class="actions__select" @click="selectCategory(row)">
                            <font-awesome-icon icon="lock"/>&nbsp;Manage Access
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="categories.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import prequal from '@/services/company/prequal'
import tender from '@/services/company/tender'
import rfq from '@/services/company/rfq'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'category_name', 'code', 'status', 'suppliers', 'actions'],
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
        ...mapGetters('Archive',['selectedJob',]),
    },
    mounted() {
        this.getCategories()
    },
    methods: {
        selectCategory: function(category) {
            this.$store.dispatch('Archive/setSelectedCategory', {category})
            this.$router.push('/company/archive/jobs/' + this.$route.params.jobId + '/' + this.$route.params.sourcing_activity + '/categories/' + category.id + '/suppliers')
        },
        async getCategories() {
            if (this.$route.params.sourcing_activity === 'prequalification') {
                try {
                    const response = await prequal.categories(this.$route.params.jobId, this.page)
                    this.dataCount = response.data.count
                    this.categories = response.data.results
                } catch (err) {
                    console.log(err)
                }
            } else if (this.$route.params.sourcing_activity === 'tender') {
                try {
                    const response = await tender.categories(this.$route.params.jobId)
                    this.dataCount = response.data.count
                    this.categories = response.data.results
                } catch (err) {
                    console.log(err)
                }
            } else if (this.$route.params.sourcing_activity === 'rfq') {
                try {
                    const response = await rfq.categories(this.$route.params.jobId)
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
