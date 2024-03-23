<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Tender Jobs > {{ tender.title }} > {{ category.name }} > Technical Details
            </span>

        <div class="page__head--links">
          <router-link class="button is-primary is-small" :to="'/company/tender/financial/details/'+tender.id+'/'+category.id">
            Financial Details
          </router-link>
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
            <p v-if="tender.is_open === true"><strong>Approval Status:</strong> Open</p>
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
                  <a download="download" :href="category.question_template" class="button is-primary is-small">
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
                <a href="#" @click="refresh_scores()" class="button is-primary is-block is-small">Refresh Scores</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" @click="openNotificationsModal" class="button is-primary is-block is-small">Send Category Notifications</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns" v-if="category.invite_only === true">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <router-link
                    :to="'/company/tender/invited/suppliers/'+$route.params.tender_id+'/'+$route.params.category_id"
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
               Question Sections
            </span>

            <div class="page__head--links column is-8" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">

                </div>
                <div class="column is-6">
                  <router-link :to="'/company/tender/create/section/' + tender.id + '/' + category.id" 
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
                  <input @keyup.enter="section_search()" id="section_query" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="section_columns" :options="section_options" :data="sections">
                <span slot="Section" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

                <span slot="#Qs" slot-scope="{row}">
                    <span> {{ row.question_count }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <span class="actions__delete">
                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>
                  </span>

                  <router-link :to="'/company/tender/edit/section/'+tender.id+'/'+category.id+'/'+row.id"
                               class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                  </router-link>

                  <router-link :to="'/company/tender/section/questions/' + row.id"
                               class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>
                  </router-link>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="sectionDataCount" v-model="sectionPage" :per-page="sectionDataPerPage" @paginate="getSections()">
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
                    <button type="button" class="button is-primary is-pulled-right is-small" @click="close_category()" v-if="category.is_open === true">
                      Close Category
                    </button>

                    <template v-else>
                      <div class="columns">
                        <div class="column is-6">
<!--                          <router-link :to="'/company/tender/letters/'+tender.id+'/'+category.id" class="button is-primary is-fullwidth" style="margin-right: 2px">-->
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
                  <input @keyup.enter="searchParticipants()" id="participants_query" class="table-search__search--input" type="text"
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

                <span slot="Actions" slot-scope="{row}">
<!--                  <span class="actions__edit">-->
<!--                      <font-awesome-icon class="actions__icon" icon="pen-alt"/>-->
<!--                  </span>-->
<!--                  <span class="actions__delete">-->
<!--                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>-->
<!--                  </span>-->

                  <template v-if="category.is_open === false && category.has_qa_instance === true">
                     <router-link :to="'/company/tender/conduct/qa/'+ category.id +'/' + row.id"
                               class="button is-primary is-small">
                      <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Conduct QA</p>
                    </router-link>
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

    <div class="modal" id="open_tender">
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
                      <label style="font-weight: bold">To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="type">
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

                    <div class ="hidden_div"  hidden>
                        <label>Bidder *</label>
                        <select name="specific-bidder" id="specific-bidder" multiple>
                          <option v-for="participant in participants" v-bind:key="participant.id" :value="participant.email">{{ participant.company_name }}</option>
                        </select>
                    </div>

                    <div class="select" id="hidden_div_potential" hidden>
                        <label>Type</label>
                        <select name="selection_potential" id="selection_potential"  onchange="toggleFieldsSelection()">
                            <option value="Default">Default</option>
                            <option value="Custom" selected="selected">Custom</option>
                            <option value="Reminder">Reminder</option>
                            <option value="Extension">Extension</option>
                        </select>
                    </div>

                    <div class="select" id="hidden_div_non_responsive" hidden>
                        <select name="nonresponsive_selection" id="nonresponsive_selection" style="max-width: 100%;" onchange="toggleFieldsNonresponsiveSelection()">
                            <option value="Custom" selected="selected">Custom</option>
                            <option value="Reminder">Reminder</option>
                        </select>
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
      sectionPage: 1,
      sectionDataCount: 0,
      sectionDataPerPage: 10,
      participant_columns: ['Company', 'Contact', 'Actions'],
      section_columns: ['Section', '#Qs', 'Actions'],
      participant_options: {
        sortable: ['Company',],
        perPageValues: [20],
        filterable: false,
      },
      section_options: {
        sortable: ['Section',],
        perPageValues: [20],
        filterable: false,
      },
      tender: {},
      category: {},
      participants: [],
      sections: [],
      open_form: {
        "closing_date": ""
      },
    }
  },
  methods: {
    openNotificationsModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeNotificationsModal() {
      document.getElementById('notifications').classList.remove('is-active');
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
      document.getElementById('open_tender').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('open_tender').classList.remove('is-active');
    },
    
    async fetchData() {
      console.log(this.page);
    },
    async getCategory() {
      try {
        let response = await tender.category(this.$route.params.tender_id, this.$route.params.category_id)
        this.category = response.data
        this.tender = this.category.tender
        // this.participants = response.data['participants']
        console.log(response.data.participants)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getSections(){
      console.log(this.sectionPage)
      try{
        let response = await tender.sections(this.$route.params.category_id, this.sectionPage, this.sectionDataPerPage)
        this.sectionDataCount = response.data['count']
        this.sections = response.data['results']
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async section_search() {
      this.sections = []
      this.sectionPage = 1
      let query = document.getElementById('section_query').value
      try{
        let response = await tender.section_search(this.$route.params.category_id, query, this.sectionPage, this.sectionDataPerPage)
        if (response.status === 200){
          this.sections = response.data['results']
          this.sectionDataCount = response.data['count']
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred, please try again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async refresh_scores(){
      try{
        let response = await tender.refresh_category_scores(this.$route.params.tender_id, this.$route.params.category_id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Category score evaluation started"})
          let task_id = response.data['task_id']
          this.$router.push(
            `/company/tender/category/refresh/scores/${this.$route.params.tender_id}/${this.$route.params.category_id}/${task_id}`)
        }else{
          window.toast.fire({icon: 'error', title: "An error occured! Please Try Again."})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    // async getSections() {
    //   try {
    //     let response = await tender.sections(this.$route.params.tender_id, this.$route.params.category_id)
    //     this.dataCount = response.data['count']
    //     this.sections = this.category.sections
    //   } catch (err) {
    //     window.toast.fire({icon: 'error', title: err})
    //   }
    // },
    async getParticipants() {
      try {
        let response = await tender.technical_bidders(
          this.$route.params.tender_id, this.$route.params.category_id, this.page, this.dataPerPage)
        this.dataCount = response.data['count']
        this.participants = response.data['results']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async searchParticipants(){
      try{
        let query = document.getElementById('participants_query').value
        let response = await tender.search_technical_bidders(
          this.$route.params.tender_id, this.$route.params.category_id, this.page, query, this.dataPerPage) 
        this.dataCount = response.data['count']
        this.participants = response.data['results']
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async close_category(){
      try{
        let response = await tender.close_category(this.tender.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async open_category(){
      try{
        let response = await tender.open_category(this.open_form, this.tender.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.open_form.closing_date = ""
        this.closeModal()
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
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

.page__head{
  padding: 1px 30px;
}
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
  padding-top: 1px;
}

.page .table-search[data-v-e49b950c] {
    padding: 12px 6px
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
.VueTables__table tbody td {
    padding: 5px 24px;
}
hr{
  margin: 0.5rem 0 !important;
}
</style>