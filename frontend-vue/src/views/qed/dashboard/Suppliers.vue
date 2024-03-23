<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Jobs
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="jobs" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="jobs.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p slot="company">
                        Gathage Buyer
                    </p>

                    <p class="standard-column link" slot="job" slot-scope="{row}">
                        <router-link :to="'/buyer/livejobs/' + row.id + '/' + row.sourcing_activity + '/categories'">
                            {{ row.title }}
                        </router-link>
                    </p>

                    <p slot="code" slot-scope="{row}">
                        {{ row.unique_reference }}
                    </p>

                    <p class="standard-column capitalize" slot="sourcing_activity" slot-scope="{row}">
                        {{ row.sourcing_activity }}
                    </p>      
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getJobs()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
import {mapGetters} from 'vuex'

export default {
    name: 'Jobs',
    data() {
        return {
            columns: ['#', 'company', 'job', 'code', 'sourcing_activity'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            jobs: []
        }
    },
    computed: {
        ...mapGetters('Auth', ['authUser']),
    },
    mounted() {
        this.getJobs()
    },
    methods: {
        selectJob: function() {
        },
        async getJobs() {
            try {
                const response = await contracts.jobs(1)
                this.dataCount = response.data.count
                this.jobs = response.data.results
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
