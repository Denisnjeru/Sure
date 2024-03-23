<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               List of Tender Jobs
            </span>

            <div class="page__head--links">
                    <router-link to="/company/create/tender" class="button is-primary is-small">
                        New Tender
                    </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Company Tenders
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" v-model="search_key" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="tenders">
                <span slot="Job Title" slot-scope="{row}">
                    <span> {{ row.title }}</span>
                </span>

                <span slot="Job Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

                <span slot="Approved By" slot-scope="{row}">
                    <span> {{ row.approved_by }}</span>
                </span>

                <span slot="Status" slot-scope="{row}">
                    <span v-if="row.status === 'draft'"> Draft</span>
                    <span v-else-if="row.status === 'final'"> Published</span>
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
                          <router-link :to="'/company/edit/tender/'+row.id" class="dropdown-item" style="margin-right: 2px;">
                            <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Edit</span>
                          </router-link>
                          <hr class="dropdown-divider">
                        </template>

                        <a @click="tenderDetails(row)" class="dropdown-item">
                          <font-awesome-icon class="view__icon" icon="eye"/>
                          Categories
                        </a>
<!--                        <hr class="dropdown-divider">-->
<!--                        <router-link :to="'#'+row.id" class="dropdown-item">-->
<!--                          <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                          Interim Report-->
<!--                        </router-link>-->


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
        </div>
    </div>
</template>

<script>
import tender from "@/services/company/tender";
export default {
  name: "PrequalList",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      columns: ['Job Title', 'Job Code', 'Approved By', 'Status', 'Actions'],
      options: {
        sortable: ['Job Title', 'Job Code', 'Approved By', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      tenders: [],
      search_key: "",
    }
  },
  methods: {
    // openModal() {
    //   console.log('got here')
    //   document.getElementById('create_tender').classList.add('is-active');
    // },
    show_category_options(row) {
      let element = document.getElementById('row_' + row.id)
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
    tenderDetails(row){
      this.$router.push(`/company/tender/details/${row.id}`)
    },
    async search() {
      if (this.search_key != ""){
        try{
          let response = await tender.job_search(this.page, this.search_key, this.dataPerPage)
          this.page = 1
          this.tenders = response.data['results']
          this.dataCount = response.data['count']
        }catch (err){
          window.toast.fire({icon: 'error', title: err})
        }
      }else{
        this.getTenders()
      }
    },
    async fetchData() {
        console.log('this.page');
    },
    async getTenders(){
      try{
        let response = await tender.tenders(this.page, this.dataPerPage)
        this.tenders = response.data['results']
        this.dataCount = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getTenders()
  }
}

// document.addEventListener('DOMContentLoaded', () => {
//   // Functions to open and close a modal
//   function openModal($el) {
//     $el.classList.add('is-active');
//   }
//
//   function closeModal($el) {
//     $el.classList.remove('is-active');
//   }
//
//   function closeAllModals() {
//     (document.querySelectorAll('.modal') || []).forEach(($modal) => {
//       closeModal($modal);
//     });
//   }
//
//   // Add a click event on buttons to open a specific modal
//   (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
//     const modal = $trigger.dataset.target;
//     const $target = document.getElementById(modal);
//
//     $trigger.addEventListener('click', () => {
//       openModal($target);
//     });
//   });
//
//   // Add a click event on various child elements to close the parent modal
//   (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
//     const $target = $close.closest('.modal');
//
//     $close.addEventListener('click', () => {
//       closeModal($target);
//     });
//   });
//
//   // Add a keyboard event to close all modals
//   document.addEventListener('keydown', (event) => {
//     const e = event || window.event;
//
//     if (e.keyCode === 27) { // Escape key
//       closeAllModals();
//     }
//   });
// });
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