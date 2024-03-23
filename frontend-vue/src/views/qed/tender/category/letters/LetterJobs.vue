<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Letters > Tender
            </span>

            <div class="page__head--links">
<!--                    <router-link to="/qed/create/prequalification" class="button is-primary">-->
<!--                        New Prequalification-->
<!--                    </router-link>-->
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Company Tender Jobs
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="prequals">
                <span slot="Job Title" slot-scope="{row}">
                    <span> {{ row.title }}</span>
                </span>

                <span slot="Job Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <a to="#" class="button is-small is-primary" @click="details(row)">
                    <span><font-awesome-icon class="view__icon" icon="eye"/> View</span>
                  </a>
                </span>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getPrequals()">
                </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import tender from "@/services/qed/tender";

export default {
  name: "LetterJobs",
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      columns: ['Job Title', 'Job Code', 'Actions'],
      options: {
        sortable: ['Job Title', 'Job Code'],
        perPageValues: [20],
        filterable: false,
      },
      prequals: []
    }
  },
  methods: {
    details(row){
      console.log('test')
      this.$router.push(`/qed/tender/letters/${row.id}`)
    },
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getPrequals(){
      try{
        let response = await tender.tenders(this.page)
        this.prequals = response.data['results']
        this.dataCount = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getPrequals()
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
//.VueTables__table tbody td {
//    padding: 5px 24px;
//}
.dropdown-content {
  position: fixed !important;
}
.page__content {
    position: relative;
    z-index: 0;
}
.dropdown-item {
    padding: 0.1rem 1rem;
    font-size: 12px;
}
.dropdown-item svg:not(:root).svg-inline--fa {
    overflow: visible;
    color: green;
}
</style>