<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Contract Sections
            </span>
            <div class="page__head--links">
                <router-link :to="'/buyer/contracts/sections/create'">
                    <a class="page__head--link button button-link">
                        Create New Contract Section
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Contract sections to use in creating contracts
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="contractSections" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="contractSections.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <span class="view" slot="section" slot-scope="{row}">
                        <router-link :to="'/buyer/contracts/sections/' + row.id + '/view'">
                            <font-awesome-icon class="view__icon" icon="eye" />
                            <span> View Section</span>
                        </router-link>
                    </span>

                    <p slot="created">
                        April 29, 2022
                    </p>

                    <p slot="updated">
                        May 1, 2022
                    </p>
                    
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/buyer/contracts/sections/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete" @click="deleteContractSection(row)">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
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

export default {
    name: 'ContractSections',
    data() {
        return {
            columns: ['#', 'name', 'section', 'created_by', 'created', 'updated', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            data: [
                {
                    name: 'Introduction',
                    created_by: 'Emmanuel',
                    created: 'April 26, 2022',
                    updated: 'June 11, 2022'
                },
            ],
            contractSections: []
        }
    },
    mounted() {
        this.getContractSections()
    },
    methods: {
        async getContractSections() {
            try {
                const response = await contracts.contractSections()
                this.dataCount = response.data.count
                this.contractSections = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async deleteContractSection(section) {
            try {
                await contracts.deleteContractSection(section.id)                
            } catch (err) {
                window.toast.fire({
                    icon: 'success',
                    title: section.name + ' deleted successfully'
                })
                this.getContractSections()
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
