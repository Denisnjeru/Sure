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
                   
                     <router-link to="/company/create/rfq" class="button is-primary is-small">
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

                <span slot="Actions" slot-scope="{row}">
                  <div class="dropdown" :id="'row_'+row.id">
                    <div class="dropdown-trigger">
                      <button class="button is-primary is-small" @click="show_category_options(row)" aria-haspopup="true"
                              aria-controls="dropdown-menu3">
                        <span> Actions <font-awesome-icon
                            class="view__icon" icon="angle-down"/></span>
                        <span class="icon is-small">
                                  <i class="angle-down" aria-hidden="true"></i>
                                </span>
                      </button>
                    </div>
                    <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                      <div class="dropdown-content">
                        <template v-if="row.is_open === false && row.has_participants === false">
                          <router-link :to="'#'" class="dropdown-item" style="margin-right: 2px;">
                            <span><font-awesome-icon class="view__icon" icon="trash-alt"/> Delete</span>
                          </router-link>
                          <hr class="dropdown-divider">
                        </template>

                        <template v-if="row.is_open === false">
                          <router-link class="dropdown-item" style="margin-right: 2px;">
                            <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Edit</span>
                          </router-link>
                          <hr class="dropdown-divider">
                        </template>

                        <a @click="rfqDetails(row)" class="dropdown-item">
                          <font-awesome-icon class="view__icon" icon="eye"/>
                          Categories
                        </a>
                      </div>
                    </div>
                  </div>
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
import rfq from "@/services/company/rfq";

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
  methods: {
    show_category_options(row) {
      let element = document.getElementById('row_' + row.id)
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
    rfqDetails(row){
      this.$router.push(`/company/rfq/details/${row.id}`)
    },
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