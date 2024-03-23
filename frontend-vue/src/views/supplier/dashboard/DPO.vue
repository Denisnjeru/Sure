<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title page__head--title-image">
                <img class="img" src="@/assets/cards.png" alt="">
                &nbsp;&nbsp;
                <span>Payment using cards and other methods</span>
            </span>
        </div>
        
        <div class="page__content columns">
            <div class="column is-12 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Proceed to make payment</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">
                </div>
            </div>
            
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div><div class="column is-3">
            </div>
        </div>
            
    </div>
</template>
<script>
import dashboard from '@/services/supplier/dashboard'
export default {
    name: 'SupplierPaymentDPO',
    data() {
        return {
           phone_number: "",
           categories: [],
           cartTotal: 0,
           cartCurrency: "",
           cartCode: "",
           dpoDetails: {}
        }
    },
    computed: {
    },
    created() {
        this.getDPOPayment()
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
        async getDPOPayment() {
            try {
                let payload = {
                   
                }
                const response = await dashboard.dpoPayment(payload)
                this.dpoDetails = response.data

                if (this.dpoDetails.url) {
                    window.toast.fire({
                        icon: 'success',
                        title: 'Payment initiated successfully'
                    })
                    location.href = this.dpoDetails.url
                } else {
                    window.toast.fire({
                        icon: 'error',
                        title: 'Payment could not be processed'
                    })
                    this.$router.push('/supplier/dashboard/cart');
                }
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

.detail__title {
    font-size: $font-size-text;
}

.column-details__head--desc {
    font-size: $font-size-text !important;
}
</style>
