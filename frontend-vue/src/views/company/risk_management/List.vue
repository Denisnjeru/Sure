<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                List of Risk Management Jobs
            </span>

            <div class="page__head--links">
                <router-link to="/buyer/add/job/risk-management">
                    <a class="page__head--link button button-link">
                    New Risk Management Job 
                    </a>
                </router-link>
            </div>
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
                <v-client-table :data="risks" :columns="columns" :options="options">
                    <p class="table_link" slot="Job Title" slot-scope="{row}" @click="selectjob(row)">
                        {{row.title}}
                    </p>

                    <p slot="Job Code" slot-scope="{row}">
                        {{row.unique_reference}}
                    </p>

                    <a class= "row-no row-link" v-if="data.length !== 0" slot="actions" slot-scope="{row}">
                        <p class="row-link__edit" @click="addcategory(row)">Add Category</p>
                    </a>
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
import risk_management from '@/services/company/risk_management'
import { mapGetters } from 'vuex'

export default {
    name: 'risk-management-list-buyer',
    data () {
        return{
            columns: ['Job Title', 'Job Code', 'created_by', 'status' ,'actions'],
            risks: [],
            data: [
                {
                    'Job_Title':'MetaVerse RFQ', 
                    'Job_Code':'Test2', 
                    'Approved_By':'help@qedsolutions.co.ke', 
                    'Status':'Closed'
                },{
                    'Job_Title':'RFQ Branding Sevices', 
                    'Job_Code':'Test2', 
                    'Approved_By':'demo@company.com', 
                    'Status':'Closed'
                },{
                    'Job_Title':'Test Negotiation', 
                    'Job_Code':'Test2', 
                    'Approved_By':'none', 
                    'Status':'Closed'
                },
                {
                    'Job_Title':'DTB Risk Management', 
                    'Job_Code':'Test1', 
                    'Approved_By':'dtb@company.com', 
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
    computed:{
        ...mapGetters('Risk',['selectedJob',]),
    },
    mounted(){
        this.getRisks()
    },
    methods:{ 
        selectjob: function(job){
            this.$router.push('/buyer/details/job/'+ job.id +'/risk-management/')
        },
        addcategory: function(job){
            this.$router.push('/buyer/add/category/job/'+job.id+'/risk-management')
        },
        async getRisks(){
            try{
                const response = await risk_management.risks()
                console.log(response.data)
                this.dataCount = response.data.count
                this.risks = response.data.results
            } catch(error){
                console.log(error)
            }
        },
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
    .table_link{
        color: #0859B9;
        
        &:hover, :focus {
            cursor: pointer;
            transform: translateX(-0.25em);
        }
    }

    .row-link{
        &__edit{
            color: #4CAF50;
            font-weight: 600;
            text-decoration: underline;
            
            &:hover, :focus {
                transform: translateX(-0.25em);
            }
        }
    }
}
</style>