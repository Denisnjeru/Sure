<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Job > Category > Letter Options
            </span>

            <div class="page__head--links">

            </div>
        </div>

        <div class="page__head">
            <span class="page__head--title">
               Qualified Bidders
            </span>

            <div class="page__head--links">

            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">

                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="qualified_bidders">
                <span slot="Company Name" slot-scope="{row}">
                    <span> {{ row.supplier.company_name }}</span>
                </span>

<!--                <span slot="Phone Number" slot-scope="{row}">-->
<!--                    <span> {{ row.supplier.phone_number }}</span>-->
<!--                </span>-->

<!--                <span slot="Contact Name" slot-scope="{row}">-->
<!--                    <span> {{ row.supplier.contact_name }}</span>-->
<!--                </span>-->

                <span slot="Score" slot-scope="{row}">
                    <span> {{ row.score }}</span>
                </span>

                <span slot="Rank" slot-scope="{row}">
                    <span> {{ row.rank }}</span>
                </span>

                <template slot="Actions" slot-scope="{row}">
                  <div class="dropdown" :id="'row_'+row.id">
                    <div class="dropdown-trigger">
                      <button class="button is-primary is-small" @click="show_options(row)" aria-haspopup="true" aria-controls="dropdown-menu3">
                        <span>Letter Options</span>
                        <span class="icon is-small">
                          <i class="angle-down" aria-hidden="true"></i>
                        </span>
                      </button>
                    </div>
                    <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                      <template v-if="row.has_award_letter === true">
                        <div class="dropdown-content">
                          <router-link :to="`/company/tender/preview/award/letter/${$route.params.job_id}/${$route.params.category_id}/${row.supplier.id}`" class="dropdown-item">
                            Award Letter Preview
                          </router-link>
                          <hr class="dropdown-divider">
                          <a href="#" class="dropdown-item">
                            Delete Award Letter
                          </a>
                        </div>
                      </template>
                      <template v-else-if="row.has_regret_letter === true">
                        <div class="dropdown-content">
                          <router-link :to="`/company/tender/preview/regret/letter/${$route.params.job_id}/${$route.params.category_id}/${row.supplier.id}`" class="dropdown-item">
                            Regret Letter Preview
                          </router-link>
                          <hr class="dropdown-divider">
                          <a href="#" class="dropdown-item">
                            Delete Regret Letter
                          </a>
                        </div>
                      </template>
                      <template v-else-if="row.has_award_letter === false && row.has_regret_letter === false">
                        <div class="dropdown-content">
                          <a href="#" class="dropdown-item" @click="create_award_letter(row)">
                            Create Award Letter
                          </a>
                          <hr class="dropdown-divider">
                          <a href="#" class="dropdown-item" @click="create_regret_letter(row)">
                            Create Regret Letter
                          </a>
                        </div>
                      </template>
                    </div>
                  </div>
                </template>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>

        <div class="page__head">
            <span class="page__head--title">
               Un-Qualified Bidders
            </span>

            <div class="page__head--links">
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="unqualified_bidders">
                <span slot="Company Name" slot-scope="{row}">
                    <span> {{ row.supplier.company_name }}</span>
                </span>

                <span slot="Phone Number" slot-scope="{row}">
                    <span> {{ row.supplier.phone_number }}</span>
                </span>

                <span slot="Contact Name" slot-scope="{row}">
                    <span> {{ row.supplier.contact_name }}</span>
                </span>

                <span slot="Score" slot-scope="{row}">
                    <span> {{ row.score }}</span>
                </span>

                <span slot="Rank" slot-scope="{row}">
                    <span> {{ row.rank }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <router-link :to="'/company/tender/dd/supplier/questions/'+$route.params.category_id+'/'+row.id" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Letter Options</p>
                  </router-link>
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
import tender from "@/services/company/tender";

export default {
  name: "ParticipantList",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Company Name', 'Score', 'Rank', 'Actions'],
      options: {
        sortable: ['Company Name',],
        perPageValues: [20],
        filterable: false,
      },
      qualified_bidders: [],
      unqualified_bidders: [],
    }
  },
  methods: {
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
    async get_qualified_bidders(){
      try{
        let response = await tender.qualified_bidders(this.$route.params.job_id, this.$route.params.category_id)
        this.qualified_bidders = response.data['data']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_unqualified_bidders(){
      try{
        let response = await tender.unqualified_bidders(this.$route.params.job_id, this.$route.params.category_id)
        this.unqualified_bidders = response.data['data']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_award_letter(row){
      let content = {
        "supplier": row.supplier.id,
        "category": this.$route.params.category_id
      }
      try{
        await tender.create_award_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        this.$router.push(
            `/company/tender/preview/award/letter/${this.$route.params.job_id}/${this.$route.params.category_id}/${row.supplier.id}`
        )
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_regret_letter(row){
      let content = {
        "supplier": row.supplier.id,
        "category": this.$route.params.category_id
      }
      try{
        await tender.create_regret_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        this.$router.push(
            `/company/tender/preview/regret/letter/${this.$route.params.job_id}/${this.$route.params.category_id}/${row.supplier.id}`
        )
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },

    async delete_award_letter(){

    },
    async delete_regret_letter(){

    },
  },
  mounted() {
    this.get_qualified_bidders()
    this.get_unqualified_bidders()
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
.is-primary{
  background-color: #073A82 !important;
}
</style>