<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                List of Risk Management Jobs
            </span>
        </div>

        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__title">
                        <!-- Card Title Header -->
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search"/>
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :data="data" :columns="columns" :options="options">
                    <p class = "row-no" v-if="data.length !== 0" slot="#" slot-scope="props">
                        {{ props.index }}
                    </p>
                    <a class= "row-no row-link" v-if="data.length !== 0" slot="Apply">
                        <span class="row-link__text">Created  </span>
                        <font-awesome-icon  class="row-link__arrow" icon="chevron-right" />
                    </a>
                    <p v-if="data.length = 0">
                        Currently no Risk Management jobs.
                    </p>
                </v-client-table>
                <div class="page__pagination">
                    <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                    </pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'risk-management-list-supplier',
    data () {
        return{
            columns: ['#', 'Job Title', 'Job Code', 'Approved By', 'Status', 'Apply'],
            data: [
                {
                    'Job Title':'MetaVerse RFQ', 
                    'Job Code':'Test2', 
                    'Approved By':'help@qedsolutions.co.ke', 
                    'Status':'Closed'
                },{
                    'Job Title':'RFQ Branding Sevices', 
                    'Job Code':'Test2', 
                    'Approved By':'demo@company.com', 
                    'Status':'Closed'
                },{
                    'Job Title':'Test Negotiation', 
                    'Job Code':'Test2', 
                    'Approved By':'none', 
                    'Status':'Closed'
                },
                {
                    'Job Title':'DTB Risk Management', 
                    'Job Code':'Test1', 
                    'Approved By':'dtb@company.com', 
                    'Status':'Open'
                },
            ],
            options: {
                headings : {

                },
                editableColumns:['Job Title'],
                sortable:['Job Title', 'Job Code', 'status', ''],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
        }
    },
    methods: {
        async fetchData(){
            console.log(this.page)
        },
        async search(){
            console.log('search')
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page{
    &__head {
        @include grid_row;
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
        
        &--title {
            font-size: 25px;
            color: rgba(18, 31, 62, 0.8);
            font-weight: 600;
        }

    }
    &__content{
        margin: 0 !important;
        @include grid_column;
        width: 100%;
        padding: $line-height $line-height;
    }

    .row-link{
        color: rgba(18, 31, 62, 0.8);
        flex-flow: row nowrap;
        justify-content: space-evenly;
        
        &__text{
            text-decoration-line: underline;
        }
        &__arrow{
            display: inline;
            border-radius: 5px;
        }
    }
}
</style>