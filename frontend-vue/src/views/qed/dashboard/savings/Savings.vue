<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > <span class="title__active">Buyer Savings</span>
            </span>
            <div class="page__head--links">
               
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Buyer Savings
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="buyers" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="buyers.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <router-link :to="'/qed/savings/' + row.id + '/buyer'" class="standard-column link" slot="company" slot-scope="{row}">
                        Gathage Buyer
                    </router-link>

                    <p class="standard-column" slot="savings" slot-scope="{row}">
                        {{row.savings | toCurrency('KSH')}}
                    </p>
     
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getBuyers()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
    name: 'QedBuyers',
    data() {
        return {
            columns: ['#', 'company', 'initial', 'savings'],
            options: {
                sortable: ['company', 'initial'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            buyers: [
                {
                    "id": 1,
                    "company": 'QED Solutions Limited',
                    "initial": 'QSL',
                    "savings": 1200000
                }
            ]
        }
    },
    computed: {
        ...mapGetters('Auth', ['authUser']),
    },
    mounted() {
        this.getBuyers()
    },
    methods: {
        selectJob: function() {
        },
        async getBuyers() {
            try {
                console.log()
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        deleteBuyer() {
            this.$swal({
                text: 'This buyer will be permanently deleted',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    alert('done')             
                }
            });
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
