<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title page__head--title-image">
                <img class="img" src="@/assets/mpesa-logo.png" alt="">
                &nbsp;&nbsp;
                <span>Payment Using Mpesa</span>
            </span>
        </div>
        
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Option 1</p>
                    <p class="column-details__head--desc">Get M-PESA payment prompt on your phone.</p>
                    <br>
                </div>
                <div class="column-details__content">
                <form class="form" v-on:submit.prevent="getStkPrompt()">
                   <div class="field">
                        <label class="label">Enter Phone Number to make Mpesa Payment From</label>
                        <div class="control">
                            <input class="input" required v-model="phone_number" type="text" placeholder="Phone number Must be in this formart 2547200000000">
                        </div>
                        <p class="help">Ensure that the phone start with 254 e.g. 25472000000</p>
                    </div>         
                    <div class="field">
                        <input type="submit" class="button blue-button button-submit" value="Make Mpesa Payment">
                    </div>
                    <p class="caution">If you don't get a popup on your phone, please use option 2.</p>
                </form> 
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Option 2</p>
                    <p class="column-details__head--desc">Send M-PESA <strong>{{cartTotal | toCurrency(cartCurrency)}}</strong> to Pay Bill Business number <strong>379127</strong> and Account Number <strong>{{cartCode}}</strong>.</p>
                </div>
                <div class="column-details__content">
                   <p class="detail">
                        <span class="detail__title">1. Go to Mpesa on your phone</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">2. Select Pay Bill option</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">3. Enter Business no. <span class="highlight">379127</span></span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">4. Enter Account no. <span class="highlight">{{cartCode}}</span></span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">5. Enter the Amount <span class="highlight">{{cartTotal | toCurrency(cartCurrency)}}</span></span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">6. Enter your M-PESA PIN and Send</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">7. You will receive a confirmation SMS from M-PESA with a Confirmation Code</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">8. After you receive the confirmation SMS, please select the choice you paid on the navigation bar on the left hand side of the screen.</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">9. You will be directed to the job you have paid for to start the bidding process</span>
                    </p>
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div><div class="column is-3">
                <router-link to="/">
                    <button class="button button-submit">Proceed</button>
                </router-link>
            </div>
        </div>
            
    </div>
</template>

<script>
import dashboard from '@/services/supplier/dashboard'
export default {
    name: 'MpesaPayment',
    data() {
        return {
           phone_number: "",
           categories: [],
           cartTotal: 0,
           cartCurrency: "",
           cartCode: ""
        }
    },
    computed: {
    },
    created() {
       this.getCategories()
    },
    watch: {
        
    },
    methods: {
        
        async getCategories() {
            try {
                const response = await dashboard.cartCategories()
                this.categories = response.data
                this.cartTotal = this.categories.reduce((n, {bid_charge}) => n + bid_charge, 0)
                if (this.categories.length > 0) {
                    this.cartCurrency = this.categories[0].currency
                    this.cartCode = this.categories[0].code
                }
            } catch (err) {
                console.log(err)
            }
        },
        async getStkPrompt() {
            try {
                let payload = {
                    "phone_number": this.phone_number,
                }

                await dashboard.stkMpesaPrompt(payload)
                window.toast.fire({
                    icon: 'success',
                    title: 'Mpesa prompt initiated successfully'
                })
                
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: err.response.data.error
                })
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
}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

.popup {
    position: absolute; 
    top: 0vh;
    width: 100%;
    height: 100%; 
    z-index: 90;
    background-color: rgba(0, 0, 0, 0.2); 
    @include grid_row;
    align-items: flex-start;
    transition: opacity .3s;
    
    &__details {
        // position: sticky;
        // top: 20vh;
        min-height: 70vh;
        background-color: $color-white-main;
        $width: 97%;
        width: $width;
        margin: 5vh calc((100% - #{$width})/2);
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: $line-height $line-height/3;

        .page__content {
            padding-top: $line-height*2;
        }

        .column-page {
            box-shadow: none;
            padding: 0 $line-height;
            border-radius: 0;
            
            &:first-child {
                border-right: 1px solid $color-gray-medium;
            }
        }
    }
}

.selected-sections {
    text-align: left;
    align-items: flex-start !important;
    justify-content: flex-start !important;

    &__section {
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/4;
        padding: $line-height/3;
        margin: $line-height/3 0;
        width: 100%;
    }

    .delete-icon {
        color: $color-red-main;
        padding: 0 $line-height;

        &__icon {
            color: $color-red-main;
            cursor: pointer;
        }
    }
}

.caution {
    margin-top: $line-height;
    color: $color-red-main;
    font-size: $font-size-text;
}

.highlight {
    color: $color-blue-main;
}

.detail {
    padding: $line-height/2 0 !important;
}

.detail__title {
    font-size: $font-size-text;
}

.column-details__head--desc {
    font-size: $font-size-text !important;
}
</style>
