<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Archive > Job > Category > Suppliers
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                        <span v-if="selectedCategory !== null">{{selectedCategory.name}}</span>&nbsp;>&nbsp;Suppliers
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="suppliers" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="suppliers.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    
                    <p slot="supplier" slot-scope="{row}">
                        {{ row.company_name }}
                    </p>

                    <p slot="contact_person" slot-scope="{row}">
                        {{ row.contact_name }}
                    </p>

                    <p slot="email" slot-scope="{row}">
                        {{ row.email_address }}
                    </p>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <span class="actions__select" @click="selectSupplier(row)"> 
                            <font-awesome-icon icon="eye"/>&nbsp;Documents
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="suppliers.length > 0">
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
    name: 'BWQedArchiveJobsCategorySuppliers',
    data() {
        return {
            columns: ['#', 'supplier', 'contact_person', 'phone_number', 'email', 'actions'],
            options: {
                sortable: ['supplier', 'email'],
                perPageValues: [20], 
                editableColumns:[],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            suppliers: []
        }
    },
    computed: {
        ...mapGetters('Archive',['selectedJob', 'selectedCategory',]),
    },
    mounted() {
        this.getSuppliers()
    },
    methods: {
        selectSupplier: function(supplier) {
            this.$store.dispatch('Archive/setSelectedSupplier', {supplier})
            this.$router.push('/qed/archive/'+ this.$route.params.sourcing_activity +'/categories/' + this.$route.params.categoryId + '/suppliers/' + supplier.id)
        },
        async getSuppliers() {
            try {
                if (this.$route.params.sourcing_activity === 'prequalification') {
                    const response = await prequal.category_participants(this.$route.params.categoryId, this.$route.params.jobId, this.page)
                    this.dataCount = response.data.count
                    this.suppliers = response.data.results
                } else if (this.$route.params.sourcing_activity === 'tender') {
                    const response = await tender.financial_participants(this.$route.params.jobId, this.$route.params.categoryId)
                    this.dataCount = response.data.count
                    this.suppliers = response.data.results
                } else if (this.$route.params.sourcing_activity === 'rfq') {
                    const response = await rfq.rfqGetParticipants(this.$route.params.jobId, this.$route.params.categoryId)
                    this.dataCount = response.data.count
                    this.suppliers = response.data.results
                } else {
                    this.suppliers = []
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
