<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               List of RFQ Jobs
            </span>

            <div class="page__head--links">
                   
                      <!-- <button type="button" class="button is-primary" @click="openModal()">
                          New RFQ
                      </button> -->
                   
                     <router-link to="/qed/create/rfq" class="button is-primary">
                        New RFQ
                    </router-link>

            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Company RFQs
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

                <span slot="Approved By" slot-scope="{row}">
                    <span> {{row.approved_by }}</span>
                </span>

                <span slot="Status" slot-scope="{row}">
                    <span> {{ row.status }}</span>
                </span>

                <span class="actions" slot="Actions" slot-scope="{row}" >
                  <span class="actions__edit">
                      <font-awesome-icon class="actions__icon" icon="pen-alt" />
                  </span>
                  <span class="actions__delete">
                      <font-awesome-icon class="actions__icon" icon="trash-alt" />
                  </span>
                  <button @click="rfqDetails(row)" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Categories</p>
                  </button>
                </span>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>

          <CreatePrequal/>
        </div>
    </div>
</template>

<script>
import rfq from "@/services/qed/rfq";
import {mapGetters} from 'vuex'

export default {
  name: "RfqList",
  components:{
  },
  data(){
    return {
      page: 1,
      dataCount: null,
      dataPerPage: null,
      columns: ['Job Title', 'Job Code', 'Approved By', 'Status', 'Actions'],
      options: {
        sortable: ['Job Title', 'Job Code', 'Approved By', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      rfqs: []
    }
  },
  computed: {
      ...mapGetters('Qed', ['selectedBuyer']),
  },
  methods: {
    rfqDetails(row){
      this.$router.push(`/qed/rfq/details/${row.id}`)
    },
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log(this.page);
    },
    async getRfqs(){
      try{
        let response = await rfq.rfqs(this.page, this.selectedBuyer.id)
        this.rfqs = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.rfqs)
      }catch (err){
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