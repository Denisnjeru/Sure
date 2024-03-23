<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               RFQ Jobs > {{rfq.title}} > {{ category.name }}
            </span>

        <div class="page__head--links">
        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title:{{ rfq.title }} </p>
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
            <p><strong>Opening Date:</strong> {{ category.opening_date }}</p>
            <hr>
            <p><strong>Closing Date:</strong> {{ category.closing_date }}</p>
            <hr>
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
                <router-link :to="'/company/rfq/invited/suppliers/'+rfq.id+'/'+category.id" 
                  class="button is-primary is-fullwidth is-small" style="margin-right: 2px">
                    Invite Suppliers  
                </router-link>
              </div>
              <div class="column is-2">
              </div>
            </div>
            <div class="columns">
              <div class="column is-2">
              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-small is-block">Refresh Scores</a>
              </div>
              <div class="column is-2">
              </div>
            </div>

            <div class="columns">
              <div class="column is-2">
              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-small is-block" @click="openNotificationsModal()">Send Category Notifications</a>
              </div>
              <div class="column is-2">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="page__head">
            <span class="page__head--title column is-6">
               RFQ Items
            </span>

            <div class="page__head--links column is-6" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">
                  <button type="button" class="button is-primary is-small is-pulled-right" @click="downloadCurrentPriceTemplate()">
                      Prices Template
                  </button>
                </div>
                <div class="column is-6">
                  <button type="button" class="button is-primary is-small is-pulled-right" @click="openImportModal">
                      Import Prices
                    </button>
                </div>
              </div>
            </div>
          </div>
          <div class="page__content columns bottom_content">
            <div class="table-search">
                <p class="table-search__instruction">

                </p>
                <div class="table-search__search">
                  <font-awesome-icon class="table-search__search--icon" icon="search"/>
                  <input @keyup.enter="search()" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="item_columns" :data="items">
                <span slot="No." slot-scope="{row}">
                  {{ row.item_number }}
                </span>
                <span slot="Item" slot-scope="{row}">
                  <span> {{ row.item_description }} </span>
                </span>
                <span slot="Reserve" slot-scope="{row}">
                  <span> {{ row.current_price }} </span>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>

        </div>

        <div class="column-details column">
          <div class="page__head">
              <span class="page__head--title column is-4">
                 Participants
              </span>
                <div class="page__head--links column is-8" style="display: inline !important;">
                    <button type="button" class="button is-primary is-small is-pulled-right" @click="closeCategory()" v-if="category.status_open === true">
                      Close Category
                    </button>

                    <button type="button" v-else class="button is-small is-primary is-pulled-right" @click="openModal">
                      Open Category
                    </button>
                </div>
          </div>
          <div class="page__content columns bottom_content">
            <div class="table-search">
                <p class="table-search__instruction">
                </p>
                <div class="table-search__search">
                  <font-awesome-icon class="table-search__search--icon" icon="search"/>
                  <input @keyup.enter="search()" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="participant_columns" :options="participant_options" :data="participants">
                <span slot="Company" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                    <span>{{ row.company_name }}</span>
                  </template>
                  <template v-if="category.status_open === false">
                    <span>{{ row.company_name }}</span>
                  </template>
                   <template>
                    <span></span>
                  </template>
                </span>

                <span slot="Contact Name" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template v-if="category.status_open === false">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template>
                    <span></span>
                  </template>

                </span>

                <span slot="Actions" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                   <span>{{row.phone_number}}</span>
                  </template>
                  <template v-else>
                    <button class="button is-primary is-small" @click="downloadSupplierResponse(row)" aria-haspopup="true" aria-controls="dropdown-menu3">
                        <span>Report</span>
                        <span class="icon is-small">
                          <i class="angle-down" aria-hidden="true"></i>
                        </span>
                  </button>
                  </template>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" id="open_rfq">
        <div class="modal-background"></div>
        <div class="modal-card" style="margin-left: 37%; background-color: #DBE9FE !important; border-radius: 12px">
          <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important; display: block">
            <div class="columns">
              <div class="column is-6">
                <p class="modal-card-title">Open RFQ</p>
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
              </div>
            </div>
            <div class="columns">
              <div class="column">
                <p>Fill in the required fields</p>
              </div>
            </div>
          </header>
          <section class="modal-card-body" style="padding: 2%">
            <form>
              <div class="field">
                <label class="label">New Closing Date *</label>
                <div class="control">
                  <input class="input" type="datetime-local" v-model="open_form.closing_date" required>
                </div>
              </div>
            </form>
          </section>

          <section class="modal-card-body">
            <button class="button is-fullwidth is-primary" @click="openCategory()">Submit</button>
          </section>
        </div>
    </div>
    
    <div class="columns">
      <div class="column is-4">
          <div class="modal" id="import_prices">
            <div class="modal-background"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <h5 class="modal-card-title">Import Current Prices</h5>
                <button class="delete is-pulled-right" @click="closeImportModal" aria-label="close"></button>
              </header>
              <section class="modal-card-body">
                <input class="input" type="file" name="price_import" id="price_import" @change="fetchFileUpload($event)">
              </section>
              <footer class="modal-card-foot">
                <button class="button is-primary" @click="uploadCurrentPriceTemplate()">Submit</button>
              </footer>
            </div>
        </div>
      </div>
    </div>


    <div class="columns">
      <div class="column is-6">
        <div class="modal" id="notifications">
          <div class="modal-background"></div>
          <div class="modal-card">
            <header class="modal-card-head is-danger">
              <div class="columns">
                <div class="column is-12">
                  <h5>RFQ Category Notifications</h5>
                </div>
                <div class="column is-2">
                  <button class="delete is-pulled-right" @click="closeNotificationsModal" aria-label="close"></button>
                </div>
              </div>

            </header>
            <section class="modal-card-body" style="padding: 2%">
              <div class="tabs">
                <ul>
                  <li class="is-active" id="reminder_tab" ><a>Reminder Notification</a></li>
                  <li id="extension_tab"><a>Extension Notification</a></li>
                  <li id="custom_tab"><a>Custom Notifications</a></li>
                </ul>
              </div>
              <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
                <div class="columns" id="reminder_notifications">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Invited Suppliers</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                <div class="columns" id="extension_notifications" style="display: none;">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Invited Suppliers</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                <div class="columns" id="custom_notifications" style="display: none;">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Subject *</label>
                          <div class="control">
                            <input type="text" class="input" name="subject">
                          </div>
                        </div>

                        <div class="field">
                          <label style="font-weight: bold">Message *</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import rfq from "@/services/company/rfq";

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      participant_columns: ['Company', 'Contact Name', 'Actions'],
      item_columns: ['No.', 'Item', 'Reserve'],
      participant_options: {
        sortable: ['Company',],
        perPageValues: [20],
        filterable: false,
      },
      item_options: {
        sortable: ['Item',],
        perPageValues: [20],
        filterable: false,
      },
      rfq: {},
      category: {},
      participants: [],
      items: [],
      price_import:"",
      open_form: {
        "closing_date": ""
      },
    }
  },
  methods: {
    openModal() {
      console.log('got here')
      document.getElementById('open_rfq').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('open_rfq').classList.remove('is-active');
    },
    openNotificationsModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeNotificationsModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    openImportModal(){
      document.getElementById('import_prices').classList.add('is-active');
    },
    closeImportModal(){
      document.getElementById('import_prices').classList.remove('is-active');
    },
    fetchFileUpload(event) {
      this.price_import = event.target.files[0]
    },
    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    async getCategory() {
      try {
        let response = await rfq.rfqCategoryDetails(this.$route.params.rfq_id, this.$route.params.category_id)
        this.category = response.data
        this.rfq = this.category.rfq
        this.items = this.category.items
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.category)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getParticipants(){
      try {
        let response = await rfq.rfqGetParticipants(this.$route.params.rfq_id, this.$route.params.category_id)
        this.participants = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }

    },
    async closeCategory(){
      try{
        let response = await rfq.closeRFQCategory(this.rfq.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async openCategory(){
      try{
        let response = await rfq.openRFQCategory(this.open_form, this.rfq.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.open_form.closing_date = ""
        this.closeModal()
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async downloadSupplierResponse(row){
      try{
        let response = await rfq.rfqDownloadSupplierResponse(this.$route.params.rfq_id, this.$route.params.category_id, row.id)
        
        if(response.status == 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          console.log(process.env.VUE_APP_DOWNLOAD_URL)
          try{
            window.open(reportUrl)
          }catch(err){
            window.toast.fire({icon: 'error', title: err})
          }
        }
        else{
           window.toast.fire({icon: 'error', title: 'Error downloading the report'})
        }

      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
     async downloadCurrentPriceTemplate(){
      try{
        let response = await rfq.rfqDownloadCurrentSupplierTemplate(this.$route.params.rfq_id,this.$route.params.category_id)
        console.log(response)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "File download initiated"})
          this.$router.push(`/company/rfq/category/download/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
   async uploadCurrentPriceTemplate(){
      let formData = new FormData();
      formData.append("price_import_file", this.price_import, this.price_import.name)
      let content = formData

      try{
        let response = await rfq.rfqUploadCurrentSupplierTemplate(content,this.$route.params.rfq_id,this.$route.params.category_id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "File upload initiated"})
          this.$router.push(`/company/rfq/category/upload/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Error uploading file"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getCategory()
    this.getParticipants()
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
.top_content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom_content {
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  align-items: center;
}

.page .table-search[data-v-e49b950c] {
    padding: 12px 6px
}

.is-primary {
  background-color: #073A82 !important;
}

hr{
  margin: 0.5rem 0 !important;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
</style>