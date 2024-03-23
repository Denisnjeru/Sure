<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               RFQ Job Details > 
            </span>

        <div class="page__head--links">

        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
            <div class="column-details__head">
              <p class="column-details__head--title">Job Title: {{ rfq.title }} </p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <p><strong>Sourcing Activity:</strong> Request for Quotation</p>
              <hr>
              <p><strong>Job Code:</strong> {{ rfq.unique_reference }}</p>
              <hr>
              <p v-if="rfq.is_open === true"><strong>Approval Status:</strong> Open</p>
              <p v-else><strong>Approval Status:</strong> Closed</p>
              <hr>
              <template>
                <div class="field">
                  <label class="label">Upload Category Suppliers<span class="required"> *</span></label>
                  <div class="control">
                    <input class="input" type="file" @change="uploadCategorySuppliers($event)" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                  </div>
                </div>
              </template>
            </div>

        </div>

        <div class="column-details column">
          <div class="column-details__head">
              <p class="column-details__head--title">Actions</p>
          </div>
            <!-- Form Details -->
          <div class="column-details__content">
            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                 <router-link :to="'/company/rfq/job/reports/' + rfq.id" class="button is-primary is-block is-small">
                  View Reports
                 </router-link>
                <!-- <a href="#" class="button is-primary is-block">View Reports</a> -->
              </div>
              <div class="column is-2">

              </div>
            </div>

            <!-- <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">Supplier Documents Update</a>
              </div>
              <div class="column is-2">

              </div>
            </div> -->

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block is-small">Zip Files</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block is-small">Send Job Notifications</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Categories belonging to this job
            </span>

        <div class="page__head--links">
          <router-link :to="'/company/rfq/create/category/' + rfq.id" class="button is-primary is-small">
            Add Category
          </router-link>
        </div>
      </div>
      <div class="page__content columns bottom_content">
        <div class="column is-12 column-page">
          <div class="table-search">
            <p class="table-search__instruction">
              {{ rfq.title }} Categories
            </p>
            <div class="table-search__search">
              <font-awesome-icon class="table-search__search--icon" icon="search"/>
              <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
            </div>
          </div>

          <v-client-table :columns="columns" :options="options" :data="categories">
                <span slot="Category Title" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

            <span slot="Category Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

            <span slot="Status" slot-scope="{row}">
                    <span v-if="row.status_open === true"> Open</span>
                    <span v-else > Closed</span>
                </span>

            <span slot="Actions" slot-scope="{row}">
              <template v-if="row.is_open === false && row.has_participants === true">
                <button class="button is-danger" style="margin-right: 2px">
                  <p><font-awesome-icon class="view__icon" icon="trash-alt"/></p>
                </button>
              </template>

              <template v-if="row.is_open === false">
                <router-link
                    :to="'/company/rfq/edit/category/'+ rfq.id + '/' + row.id"
                    class="button is-primary" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                </router-link>
              </template>

              <router-link :to="'/company/rfq/category/details/'+ rfq.id +'/' + row.id"
                           class="button is-primary is-small">
                <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>
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
  </div>
</template>

<script>
import rfq from "@/services/company/rfq";

export default {
  name: "RfqDetails",
  data() {
    return {
      page: 2,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Category Title', 'Category Code', 'Status', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Code', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      rfq: {},
      categories: [],
    }
  },    
  methods: {
    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    async uploadCategorySuppliers(event){
      let f = event.target.files[0]
      let form_data = new FormData()
      form_data.append('category_suppliers', f, f.name)

      try{
        let response = await rfq.upload_category_suppliers(this.rfq.id, form_data)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.$router.push(`/company/rfq/cat/suppliers/progress/${this.rfq.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: response.data['response_message']})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getRfq() {
      try {
        let response = await rfq.rfq(this.$route.params.id)
        this.rfq = response.data
        console.log(this.rfq)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await rfq.categories(this.$route.params.id)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.dataPerPage)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    openModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
  },
  mounted() {
    this.getRfq()
    this.getCategories()
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
  margin: 0 !important;
  //@include grid_column;
}
.page__head{
  padding: 1px 30px;
}
.top_content{
  display: flex; justify-content: space-between; align-items: center;
}
.bottom_content{
  display: flex; flex-flow: column nowrap; justify-content: space-between;align-items: center;
}
.is-primary {
  background-color: #073A82 !important;
}
.modal-card{
  margin-left: 36%; width: 560px; background-color: #ffffff !important; border-radius: 12px;
}
.modal{
  z-index: 9999;
}
.modal-card-head{
  background-color: #ffffff !important; display: block
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
hr {
  margin: 0.5rem 0 !important;
}
</style>