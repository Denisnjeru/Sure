<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                List of Risk Assessment
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
                <v-client-table :data="riskassessments" :columns="columns" :options="options">
                    <p class="table_link" slot="Title" slot-scope="{row}" @click="selectriskassessment(row)">
                        {{row.title}}
                    </p>

                    <a class = "row-no row-link" v-if="riskassessments.length !== 0" slot-scope="{row}" slot="Actions" >
                        <font-awesome-icon  class="row-link__edit" icon="pencil-alt"/>
                        <font-awesome-icon  class="row-link__delete" icon="trash-alt" @click="deleteRiskAssesment(row.id)"/>
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
            columns: ['Title','Actions'],
            riskassessments: [],
            data: [
                {
                    'title':'Test Supply of Computer Servers QA',
                },{
                    'title':'Test Supply of Computer Servers QA',
                },{
                    'title':'Test Supply of Computer Servers QA',
                },
                {
                    'title':'Test Supply of Computer Servers QA',
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
        this.getRiskAssessments()
    },
    methods:{ 
        selectriskassessment: function(assessment){
            this.$router.push('/buyer/ra/'+this.$route.params.categoryId+'/'+assessment.id+'/risk-management/')
        },
        async getRiskAssessments(){
            try{
                const response = await risk_management.getRiskAssessments(this.$route.params.categoryId)
                console.log(response.data)
                this.riskassessments = response.data.results
            } catch(error){
                console.log(error)
            }
        },
        async deleteRiskAssesment(raid){
            await window.toast.fire(
                {
                    icon: 'question',
                    showDenyButton: true,  showConfirmButton: true,
                    confirmButtonText: 'Delete',
                    denyButtonText: `Don't delete`,
                    title: "do you want to delete this risk assessment !"
                }
            ).then((result) => {
                if (result.isConfirmed){
                    try {
                        const response = risk_management.deleteRiskAssessment(this.$route.params.categoryId, raid)
                        console.log(response.data)
                        this.getRiskAssessments()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            })
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
        text-align: center;
        
        &__link{
            display: inline;
            margin-right: 0.5em;
            color: #4CAF50;
            font-weight: 600;
            text-decoration: underline;
            
            &:hover, :focus {
                transform: translateX(-0.25em);
            }
        }

        &__text{
            display: inline;
            color: $color-blue-main;
        }

        &__edit{
            color: #4CAF50;
            display: inline;
            margin-right: 1em;
            
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateX(-0.25em);
            }
        }

        &__delete{
            display: inline;
            color: #FF6760;

            &:hover, :focus{
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em); 
            }
        }
    }
}
</style>