<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               List of Tender Jobs
            </span>

            <div class="page__head--links">
                    <router-link to="/company/create/tender" class="button is-primary">
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
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
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
                    <span> {{ row.status }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <template v-if="row.is_open === false && row.has_participants === false">
                    <button class="button is-danger is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="trash-alt"></font-awesome-icon></p>
                    </button>
                  </template>

                  <template v-if="row.is_open === false">
                    <router-link :to="'/company/edit/tender/'+row.id" class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt" /></p>
                    </router-link>
                  </template>

                  <button @click="tenderDetails(row)" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Categories</p>
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
import tender from "@/services/company/tender";
export default {
  name: "PrequalList",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Job Title', 'Job Code', 'Approved By', 'Status', 'Actions'],
      options: {
        sortable: ['Job Title', 'Job Code', 'Approved By', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      tenders: []
    }
  },
  methods: {
    // openModal() {
    //   console.log('got here')
    //   document.getElementById('create_tender').classList.add('is-active');
    // },
    tenderDetails(row){
      this.$router.push(`/company/tender/details/${row.id}`)
    },
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getTenders(){
      try{
        let response = await tender.tenders(this.page)
        this.tenders = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
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
</style>