<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive for <span v-if="selectedCategory !== null">{{selectedCategory.name}}</span> ( <span v-if="selectedSupplier !== null">{{selectedSupplier.company_name}} - {{selectedSupplier.email_address}}</span> )
            </span>
            <div class="page__head--links">
                
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        Supplier Reports
                    </p>
                    <div class="table-search__search">
                    </div>
                </div>
                <v-client-table :columns="columnsReports" :data="other_documents" :options="options" class="hasRowNo hasArchive">
                    <p class="row-no" v-if="other_documents.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    
                    <p slot="report" slot-scope="{row}">
                        {{ row.name }}
                    </p>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <a v-if="row.document_url !== null" class="actions__select" :href="row.document_url" download> 
                            <font-awesome-icon icon="download"/>&nbsp;Download
                        </a>
                        <span v-else>
                            Not available
                        </span>
                    </span>
                </v-client-table>
                <div class="table-search">
                    <p class="table-search__instruction">
                        Supplier Documents
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="documents" :options="options" class="hasRowNo hasArchive">
                    <p class="row-no" v-if="documents.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    
                    <p slot="document" slot-scope="{row}">
                        {{ row.short_description }}
                    </p>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <a v-if="row.supplier_response !== null" class="actions__select" :href="row.supplier_response.document_url" download> 
                            <font-awesome-icon icon="download"/>&nbsp;Download
                        </a>
                        <span v-else>
                            Not attached
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="documents.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import prequal from '@/services/company/prequal'
import tender from '@/services/company/tender'
import rfq from '@/services/company/rfq'

import { mapGetters } from 'vuex'

export default {
    name: 'BuyerContractsSupplierCategorySuppliers',
    data() {
        return {
            columnsReports: ['#', 'report', 'actions'],
            columns: ['#', 'document', 'actions'],
            options: {
                sortable: ['document'],
                editableColumns:[],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            documents: [],
            other_documents: []
        }
    },
    computed: {
        ...mapGetters('Archive',['selectedJob', 'selectedCategory', 'selectedSupplier']),
    },
    mounted() {
        this.getSupplierDocuments()
    },
    methods: {
        async getSupplierDocuments() {
            try {
                if (this.$route.params.sourcing_activity === 'prequalification') {
                    const response = await prequal.participant_documents(this.$route.params.categoryId, this.$route.params.supplierId)
                    this.documents = response.data.documents
                    this.dataCount = response.data.documents.length
                    this.other_documents = response.data.other_documents
                } else if (this.$route.params.sourcing_activity === 'tender') {
                    const response = await tender.participant_documents(this.$route.params.categoryId, this.$route.params.supplierId)
                    this.documents = response.data.documents
                    this.dataCount = response.data.documents.length
                    this.other_documents = response.data.other_documents
                } else if (this.$route.params.sourcing_activity === 'rfq') {
                    const response = await rfq.participant_documents(this.$route.params.categoryId, this.$route.params.supplierId)
                    this.documents = response.data.documents
                    this.dataCount = response.data.documents.length
                    this.other_documents = response.data.other_documents
                } else {
                    this.documents = []
                }
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
