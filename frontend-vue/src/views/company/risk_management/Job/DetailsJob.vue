<template>
    <div class="risk_job_details">
        <div class="page__head">
            <div class="page__head--title">
                <span class="left nav-links__link">
                    <router-link to="/buyer/list/risk-management"><font-awesome-icon icon="chevron-left" /> <span class="text">Back</span></router-link>
                </span>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Job Title: {{ risk.title }}</p>
                </div>
                <div class="column-details__content">
                    <p class="detail">
                        <span class="detail__title">Sourcing Activity:</span>
                        <span class="detail__text">Risk Management</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Job Code:</span>
                        <span class="detail__text">{{ risk.unique_reference }}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Approval Status:</span>
                        <span v-if="risk.approved" class="detail__text_approved">Approved!Suppliers can access this job.</span>
                        <a class="button detail__button-approve-job" @click="approvejob()" v-else>Approve Job</a>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Import Questions from Excel:</span>
                        <a class="button detail__button-detail" :href=risk.questions_template>
                            <span class="detail__button-detail__button-text">Questions Template</span><font-awesome-icon  class="detail__button-detail__button-text" icon="inbox"/>
                        </a>
                        <span class="document">
                            <span class="document__title">
                                <span class="document__title--name">Supporting Documents</span>
                                <span class="document__title--icon">
                                    <font-awesome-icon class="icon" icon="folder-plus" />
                                </span>
                            </span>

                            <span v-for="doc in risk.supporting_docs" :key="doc.id">
                                <span class="document__name">
                                    <span class="document__name--text">
                                        <img :src="extensionSource(doc.documentextension)" class="icon">
                                        <span class="name">{{ doc.documentname }}</span>
                                    </span>
                                    <span class="document__name--delete" @click="deletesupportingdoc(doc.id)">
                                        <span class="selected__icon">
                                            <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                        </span> 
                                    </span>
                                </span>
                            </span>
                        </span>
                    </p>
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__content_documents">
                    <p class="detail_button">
                        <router-link to="/buyer/reports/job/${this.$route.params.riskId}/risk-management/">
                            <a class="button button-detail">
                                View Reports
                            </a>
                        </router-link>
                    </p>
                    <p class="detail_button">
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Send Job Notifications
                            </a>
                        </router-link>
                    </p>
                </div>
            </div>
        </div>
        <div class="page__head">
            <span class="page__head--title">
                Categories belonging to this job 
            </span>

            <div class="page__head--links">
                <a class="page__head--link button button-link" @click="addcategory()">
                    Add Category
                </a>
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
                <v-client-table :data="risk.risk_categories" :columns="columns" :options="options">                    
                    <p class="table_link" slot="category name" slot-scope="{row}" @click="selectcategory(row)">
                        {{row.name}}
                    </p>

                    <p slot="status" slot-scope="{row}" @click="selectcategory(row)">
                        {{row.is_open}}
                    </p>

                    <a class= "row-link" v-if="risk.risk_categories.length !== 0" slot="Actions">
                        <a class="row-link__link">QA</a>
                        <a class="row-link__link">DD</a>
                    </a>

                    <p class = "row-link" v-if="risk.risk_categories.length !== 0" slot="More Actions" >
                        <font-awesome-icon  class="row-link__edit" icon="pencil-alt"/>
                        <font-awesome-icon  class="row-link__delete" icon="trash-alt"/>
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
import risk_management from '@/services/company/risk_management'

export default {
    name: 'risk-management-details-buyer',
    data () {
        return{
            columns: ['category name', 'bid_charge', 'category_type', 'status', 'Actions', 'More Actions'],
            data: [
                {
                    'Category_Name':'January Risk Management 2022', 
                    'Bid_Fee':'KES 0.00', 
                    'Category_Type':'G0005 - Supply of computers, laptops, tablets and accessories', 
                    'Status':'False'
                },{
                    'Category_Name':'January Risk Management 2022', 
                    'Bid_Fee':'KES 0.00', 
                    'Category_Type':'G0006 - Supply of pharmaceutical dugs', 
                    'Status':'False'
                },{
                    'Category_Name':'January Risk Management 2022', 
                    'Bid_Fee':'KES 0.00', 
                    'Category_Type':'G0005 - Provision of security guarding services', 
                    'Status':'False'
                },
                {
                    'Category_Name':'January Risk Management 2022', 
                    'Bid_Fee':'KES 0.00', 
                    'Category_Type':'G0005 - Provision of debt collection services', 
                    'Status':'False'
                },
            ],
            options: {
                headings : {

                },
                sortable:['#','Category Name', 'Bid Fee', 'Category Type', 'Status', 'Actions', 'More Actions'],
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
            risk: {
                "approved": false,
                "approved_by": '',
                "company": 0,
                "created_by": '',
                "id": 0,
                "status": '',
                "title": '',
                "unique_reference": '',
                "questions_template": '',
                "supporting_docs": [],
                "risk_categories":[],
            },
            wordextensions: ['.doc', '.docx'],
            excelextensions: ['.xlsx', '.xls'],
            pdfextensions: ['.pdf']
        }
    },
    mounted(){
        this.getRisk()
    },
    computed: {

    },
    methods:{
        selectcategory: function(category){
            this.$router.push('/buyer/category/'+ this.$route.params.riskId + '/'+ category.id +'/risk-management/')
        },
        addcategory: function(){
            this.$router.push('/buyer/add/category/job/'+ this.$route.params.riskId +'/risk-management')
        },
        extensionSource(ext){

            // Word Extensions
            if (this.wordextensions.includes(ext) == true) {
                return require("@/assets/word.png")
            }

            // Excel Extensions
            if (this.excelextensions.includes(ext) == true){
                return require('@/assets/excel.png')
            }

            // PDF Extensions
            if (this.pdfextensions.includes(ext) == true){
                return require('@/assets/adobe.png')
            }

            return require('@/assets/support_doc.png')
        },
        async approvejob(){
            await window.toast.fire({
                icon: 'question',
                showDenyButton: true,  showConfirmButton: true,
                confirmButtonText: 'Approve',
                denyButtonText: `Don't approve`,
                title: "do you want to approve this job !"
            }).then((result) => {
                if (result.isConfirmed){
                    try {
                        const response = risk_management.approveRisk(this.$route.params.riskId)
                        console.log(response.data)
                        this.getRisk()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            })
        },
        async deletesupportingdoc(docid){
            await window.toast.fire(
                {
                    icon: 'question',
                    showDenyButton: true,  showConfirmButton: true,
                    confirmButtonText: 'Delete',
                    denyButtonText: `Don't delete`,
                    title: "do you want to delete this document !"
                }
            ).then((result) => {
                if (result.isConfirmed){
                    try {
                        const response = risk_management.deleteRiskSupportingDocument(this.$route.params.riskId, docid)
                        console.log(response.data)
                        this.getRisk()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            })
        },
        async getRisk(){
          try {
            const response = await risk_management.getRisk(this.$route.params.riskId)
            console.log(response.data)
            this.risk = response.data
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
    &__content{
        width: 100%;
        padding: $line-height $line-height;

        .column-details {
            margin: 0 $line-height/4;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: 0;
            margin-bottom: $line-height/2;

            &__head {
                background: $color-baby-blue;
                padding: $line-height/4 $line-height;
                border-radius: $line-height/2 $line-height/2 0 0;

                &--title {
                    color: rgba(18, 31, 62, 0.8);
                    font-size: $font-size-title;
                    font-weight: 600;
                    margin-bottom: $line-height/6 !important;
                }

                &--desc {
                    color: $color-black-medium;
                    margin: $line-height/4 0;
                }
            }

            &__content {
                padding: $line-height/2 $line-height;
                margin-bottom: $line-height*2;

                .detail {
                    padding: $line-height 0;
                    border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

                    &__title {
                        font-weight: 600;
                        margin-right: $line-height/2;
                        color: $color-black-main;
                    }

                    &__text {
                        color: $color-lightblue-text;
                    }
                    &__text_approved{
                        color: #4CAF50;
                    }

                    &__button-approve-job{
                        width: 200px;
                        font-size: $font-size-text;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: 1px solid $color-blue-main;
                        border-radius: 5px;
                        transform: rotate(0.02deg);

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                    &__button-detail {

                        width: 200px;
                        color: $color-blue-main;
                        font-size: $font-size-text;
                        background-color: $color-white-main;
                        border: 1px solid $color-blue-main;
                        border-radius: 5px;
                        transform: rotate(0.02deg);

                        &__button-text{
                            display: inline;
                            margin-right: 1em;
                        }

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                }


                .document {
                    padding: $line-height 0;
                    border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
                    position: relative;
                    z-index: 1;

                    &__status {
                        position: absolute;
                        z-index: 20;
                        padding: $line-height/6 $line-height/3;
                        color: $color-lightblue-text;
                        background: #F2F6FF;
                        border: 1px solid #073A82;
                        box-sizing: border-box;
                        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                        border-radius: 10px;
                        font-size: $font-size-small;
                        left: 60%;
                        display: none;
                    }                    

                    &__title {
                        width: 100%;
                        @include grid_row;
                        margin-top: 2em;
                        &--name {
                            font-weight: 600;
                            color: $color-black-main;
                        }

                        &--icon {
                            color: $color-gray-main;
                        }

                        .missing {
                            color: $color-red-main;
                        }
                    }

                    &__name {
                        width: 100%;
                        @include grid_row;
                        align-items: center;
                        margin-top: $line-height/3;
                        background: #F8F8F8;
                        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                        border-radius: $line-height/2;
                        padding: $line-height/4 $line-height/2;
                        font-size: $font-size-text;

                        &--text {
                            @include grid_row;
                            align-items: center;

                            .icon {
                                margin-right: $line-height/4;
                                height: $line-height;
                            }
                        }

                        &--delete {

                            .selected__icon {
                                margin: 0 $line-height/4;

                                &--img {
                                    height: $line-height/1.2;
                                    padding: $line-height/6;
                                    background-color: $color-gray-main;
                                    color: $color-white-main;
                                    border-radius: 50%;
                                    cursor: pointer;

                                    &:hover {
                                        background-color: $color-red-main;
                                    }
                                }
                            }
                        }

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateX(-0.25em);
                        }
                    }

                    &:hover {
                        .doc-missing {
                            color: $color-red-main;
                            cursor: pointer;
                        }

                        .document__status {
                            display: block;
                        }
                    }
                }
            }
            &__content_documents{
                padding: $line-height*2 0;
                margin-bottom: $line-height;
                display: block;
                text-align: center;


                .detail_button {
                    padding: $line-height $line-height*2;

                    .button-detail {
                        width: 300.51px;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: none;                
                        font-size: $font-size-text;
                        border-radius: 5px;
                        box-sizing: border-box;
                        transform: rotate(0.02deg);


                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                }
            }
        }
    }

    .table_link{
        color: #0859B9;
        
        &:hover, :focus {
            cursor: pointer;
            transform: translateX(-0.25em);
        }
    }

    .row-link{

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
            display: inline;
            margin-right: 1em;
            color: #4CAF50;

            &:hover, :focus{
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
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