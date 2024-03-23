<template>
    <div class="risk_category_details">
        <div class="page__head">
            <div class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left" /> <span class="text">Back</span>
                </span>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Category Title: {{ riskcategory.name }} </p>
                </div>
                <div class="column-details__content">
                    <!--This is for QED Pages -->
                    <!-- <p class="detail">
                        <span class="detail__title">Owner:</span>
                        <span class="detail__text">DEMO TENDERSURE VERSION 2</span>
                    </p> -->
                    <p class="detail">
                        <span class="detail__title">Sourcing Activity:</span>
                        <span class="detail__text">Risk Management</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Category Type:</span>
                        <span class="detail__text">{{ riskcategory.category_type }}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Opening Date:</span>
                        <span class="detail__text"> {{ riskcategory.opening_date | moment }}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Closing Date:</span>
                        <span class="detail__text">{{ riskcategory.closing_date | moment }}</span>
                    </p>
                    <p class="detail">
                        <!--Todo list supporting documents-->
                        <span class="document">
                            <span class="document__title">
                                <span class="document__title--name">Supporting Documents</span>
                                <span class="document__title--icon">
                                    <font-awesome-icon class="icon" icon="folder-plus" />
                                </span>
                            </span>

                            <span v-for="doc in riskcategory.category_supporting_docs" :key="doc.id">
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
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Contact Details
                            </a>
                        </router-link>
                    </p>
                    <p class="detail_button">
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Send Category Notifications
                            </a>
                        </router-link>
                    </p>
                    <p class="detail_button">
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Invited Suppliers
                            </a>
                        </router-link>
                    </p>
                </div>
            </div>
        </div>

        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <div class="card_header">
                        <p class="card_header__text">Sections</p>
                        <router-link :to="`/buyer/add/section/${this.$route.params.categoryId}/risk-management/`">
                            <a class="button card_header__button">
                                Add Section
                            </a>
                        </router-link>
                        <router-link to="/buyer/add/category/job/:riskId/risk-management">
                            <a class="button card_header__button">
                                Preview
                            </a>
                        </router-link>
                    </div>
                </div>
                <div class="column-details__content">
                    <div class="table-search">
                        <p class="table-search__title">
                            <!-- Card Title Header -->
                        </p>
                        <div class="table-search__search">
                            <font-awesome-icon class="table-search__search--icon" icon="search"/>
                            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                        </div>
                    </div>
                    <v-client-table :data="riskcategory.risk_sections" :columns="columns" :options="options">
                        <p class="table_link" slot="Section" slot-scope="{row}" @click="selectsection(row)">
                            {{row.name}}
                        </p>
                        <p slot="Questions" slot-scope="{row}">
                            {{row.questions_count}}
                        </p>
                        <a class= "row-no row-link" v-if="riskcategory.risk_sections.length !== 0" slot-scope="{row}" slot="Actions">
                            <font-awesome-icon  class="row-link__edit" icon="pencil-alt" @click="onClickEditSection(row)"/>
                            <font-awesome-icon  class="row-link__delete" icon="trash-alt" @click="onClickDeleteSection(row)"/>
                        </a>
                    </v-client-table>
                    <div class="page__pagination">
                        <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                        </pagination>
                    </div>
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <div class="card_header">
                        <p class="card_header__text">Participants List</p>
                        <router-link to="/buyer/add/category/job/:riskId/risk-management">
                            <a class="button card_header__button">
                                Invite From:<font-awesome-icon icon="chevron-up" />
                            </a>
                        </router-link>
                        <a class="button card_header__button" @click="closeCategory(this.$route.params.categoryId)">
                            Close
                        </a>
                    </div>
                </div>
                <div class="column-details__content">
                    <div class="table-search">
                        <p class="table-search__title">
                            <!-- Card Title Header -->
                        </p>
                        <div class="table-search__search">
                            <font-awesome-icon class="table-search__search--icon" icon="search"/>
                            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                        </div>
                    </div>
                    <v-client-table :data="riskcategory.participants" :columns="columns2" :options="options">
                        <p class="table_link" slot="Company Name" slot-scope="{row}" @click="onRowClick()">
                            {{row.company_name}}
                        </p>
                        <p slot="Contact Name" slot-scope="{row}">
                            {{row.contact_name}}
                        </p>
                        <a class= "row-link"  slot="Actions"> 
                            <a class="row-link__link2" @click="onClickUpdateRA(riskcategory.no_assessments)" v-if="riskcategory.has_risk_assessment">
                                Update QA
                            </a>
                            <a class="row-link__link" @click="onClickConductRA()" v-else>
                                Conduct QA
                            </a>
                        </a>
                    </v-client-table>
                    <div class="page__pagination">
                        <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                        </pagination>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import risk_management from '@/services/company/risk_management'
import moment from 'moment'


export default {
    name: 'risk-management-details-category--buyer',
    data () {
        return{
            columns: [ 'Section', 'Questions', 'Actions'],
            columns2: ['Company Name', 'Contact Name', 'Actions'],
            data: [
                {
                    'Section':'Business compliance and continuity', 
                    'Questions':'3'
                },{
                    'Section':'Business compliance and continuity', 
                    'Questions':'3'
                },{
                    'Section':'Business compliance and continuity', 
                    'Questions':'3'
                },
                {
                    'Section':'Business compliance and continuity', 
                    'Questions':'3'
                },
            ],
            data2: [
                {
                    'Company Name':'Demo Supplier', 
                    'Contact Name':'Denis'
                },{
                     'Company Name':'Test User', 
                    'Contact Name':'Emmanuel'
                },{
                    'Company Name':'Demo Supplier', 
                    'Contact Name':'Simon'
                },
                {
                    'Company Name':'Test User', 
                    'Contact Name':'Xavier'
                },
            ],
            options: {
                headings : {

                },
                sortable:['#', 'Section', 'Questions', 'Actions'],
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
            riskcategory: {
                "name": '',
                "trans_name": '',
                "currency": '',
                "category_type": '',
                "id": 0,
                "status": '',
                "is_open":false,
                "bid_charge": 0.00,
                "unique_reference": '',
                "risk_sections": [],
                "participants": [],
                "category_supporting_docs": [],
                "opening_date": '',
                "closing_date": '',
                "has_risk_assessment": false
            },
            wordextensions: ['.doc', '.docx'],
            excelextensions: ['.xlsx', '.xls'],
            pdfextensions: ['.pdf']
        }
    },
    filters: {
        moment: function (date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    mounted(){
        this.getRiskCategory()
    },
    computed: {

    },
    methods:{
        selectsection: function(section){
            this.$router.push('/buyer/section/'+ this.$route.params.categoryId + '/'+ section.id +'/risk-management/')
        },
        onClickEditSection: function(section){
            this.$router.push('/buyer/edit/section/'+ this.$route.params.categoryId + '/'+ section.id +'/risk-management/')
        },
        onClickConductRA: function(){
            this.$router.push('/buyer/add/ra/'+ this.$route.params.categoryId +'/risk-management/')
        },
        onClickUpdateRA: function(){
           this.$router.push('/buyer/list/ra/'+ this.$route.params.categoryId +'/risk-management/')
        },
        async onRowClick() {
            this.$router.push('/buyer/section/'+ 1 +'/'+ 1 +'/risk-management/')
        },
        async onEditClick() {
            this.$router.push('/buyer/edit/section/'+ 1 +'/'+ 1 +'/'+ 1 +'/risk-management/')
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
                        const response = risk_management.deleteRiskCategorySupportingDocument(this.$route.params.categoryId, docid)
                        console.log(response.data)
                        this.getRiskCategory()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            })
        },
        async onClickDeleteSection(section){
            await window.toast.fire(
                {
                    icon: 'question',
                    showDenyButton: true,  showConfirmButton: true,
                    confirmButtonText: 'Delete',
                    denyButtonText: `Don't delete`,
                    title: "do you want to delete this section !"
                }
            ).then((result) => {
                if (result.isConfirmed){
                    try {
                        const response = risk_management.deleteRiskCategorySection(this.$route.params.categoryId, section.id)
                        console.log(response.data)
                        this.getRiskCategory()
                    } catch (err) {
                        console.log(err)
                    }      
                }
            }) 
        },
        async closeCategory(){

        },
        async getRiskCategory(){
            try {
                // :riskId, :categoryId
                const response = await risk_management.getRiskCategory(this.$route.params.riskId, this.$route.params.categoryId)
                console.log(response.data)
                this.riskcategory = response.data
            } catch (err) {
                console.log(err)
            }
        }
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
        text-align: center;

        &__link{
            display: inline;
            margin-right: 0.5em;
            color: #4CAF50;

            &:hover, :focus {
                cursor: pointer;
                transform: translateX(0.25em);
            }
        }

        &__link2{
            display: inline;
            margin-right: 0.5em;
            color: $color-blue-main;

            &:hover, :focus {
                cursor: pointer;
                transform: translateX(0.25em);
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

    .card_header{

        
        &__text{
            display: inline;
            color: $color-black-main;
            font-weight: 600;
            padding: 0 $line-height*10 0 0;
        }

        &__button{
            display: inline;
            margin-right: 1em;
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
            border-radius: 5px;
            box-sizing: border-box;


            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(255, 255, 255, 0.05);
                transform: translateY(-0.25em);
            }

        }
    }
}
</style>