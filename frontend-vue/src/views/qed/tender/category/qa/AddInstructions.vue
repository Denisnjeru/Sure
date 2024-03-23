<template>
  <div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Job > Category > QualityAssurance > Instructions
            </span>

      <div class="page__head--links">

      </div>
    </div>

    <div class="page__content columns">

      <div class="column is-12 column-page" style="align-items: initial !important; padding: 12px 24px;!important;">
        <div class="table-search" style="padding: 0px 0px;!important;">
          <p class="table-search__instruction">
            Quality Assurance
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
                  <p>{{ question.question.description }}</p>
                </div>
                </a>

                <div :id="'collapsible-message-'+question.id" class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <form >
                      <div class="columns">
                        <div class="column is-12">
                          <div class="field">
                            <label>Verification Instructions</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_instructions(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_instructions(question.id)">Save</button>
                          </div>
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
  name: "AddInstructions",
  data() {
    return {
      sections: [],
      active_section: '',
      next_section: '',
      section_questions: ''
    }
  },
  methods: {
    async get_sections() {
      try {
        let response = await tender.qa_sections(this.$route.params.category_id)
        this.sections = response.data
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
        console.log(this.next_section)
      }else{
        this.next_section = ''
      }
      try {
        let response = await tender.qa_section_questions(this.$route.params.category_id, section.id)
        this.section_questions = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    go_to_next_section(){
      let n = document.getElementById('button_'+this.next_section.id)
      n.click()
    },
    async submit_instructions(question_id){
      let value = document.getElementById('instructions_'+question_id).value
      let content = {
        "question_id": question_id,
        "verification_instruction": value
      }
      try {
        await tender.submit_instructions(content, this.$route.params.category_id, question_id)
        window.toast.fire({icon: 'success', title: 'Instructions submitted'})
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }

      console.log(value)
    }

  },
  mounted() {
    this.get_sections()
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
.message-header{
    background-color: #073A82 !important;
}
</style>