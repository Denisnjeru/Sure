<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Tender Jobs > {{ tender.title }}
            </span>

        <div class="page__head--links">

        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title: {{ tender.title }}</p>
<!--            <p class="column-details__head&#45;&#45;desc">Fill in the required details</p>-->
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <p><strong>Sourcing Activity:</strong> Tender</p>
            <hr>
            <p><strong>Job Code:</strong> {{ tender.unique_reference }}</p>
            <hr>
            <p v-if="tender.status === 'draft'"><strong>Approval Status:</strong> Draft <a @click="publish_job()">Click Here To Publish</a></p>
            <p v-else><strong>Approval Status:</strong> Published </p>
<!--            <p v-if="tender.is_open === true"><strong>Approval Status:</strong> Open</p>-->
<!--            <p v-else><strong>Approval Status:</strong> Closed</p>-->
            <hr>
            <template v-if="tender.has_participants === false && tender.is_open === false">
              <div class="field">
                <label class="label">Import Questions From Excel<span class="required"> *</span></label>
                <a @click="generate_criteria_job_template()" class="button is-primary is-small">
                  <span><font-awesome-icon class="view__icon" icon="download"/> Questions Template</span>
                </a>
                <div class="control">
                  <br>
                  <input class="input" type="file" @change="tender_upload_template($event)">
                </div>
              </div>
              <hr>
            </template>

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
<!--            <p class="column-details__head&#45;&#45;desc">Job Actions </p>-->
<!--            <hr>-->
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <router-link :to="'/qed/tender/reports/'+tender.id"
                             class="button is-primary is-block is-small">
                  View Reports</router-link>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block is-small">Supplier Documents Update</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

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
                <a @click="openModal" class="button is-primary is-block is-small">Send Job Notifications</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a @click="openCurrentSuppliersModal" class="button is-primary is-block is-small">Current Suppliers</a>
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
          <router-link :to="'/qed/tender/create/category/' + tender.id" class="button is-primary is-small">
            Add Category
          </router-link>
        </div>
      </div>
      <div class="page__content columns bottom_content" style="position: relative; z-index: 0;">
        <div class="column is-12 column-page">
          <div class="table-search">
            <p class="table-search__instruction">
              {{ tender.title }} Categories
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

            <span slot="Category Number" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

            <span slot="Status" slot-scope="{row}">
                    <span v-if="row.is_open === true"> Open</span>
                    <span v-if="row.is_open === false"> Closed</span>
                </span>

            <span slot="Actions" slot-scope="{row}">
              <div class="dropdown" :id="'row_'+row.id">
              <div class="dropdown-trigger">
                <button class="button is-primary is-small" @click="show_category_options(row)" aria-haspopup="true"
                        aria-controls="dropdown-menu3">
                  <span> Actions <font-awesome-icon class="view__icon" icon="angle-down"/></span>
                  <span class="icon is-small">
                            <i class="angle-down" aria-hidden="true"></i>
                          </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                <div class="dropdown-content">
                  <template v-if="row.is_open === false && row.has_participants === true">
                    <router-link to="#" class="dropdown-item" style="margin-right: 2px">
                      <font-awesome-icon class="view__icon" icon="trash-alt"/>
                      Delete
                    </router-link>
                    <hr class="dropdown-divider">
                  </template>

                  <template v-if="row.is_open === false">
                    <router-link
                        :to="'/qed/tender/edit/category/'+tender.id + '/' + row.id"
                        class="dropdown-item" style="margin-right: 2px">
                        <font-awesome-icon class="view__icon" icon="pencil-alt"/>
                      Edit
                    </router-link>
                    <hr class="dropdown-divider">
                    <template>
                      <a href="#" v-if="row.has_dd_instance === false" @click="open_dd_confirm_alert(row)"
                              class="dropdown-item" style="margin-right: 2px">
                        <font-awesome-icon class="view__icon" icon="hammer"/>
                        DD
                      </a>
                      <router-link :to="'/qed/tender/dd/details/'+row.id" v-else-if="row.has_dd_instance === true"
                                   class="dropdown-item" style="margin-right: 2px">
                        <font-awesome-icon class="view__icon" icon="shield-alt"></font-awesome-icon>
                        DD
                      </router-link>
                      <hr class="dropdown-divider">
                    </template>

                    <template>
                      <a href="#" v-if="row.has_qa_instance === false"
                        @click="open_qa_confirm_alert(row)"
                        class="dropdown-item" style="margin-right: 2px">
                        <font-awesome-icon class="view__icon" icon="shield-alt"/>
                        QA
                      </a>
                      <router-link :to="'/qed/tender/qa/instructions/'+row.id" v-else-if="row.has_qa_instance === true"
                                   class="dropdown-item" style="margin-right: 2px">
                          <font-awesome-icon class="view__icon" icon="shield-alt"/>
                        QA
                      </router-link>
                      <hr class="dropdown-divider">
                    </template>
                  </template>

                  <router-link :to="'/qed/tender/category/details/'+ tender.id +'/' + row.id"
                           class="dropdown-item">
                    <font-awesome-icon class="view__icon" icon="eye"/>
                    View
                  </router-link>

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

    <div class="columns">
      <div class="column is-6"></div>
      <div class="column is-6">
        <div class="modal" id="notifications">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head is-danger">
          <div class="columns">
            <div class="column is-6">
              <h5>Job Notifications</h5>
            </div>
            <div class="column is-6">
              <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
            </div>
          </div>

        </header>
        <section class="modal-card-body" style="padding: 2%">
          <div class="tabs">
            <ul>
              <li class="is-active" id="broadcast_tab" @click="show_content('broadcast_notifications')"><a>Broadcast
                Notifications</a></li>
              <li id="email_tab" @click="show_content('email_notifications')"><a>Email Notifications</a></li>
              <li id="sms_tab" @click="show_content('sms_notifications')"><a>SMS Notifications</a></li>
            </ul>
          </div>
          <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
            <div class="columns" id="broadcast_notifications">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">Level *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select Level</option>
                          <option value="success">Success</option>
                          <option value="info">Info</option>
                          <option value="warning">Warning</option>
                          <option value="error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Action *</label>
                      <div class="control">
                        <input type="text" class="input" name="action">
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Description *</label>
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

            <div class="columns" id="email_notifications" style="display: none;">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">Level *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select Level</option>
                          <option value="success">Success</option>
                          <option value="info">Info</option>
                          <option value="warning">Warning</option>
                          <option value="error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Type *</label><br>
                      <div class="select is-fullwidth">
                        <select name="type">
                          <option selected disabled>Select Type</option>
                          <option >Paid</option>
                          <option >Potential</option>
                          <option >Qualified</option>
                          <option >Unqualified</option>
                          <option >Non-Responsive</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Action *</label>
                      <div class="control">
                        <input type="text" class="input" name="action">
                      </div>
                    </div>

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
                      <label>Attach Files *</label>
                      <div class="control">
                        <input type="file" multiple name="files" required>
                      </div>
                    </div>

                    <div class="field">
                      <a  class="button is-block is-primary">Send</a>
                    </div>
                  </form>
                </div>
              </div>
            </div>

            <div class="columns" id="sms_notifications" style="display: none">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select</option>
                          <option >All</option>
                          <option >Potential</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Content *</label>
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

        <section class="modal-card-body">
          <!--            <button class="button is-fullwidth is-primary">Submit</button>-->
        </section>
      </div>
    </div>
    <div class="modal" id="current_suppliers">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head is-danger">
            <div class="columns">
              <div class="column is-6">
                <h5>Current Suppliers</h5>
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeCurrentSuppliersModal" aria-label="close"></button>
              </div>
            </div>

          </header>
          <section class="modal-card-body">
            <div class="tabs">
              <ul>
                <li class="is-active" id="upload_cs_tab" @click="show_current_suppliers_content('upload_current_suppliers')"><a>Upload Current Suppliers</a></li>
                <li id="send_cs_letter_tab" @click="show_current_suppliers_content('send_current_suppliers_letter')"><a>Send Letter</a></li>
              </ul>
            </div>
            <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
              <div class="columns" id="upload_current_suppliers">
                <div class="column is-12">
                  <div class="container">
                    <form v-on:submit.prevent="uploadCurrentSuppliers()">
                      <div class="field">
                        <label style="font-weight: bold">Excel document *</label>
                        <div class="control">
                          <input id="current_suppliers_input" type="file" class="input" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel">
                        </div>
                      </div>
                      <br>
                      <div class="field">
                        <input type="submit" class="button is-block is-primary" value="Upload">
                      </div>
                    </form>
                  </div>
                </div>
              </div>
              <div class="columns" id="send_current_suppliers_letter" style="display: none">
                <div class="column is-12">
                  <div class="container">
                    <form v-on:submit.prevent="sendCurrentSuppliersLetter()">
                      <div class="field">
                        <label style="font-weight: bold">Letter *</label>
                        <div class="control">
                          <input id="current_suppliers_letter_input" type="file" class="input" accept=".pdf">
                        </div>
                      </div>
                      <br>
                      <div class="field">
                        <input type="submit" class="button is-block is-primary" value="Send">
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="modal-card-body">
            <!--            <button class="button is-fullwidth is-primary">Submit</button>-->
          </section>
      </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/qed/tender";
import {mapGetters} from 'vuex'

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Category Title', 'Category Number', 'Status', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Number', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      tender: {},
      categories: [],
    }
  },
  computed: {
      ...mapGetters('Qed', ['selectedBuyer']),
  },
  methods: {
    async uploadCategorySuppliers(event){
      let f = event.target.files[0]
      let form_data = new FormData()
      form_data.append('category_suppliers', f, f.name)

      try{
        let response = await tender.upload_category_suppliers(this.tender.id, form_data)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.$router.push(`/qed/tender/cat/suppliers/progress/${this.tender.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: response.data['response_message']})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async publish_job(){
      try{
        let response = await tender.publish_job(this.tender.id)
        if (response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.getTender()
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    show_category_options(row) {
      let element = document.getElementById('row_' + row.id)
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
    show_content(tab) {
      if (tab === 'broadcast_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'block'
        document.getElementById('email_notifications').style.display = 'none'
        document.getElementById('sms_notifications').style.display = 'none'

        document.getElementById('broadcast_tab').classList.add('is-active')
        document.getElementById('email_tab').classList.remove('is-active')
        document.getElementById('sms_tab').classList.remove('is-active')
      } else if (tab === 'email_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'none'
        document.getElementById('email_notifications').style.display = 'block'
        document.getElementById('sms_notifications').style.display = 'none'

        document.getElementById('broadcast_tab').classList.remove('is-active')
        document.getElementById('email_tab').classList.add('is-active')
        document.getElementById('sms_tab').classList.remove('is-active')
      } else if (tab === 'sms_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'none'
        document.getElementById('email_notifications').style.display = 'none'
        document.getElementById('sms_notifications').style.display = 'block'

        document.getElementById('broadcast_tab').classList.remove('is-active')
        document.getElementById('email_tab').classList.remove('is-active')
        document.getElementById('sms_tab').classList.add('is-active')
      }
    },
    show_current_suppliers_content(tab) {
      if (tab === 'upload_current_suppliers') {
        document.getElementById('upload_current_suppliers').style.display = 'block'
        document.getElementById('send_current_suppliers_letter').style.display = 'none'

        document.getElementById('upload_cs_tab').classList.add('is-active')
        document.getElementById('send_cs_letter_tab').classList.remove('is-active')
      } else if (tab === 'send_current_suppliers_letter') {
        document.getElementById('upload_current_suppliers').style.display = 'none'
        document.getElementById('send_current_suppliers_letter').style.display = 'block'

        document.getElementById('upload_cs_tab').classList.remove('is-active')
        document.getElementById('send_cs_letter_tab').classList.add('is-active')
      }
    },
    async tender_upload_template(event){
      let file = event.target.files[0]
      let form_data = new FormData();
      form_data.append("question_template", file, file.name)

      try{
        let response = await tender.upload_criteria(form_data, this.tender.id)
        print(response.status)
        if (response === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async generate_criteria_job_template(){
      try{
        let response = await tender.criteria_job_template(this.tender.id)
        if (response.status === 200){
          this.template_url = ''+process.env.VUE_APP_DOWNLOAD_URL+'/'+response.data['filepath']
          // document.getElementById('criteria_template_download').click()
          this.downloadFile(this.template_url)
        }else{
          window.toast.fire({icon: 'success', title: 'Error. Try Again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    downloadFile(url) {
      // Create a link and set the URL using `createObjectURL`
      const link = document.createElement("a");
      link.style.display = "none";
      link.href = url;
      link.download = 'Questions Template';
      link.innerText = 'Download'
      // link.target = '_blank'

      document.body.appendChild(link);
      link.click();

      setTimeout(() => {
        URL.revokeObjectURL(link.href);
        link.parentNode.removeChild(link);
      }, 0);
    },

    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    openModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    openCurrentSuppliersModal() {
      document.getElementById('current_suppliers').classList.add('is-active');
    },
    closeCurrentSuppliersModal() {
      document.getElementById('current_suppliers').classList.remove('is-active');
    },
    async getTender() {
      try {
        let response = await tender.tender(this.$route.params.id, this.selectedBuyer.id)
        this.tender = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await tender.categories(this.$route.params.id)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.dataPerPage)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async uploadCurrentSuppliers() {
      try {
        this.closeCurrentSuppliersModal()
        let form_data = new FormData()
        let current_suppliers_file = document.getElementById("current_suppliers_input").files[0];
        form_data.append("current_suppliers", current_suppliers_file, current_suppliers_file.name)

        let response = await tender.upload_current_suppliers(form_data, this.$route.params.id)
        window.toast.fire({icon: 'success', title: response.data.response_message})
      } catch (err) {
        window.toast.fire({icon: 'error', title: err.response.data.response_message})
      }
    },
    async sendCurrentSuppliersLetter() {
      try {
        this.closeCurrentSuppliersModal()
        let form_data = new FormData()
        let current_suppliers_file = document.getElementById("current_suppliers_letter_input").files[0];
        form_data.append("current_suppliers_letter", current_suppliers_file, current_suppliers_file.name)

        let response = await tender.send_current_suppliers_letter(form_data, this.$route.params.id)
        window.toast.fire({icon: 'success', title: response.data.response_message})
      } catch (err) {
        window.toast.fire({icon: 'error', title: err.response.data.response_message})
      }
    },
    async initiate_qa(row) {
      let content = {
        "category": row.id,
        "title": row.name
      }
      try {
        let response = await tender.initiate_qa(content, row.id)
        console.log(response)
        window.toast.fire({icon: 'success', title: 'Quality assurance initiated successfully'})
        this.$router.push(`/qed/tender/qa/instructions/${row.id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async initiate_dd(row) {
      let content = {
        "category": row.id,
        "title": row.name
      }
      try {
        let response = await tender.initiate_dd(content, row.id)
        console.log(response)
        window.toast.fire({icon: 'success', title: 'Due diligence initiated successfully'})
        this.$router.push(`/qed/tender/dd/details/${row.id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    open_qa_confirm_alert(row) {
      let self = this
      this.$swal.fire({
        title: 'Quality Assurance',
        icon: 'info',
        html:
            'Are you sure you want to initiate the quality assurance process ??',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonColor: '#073A82',
        confirmButtonText:
            '<i class="fa fa-thumbs-up"></i> Confirm',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        cancelButtonText:
            '<i class="fa fa-thumbs-down"></i>Cancel',
        cancelButtonAriaLabel: 'Thumbs down',
      }, function (isConfirm) {
        if (isConfirm) {
          self.initiate_qa(row)
        }
      })
    },
    open_dd_confirm_alert(row) {
      let self = this
      this.$swal.fire({
        title: 'Due Diligence',
        icon: 'info',
        html:
            'Are you sure you want to initiate the due diligence process ??',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonColor: '#073A82',
        confirmButtonText:
            '<i class="fa fa-thumbs-up"></i> Confirm',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        cancelButtonText:
            '<i class="fa fa-thumbs-down"></i>Cancel',
        cancelButtonAriaLabel: 'Thumbs down',
      }, function (isConfirm) {
        if (isConfirm) {
          self.initiate_dd(row)
        }
      })
    },
  },
  mounted() {
    this.getTender()
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

.is-primary {
  background-color: #073A82 !important;
}
.input {
  border-radius: 15px !important;
}
select {
  border-radius: 15px !important;
}

.textarea{
  border-radius: 15px !important;
}
.tabs li.is-active a {
    border-bottom-color: #073A82;
    color: #073A82;
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
//.VueTables__table tbody td {
//    padding: 5px 24px;
//}
hr {
  margin: 0.5rem 0 !important;
}
//.dropdown-content {
//  position: fixed !important;
//}
//.page__content {
//    position: relative;
//    z-index: 0;
//}
.dropdown-item {
    padding: 0.1rem 1rem;
    font-size: 12px;
}
.dropdown-item svg:not(:root).svg-inline--fa {
    overflow: visible;
    color: green;
}
</style>