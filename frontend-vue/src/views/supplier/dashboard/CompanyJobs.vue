<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                {{company.company_name}}
            </span>
            <div class="page__head--links">
                <span class="page__head--link text-link">
                    Helpful Pointers
                </span>
                <router-link to="/supplier/dashboard/cart">
                    <a class="page__head--link button button-link">
                        Proceed to Cart
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       <a class="instruction" :class="{ 'button': showPrequals === true, 'blue-button': showPrequals === true, 'text-link' : showPrequals === false}" @click="updateShowPrequals()">Prequalifications</a>
                       <a class="instruction" :class="{ 'button': showTenders === true, 'blue-button': showTenders === true, 'text-link' : showTenders === false }" @click="updateShowTenders()">Tenders</a>
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                
                <div class="row" v-if="showPrequals === true">
                    <v-client-table v-if="showPrequals === true" :columns="columns" :data="prequals" :options="options" class="hasRowNo">
                        <p class="row-no" v-if="prequals.length !== 0" slot="#" slot-scope="props">
                            {{props.index}}
                        </p>

                        <p class="standard-column bold" slot="category" slot-scope="{row}">
                            {{row.name}}
                        </p>

                        <p slot="bid_fees" slot-scope="{row}">
                            {{ row.bid_charge | toCurrency(row.currency.initials) }}
                        </p>   

                        <p slot="closing_date" slot-scope="{row}">
                            {{ row.closing_date | formatDateTime }}
                        </p> 

                        <p slot="closes_in" slot-scope="{row}">
                            <countdown :end-time="row.closing_date">
                            <span
                                slot="process"
                                slot-scope="anyYouWantedScopName">{{ `${anyYouWantedScopName.timeObj.ceil.s}` | timeLeft }}</span>
                            <span slot="finish">Closed</span>
                            </countdown>
                        </p>                      

                        <p class="actions" slot="action" slot-scope="{row}">                            

                            <a  v-if="row.payed_for === null" class="actions__icon actions__cart-icon actions__edit" @click="addCategoryToCart('prequal', row.id)">
                                <font-awesome-icon icon="cart-plus" />
                            </a>
                            <a v-if="row.payed_for === 'Pending'" class="actions__cart-icon actions__icon  actions__delete" @click="removeCategoryFromCart('prequal', row.id)">
                                <font-awesome-icon icon="trash-alt" />
                            </a>
                            <router-link to="/supplier/prequal/ordered/categories/">
                                <a v-if="row.payed_for === 'Paid'" class="actions__cart-icon actions__icon">
                                    <font-awesome-icon icon="pen" />
                                </a>
                            </router-link>
                            
                        </p>     
                    </v-client-table>
                    <br>
                    <div class="page__pagination" v-if="prequals.length !== 0">
                        <pagination :records="prequals.length" v-model="prequalPage" :per-page="dataPerPage" @paginate="getJobs()">
                        </pagination>
                    </div>
                </div>
                <div class="row" v-if="showTenders === true">
                    <v-client-table v-if="showTenders === true" :columns="columns" :data="tenders" :options="options" class="hasRowNo">
                         <p class="row-no" v-if="tenders.length !== 0" slot="#" slot-scope="props">
                            {{props.index}}
                        </p>

                        <p class="standard-column bold" slot="category" slot-scope="{row}">
                            {{row.name}}
                        </p>

                        <p slot="bid_fees" slot-scope="{row}">
                            {{ row.bid_charge | toCurrency(row.currency.initials) }}
                        </p>   

                        <p slot="closing_date" slot-scope="{row}">
                            {{ row.closing_date | formatDateTime }}
                        </p> 

                        <p slot="closes_in" slot-scope="{row}">
                            <countdown :end-time="row.closing_date">
                            <span
                                slot="process"
                                slot-scope="anyYouWantedScopName">{{ `${anyYouWantedScopName.timeObj.ceil.s}` | timeLeft }}</span>
                            <span slot="finish">Closed</span>
                            </countdown>
                        </p>                      

                        <p class="actions" slot="action" slot-scope="{row}">                            

                            <a  v-if="row.payed_for === null" class="actions__icon actions__cart-icon actions__edit">
                                <font-awesome-icon icon="cart-plus" @click="addCategoryToCart('tender', row.id)" />
                            </a>
                            <a v-if="row.payed_for === 'Pending'" class="actions__cart-icon actions__icon  actions__delete"  @click="removeCategoryFromCart('tender', row.id)">
                                <font-awesome-icon icon="trash-alt" />
                            </a>
                            <router-link to="/supplier/tender/ordered/categories/">
                                <a v-if="row.payed_for === 'Paid'" class="actions__cart-icon actions__icon">
                                    <font-awesome-icon icon="pen" />
                                </a>
                            </router-link>
                        </p>    
                    </v-client-table>
                    <br>
                    <div class="page__pagination" v-if="tenders.length !== 0">
                        <pagination :records="tenders.length" v-model="tenderPage" :per-page="dataPerPage" @paginate="getJobs()">
                        </pagination>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import dashboard from '@/services/supplier/dashboard'

export default {
    name: 'SupplierCompanyJobs',
    data() {
        return {
            columns: ['#', 'category', 'closing_date', 'closes_in', 'bid_fees', 'action'],
            options: {
                sortable: ['category', 'closing_date'],
                perPageValues: [20], 
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            prequalPage: 1,
            tenderPage: 1,
            dataCount: 20,
            dataPerPage: 20,
            categories: [
               
            ],
            company: {},
            prequals: [],
            tenders: [],
            showPrequals: false,
            showTenders: false
        }
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus']),
    },
    created() {
        this.getPrequals()
        this.getTenders()        
    },
    methods: {
        updateShowTenders: function() {
            if (this.showTenders === false) {
                this.showPrequals = false
                this.showTenders = true
            }
        },
        updateShowPrequals: function() {
            if (this.showPrequals === false) {
                this.showTenders = false
                this.showPrequals = true
            }
        },
        async search() {
            console.log('search');
        },
        async getPrequals() {
            try {
                const response = await dashboard.openPrequals(this.$route.params.id)
                this.prequals = response.data
                if (this.prequals.length > 0) {
                    this.showPrequals = true
                    this.company = this.prequals[0].prequalification.company
                } else {
                    this.showTenders = true
                }
            } catch (err) {
                console.log(err)
            }
        },
        async getTenders() {
            try {
                const response = await dashboard.openTenders(this.$route.params.id)
                this.tenders = response.data
                if (this.tenders.length > 0) {
                    this.company = this.tenders[0].tender.company
                }
            } catch (err) {
                console.log(err)
            }
        },
        async addCategoryToCart(target_name,  categoryId) {
            try {
                let payload = {
                    "target": 10,
                    "target_name": target_name,
                    "category_id": categoryId,
                    "supplier": this.authUser.user_id
                }
                await dashboard.addCategoryToCart(payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Category added to cart'
                })
                
                if (target_name === 'prequal') {
                    this.getPrequals()
                } else {
                    this.getTenders()
                }
                this.$forceUpdate();
                
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: err.response.data.error
                })
            }
        },
        async removeCategoryFromCart(target_name,  categoryId) {
            try {
                let payload = {
                    "target": 10,
                    "target_name": target_name,
                    "category_id": categoryId,
                    "supplier": 4
                }

                await dashboard.removeCategoryFromCart(payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Category removed to cart'
                })
                
                if (target_name === 'prequal') {
                    this.getPrequals()
                } else {
                    this.getTenders()
                }
                this.$forceUpdate();
                
            } catch (err) {
                console.log(err)
            }
        },

    }
}
</script>

<style lang="scss" scoped>
@include page;
@include form;

.page__content {
    padding: $line-height $line-height;
    margin-top: $line-height;
    @include grid_column;
}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

.row {
    width: 100%;
}

// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

</style>
