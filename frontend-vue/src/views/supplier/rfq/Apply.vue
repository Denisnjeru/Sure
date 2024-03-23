<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title" v-if="category.supplier_participation_status">
                Submit RFQ Responses
            </span>
            <span class="page__head--title" v-else>
                Update RFQ Responses
            </span>
        </div>

        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      RFQ Items
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search"/>
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <div class="table-search">
                    <p class="table-search__instruction">
                      
                    </p>
                    <div class="table-search__search rfq-table">
                        <label class="form-label" style="margin-right: 10px;"> Cumulative Total Inc VAT ({{category.currency}})</label>
                        <input class="table-search__search--input" style="text-align: right; margin-right: 5px;" type="currency" placeholder="Total Inc VAT" v-model="total_price" readonly>
                    </div>
                </div>
                <v-client-table :data="items" :columns="columns" :options="options">
                    <span slot="#" slot-scope="{row}">
                        <span> {{ row.item_number }}</span>
                    </span>

                    <span slot="Item" slot-scope="{row}">
                        <span> {{ row.item_description }}</span>
                    </span>
                    <span slot="UoM" slot-scope="{row}">
                        <span> {{ row.unit_of_measure }}</span>
                    </span>
                    <span slot="Specification 1" slot-scope="{row}">
                        <span style="text-align: center;"> {{ row.specification_1 }}</span>
                    </span>

                    <span slot="Qty" slot-scope="{row}">
                        <span style="text-align:center;"> {{ row.quantity }}</span>
                    </span>

                    <span slot="Specification 2" slot-scope="{row}">
                        <span style="text-align: center;"> {{ row.specification_2 }}</span>
                    </span>

                    <span slot="Unit Price Inc VAT" slot-scope="{row}">
                        <template v-if="row.item_responses.length > 0">
                            <span>
                            <input class="input is-small" type="number" placeholder="Unit Price" :id="'input_'+row.id"
                                    style="text-align: right; max-width: 70%!important; width: 70%!important;"
                                    @focusout="submitItemPrice(row)" @input="calculate_total(row)" v-model="row.item_responses[0].unit_price" />
                            </span>
                        </template>
                        <template v-else>
                            <span>
                            <input class="input is-small" type="number" placeholder="Unit Price" :id="'input_'+row.id"
                                    style="text-align: right; max-width: 70%!important; width: 70%!important;"
                                    @focusout="submitItemPrice(row)" @input="calculate_total(row)" />
                            </span>
                        </template>
                        
                    </span>
                    <span slot="Total Inc VAT" slot-scope="{row}">
                        <!-- <span>{{category.currency}} </span> -->
                        <template v-if="row.item_responses.length > 0">
                            <span>
                            <input class="input is-small" type="number" id="'total_'+row.id" style="text-align: right; max-width: 70%!important; width: 70%!important;" v-model="row.item_responses[0].total_price" readonly>
                            </span>
                        </template>
                        <template v-else>
                            <span>
                            <input class="input is-small" type="number" id="'total_'+row.id" style="text-align: right; max-width: 70%!important; width: 70%!important;" readonly>
                            </span>
                        </template>
                    </span>

                </v-client-table>
                <div class="rfq-submit">
                     <span v-if="category.supplier_participation_status">
                        <button type="button" class="button submit-button is-primary is-pulled-right" @click="submitRfq()">Update</button>
                    </span>
                    <span v-else>
                         <button type="button" class="button submit-button is-primary is-pulled-right" @click="submitRfq()">Submit</button>
                    </span>  
                </div>
                
                <div class="page__pagination">
                    <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                    </pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import rfq from "@/services/company/rfq";
import supplierRfq from "@/services/supplier/rfq";

export default {
    name: 'supplierApplyRFQ',
    data () {
        return{
            columns: ['#', 'Item', 'UoM', 'Specification 1', 'Specification 2', 'Qty', 'Unit Price Inc VAT','Total Inc VAT'],
            options: {
                headings : {},
                perPage: 10,
                perPageValues: [10],
                sortable:['#', 'Item'],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
                columnsClasses: {
                    '#':'custom-columns__small',
                    'Item': 'custom-columns__large',
                    'UoM': 'custom-columns__medium',
                    'Specification 1': 'custom-columns__medium',
                    'Specification 2': 'custom-columns__medium',
                    'Qty': 'custom-columns__medium',
                    'Unit Price Exc.VAT': 'custom-columns__medium',
                    'Total Inc.VAT': 'custom-columns__medium'
                }
            },
            page: 1,
            dataCount: 0,
            dataPerPage: 10,
            category: {},
            rfq:{},
            items:[],
            item_unit_price:0,
            total_price: 0
        }
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
    },
    methods: {
        async fetchData(){
            console.log(this.page)
        },
        async search(){
            console.log('search')
        },
        async getRfqItems(){
            try{
                let response = await supplierRfq.rfqDetails(this.$route.params.category_id)
                this.category = response.data
                this.items = this.category.items
                this.rfq=this.category.rfq
                this.dataCount= this.items.length
                console.log(this.category)
        
            }catch (err){
                window.toast.fire({icon: 'error', title: err})
            }
        },
      
        fetchItemPrice(row){
            let unit_price = document.getElementById('item_'+row.id).value
            this.item_unit_price = unit_price
        },   
        calculate_total(row){
            let element = document.getElementById('input_'+row.id)
            let value = element.value
            let total = row.quantity * parseFloat(value)
            document.getElementById('total_'+row.id).innerText = ''+total.toLocaleString()
        }, 
        async submitItemPrice(row){
            //submit individual supplier responses
            let unit_price = document.getElementById('input_'+row.id).value
            let quantity = row.quantity
            let item_total_price = 0
            
            if(unit_price !== 0 || unit_price !== ''){
                item_total_price = ((unit_price * quantity) * (1 + this.category.vat_rate/100)).toFixed(2);
            }else{ item_total_price = 0}

           
            let content = {
                'item_number': row.item_number,
                'unit_price': unit_price,
                'total_price': item_total_price,
            }
            
            try {
                let response = await rfq.rfqSubmitItemResponse(content,row.id, this.authUser.user_id)
                if(response.status === 201){
                    this.total_price += parseFloat(item_total_price)
                    window.toast.fire({icon: 'success', title: 'Response submitted'})
                }else{
                    window.toast.fire({icon: 'info', title: 'Response not submitted'})
                }
                
            } catch (err) {
                window.toast.fire({icon: 'error', title: err})
            }
        },
        async submitRfq(){
            // submit supplier total RFQ
            let content = {
                'score': this.total_price,
                'supplier': this.authUser.user_id,
                'category': this.$route.params.category_id
            }
            try{
                let response = await rfq.rfqSubmitTotal(content,this.$route.params.category_id,this.authUser.user_id)
                console.log(response)
                if(response.status ===201){
                    this.total_price = 0
                    window.toast.fire({icon: 'success', title: 'RFQ Responses submitted'})
                }
            } catch (err){
                window.toast.fire({icon:'error', title:err})
            }

        },
    },
    mounted() {
        this.getRfqItems()
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page{
    &__head {
        @include grid_row;
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
        
        &--title {
            font-size: $font-size-title;
            color: rgba(18, 31, 62, 0.8);
            font-weight: 600;
        }

    }
    &__content{
        margin: 0 !important;
        @include grid_column;
        width: 100%;
        // padding: $line-height $line-height;
    }

    .row-link{
        color: rgba(18, 31, 62, 0.8);
        flex-flow: row nowrap;
        justify-content: space-evenly;
        
        &__text{
            text-decoration-line: underline;
        }
        &__arrow{
            display: inline;
            border-radius: 5px;
        }
        &__prices{
            text-align: right;
            font-weight: 900;
        }
        &__input{
            border-radius: 4px;
            border-color: #dbdbdb;
            background-color: white;
            color: #363636;
            text-align: right;
        }
        &__quantity{
            text-align: center;
        }
    }
    .custom-columns{
        &__small {
            width: 5%;
        }
        &__medium{
            width: 10%;
        }
        &__large{
            width: 20%;
        }
        &__x-large{
            width: 30%;
        }
    }
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
.is-primary{
  background-color: #073A82 !important;
}
.form-label{
    font-weight: 900;
}
.submit-button{
    margin-right: 24px;
    border-radius: 4px;
    background-color:$color-green-main;
    color: #fff;

}
.rfq-table{
    padding: 5px 0px !important;
}
.rfq-submit{
    width: 100%;
    margin: 12px 0px;
    padding-right: 24px; 
}
</style>