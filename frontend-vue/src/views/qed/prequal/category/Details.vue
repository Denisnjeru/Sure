<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Prequalification Jobs > {{ prequal.title }} > {{ category.name }}
            </span>

        <div class="page__head--links">
        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title: {{ prequal.title }} </p>
<!--            <p class="column-details__head&#45;&#45;desc">Fill in the required details</p>-->
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <p><strong>Sourcing Activity:</strong> Prequalification</p>
            <hr>
            <p><strong>Job Code:</strong> {{ prequal.unique_reference }}</p>
            <hr>
            <p v-if="prequal.is_open === true"><strong>Approval Status:</strong> Open</p>
            <p v-else><strong>Approval Status:</strong> Closed</p>
            <hr>
            <p><strong>Opening Date:</strong> {{ category.opening_date }}</p>
            <hr>
            <p><strong>Closing Date:</strong> {{ category.closing_date }}</p>
            <hr>
            <p><strong>Pass Mark:</strong> {{ category.pass_score }}%</p>
            <hr>
            <template v-if="category.has_participants === false && category.is_open === false">
                <div class="field">
                  <label class="label">Import Questions From Excel<span class="required"> *</span></label>
                  <a download="download" href="#" class="button is-primary">
                    <span><font-awesome-icon class="view__icon" icon="download"/> Questions Template</span>
                  </a>
                  <div class="control">
                    <br>
                    <input class="input" type="file">
                  </div>
                </div>
                <hr>
              </template>
          </div>

        </div>

        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Actions</p>
<!--            <p class="column-details__head&#45;&#45;desc">Category Actions </p>-->
<!--            <hr>-->
          </div>
          <!-- Form Details -->
          <div class="column-details__content">

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" @click="refreshScores()"
                   class="button is-primary is-block is-small">Refresh Scores</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" @click="openNotificationsModal"
                   class="button is-primary is-block is-small">Send Category Notifications</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns" v-if="category.invite_only === true">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <router-link
                    :to="'/qed/prequal/invited/suppliers/'+$route.params.prequal_id+'/'+$route.params.category_id"
                    class="button is-primary is-block is-small">Invited Suppliers</router-link>
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
            <span class="page__head--title column is-4">
               Sections
            </span>

            <div class="page__head--links column is-8" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">

                </div>
                <div class="column is-6">
                  <router-link :to="'/qed/prequal/create/section/' + prequal.id + '/' + category.id"
                               class="button is-primary is-block is-small">
                    Add Section
                  </router-link>
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
                  <input @input="section_search()" id="section_query" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="section_columns" :options="section_options" :data="sections">
                <p slot="Section" slot-scope="{row}">
                     {{ row.name }}
                </p>

                <p slot="#Qs" slot-scope="{row}">
                    <span> {{ row.question_count }}</span>
                </p>

                <span slot="Actions" slot-scope="{row}" class="is-justify-content-right">
                  <router-link to="#" class="button is-danger is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="trash-alt"/></p>
                  </router-link>

                  <router-link :to="'/qed/prequal/edit/section/'+prequal.id+'/'+category.id+'/'+row.id"
                               class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                  </router-link>

                  <router-link :to="'/qed/prequal/section/questions/' + row.id"
                               class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>
                  </router-link>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="section_data_count" v-model="section_page" :per-page="section_data_per_page" @paginate="getSections()">
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
                    <button type="button" class="button is-primary is-pulled-right is-small"
                            @click="close_category()" v-if="category.is_open === true">
                      Close Category
                    </button>

                    <template v-else>
                      <div class="columns">
                        <div class="column is-6">
<!--                          <router-link :to="'/qed/prequal/letters/'+prequal.id+'/'+category.id" class="button is-primary is-fullwidth" style="margin-right: 2px">-->
<!--                            Letters-->
<!--                          </router-link>-->
                        </div>

                        <div class="column is-6">
                          <button type="button" class="button is-primary is-small" @click="openModal">
                            Open Category
                          </button>
                        </div>
                      </div>
                  </template>

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
                  <template>
                    <span>{{ row.company_name }}</span>
                  </template>
                </span>

                <span slot="Contact" slot-scope="{row}">
                  <template>
                    <span> {{ row.contact_name }}</span>
                  </template>
                </span>

                <span slot="Actions" slot-scope="{row}" >
<!--                  <span class="actions__edit">-->
<!--                      <font-awesome-icon class="actions__icon" icon="pen-alt"/>-->
<!--                  </span>-->
<!--                  <span class="actions__delete">-->
<!--                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>-->
<!--                  </span>-->

                  <template v-if="category.is_open === false && category.has_qa_instance === true">
                     <router-link :to="'/qed/prequal/conduct/qa/'+ category.id +'/' + row.id"
                               class="button is-primary is-small">
                      <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Conduct QA</p>
                    </router-link>
                  </template>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getParticipants()">
              </pagination>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" id="open_prequal">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important;">
            <div class="columns">
              <div class="column is-6">
                <strong>Open Category</strong><br>
                <small>Fill in the required fields</small>
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
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
            <button class="button is-fullwidth is-primary" @click="open_category()">Submit</button>
          </section>
        </div>
      </div>

    <div class="columns">
      <div class="column is-12">
        <div class="modal" id="notifications">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head is-danger">
          <div class="columns">
            <div class="column is-6">
              <h5>Category Notifications</h5>
            </div>
            <div class="column is-6">
              <button class="delete is-pulled-right" @click="closeNotificationsModal" aria-label="close"></button>
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
                          <option value="Success">Success</option>
                          <option value="Info">Info</option>
                          <option value="Warning">Warning</option>
                          <option value="Error">Error</option>
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
                  <form @submit.prevent="send_email_notifications()">
                    <div class="field">
                      <label style="font-weight: bold">Level *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level" v-model="email_notification.level">
                          <option selected disabled>Select Level</option>
                          <option value="Success">Success</option>
                          <option value="Info">Info</option>
                          <option value="Warning">Warning</option>
                          <option value="Error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="type" id="type" v-model="email_notification.to" @change="toggleFieldsSelection()">
                          <option selected disabled>Select Type</option>
                          <option value="paid">Paid</option>
                          <option value="potential">Potential</option>
                          <option value="qualified"> Qualified </option>
                          <option value="unqualified"> Unqualified </option>
                          <option value="specific"> Specific </option>
                          <option value="responsive">Responsive</option>
                          <option value="non-responsive">Non-Responsive</option>
                        </select>
                      </div>
                    </div>

                    <div class="field" id="specific_bidder"  hidden>
                      <label style="font-weight: bold">Bidder *</label>
                      <div class="select is-multiple is-fullwidth">
                          <select multiple name="specific-bidder" v-model="email_notification.specific_bidders" id="specific-bidder">
                            <option v-for="participant in participants" v-bind:key="participant.id" :value="participant.email">{{ participant.company_name }}</option>
                          </select>
                      </div>
                    </div>

                    <div class="field" id="hidden_div_potential" hidden>
                      <label style="font-weight: bold">Type</label>
                      <div class="select is-fullwidth">
                          <select name="selection_potential" v-model="email_notification.selection_potential" id="selection_potential">
                              <option value="Default">Default</option>
                              <option value="Custom" selected="selected">Custom</option>
                              <option value="Reminder">Reminder</option>
                              <option value="Extension">Extension</option>
                          </select>
                      </div>
                    </div>

                    <div class="field" id="hidden_div_non_responsive" hidden>
                      <div class="select is-fullwidth">
                        <select name="nonresponsive_selection" v-model="email_notification.nonresponsive_selection"
                                id="nonresponsive_selection" style="max-width: 100%;" onchange="toggleFieldsNonresponsiveSelection()">
                            <option value="Custom" selected="selected">Custom</option>
                            <option value="Reminder">Reminder</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Action *</label>
                      <div class="control">
                        <input type="text" class="input" name="action" v-model="email_notification.verb">
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Subject *</label>
                      <div class="control">
                        <input type="text" class="input" v-model="email_notification.subject" name="subject">
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Message *</label>
                      <div class="control">
                        <textarea class="textarea" name="description" v-model="email_notification.content"></textarea>
                      </div>
                    </div>

                    <div class="field">
                      <label>Attach Files *</label>
                      <div class="control">
                        <input type="file" multiple name="files" @change="select_email_files" required>
                      </div>
                    </div>

                    <div class="field">
                      <button type="submit"  class="button is-block is-primary">Send</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>

            <div class="columns" id="sms_notifications" style="display: none">
              <div class="column is-12">
                <div class="container">
                  <form @submit.prevent="send_sms_notifications()">
                    <div class="field">
                      <label>To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level" @change="toggleFieldBidders($event)" v-model="sms_notification.to">
                          <option selected disabled>Select</option>
<!--                          <option value="allsms"> All </option>-->
<!--                          <option value="paidsms">Paid</option>-->
                          <option value="potentialsms">Potential</option>
<!--                          <option value="qualifiedsms"> Qualified </option>-->
<!--                          <option value="unqualifiedsms"> Unqualified </option>-->
<!--                          <option value="specificsms"> Specific </option>-->
                          <option value="responsivesms">Responsive</option>
                          <option value="non-responsivesms">Non-Responsive</option>
                        </select>
                      </div>
                    </div>

<!--                    <div class="field" id="sms_specific_bidder_div" hidden>-->
<!--                        <label>Bidder *</label>-->
<!--                        <div class="select is-fullwidth">-->
<!--                          <select id="specific-biddersms"  multiple>-->
<!--                            <option>Select participants</option>-->
<!--                            <option v-for="participant in participants" :value="participant.email" v-bind:key="participant.id">-->
<!--                              {{ participant.company_name }}</option>-->
<!--                        </select>-->
<!--                        </div>-->
<!--                    </div>-->

                    <div class="field" id="sms_type_div" hidden>
                      <label>Type *</label>
                      <div class="select is-fullwidth">
                        <select id="potential_selectionsms" style="max-width: 100%;" @change="toggleFieldSmsType($event)" v-model="sms_notification.type">
<!--                          <option value="Customsms" selected="selected">Custom</option>-->
                          <option value="Defaultsms" selected>Default</option>
                        </select>
                      </div>
                    </div>

                    <div class="field" id="sms_subject_div">
                      <label>Content *</label>
                      <div class="control">
                        <textarea class="textarea" name="description" v-model="sms_notification.content"></textarea>
                      </div>
                    </div>

                    <div class="field">
                      <button type="submit"  class="button is-block is-primary" style="width: 100%">Send</button>
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
import prequal from "@/services/qed/prequal";

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      section_page: 1,
      section_data_count: 0,
      section_data_per_page: 10,
      participant_columns: ['Company', 'Contact', 'Actions'],
      section_columns: ['Section', '#Qs', 'Actions'],
      participant_options: {
        sortable: ['Company',],
        perPageValues: [10],
        filterable: false,
      },
      section_options: {
        sortable: ['Section',],
        perPageValues: [10],
        filterable: false,
      },
      prequal: {},
      category: {},
      participants: [],
      sections: [],
      open_form: {
        "closing_date": ""
      },
      email_notification: {
        "files": "",
        "specific_bidders": []
      },
      sms_notification: {

      },
    }
  },
  methods: {
    select_email_files(){
      this.email_notification.files = event.target.files;
    },
    openNotificationsModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeNotificationsModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    async send_email_notifications(){
      let formData = new FormData();
      if(this.email_notification.files){
        formData.append("files", this.email_notification.files)
      }
      formData.append("level", this.email_notification.level)
      formData.append("to", this.email_notification.to)
      formData.append("specific_bidders", this.email_notification.specific_bidders)
      formData.append("selection_potential", this.email_notification.selection_potential)
      formData.append("nonresponsive_selection", this.email_notification.nonresponsive_selection)
      formData.append("verb", this.email_notification.verb)
      formData.append("subject", this.email_notification.subject)
      formData.append("content", this.email_notification.content)
      formData.append("level", this.email_notification.level)

      console.log(this.email_notification)
      console.log(formData)
      try{
        let response = await prequal.category_email_notifications(formData, this.prequal.id, this.category.id)
        if (response.status === 200){
          this.closeModal()
          this.email_notification = {
            "files": "",
            "specific_bidders": []
          }
          window.toast.fire({icon: 'success', title: 'Email notifications sent'})
        }else{
          window.toast.fire({icon: 'error', title: 'Error, try again!!'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async send_sms_notifications(){
      try{
        let response = await prequal.category_sms_notifications(this.sms_notification, this.prequal.id, this.category.id)
        if (response.status === 200){
          this.sms_notification = {}
          window.toast.fire({icon: 'success', title: 'Notifications sent successfully'})
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again!!'})
        }
        console.log(response)
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    toggleFieldsSelection(){
      let t = document.getElementById('type')
      if (t.value === 'potential') {
        document.getElementById('hidden_div_potential').style.display = 'block'
      // }else if(t.value === 'specific'){
      //   document.getElementById('specific_bidder').style.display = 'block'
      }else if(t.value === 'non-responsive'){
        document.getElementById('hidden_div_non_responsive').style.display = 'block'
      }else{
        document.getElementById('hidden_div_potential').style.display = 'none'
        document.getElementById('hidden_div_non_responsive').style.display = 'none'
      }
    },
    toggleFieldSmsType(event){
      let value = event.target.value
      let content_div = document.getElementById('sms_subject_div')
      if (value === "Defaultsms"){
            content_div.style.display = 'none'
        }
        else{
            content_div.style.display = 'block'
        }
    },
    toggleFieldBidders(event){
      let value = event.target.value
      if (value === 'potentialsms'){
        document.getElementById('sms_type_div').style.display = 'block'
      }else if (value === 'specificsms'){
        document.getElementById('sms_type_div').style.display = 'none'
        document.getElementById('sms_specific_bidder_div').style.display = 'block'
      }else{
        document.getElementById('sms_type_div').style.display = 'none'
        document.getElementById('sms_specific_bidder_div').style.display = 'none'
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
    openModal() {
      console.log('got here')
      document.getElementById('open_prequal').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('open_prequal').classList.remove('is-active');
    },

    async section_search() {
      this.sections = []
      let query = document.getElementById('section_query').value
      try{
        let response = await prequal.section_search(this.$route.params.category_id, query)
        if (response.status === 200){
          this.sections = response.data['results']
          this.section_data_count = response.data['count']
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred, please try again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    // async fetchData() {
    //   this.getSections()
    // },
    async getCategory() {
      try {
        let response = await prequal.category(this.$route.params.prequal_id, this.$route.params.category_id)
        this.category = response.data
        this.prequal = this.category.prequalification
        // this.dataPerPage = response.data['count']

      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getSections(){
      try{
        let response = await prequal.sections(this.$route.params.category_id, this.section_page)
        if (response.status === 200){
          this.sections = response.data['results']
          this.section_data_count = response.data['count']
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred, please try again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async getParticipants(){
      try{
        let response = await prequal.category_participants(this.$route.params.category_id, this.$route.params.prequal_id, this.page)
        if (response.status === 200){
          console.log(response.data)
          this.dataCount = response.data['count']
          this.participants = response.data['results']
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred while getting participants'})
        }
      }catch (e){
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async close_category(){
      try{
        let response = await prequal.close_category(this.prequal.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async open_category(){
      try{
        let response = await prequal.open_category(this.open_form, this.prequal.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.open_form.closing_date = ""
        this.closeModal()
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async refreshScores(){
      try{
        let response = await prequal.refresh_scores(
            this.$route.params.prequal_id, this.$route.params.category_id
        )
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: 'Score refresh started'})
          this.$router.push(
            `/company/prequal/category/refresh/scores/${this.$route.params.prequal_id}/${this.$route.params.category_id}/${response.data['task_id']}`
          )
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    }
  },
  mounted() {
    this.getCategory()
    this.getSections()
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
.VueTables__table tbody td {
    padding: 5px 24px;
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
   width: 560px; background-color: #ffffff !important; border-radius: 12px;
}
.modal{
  z-index: 9999;
}
.modal-card-head{
  background-color: #ffffff !important; display: block
}
hr{
  margin: 0rem 0 !important;
}
</style>