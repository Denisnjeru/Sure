<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Contracts
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__title">
                        My contracts with companies
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="data" :options="options">
                    <p class="row-no" v-if="data.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
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
export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'company', 'category', 'status', 'actions'],
            options: {
                sortable: ['company', 'category'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            data: [
                
            ],
        }
    },
    methods: {
        async fetchData() {
            console.log(this.page);
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
