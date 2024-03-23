<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
               Cart
            </span>
            <div class="page__head--links">
                <span class="page__head--link text-link">
                    Helpful Pointers
                </span>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Selected categories
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="categories" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="categories.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p class="standard-column link" slot="category" slot-scope="{row}">
                        {{row.name}}
                    </p>

                    <p slot="bid_fees" slot-scope="{row}">
                        {{ row.bid_charge | toCurrency(row.currency) }}
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
                        <a class="actions__cart-icon actions__icon  actions__delete" @click="removeCategoryFromCart(row.target, row.id)">
                            <font-awesome-icon icon="trash-alt" />
                        </a>
                    </p>     
                </v-client-table>
                <div class="cart__summary">
                    <p class="cart__summary-title">Total Amount</p>
                    <p class="cart__summary-title" v-if="cartCurrency !== ''">{{cartTotal | toCurrency(cartCurrency)}}</p>
                </div> 
            </div>  
                     
        </div>
        
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
                <div class="dropdown is-hoverable is-up payment-button">
                    <div class="dropdown-trigger payment-button" v-if="cartTotal > 0">
                        <a class="button button-submit payment-button" aria-haspopup="true" aria-controls="dropdown-menu4">
                            <span>Payment Using</span> 
                            &nbsp;&nbsp;&nbsp;&nbsp;                           
                            <span class="icon is-small">
                                <font-awesome-icon icon="chevron-down" />
                            </span>
                        </a>
                    </div>
                    <div class="dropdown-trigger payment-button" v-if="cartTotal === 0">
                        <a @click="makeZeroCharge()" class="button button-submit payment-button" aria-haspopup="true" aria-controls="dropdown-menu4">
                            <span>Proceed</span> 
                            &nbsp;&nbsp;&nbsp;&nbsp;                           
                            <span class="icon is-small">
                            </span>
                        </a>
                    </div>
                    <div class="dropdown-menu payment-button" id="dropdown-menu4" role="menu" v-if="cartTotal > 0">
                        <div class="dropdown-content payment-button">
                            <div class="dropdown-item payment-options">
                                <router-link to="/supplier/payment/mpesa" class="payment-options__option">
                                    <span class="payment-options__option--img">
                                        <img class="img" src="@/assets/mpesa.png" alt="">
                                    </span>
                                    <span class="payment-options__option--name">
                                        Mpesa Payment
                                    </span>
                                </router-link> 
                                <router-link to="/supplier/payment/cards/c" class="payment-options__option">
                                    <span class="payment-options__option--img">
                                        <img class="img" src="@/assets/cards.png" alt="">
                                    </span>
                                    <span class="payment-options__option--name">
                                        Cellulant
                                    </span>
                                </router-link> 
                                <router-link to="/supplier/payment/cards/d" class="payment-options__option">
                                    <span class="payment-options__option--img">
                                        <img class="img" src="@/assets/cards.png" alt="">
                                    </span>
                                    <span class="payment-options__option--name">
                                        DPO
                                    </span>
                                </router-link> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import dashboard from '@/services/supplier/dashboard'
export default {
    name: 'SupplierCompanyJobs',
    data() {
        return {
            columns: ['#', 'category', 'closing_date', 'closes_in', 'bid_fees', 'action'],
            options: {
                sortable: ['category', 'closing_date'],                
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            categories: [],
            cartTotal: 0,
            cartCurrency: ''
        }
    },
    created() {
        this.getCategories()
    },
    methods: {
        async search() {
            console.log('search');
        },
        async getCategories() {
            try {
                const response = await dashboard.cartCategories()
                this.categories = response.data
                this.cartTotal = this.categories.reduce((n, {bid_charge}) => n + bid_charge, 0)
                if (this.categories.length > 0) {
                    this.cartCurrency = this.categories[0].currency
                }
            } catch (err) {
                console.log(err)
            }
        },
        async removeCategoryFromCart(target,  categoryId) {
            try {
                let payload = {
                    "target": 10,
                    "target_name": target,
                    "category_id": categoryId,
                    "supplier": 4
                }

                await dashboard.removeCategoryFromCart(payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Category removed to cart'
                })
                
                this.getCategories()
                this.$forceUpdate();
                
            } catch (err) {
                console.log(err)
            }
        },
        async makeZeroCharge() {
            try {
                let payload = {}

                await dashboard.makeZeroCharge(payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Categories processed successfully'
                })
                this.$router.push('/');
                
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

.payment-button {
    width: 100%;
}

// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

.additions {
    margin-top: -$line-height*3;
}

.cart__summary {
    width: 100%;
    @include grid_row;
    padding: $line-height 5%;
    font-weight: 700;
    color: $color-black-main;
    margin-top: $line-height/2;
    border-top: 0.5px solid rgba(0, 0, 0, 0.2);
    border-bottom: 0.5px solid rgba(0, 0, 0, 0.2);
}

.payment-options {
    &__option {
        &:not(:last-child) {
            border-bottom: 0.5px solid rgba(0, 0, 0, 0.9);
        }

        color: $color-black-main;
        font-weight: 700;
        padding: $line-height/2 $line-height/3;
        cursor: pointer;
        @include grid_row;
        justify-content: flex-start;

        &:hover {
            color: $color-black-medium;
        }

        .img {
            height: $line-height/2;
            margin-right: $line-height/2;
        }
    }
}

</style>
