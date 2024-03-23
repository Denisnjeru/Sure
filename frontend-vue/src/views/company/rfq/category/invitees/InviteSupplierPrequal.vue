<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               RFQ > Category > Invite Suppliers
            </span>

            <div class="page__head--links">
            </div>
        </div>

        <div class="page__head">
            <span class="page__head--title">
               Inviting for RFQ: {{}}
            </span>
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

              <v-client-table :columns="columns" :options="options" :data="prequals">
                <span slot="Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>
                <span slot="Category Name" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

                <span slot="Participants" slot-scope="{row}">
                    <span> {{ row.has_participants }}</span>
                </span>

              <span slot="Invite">
                 <!-- <router-link :to="'/company/prequalification/create/category/' + rfq.id" class="button is-primary">
                    Invite
                  </router-link> -->
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
  name: "InviteSupplierPrequal",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Code', 'Category Name', 'Participants', 'Invite'],
      options: {
        sortable: ['Code', 'Category Name'],
        perPageValues: [20],
        filterable: false,
      },
      prequals: [],
    }
  },
  methods: {
    async search() {
      console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getRelatedPrequals() {
      //get related prequal categories
      try {
        let response = await rfq.rfqRelatedPrequals(this.$route.params.rfq_id, this.$route.params.category_id)
        console.log(response.data)
        this.prequals = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getRelatedPrequals()
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