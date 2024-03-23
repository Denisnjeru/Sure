<template>
  <div class="risk">
    <div class="page__head">
            <span class="page__head--title">
                Submit Financial Responses
            </span>
    </div>

    <div class="page__content columns">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__title">
            {{ category.name }}
            <!-- Card Title Header -->
          </p>
          <div class="table-search__search">
            <font-awesome-icon class="table-search__search--icon" icon="search"/>
            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
          </div>
        </div>
        <v-client-table :data="items" :columns="columns" :options="options">
                    <span slot="#" slot-scope="{row}">
                        <span> {{ row.number }}</span>
                    </span>

          <span slot="Item Description" slot-scope="{row}">
                        <span> {{ row.description }}</span>
                    </span>

          <span slot="Specification" slot-scope="{row}">
                        <span> {{ row.second_description }}</span>
                    </span>

          <span slot="Qty" slot-scope="{row}" class="is-justify-content-center">
            <span class="is-center"> {{ row.quantity }}</span>
          </span>

          <span slot="Unit Price Exc.VAT" slot-scope="{row}">
            <span>
              <input class="input is-small" type="number" :value="row.response.unit_price" placeholder="Unit Price" :id="'input_'+row.id"
                     style="text-align: right; max-width: 70%!important; width: 70%!important;"
                     @input="calculate_total(row)" @focusout="submit_price(row)" />
            </span>
          </span>

          <span slot="Total Inc.VAT" slot-scope="{row}">
            <span>{{ category.currency.initials }}</span>
            <span class="row-link__prices is-pulled-right" :id="'total_'+row.id" v-if="row.response.value">{{ parseFloat(row.response.total).toLocaleString() }}</span>
            <span class="row-link__prices is-pulled-right" :id="'total_'+row.id" v-else></span>
          </span>
        </v-client-table>
<!--        <br>-->
<!--        <div class="columns">-->
<!--          <div class="column is-12">-->
<!--            <button class="button is-primary is-small is-pulled-right">Submit</button>-->
<!--          </div>-->
<!--        </div>-->

        <div class="page__pagination">
          <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
          </pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/supplier/tender";

export default {
  name: "Bid",
  data() {
    return {
      columns: ['#', 'Item Description', 'Specification', 'Qty', 'Unit Price Exc.VAT', 'Total Inc.VAT'],
      options: {
        headings: {},
        sortable: ['#', 'Item Description'],
        sortIcon: {
          is: "glyphicon-sort",
          base: "glyphicon",
          up: "glyphicon-chevron-up",
          down: "glyphicon-chevron-down"
        },
      },
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      category: {},
      rfq: {},
      items: [],
      item_unit_price: 0,
      item_total_price: 0
    }
  },
  methods: {
    async fetchData() {
      console.log(this.page)
    },
    async search() {
      console.log('search')
    },
    async getItems() {
      try {
        let response = await tender.items(this.$route.params.category_id, this.page)
        this.items = response.data['data']
        this.dataCount = response.data['recordsTotal']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategory() {
      try {
        let response = await tender.category_instructions(this.$route.params.category_id)
        this.category = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    calculate_total(row){
      let element = document.getElementById('input_'+row.id)
      let value = element.value
      let total = row.quantity * parseFloat(value)
      document.getElementById('total_'+row.id).innerText = ''+total.toLocaleString()
    },
    async submit_price(row) {
      let form = {
        "item": row.id,
        "item_number": row.number,
        "unit_price": parseFloat(document.getElementById('input_'+row.id).value),
        "total": parseFloat(document.getElementById('total_'+row.id).innerText.replace(/,/g, ''))
      }
      console.log(form)
      try{
        let response = await tender.submit_item_response(this.category.id, form)
        // console.log(response.statusCode)
        if(response.status === 201){
          window.toast.fire({icon: 'success', title: "Response submitted"})
        }else if(response.status === 200){
            window.toast.fire({icon: 'error', title: response.data['response_message']})
            this.$router.push('/supplier/tender/ordered/categories')
        } else{
          window.toast.fire({icon: 'error', title: "An error occurred!! Please try again"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    // fetchItemPrice(row){
    //     let unit_price = document.getElementById('item_'+row.id).value
    //     this.item_unit_price = unit_price
    // },
    // submitItemPrice(row){
    //     let unit_price = document.getElementById('item_'+row.id).value
    //     let quantity = row.quantity
    //
    //
    //     if(unit_price !== 0 || unit_price !== ''){
    //         this.item_total_price = (unit_price * quantity) *1.16
    //     }else{ this.item_total_price = 0}
    //
    //     try {
    //         //
    //         window.toast.fire({icon: 'success', title: 'Response submitted'})
    //     } catch (err) {
    //         window.toast.fire({icon: 'error', title: err})
    //     }
    // },
  },
  mounted() {
    this.getCategory()
    this.getItems()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.page .column-page[data-v-6a003f38] {
    padding: 12px 24px;
}
.page .table-search[data-v-6a003f38] {
    padding: 6px 0px;
}
.VueTables__table tbody td {
    padding: 2px 24px !important;
}
</style>