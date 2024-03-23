<template>
<div>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Tender jobs you have paid for
            </span>

            <div class="page__head--links">
<!--                    <router-link to="/company/create/prequalification" class="button is-primary">-->
<!--                        New Prequalification-->
<!--                    </router-link>-->
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Tenders
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="tenders">

                <span slot="Buyer" slot-scope="{row}">
                    <span> {{ row.tender.company.company_name }}</span>
                </span>

                <span slot="Job" slot-scope="{row}">
                    <span> {{ row.tender.title }}</span>
                </span>

                <span slot="Category" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

                <span slot="Category Number" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

                <span slot="Closing Time" slot-scope="{row}">
                    <span> {{ row.closing_date }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <template v-if="row.is_open === true">
                    <div class="dropdown" :id="'row_'+row.id">
                      <div class="dropdown-trigger">
                        <button class="button is-primary is-small" @click="show_options(row)" aria-haspopup="true" aria-controls="dropdown-menu3">
                          <span>Choose Option <font-awesome-icon class="view__icon" icon="angle-down"/></span>
                          <span class="icon is-small">
                            <i class="angle-down" aria-hidden="true"></i>
                          </span>
                        </button>
                      </div>
                      <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                        <div class="dropdown-content">
                          <router-link :to="'/supplier/tender/category/instructions/'+row.id" class="dropdown-item">
                            Technical Envelope
                          </router-link>
                          <hr class="dropdown-divider">
                          <template>
                            <router-link v-if="row.rfq_type == 'basic'" :to="'/supplier/tender/category/financial/bid/'+row.id" class="dropdown-item" >
                              Price Envelope
                            </router-link>

                            <router-link v-else-if="row.rfq_type == 'advanced'" :to="'/supplier/tender/category/advanced/financial/bid/'+row.id" class="dropdown-item">
                              Price Envelope
                            </router-link>
                          </template>
                        </div>
                      </div>
                    </div>
                  </template>

                  <template v-else>
                    <router-link to="#" class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="download" /> Report</p>
                    </router-link>
                  </template>


                </span>
              </v-client-table>

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
import supplier_tender from "@/services/supplier/tender";

export default {
  name: "OrderedCategories",
  data(){
    return{
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      columns: ['Buyer', 'Job', 'Category','Category Number',  'Closing Time', 'Actions'],
      options: {
        sortable: ['Buyer', 'Job', 'Category'],
        perPageValues: [10],
        filterable: false,
      },
      tenders: []
    }
  },
  methods:{
    show_options(row){
      let element = document.getElementById('row_'+row.id)
      if (element.classList.contains('is-active')){
        element.classList.remove('is-active')
      }else{
        element.classList.add('is-active')
      }
    },
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getTenders(){
      try{
        let response = await supplier_tender.ordered_categories(this.page, this.dataPerPage)
        this.tenders = response.data['results']
        this.dataCount = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getTenders()
  },
  created() {

  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}
.is-primary{
  background-color: #073A82 !important;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
.dropdown-content{
  position: fixed !important;
}
</style>