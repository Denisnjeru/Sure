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
                <router-link :to="'/company/tender/reports/'+tender.id"
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
                <a @click="confirmInviteEmail()" class="button is-primary is-block is-small">Send Invite Email</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a @click="confirmInviteSMS()" class="button is-primary is-block is-small">Send Invite SMS</a>
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
          <router-link :to="'/company/tender/create/category/' + tender.id" class="button is-primary is-small">
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
              <input @keyup.enter="search()" v-model="category_search_key" class="table-search__search--input" type="text" placeholder="Search here">
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
                        :to="'/company/tender/edit/category/'+tender.id + '/' + row.id"
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
                      <router-link :to="'/company/tender/dd/details/'+row.id" v-else-if="row.has_dd_instance === true"
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
                      <router-link :to="'/company/tender/qa/instructions/'+row.id" v-else-if="row.has_qa_instance === true"
                                   class="dropdown-item" style="margin-right: 2px">
                          <font-awesome-icon class="view__icon" icon="shield-alt"/>
                        QA
                      </router-link>
                      <hr class="dropdown-divider">
                    </template>
                  </template>

                  <router-link :to="'/company/tender/category/details/'+ tender.id +'/' + row.id"
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
                  <form @submit.prevent="send_broadcast_notification()">
                      <div class="field">
                        <label style="font-weight: bold">Level *</label><br>
                        <div class="select is-fullwidth">
                          <select name="level" v-model="broadcast_notification.level" required>
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
                          <input type="text" v-model="broadcast_notification.verb" class="input" name="action" required>
                        </div>
                      </div>

                      <div class="field">
                        <label style="font-weight: bold">Description *</label>
                        <div class="control">
                          <textarea class="textarea" v-model="broadcast_notification.description" name="description" required></textarea>
                        </div>
                      </div>

                      <div class="field">
                        <button type="submit" class="button is-block is-primary">Send</button>
                      </div>
                    </form>
                </div>
              </div>
            </div>

            <div class="columns" id="email_notifications" style="display: none;">
              <div class="column is-12">
                <div class="container">
                  <form @submit.prevent="send_email_notification()">
                      <div class="field">
                        <label style="font-weight: bold">Level *</label><br>
                        <div class="select is-fullwidth">
                          <select name="level" v-model="email_notification.level" required>
                            <option value="" selected disabled>Select Level</option>
                            <option value="success">Success</option>
                            <option value="info">Info</option>
                            <option value="warning">Warning</option>
                            <option value="error">Error</option>
                          </select>
                        </div>
                      </div>

                      <div class="field">
                        <label style="font-weight: bold">To *</label><br>
                        <div class="select is-fullwidth">
                          <select name="type" v-model="email_notification.to" id="email_to" @change="togglePotentialSelection()" required>
                            <option value="" selected disabled>Select Type</option>
                            <!-- <option value="paid">Paid</option> -->
                            <option value="potential">Potential</option>
                            <!-- <option value="qualified">Qualified</option> -->
                            <!-- <option value="unqualified">Unqualified</option> -->
                            <option value="non-responsive">Non-Responsive</option>
                          </select>
                        </div>
                      </div>

                      <div class="field" id="potential_selection" hidden>
                        <label style="font-weight: bold">Potential Selection</label>
                        <div class="select is-fullwidth">
                          <select name="potential_selection" id="email_potential_selection" @change="toggleOtherFields()" v-model="email_notification.potential_selection">
                            <option value="" selected disabled>Select Option</option>
                            <option value="Default">Default</option>
                            <!-- <option value="Custom">Custom</option> -->
                            <option value="Reminder">Reminder</option>
                            <option value="Extension">Extension</option>
                          </select>
                        </div>
                      </div>

                      <div class="field" id="email_action">
                        <label style="font-weight: bold">Action *</label>
                        <div class="control">
                          <input type="text" class="input" name="action" v-model="email_notification.verb">
                        </div>
                      </div>

                      <div class="field" id="email_subject">
                        <label style="font-weight: bold">Subject *</label>
                        <div class="control">
                          <input type="text" class="input" name="subject" v-model="email_notification.subject">
                        </div>
                      </div>

                      <div class="field" id="email_message">
                        <label style="font-weight: bold">Message *</label>
                        <div class="control">
                          <textarea class="textarea" name="description" v-model="email_notification.content"></textarea>
                        </div>
                      </div>

                      <div class="field" id="email_files">
                        <label>Attach Files *</label>
                        <div class="control">
                          <input type="file" multiple name="files" @change="emailNotificationFiles($event)">
                        </div>
                      </div>

                      <div class="field">
                        <button type="submit" class="button is-block is-primary">Send</button>
                      </div>
                    </form>
                </div>
              </div>
            </div>

            <div class="columns" id="sms_notifications" style="display: none">
              <div class="column is-12">
                <div class="container">
                  <form @submit.prevent="send_sms_notification()">
                      <div class="field">
                        <label style="font-weight: bold">To *</label><br>
                        <div class="select is-fullwidth">
                          <select name="level" id="sms_to" @change="hideShowSmsTypeOptions($event)" required>
                            <option selected disabled>Select</option>
                            <option value="all">All</option>
                            <option value="potential">Potential</option>
                          </select>
                        </div>
                      </div>

                      <div class="field" id="sms_type" hidden>
                        <label style="font-weight: bold">Type *</label><br>
                        <div class="select is-fullwidth">
                          <select name="level" id="sms_type_select" @change="hideShowSmsContent()">
                            <option selected disabled>Select</option>
                            <option >Default</option>
                            <option >Custom</option>
                          </select>
                        </div>
                      </div>

                      <div class="field" id="sms_content">
                        <label style="font-weight: bold">Content *</label>
                        <div class="control">
                          <textarea class="textarea" name="description"></textarea>
                        </div>
                      </div>

                      <div class="field">
                        <button type="submit" class="button is-block is-primary">Send</button>
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
import tender from "@/services/company/tender";

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      columns: ['Category Title', 'Category Number', 'Status', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Number', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      tender: {},
      categories: [],
      broadcast_notification: {},
      email_notification: {},
      sms_notification: {},
      category_search_key: "",
    }
  },
  methods: {
    togglePotentialSelection(){
      let el = document.getElementById("email_to")
      if (el.value == "potential"){
        document.getElementById('potential_selection').style.display = "block"
      }else{
        document.getElementById('potential_selection').style.display = "none"
      }
    },
    
    hideShowSmsTypeOptions(){
      let el = document.getElementById("sms_to")
      if(el.value == "all"){
        document.getElementById('sms_content').style.display = "block"
        document.getElementById('sms_type').style.display = "none"
      }else if (el.value == "potential"){
        document.getElementById('sms_type').style.display = "block"
        document.getElementById('sms_content').style.display = "block"
      }else{
        document.getElementById('sms_content').style.display = "block"
        document.getElementById('sms_type').style.display = "none"
      }
    },
    hideShowSmsContent(){
      let el = document.getElementById("sms_type_select")
      if (el.value === "Default"){
        document.getElementById('sms_content').style.display = "none"
      }else{
        document.getElementById('sms_content').style.display = "block"
      }
    },
    toggleOtherFields(){
      let el = document.getElementById("email_potential_selection")

      if(el.value == "Default" || el.value == "Extension"){
        document.getElementById('email_action').style.display = "none"
        document.getElementById('email_subject').style.display = "none"
        document.getElementById('email_message').style.display = "none"
        document.getElementById('email_files').style.display = "none"

      }else if (el.value == "Reminder"){
        document.getElementById('email_subject').style.display = "none"
        document.getElementById('email_message').style.display = "none"
        document.getElementById('email_files').style.display = "none"
      }else{
        document.getElementById('email_action').style.display = "block"
        document.getElementById('email_subject').style.display = "block"
        document.getElementById('email_message').style.display = "block"
        document.getElementById('email_files').style.display = "block"
      }
    },
    emailNotificationFiles(event){
      console.log(event.target.files)
      this.email_notification['files'] = event.target.files
    },
    async send_broadcast_notification(){
      this.broadcast_notification['job_id'] = this.$route.params.id
      this.broadcast_notification['type_class'] = ''
      try{
        let response = await tender.send_broadcast_notification(this.$route.params.id, this.broadcast_notification)
        if (response.status == 200){
          this.broadcast_notification = {}
          this.closeModal()
          window.toast.fire({icon: 'success', title: 'Broadcast notifications have been initiated successfully'})
        }else{
          window.toast.fire({icon: 'error', title: 'An error occured! Please Try Again.'})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async send_email_notification(){
      let formData = new FormData();
      if(this.email_notification.files){
        formData.append("files", this.email_notification.files)
      }else{
        formData.append("files", null)
      }
      formData.append("level", this.email_notification.level)
      formData.append("to", this.email_notification.to)
      formData.append("verb", this.email_notification.verb)
      formData.append("subject", this.email_notification.subject)
      formData.append("content", this.email_notification.content)
      formData.append("potential_selection", this.email_notification.potential_selection)
      formData.append("job_id", this.$route.params.id)
      
      try{
        let response = await tender.send_job_email_notification(this.$route.params.id, formData)
        if (response.status == 200){
          this.email_notification = {}
          this.closeModal()
          window.toast.fire({icon: 'success', title: 'Email notifications have been initiated successfully'})
        }else{
          window.toast.fire({icon: 'error', title: 'An error occured! Please Try Again.'})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async send_sms_notification(){

      try{
        let response = await tender.send_job_sms_notification(this.$route.params.id, this.sms_notification)
        if (response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred! Please Try Again.'})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async uploadCategorySuppliers(event){
      let f = event.target.files[0]
      let form_data = new FormData()
      form_data.append('category_suppliers', f, f.name)

      try{
        let response = await tender.upload_category_suppliers(this.tender.id, form_data)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.$router.push(`/company/tender/cat/suppliers/progress/${this.tender.id}/${response.data['task_id']}`)
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
        // print(response.status)
        if (response.status === 200){
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
          this.template_url = ''+process.env.VUE_APP_DOWNLOAD_URL+response.data['filepath']
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
      if (this.category_search_key != ""){
        try {
          let response = await tender.category_search(this.$route.params.id, this.category_search_key, this.page, this.dataPerPage)
          this.categories = response.data['results']
          this.dataCount = response.data['count']
        } catch (err) {
          window.toast.fire({icon: 'error', title: err})
        }
      }else{
        this.getCategories()
      }
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
        let response = await tender.tender(this.$route.params.id)
        this.tender = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await tender.categories(this.$route.params.id, this.page, this.dataPerPage)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
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
        this.$router.push(`/company/tender/qa/instructions/${row.id}`)
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
        this.$router.push(`/company/tender/dd/details/${row.id}`)
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
      }).then((result) => {
        console.log("got here")
        if (result.isConfirmed) {
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
      }).then((result) => {
        console.log("got here")
        if (result.isConfirmed) {
          self.initiate_dd(row)
        }
      })
    },
    async confirmInviteEmail(){
      let self = this
      this.$swal.fire({
        title: 'Send Invite Email Notification',
        icon: 'info',
        html:
            'Are you sure you want to send invite emails for the whole job ??',
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
      }).then((result) => {
        console.log("got here")
        if (result.isConfirmed === true) {
          self.send_invite_email()
        }
      })
    },
    async confirmInviteSMS(){
      let self = this
      this.$swal.fire({
        title: 'Send SMS Invite Notification',
        icon: 'info',
        html:
            'Are you sure you want to send sms invites for the whole job ??',
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
      }).then((result) => {
        console.log("got here")
        if (result.isConfirmed === true) {
          self.send_invite_sms()
        }
      })
    },
    async send_invite_email(){
      try{
        let response = await tender.send_invite_email(this.$route.params.id)
        if (response.status == 200){
          window.toast.fire({icon: 'success', title: response.data["response_message"]})
        }else{
          window.toast.fire({icon: 'error', title: "An error occurred! Please Try Again."})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async send_invite_sms(){
      try{
        let response = await tender.send_invite_sms(this.$route.params.id)
        if (response.status == 200){
          window.toast.fire({icon: 'success', title: response.data["response_message"]})
        }else{
          window.toast.fire({icon: 'error', title: "An error occurred! Please Try Again."})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
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