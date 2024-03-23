<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                Section: {{ section.name }}
            </span>
            <div class="page__head--links">
                <router-link :to="`/buyer/add/question/${this.$route.params.sectionId}/risk-management/`">
                    <a class="page__head--link button button-link">
                    Add Question
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__head2">
            <h1 class="page__head2--title">Section Details</h1>    
            <p class="page__head2--content">{{ section.description }}</p>
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
                <v-client-table :data="section.risk_questions" :columns="columns" :options="options">
                    <p class="table_link" slot="Question" slot-scope="{row}" @click="selectquestion(row)">
                            {{row.description}}
                    </p>
                    <p  slot="Type" slot-scope="{row}">
                            {{row.answer_type}}
                    </p>
                    <p  slot="Must" slot-scope="{row}">
                            {{row.is_required}}
                    </p>
                    <p  slot="Scored" slot-scope="{row}">
                            {{row.is_scored}}
                    </p>
                    <p  slot="Max" slot-scope="{row}">
                            {{row.max_score}}
                    </p>
                    <p  slot="QA" slot-scope="{row}">
                            {{row.is_qa}}
                    </p>
                    <a class= "row-no row-link" v-if="section.risk_questions.length !== 0" slot-scope="{row}"  slot="Actions">
                        <font-awesome-icon  class="row-link__edit" icon="pencil-alt" @click="onClickEditQuestion(row)"/>
                        <font-awesome-icon  class="row-link__delete" icon="trash-alt" @click="onClickDeleteQuestion(row)"/>
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
            'id', 'description', 'trans_description', 'short_description', 'trans_short_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'description_slug'
export default {
    name: 'risk-management-list-buyer',
    data () {
        return{
            columns: ['Question', 'Type', 'Must', 'Scored', 'Max', 'QA', 'Actions'],
            data: [
                {
                    'Question':'MetaVerse RFQ', 
                    'Type':'File Upload', 
                    'Must':true, 
                    'Scored': true,
                    'Max':0.0,
                    'QA':false
                },{
                    'Question':'MetaVerse RFQ', 
                    'Type':'Text', 
                    'Must':true, 
                    'Scored': true,
                    'Max':0.0,
                    'QA':false
                },{
                    'Question':'MetaVerse RFQ', 
                    'Type':'File Upload', 
                    'Must':true, 
                    'Scored': true,
                    'Max':0.0,
                    'QA':false
                },
                {
                    'Question':'MetaVerse RFQ', 
                    'Type':'Selection', 
                    'Must':true, 
                    'Scored': true,
                    'Max':0.0,
                    'QA':false
                },
            ],
            options: {
                headings : {

                },
                editableColumns:['Job Title'],
                sortable:['#', 'Question', 'Type', 'Must', 'Scored', 'Max', 'QA', 'Actions'],
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
            section: {
                "name": '',
                "description": '',
                "trans_name": '',
                "short_name": '',
                "parent_section": '',
                "category": '',
                "id": 0,
                "risk_questions": ''
            },
        }
    },
    mounted(){
        this.getRiskSection()
    },
    methods:{
        selectquestion: function(question){
            this.$router.push('/buyer/edit/question/'+ this.$route.params.sectionId + '/'+ question.id +'/risk-management/')
        },
        async onClickEditQuestion(question) {
            this.$router.push('/buyer/edit/question/'+ this.$route.params.sectionId +'/'+ question.id +'/risk-management/')
        },
        async onClickDeleteQuestion(question){
            await window.toast.fire(
                {
                    icon: 'question',
                    showDenyButton: true,  showConfirmButton: true,
                    confirmButtonText: 'Delete',
                    denyButtonText: `Don't delete`,
                    title: "do you want to delete this question !"
                }
            ).then((result) => {
                if (result.isConfirmed){
                    try {
                        const response = risk_management.deleteRiskQuestion(this.$route.params.sectionId, question.id)
                        console.log(response.data)
                        this.getRiskCategory()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            }) 
        },
        async getRiskSection(){
          try {
            const response = await risk_management.getRiskCategorySection(this.$route.params.categoryId, this.$route.params.sectionId)
            console.log(response.data)
            this.section = response.data
          } catch (err) {
            console.log(err)
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
    &__head2 {
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
        
        &--title {
            font-size: 15px;
            color: #121F3ECC;
            font-weight: 600;
        }

        &--content{
            font-size: 15px;
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
        
        &__edit{
            display: inline;
            margin-right: 1em;
            color: #4CAF50;
            
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }

        &__delete{
            display: inline;
            color: #FF6760;
            
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }
    }
}
</style>