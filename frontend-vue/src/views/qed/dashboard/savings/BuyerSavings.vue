<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Savings > <span class="title__active">Gathage Buyer</span>
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

                    <span class="actions" slot="actions">                        
                        <span class="actions__button button" @click="popupDownload()">
                            <font-awesome-icon class="actions__icon" icon="download" />
                            Download Report
                        </span>
                    </span>  
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getJobs()">
                </pagination>
            </div>
        </div> 
        <div class="popup" v-if="popDownload === true">
            <span class="popup__details">
                <div class="page__head">
                    <span class="page__head--title">
                        <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupDownload()" />
                        Contract Revision History
                    </span>

                    <div class="page__head--links">
                        
                    </div>
                </div>
                <div class="page__content columns">
                    <div class="column is-12">
                        
                    </div>                        
                </div>
            </span>
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
            columns: ['#', 'job', 'code', 'sourcing_activity', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            jobs: [],
            popDownload: false
        }
    },
    computed: {
        ...mapGetters('Auth', ['authUser']),
    },
    mounted() {
        this.getJobs()
    },
    methods: {
        popupDownload: function() {
            this.popDownload = !this.popDownload
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

.popup {
    position: absolute; 
    top: 20vh;
    width: 90%;
    height: 100%; 
    z-index: 90;
    @include grid_row;
    align-items: flex-start;
    transition: opacity .3s;
    
    &__details {
        // position: sticky;
        top: 20vh;
        min-height: 60vh;
        background-color: $color-white-main;
        $width: 40%;
        width: $width;
        margin: 5vh calc((100% - #{$width})/2);
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: $line-height $line-height/3;

        .page__content {
            padding-top: $line-height*2;
        }

        .column-page {
            box-shadow: none;
            padding: 0 $line-height;
            border-radius: 0;
            
            &:first-child {
                border-right: 1px solid $color-gray-medium;
            }
        }
    }
}

</style>
