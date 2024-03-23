<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Live Jobs > Supply of Laptops > Supply of HP Laptops
            </span>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Participants
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="participants" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="participants.length !== 0" slot="#" slot-scope="props">
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
// import prequal from '@/services/company/prequal'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'supplier_name', 'status'],
            options: {
                sortable: ['supplier_name', 'status'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            participants: [
                {
                    "supplier_name": 'Digitech International',
                    "status": "Responsive"
                }
            ]
        }
    },
    computed: {

    },
    mounted() {
        this.getParticipants()
    },
    methods: {
        selectCategory: function() {
        },
        async getParticipants() {
            
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
