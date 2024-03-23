<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Buyers
            </span>
            <div class="page__head--links">
                <router-link to="/qed/buyers/create">
                    <a class="page__head--link button button-link">
                        Add New Buyer
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Registered buyers
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

                    <router-link :to="'/qed/buyers/' + row.id + '/buyer'" class="standard-column link" slot="company" slot-scope="{row}">
                        Gathage Buyer
                    </router-link>

                    <p class="standard-column" slot="KRA Pin/Tax Registration" slot-scope="{row}">
                        {{row.kra_pin_number}}
                    </p>

                    <p class="standard-column" slot="initials" slot-scope="{row}">
                        {{row.buyer_initials}}
                    </p>

                    <p class="standard-column" slot="contact_person" slot-scope="{row}">
                        {{row.contact_name}}
                    </p>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/qed/buyers/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete" @click="deleteBuyer()">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>
     
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
import buyer from '@/services/qed/buyer'

export default {
    name: 'QedBuyers',
    data() {
        return {
            columns: ['#', 'company', 'initials', 'KRA Pin/Tax Registration', 'contact_person', 'phone_number', 'actions'],
            options: {
                sortable: ['company', 'initials'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            buyers: [
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
                const response = await buyer.buyers(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.buyers = response.data.results
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
