<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Companies
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="companies" :options="options" class="hasRowNo hasNoWrap">
                    <p class="row-no" v-if="companies.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    <p slot="company" class="hasLogo" slot-scope="{row}">
                        <img class="logo" :src="row.company_logo_url" alt="">
                        <span>{{row.company_name}}</span>
                    </p>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <span @click="selectCompany(row)" class="actions__select">
                            <font-awesome-icon icon="eye"/> &nbsp;Categories
                        </span>
                    </span>

                </v-client-table>
                
            </div>
            <div class="page__pagination" v-if="companies.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getCompanies()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import archive from '@/services/supplier/archive'
import {mapGetters} from 'vuex'

export default {
    name: 'Jobs',
    data() {
        return {
            columns: ['#', 'company', 'actions'],
            options: {
                sortable: ['company',],
                perPageValues: [20], 
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            companies: []
        }
    },
    computed: {
        ...mapGetters('Auth', ['authUser']),
    },
    mounted() {
        this.getCompanies()
    },
    methods: {
        selectCompany: function(company) {
            this.$router.push('/supplier/archive/companies/' + company.id + '/categories')
        },
        async getCompanies() {
            try {
                const response = await archive.companies()
                this.companies = response.data
                this.dataCount = this.companies.length
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
