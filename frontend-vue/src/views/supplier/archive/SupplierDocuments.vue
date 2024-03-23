<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive for <span v-if="selectedCategory !== null">{{selectedCategory.name}} ({{selectedCategory.job_name}})</span> 
            </span>
            <div class="page__head--links">
                
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        Category Reports
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
                <div class="table-search" v-if="$route.params.jobType !== 'RFQ'">
                    <p class="table-search__instruction">
                        Category Documents
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table v-if="$route.params.jobType !== 'RFQ'" :columns="columns" :data="documents" :options="options" class="hasRowNo hasArchive">
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
import archive from '@/services/supplier/archive'
import { mapGetters } from 'vuex'

export default {
    name: 'BuyerContractsSupplierCategorySuppliers',
    data() {
        return {
            columnsReports: ['#', 'report', 'actions'],
            columns: ['#', 'document', 'actions'],
            options: {
                sortable: ['document'],
                perPageValues: [20], 
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
                const response = await archive.documents(this.$route.params.categoryId, this.$route.params.jobType)
                this.documents = response.data.documents
                this.dataCount = response.data.documents.length
                this.other_documents = response.data.other_documents

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
