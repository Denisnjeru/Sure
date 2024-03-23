<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               List of Due Diligence Suppliers
            </span>

            <div class="page__head--links">
                    <router-link :to="'/qed/tender/dd/add/questions/'+$route.params.category_id" class="button is-primary">
                        New Due Diligence Question
                    </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Due Diligence
                    </p>
                    <div class="table-search__search">
<!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
<!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="participants">
                <span slot="Company Name" slot-scope="{row}">
                    <span> {{ row.supplier.company_name }}</span>
                </span>

                <span slot="Phone Number" slot-scope="{row}">
                    <span> {{ row.supplier.phone_number }}</span>
                </span>

                <span slot="Contact Name" slot-scope="{row}">
                    <span> {{ row.supplier.contact_name }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <router-link :to="'/qed/tender/dd/supplier/questions/'+$route.params.category_id+'/'+row.id" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Conduct DD</p>
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
import tender from "@/services/qed/tender";

export default {
  name: "Participants",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Company Name', 'Phone Number', 'Contact Name', 'Actions'],
      options: {
        sortable: ['Company Name',],
        perPageValues: [20],
        filterable: false,
      },
      participants: []
    }
  },
  methods: {
    async search() {
      console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async get_participants(){
      try{
        let response = await tender.dd_participants(this.$route.params.category_id)
        this.participants = response.data['data']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_participants()
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