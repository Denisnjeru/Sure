<template>
<div>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Prequalification jobs you have paid for
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
                      Prequalifications
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="prequals">

                <span slot="Buyer" slot-scope="{row}">
                    <span> {{ row.prequalification.company.company_name }}</span>
                </span>

                <span slot="Job" slot-scope="{row}">
                    <span> {{ row.prequalification.title }}</span>
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
                    <router-link v-if="row.participated === true" :to="'/supplier/prequal/category/instructions/'+row.id" class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt" /> Update</p>
                    </router-link>

                    <router-link v-else :to="'/supplier/prequal/category/instructions/'+row.id" class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt" /> Bid</p>
                    </router-link>
                  </template>

                  <template v-else>
                    <a :href="backend_url +'/' + row['report']" download="download" class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="download" /> Report</p>
                    </a>
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
import prequal from "@/services/supplier/prequal";

export default {
  name: "OrderedCategories",
  data(){
    return{
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      backend_url: process.env.VUE_APP_DOWNLOAD_URL,
      columns: ['Buyer', 'Job', 'Category','Category Code',  'Closing Time', 'Actions'],
      options: {
        sortable: ['Buyer', 'Job', 'Category'],
        perPageValues: [10],
        filterable: false,
      },
      prequals: []
    }
  },
  methods:{
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getPrequals(){
      try{
        let response = await prequal.ordered_categories(this.page, this.dataPerPage)
        this.prequals = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getPrequals()
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
</style>