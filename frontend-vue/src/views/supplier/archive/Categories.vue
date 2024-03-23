<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive > Categories
            </span>

            <div class="page__head--links">
                
            </div>
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

                    <p slot="job_name" slot-scope="{row}">
                        {{ row.job_name }}
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
                            <font-awesome-icon icon="eye"/>&nbsp;Documents
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
import archive from '@/services/supplier/archive'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'job_name', 'category_name', 'code', 'status', 'actions'],
            options: {
                sortable: ['job_name', 'category_name'],
                perPageValues: [20], 
                filterable: false,
                pagination: {show: true, dropdown: true},
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
            this.$router.push('/supplier/archive/' + category.job_type + '/categories/' + category.id + '/documents')
        },
        async getCategories() {
            try {
                const response = await archive.categories(this.$route.params.companyId)                
                this.categories = response.data
                this.dataCount = this.categories.length
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
