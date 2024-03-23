<template>
<div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Job > Category > QualityAssurance > Participant
            </span>

      <div class="page__head--links">
      </div>
    </div>

    <div class="page__content columns">

      <div class="column is-12 column-page" style="align-items: initial !important; padding: 12px 24px;!important;">
        <div class="table-search" style="padding: 0px 0px;!important;">
          <p class="table-search__instruction">
            Conduct Quality Assurance
          </p>
          <hr>
          <div class="table-search__search">
            <!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
            <!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
          </div>
        </div>

        <div class="columns">
          <div class="column is-12">
            <div class="tabs is-toggle is-fullwidth" >
              <ul>
                <li  :class="active_section.id === section.id ? 'is-active': '' " v-for="section in sections" v-bind:key="section.id" :id="'list_item_'+section.id">
                  <a type="button" @click="get_questions(section)" :id="'button_'+section.id">
                    <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
                    <span>{{ section.name }}</span>
                  </a>
                </li>
              </ul>
            </div>

          </div>
        </div>

        <div class="columns" v-if="section_questions">
          <div class="column is-12" style="padding: 16px 24px;">
            <div id="accordion_second">

              <article class="message" v-for="question in section_questions" v-bind:key="question.id">
                <a :href="'#collapsible-message-'+question.id">
                <div class="message-header">
                  <p>Question: {{ question.question.description }}</p>
                </div>
                </a>

                <div :id="'collapsible-message-'+question.id" class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">
                        <div class="column is-4">
                          <div class="field">
                            <label>Document Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)" v-model="question.qa_question_response.number"/>
                            </div>
                          </div>

                          <div class="field">
                            <label>Document Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object data="https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a href="https://media.readthedocs.org/pdf/django/2.2.x/django.pdf">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </article>

              <template v-if="next_section !== ''">
                <button type="button" @click="go_to_next_section()" class="button is-primary is-small is-pulled-right">Next</button>
              </template>
              <template v-else>
                <div class="field">
                  <router-link :to="'/qed/tender/category/details/'+sections[0].tender_id+'/'+$route.params.category_id" type="button" class="button is-primary is-small is-pulled-right">Finish</router-link>
                </div>
              </template>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/qed/tender";

export default {
  name: "ConductQa",
  data() {
    return {
      sections: [],
      active_section: '',
      next_section: '',
      section_questions: ''
    }
  },
  methods: {
    hide_show_qa_score_field(event, question){
      let element = event.target
      let value = element.value
      if (value === 'Subjective'){
        document.getElementById('score_after_qa_field_'+question.id).style.display = 'block'
      }else{
        document.getElementById('score_after_qa_field_'+question.id).style.display = 'none'
      }
    },
    async get_sections() {
      try {
        let response = await tender.qa_sections(this.$route.params.category_id)
        this.sections = response.data
        this.active_section = response.data[0]
        this.get_questions(response.data[0])
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    async get_questions(section) {
      this.active_section = section
      let active_section_index =  this.sections.indexOf(section)
      let next_section_index = active_section_index + 1
      if (this.sections.length > next_section_index ){
        this.next_section = this.sections[next_section_index]
      }else{
        this.next_section = ''
      }
      try {
        let response = await tender.qa_section_questions_supplier_response(
            this.$route.params.category_id, section.id, this.$route.params.participant_id
        )
        this.section_questions = response.data['qa_questions']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    go_to_next_section(){
      let n = document.getElementById('button_'+this.next_section.id)
      n.click()
    },
    async submit_qa_response(question){
      let date = document.getElementById('document_date_'+question.id).value
      let content = {
        'number': document.getElementById('document_number_'+question.id).value,
        'outcome': document.getElementById('document_outcome_'+question.id).value,
        'date': date ? date : null,
        'score_after_qa': document.getElementById('document_score_after_qa_'+question.id).value,
        'supplier': this.$route.params.participant_id,
        'quality_assurance_question': question.id,
        'comment': document.getElementById('document_comment_'+question.id).value,
      }
      console.log(content)
      try {
        await tender.submit_qa_question_response(content, this.$route.params.category_id, question.id)
        window.toast.fire({icon: 'success', title: 'Response submitted'})
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_sections()
    // this.active_section = this.sections[0]
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

li.is-active a{
  background-color: #073A82 !important;
  border-color: #073A82 !important;
  color: #fff;
  z-index: 1;
}
.message-header {
    background-color: #073A82 !important;
}

</style>