<template>
<div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Prequalification > Category > Bid
            </span>

      <div class="page__head--links">
        <router-link :to="'/supplier/prequal/preview/'+$route.params.category_id" class="button is-primary is-small">
          Preview
        </router-link>
      </div>
    </div>

<!--    <p class="table-search__instruction">-->
<!--            Bid-->
<!--          </p>-->
    <div class="columns" style="margin-left: 10px; margin-right: 0px">
          <div class="column is-12">
            <div class="tabs is-toggle is-fullwidth" style="font-size: 12px !important;">
              <ul>
                <template v-for="section in sections">
                  <li  :class="active_section.id === section.id ? 'is-active': '' " v-bind:key="section.id" :id="'list_item_'+section.id" >
                    <a type="button" @click="get_questions(section)" :id="'button_'+section.id">
<!--                      <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>-->
                      <span >{{ section.name }}</span>
                    </a>
                  </li>
                </template>
              </ul>
            </div>
          </div>
        </div>

  <div class="columns" v-if="active_section !== ''" style="margin-left: 10px; margin-right: 0px">
          <div class="column is-12">

             <div class="tabs is-toggle is-fullwidth" style="font-size: 12px !important;">
              <ul>
                <li v-for="section in active_section.child_sections" :class="active_sub_section.id === section.id ? 'is-active': '' " v-bind:key="section.id" :id="'list_item_'+section.id">
                  <a type="button" @click="get_sub_section_questions(section, active_section.child_sections)" :id="'button_'+section.id">
<!--                    <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>-->
                    <span>{{ section.name }}</span>
                  </a>
                </li>
              </ul>
             </div>

          </div>
        </div>

    <div class="page__content columns">

      <div class="column is-12 column-page" id="to_scroll_top" style="align-items: initial !important; padding: 12px 24px;!important;">
<!--        <div class="table-search" style="padding: 0px 0px;!important;">-->

<!--          <hr>-->
<!--          <div class="table-search__search">-->
            <!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
            <!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
<!--          </div>-->
<!--        </div>-->

        <div class="columns" v-if="section_questions">
          <div class="column is-12" style="padding: 16px 24px;">
            <div id="accordion_second">
              <template v-if="active_section.name === 'Financial Ratios'">
                <article class="message" style="font-size: 12px !important;">
                  <a :href="'#collapsible-message-'+section_questions[0].id">
                    <div class="message-header">
                      <p>{{ section_questions[0].description }}</p>
                    </div>

                    <div class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                      <div class="message-body-content">
                        <button style="font-size: 12px !important;" class="button is-primary" @click="openModal">Click Here to Continue</button>
                      </div>
                    </div>
                  </a>
                </article>
              </template>

              <template v-if="active_section.name !== 'Financial Ratios'">
                <article style="font-size: 12px !important;" class="message" v-for="question in section_questions" v-bind:key="question.id">
                <a :href="'#collapsible-message-'+question.id">
                <div class="message-header">
                  <p>{{ question.description }}</p>
                </div>
                </a>

                <div :id="'collapsible-message-'+question.id" class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <form >
                      <div class="columns">
                        <div class="column is-12">
                          <div class="field">
                            <label>Response</label>
                            <template v-if="question.answer_type === 1">
                              <div class="control">
                                <input @focusout="submit_response(question)" type="text" class="input is-small"
                                       :id="'response_'+question.id" :value="question.response.options">
                              </div>
                            </template>

                            <template v-else-if="question.answer_type === 2">
                              <br>
                              <div class="select is-fullwidth is-small">
                                <select :id="'response_'+question.id" @focusout="submit_response(question)" v-model="question.response.options">
                                  <option selected disabled>Select from the choices below</option>
                                  <option v-for='option in question.marking_scheme.options.split(",")' v-bind:key="option" :value="option">{{ option }}</option>
                                </select>
                              </div>
                            </template>

                            <template v-else-if="question.answer_type === 3">
                              <div class="checkbox">
                                <label>
                                  <input v-for='option in question.marking_scheme.options.split(",")'
                                         v-bind:key="option" type="checkbox" class="input is-small" :id="'response_'+question.id"
                                         @focusout="submit_response(question)" :name="'response_'+question.id"
                                         :checked="question.response.options.includes(option) ? 'checked': '' ">
                                  Check box
                                </label>
                              </div>
                            </template>

                            <template v-else-if="question.answer_type === 4">
                              <div class="control">
                                <label>
                                  <input type="radio" class="radio is-primary" :name="'response_'+question.id"
                                         :checked="question.response.options === 'Yes' ? 'checked': ''" value="Yes"
                                         :id="'yes_response_'+question.id" @focusout="submit_response(question)"> Yes</label>
                                <br>
                                <label>
                                  <input type="radio" class="radio is-small" :name="'response_'+question.id"
                                              :checked="question.response.options === 'No' ? 'checked': ''" value="No"
                                              :id="'no_response_'+question.id" @focusout="submit_response(question)"> No</label>
                              </div>
                            </template>

                            <template v-else-if="question.answer_type=== 5">
                              <div class="control">
                                <input type="file" class="input is-small" :id="'response_'+question.id" @focusout="submit_response(question)">
                              </div>
                              <p>OR</p>
                              <div class="select is-fullwidth">
                                <select :id="'profile_response_'+question.id" @focusout="submit_profile_response(question)" v-model="question.response.options">
                                  <option selected disabled>Choose From Profile</option>
                                  <option v-if="supplier_profile.registration_cert_url" value="registration_cert_url">Registration Certificate</option>
                                  <option v-if="supplier_profile.kra_pin_url" value="kra_pin_url">KRA PIN Certificate</option>
                                  <option v-if="supplier_profile.kra_compliance_url" value="kra_compliance_url">Tax Compliance Certificate</option>
                                  <option v-if="supplier_profile.kra_trading_licence_url" value="kra_trading_licence_url">Trading License</option>
                                  <option v-if="supplier_profile.cr_12_document_url" value="cr_12_document_url">CR12 Document</option>
                                </select>
                              </div>

                              <div v-if="question.response.document_url" :id="'delete_button_'+question.id">
                                <p style="margin-top: 10px">
                                  <small>Current: {{ question.response.document_url }}</small>
                                  <button type="button" class="button is-small is-danger" @click="delete_response_file(question.id)" style="margin-left: 15px">Delete</button></p>
                                </div>
                            </template>

                            <template v-else-if="question.answer_type===6">
                              <div class="control">
                                <input type="number" class="input is-small" :id="'response_'+question.id"
                                       @focusout="submit_response(question)" :value="question.response.options">
                              </div>
                            </template>

                            <template v-else-if="question.answer_type===7">
                              <div class="control">
                                <input type="date" class="input is-small" :id="'response_'+question.id"
                                       @focusout="submit_response(question)" :value="question.response.options">
                              </div>
                            </template>

                            <template v-else-if="question.answer_type===8">
                              <textarea class="textarea is-small" rows="4"  :id="'response_'+question.id"
                                        @focusout="submit_response(question)" v-model="question.response.options"></textarea>
                            </template>

                          </div>

<!--                          <div class="field">-->
<!--                            <button type="button" class="button is-primary is-small is-pulled-right" >Save</button>-->
<!--                          </div>-->
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </article>
              </template>

              <template v-if="next_section !== ''">
                <button type="button" @click="go_to_next_section()" class="button is-primary is-small is-pulled-right">Next</button>
              </template>
              <template v-else>
                <div class="field">
                  <a href="#" @click="finish_bid()" type="button" class="button is-primary is-small is-pulled-right">Submit</a>
                </div>
              </template>
            </div>
          </div>
        </div>

      </div>
    </div>

  <div class="modal" id="ratios">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head is-danger" style="padding: 5px 20px; background-color: #DBE9FE !important; font-size: 12px !important;">
            <div class="columns">
              <div class="column is-6">
                <strong>Financial Ratios</strong><br>
                <small>Fill in the required fields</small>
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
              </div>
            </div>

          </header>
          <form @submit.prevent="submit_ratios()" style="overflow: auto; font-size: 12px">
          <section class="modal-card-body" style="padding: 2%;">
          <table class="table is-fullwidth">
            <thead>
              <tr>
                <th>Description</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th><label class="label">Equity *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.equity" required>
                    </div>
                  </div>
                </th>
                </tr>
              <tr><th><label class="label">Current Liabilities *</label></th>
              <th>
                <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.curr_liabilities" required>
                    </div>
                  </div>
              </th>
              </tr>
              <tr><th><label class="label">Fixed Assets *</label></th>
              <th>
                <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.fixed_assets" required>
                    </div>
                  </div>
              </th>
              </tr>
              <tr><th><label class="label">Current Assets *</label></th>
              <th>
                <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.current_assets" required>
                    </div>
                  </div>
              </th>
              </tr>
              <tr><th><label class="label">Long Term Loans(Debt) *</label></th>
              <th>
                <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             v-model="form.debtors" step="any" required>
                    </div>
                  </div>
              </th>
              </tr>
              <tr>
                <th><label class="label">Cash *</label></th>
              <th>
                <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.cash" required>
                    </div>
                  </div>
              </th>
              </tr>
              <tr>
                <th><label class="label">Turnover *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.turnover" required>
                    </div>
                  </div>
                </th>
                </tr>
              <tr>
                <th><label class="label">Gross Profit *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.gross_profit" required>
                    </div>
                  </div>
                </th>
                </tr>
              <tr>
                <th><label class="label">Net Profit *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="form.net_profit" required>
                    </div>
                  </div>
                </th>
                </tr>
            </tbody>
          </table>
          </section>

          <section class="modal-card-body">
            <button style="font-size: 12px !important;" type="submit" class="button is-fullwidth is-primary">Submit</button>
          </section>
          </form>
        </div>
      </div>

  </div>
</template>

<script>
import prequal from "@/services/supplier/prequal";
import supplier_prequal from "@/services/supplier/prequal";
import auth from "@/services/authentication/auth";
export default {
  name: "Bid",
  data() {
    return {
      form: {
        "equity": "",
        "curr_liabilities": "",
        "current_assets": "",
        "fixed_assets": "",
        "debtors": "",
        "turnover": "",
        "gross_profit": "",
        "net_profit": "",
        "cash": "",
        "section": ""
      },
      sections: [],
      active_section: '',
      active_sub_section: '',
      next_section: '',
      next_sub_section: '',
      section_questions: '',
      section_data:[],
      sub_section_data: [],
      supplier_profile: []
    }
  },
  methods:{
    openModal() {
      console.log('got here')
      document.getElementById('ratios').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('ratios').classList.remove('is-active');
    },
    upsert(array, element) { // (1)
      const i = array.findIndex(_element => _element.question === element.question);
      if (i > -1) array[i] = element; // (2)
      else array.push(element);
    },
    async delete_response_file(question_id){
      try{
        let response = await supplier_prequal.delete_response(question_id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        if(response.data['response_message'] === 'Response deleted successfully'){
          document.getElementById('delete_button_'+question_id).style.display = 'none';
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async submit_ratios(){
      try{
        this.form.section = this.active_section.id
        let response = await supplier_prequal.submit_ratios(this.active_section.id, this.form)
        if (response.status === 201){
          this.closeModal()
          window.toast.fire({icon: 'success', title: 'Ratios submitted successfully'})
        }else if(response.status === 200){
          window.toast.fire({icon: 'error', title: response.data['response_message']})
          this.$router.push('/supplier/prequal/ordered/categories')
        } else{
          window.toast.fire({icon: 'error', title: 'Error, Please Try Again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async submit_profile_response(question){
      let data = {
        "file_type": document.getElementById('profile_response_'+question.id).value
      }
      try{
        let response = await prequal.submit_profile_response(data, question.id)
        if (response.status === 201){
          window.toast.fire({icon: 'success', title: "Response saved"})
        }else{
          window.toast.fire({icon: 'error', title: "Response saving was not successful"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async submit_response(question){
      if (question.answer_type === 5){
        let file = document.getElementById('response_'+question.id).files[0];
        let form_data = new FormData()
        form_data.append("document_url", file, file.name)
        form_data.append("question", question.id)
        this.upsert(this.section_data, form_data)
        // .push(form_data)
        try{
          let response = await prequal.bid(question.id, form_data)
          if (response.status === 201) {
            window.toast.fire({icon: 'success', title: "File saved"})
          }else if(response.status === 200){
            window.toast.fire({icon: 'error', title: response.data['response_message']})
            this.$router.push('/supplier/prequal/ordered/categories')
          } else{
            window.toast.fire({icon: 'error', title: 'Error. Please Try Again'})
          }
        }catch (err){
          window.toast.fire({icon: 'error', title: err})
        }

      }else{
        let options = ''
        if (question.answer_type === 4){
          // let yes =
          if (document.getElementById('yes_response_'+question.id).checked){
            options = 'Yes'
          }else if(document.getElementById('no_response_'+question.id).checked){
            options = 'No'
          }else{
            options = ''
          }
        }else{
          options = document.getElementById('response_'+question.id).value
        }
        let question_response = {
          "question": question.id,
          "options": options,
        }
        this.upsert(this.section_data, question_response)
        try{
          let response = await prequal.bid(question.id, question_response)
          if (response.status === 201){
            window.toast.fire({icon: 'success', title: "Response saved"})
          }else if(response.status === 200){
            window.toast.fire({icon: 'error', title: response.data['response_message']})
            this.$router.push('/supplier/prequal/ordered/categories')
          } else{
            window.toast.fire({icon: 'error', title: response})
          }

        }catch (err){
          window.toast.fire({icon: 'error', title: err})
        }
      }
    },
    async get_sections() {
      try {
        let response = await prequal.bid_sections(this.$route.params.category_id)
        this.sections = response.data
        this.active_section = response.data[0]
        this.get_questions(response.data[0])
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_sub_section_questions(section, sections) {
      this.active_sub_section = section
      let active_section_index =  sections.indexOf(section)
      let next_section_index = active_section_index + 1
      if (this.sections.length > next_section_index ){
        this.next_sub_section = sections[next_section_index]
        document.getElementById('to_scroll_top').scrollTop = 0;
        // console.log(this.next_section)
      }else{
        this.next_section = ''
      }
      try {
        let response = await prequal.bid_questions(section.id)
        this.section_questions = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_questions(section) {
      this.active_sub_section = ""
      this.next_sub_section = ""
      this.active_section = section
      let active_section_index =  this.sections.indexOf(section)
      let next_section_index = active_section_index + 1
      if (this.sections.length > next_section_index ){
        this.next_section = this.sections[next_section_index]
        document.getElementById('to_scroll_top').scrollTop = 0;
        // console.log(this.next_section)
      }else{
        this.next_section = ''
      }
      try {
        let response = await prequal.bid_questions(section.id)
        this.section_questions = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    go_to_next_sub_section(){
      // submit whole section data
      console.log(this.section_data)
      this.sub_section_data = []
      let n = document.getElementById('button_'+this.next_sub_section.id)
      n.click()
    },
    go_to_next_section(){
      if (this.next_sub_section){
        this.go_to_next_sub_section()
      }else{
        // submit whole section data
        console.log(this.section_data)
        this.section_data = []
        let n = document.getElementById('button_'+this.next_section.id)
        n.click()
      }
    },
    async finish_bid(){
      try {
        let response = await prequal.finish_bid(this.$route.params.category_id)
        if (response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.$router.push('/supplier/prequal/ordered/categories')
        }else{
          window.toast.fire({icon: 'error', title: 'An error occurred during submission'})
        }
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_supplier_profile(){
      try{
        let response = await auth.companyProfile()
        if(response.status === 200){
          this.supplier_profile = response.data
          console.log(this.supplier_profile)
        }else {
          window.toast.fire({icon: 'error', title: 'An error occurred while getting your profile information, please try again.'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
  },
  mounted() {
    this.get_sections()
    this.get_supplier_profile()
  },
  created() {
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
  margin: 0 !important;
  @include grid_column;
}

.is-primary {
  background-color: #073A82 !important;
}
.tabs a{
  color: #073A82;
  background: #F2F7FF;
}
li.is-active a{
  background-color: #073A82 !important;
  border-color: #073A82 !important;
  color: #fff;
  z-index: 1;
}
.message-header{
    background-color: #073A82 !important;
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
label{
  font-size: 12px !important;
}
</style>