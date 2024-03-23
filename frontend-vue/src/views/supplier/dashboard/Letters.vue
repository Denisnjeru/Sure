<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Letters
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        Letters
                    </p>
                    <div class="table-search__search">
                        <form v-on:submit.prevent="getLetters()">
                            <font-awesome-icon @click="getLetters()" class="table-search__search--icon" icon="search" />
                            <input @keyup.enter="getLetters()" v-model="searchQuery" class="table-search__search--input" type="text" placeholder="Search here">
                        </form>
                    </div>
                </div>
                <v-client-table :columns="columns" :data="letters" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="letters.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p class="link" slot="category" slot-scope="{row}">
                        <router-link to="/supplier/tender/ordered/categories/" v-if="row.sourcing_activity === 'tender'">
                            {{ row.category }}
                        </router-link>
                        <router-link :to="'/supplier/prequal/category/instructions/' + row.category_id" v-if="row.sourcing_activity === 'prequal'">
                            {{ row.category }}
                        </router-link>
                    </p>

                    <p slot="letter_Type" slot-scope="{row}">
                        {{ row.type }}
                    </p> 

                    <p slot="date" slot-scope="{row}">
                        {{ row.date | formatDateTime }}
                    </p> 

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <a v-if="row.letter !== null" class="actions__select" :href="row.letter" download> 
                            <font-awesome-icon icon="download"/>&nbsp;Download
                        </a>
                        <span v-else>
                            Not attached
                        </span>
                    </span>
                    
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="letters.length !== 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getLetters()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import dashboard from '@/services/supplier/dashboard'

export default {
    name: 'SupplierDashboardOngoingBids',
    data() {
        return {
            columns: ['#','category',  'company', 'job', 'letter_Type', 'date', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            letters: [],
            searchQuery: ''
        }
    },
    computed: {
        
    },
    mounted() {
        this.getLetters()
    },
    methods: {
        async getLetters() {
            try {
                if (this.searchQuery === '') {
                    const response = await dashboard.letters(this.page, this.dataPerPage)
                    this.letters = response.data.results
                    this.dataCount = response.data.count
                } else {
                    const response = await dashboard.letters(this.page, this.dataPerPage, this.searchQuery)
                    this.letters = response.data.results
                    this.dataCount = response.data.count
                }
            } catch (err) {
                console.log(err)
            }
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
