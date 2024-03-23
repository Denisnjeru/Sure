<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Dashboard > Savings
            </span>

            <div class="page__head--links">
                   
                      <!-- <button type="button" class="button is-primary" @click="openModal()">
                          New RFQ
                      </button> -->
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Company Job Savings
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="rfqs">
                <span slot="Job Title" slot-scope="{row}">
                    <span> {{ row.title }}</span>
                </span>

                <span slot="Job Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

                <span slot="Categories" slot-scope="">
                    <span> 10 </span>
                </span>

                <span slot="Savings" slot-scope="">
                    <span> 0 </span>
                </span>

                <span class="actions" slot="Actions" slot-scope="{row}" >
                  <button class="button is-primary is-small" @click="downloadJobSavingsReport(row)">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View Report</p>
                  </button>
                </span>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import rfq from "@/services/company/rfq";

export default {
  name: "CompanySavings",
  components:{
  },
  data(){
    return {
      page: 1,
      dataCount: null,
      dataPerPage: null,
      columns: ['Job Title', 'Job Code', 'Categories', 'Savings', 'Actions'],
      options: {
        sortable: ['Job Title', 'Job Code', 'Categories'],
        perPageValues: [20],
        filterable: false,
      },
      rfqs: []
    }
  },
  methods: {
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log(this.page);
    },
    async getRfqs(){
      try{
        let response = await rfq.rfqs(this.page)
        this.rfqs = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.dataPerPage)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async downloadJobSavingsReport(row){
      try{
        let response = await rfq.rfqDownloadJobSummaryReport(row.id)
        console.log(response)
        if(response.status === 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          try{
              window.open(reportUrl)
            }catch(err){
              window.toast.fire({icon: 'error', title: err})
            }
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getRfqs()
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