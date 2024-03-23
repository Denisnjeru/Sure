<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Participants
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       <span v-if="selectedCategory !== null">{{selectedCategory.name}} -</span> Select supplier to award contract
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

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <span class="actions__select" @click="selectSupplier(row)"> 
                            Select
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
import { mapGetters } from 'vuex'

export default {
    name: 'BuyerContractsSupplierCategorySuppliers',
    data() {
        return {
            columns: ['#', 'supplier', 'contact_person', 'phone_number', 'email', 'actions'],
            options: {
                sortable: ['supplier', 'email'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            suppliers: []
        }
    },
    computed: {
        ...mapGetters('Contracts',['selectedCategory',]),
    },
    mounted() {
        this.getSuppliers()
    },
    methods: {
        selectSupplier: function(supplier) {
            this.$store.dispatch('Contracts/setSelectedSupplier', {supplier})
            this.$router.push('/buyer/contracts/supplier/contract/create')
        },
        async getSuppliers() {
            try {
                const response = await contracts.suppliers(this.$route.params.categoryId)
                this.dataCount = response.data.count
                this.suppliers = response.data.results
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
