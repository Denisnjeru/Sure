<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Job > Category > Letter Options
            </span>

            <div class="page__head--links">
<!--                    <router-link :to="'/company/prequal/dd/add/questions/'+$route.params.category_id" class="button is-primary">-->
<!--                        New Due Diligence Question-->
<!--                    </router-link>-->
            </div>
        </div>

        <div class="page__head">
            <span class="page__head--title">
               Qualified Bidders
            </span>

            <div class="page__head--links">
<!--                    <router-link :to="'/company/prequal/dd/add/questions/'+$route.params.category_id" class="button is-primary">-->
<!--                        New Due Diligence Question-->
<!--                    </router-link>-->
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
                <span slot="Select" slot-scope="{row}">
                  <span>
                      <input type="checkbox" class="checkbox" :id="'checkbox_'+row.id"
                             @click="remove_add_supplier_ids(row)" :checked="row.id in supplier_ids ? 'checked': ''">
                    </span>
                </span>

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

        
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="qualifiedDataCount" v-model="qualified_page" :per-page="qualifiedDataPerPage" @paginate="fetchData()">
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
                <span slot="Select" slot-scope="{row}">
                    <span>
                      <input type="checkbox" class="checkbox" :id="'checkbox_'+row.id"
                             @click="remove_add_supplier_ids(row)" :checked="row.id in supplier_ids ? 'checked': ''">
                    </span>
                </span>

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

            
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="unqualifiedDataCount" v-model="unqualified_page" :per-page="unqualifiedDataPerPage" @paginate="fetchData()">
                </pagination>
            </div>

        </div>

        <div class="page__content columns">
          <div class="column is-12">
            <a href="#" class="button is-primary is-small is-pulled-right" style="margin-left: 2px"
              @click="create_multiple_custom_letters()">
              Custom Letter
            </a>
            <a href="#" class="button is-primary is-small is-pulled-right" style="margin-left: 2px"
              @click="create_multiple_dd_letters()">
              DD Letter
            </a>
            <a href="#" class="button is-primary is-small is-pulled-right" style="margin-left: 2px"
              @click="create_mutiple_regret_letter()">
              Regret Letter
            </a>
            <a href="#" class="button is-primary is-small is-pulled-right"
              @click="create_multiple_award_letter()">
              Award Letter
            </a>
          </div>
        </div>
    </div>
</template>

<script>
import prequal from "@/services/company/prequal";

export default {
  name: "ParticipantList",
  components:{
  },
  data () {
    return {
      qualified_page: 1,
      unqualified_page: 1,
      qualifiedDataCount: 0,
      unqualifiedDataCount: 0,
      qualifiedDataPerPage: 10,
      unqualifiedDataPerPage: 10,
      columns: ['Select', 'Company Name', 'Score', 'Rank'],
      options: {
        sortable: ['Company Name',],
        perPageValues: [20],
        filterable: false,
      },
      qualified_bidders: [],
      unqualified_bidders: [],
      supplier_ids: [],
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
    remove_add_supplier_ids(row){
      let el = document.getElementById('checkbox_'+row.id)
      if(el.checked === true){
        this.supplier_ids.push(row.supplier.id)
      }else{
        for( var i = 0; i < this.supplier_ids.length; i++){
          if ( this.supplier_ids[i] === row.supplier.id) {
            this.supplier_ids.splice(i, 1);
          }
        }
      }
      console.log(this.supplier_ids)
    },
    async search() {
      console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async get_qualified_bidders(){
      try{
        let response = await prequal.qualified_bidders(this.$route.params.job_id, this.$route.params.category_id)
        this.qualified_bidders = response.data['data']
        this.qualifiedDataCount = response.data['recordsTotal']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_unqualified_bidders(){
      try{
        let response = await prequal.unqualified_bidders(this.$route.params.job_id, this.$route.params.category_id)
        this.unqualified_bidders = response.data['data']
        this.unqualifiedDataCount = response.data['recordsTotal']
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
        await prequal.create_award_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        this.$router.push(
            `/company/prequal/preview/award/letter/${this.$route.params.job_id}/${this.$route.params.category_id}/${row.supplier.id}`
        )
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_multiple_award_letter(){
      let content = {
        "supplier_ids": this.supplier_ids,
        "category": this.$route.params.category_id
      }
      try{
        let response = await prequal.create_multiple_award_letter(
            content, this.$route.params.job_id, this.$route.params.category_id)
        if(response.status === 200){
          this.supplier_ids = []
          window.toast.fire({icon: 'success', title: 'Award letters created'})
        }else{
          window.toast.fire({icon: 'error', title: 'An error occured. Please Try Again!!'})
        }
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
        await prequal.create_regret_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        this.$router.push(
            `/company/prequal/preview/regret/letter/${this.$route.params.job_id}/${this.$route.params.category_id}/${row.supplier.id}`
        )
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_mutiple_regret_letter(){
      let content = {
        "supplier_ids": this.supplier_ids,
        "category": this.$route.params.category_id
      }
      try{
        let response = await prequal.create_multiple_regret_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        if (response.status === 200){
          this.supplier_ids = []
          window.toast.fire({icon: 'success', title: 'Regret letters created'})
        }else{
          window.toast.fire({icon: 'success', title: 'An error occurred. Please Try Again!!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_multiple_custom_letters(){
      let content = {
        "supplier_ids": this.supplier_ids,
        "category": this.$route.params.category_id
      }
      try{
        let response = await prequal.create_multiple_custom_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        if (response.status === 200){
          this.supplier_ids = []
          window.toast.fire({icon: 'success', title: 'Custom letters created'})
        }else{
          window.toast.fire({icon: 'success', title: 'An error occurred. Please Try Again!!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create_multiple_dd_letters(){
      let content = {
        "supplier_ids": this.supplier_ids,
        "category": this.$route.params.category_id
      }
      try{
        let response = await prequal.create_multiple_dd_letter(content, this.$route.params.job_id, this.$route.params.category_id)
        if (response.status === 200){
          this.supplier_ids = []
          window.toast.fire({icon: 'success', title: 'Regret letters created'})
        }else{
          window.toast.fire({icon: 'success', title: 'An error occurred. Please Try Again!!'})
        }
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

//.page__content {
//    margin: 0 !important;
//    @include grid_column;
//}
//.VueTables__table tbody td {
//    padding: 5px 24px;
//}
.is-primary{
  background-color: #073A82 !important;
}
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