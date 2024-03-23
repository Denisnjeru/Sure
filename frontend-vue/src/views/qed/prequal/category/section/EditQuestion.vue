<template>
  <div class="risk-job-add">
    <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left"/>  <span class="text">Back</span>
                </span>
            </span>
    </div>
    <div class="page__content">
      <div class="columns is-centered">
        <div class="column-details column is-5">
          <form v-on:submit.prevent="update()">
            <div class="column-details__head">
              <p class="column-details__head--title">Edit Question</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">What is the question?<span class="required"> *</span></label>
                <div class="control">
                  <textarea class="input" type="text" v-model="form.description"></textarea>
                </div>
              </div>

              <div class="field">
                <label class="label">Question short description?<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.trans_description">
                </div>
              </div>

              <div class="field">
                <label class="label">Type of response<span class="required"> *</span></label>
                <div class="control">
                  <select v-model="form.answer_type" class="input" @change="toggle_options">
                    <option selected>Select type of response</option>
                    <option value="1">Text</option>
                    <option value="2">Selection</option>
                    <option value="3">Checkbox</option>
                    <option value="4">True/False</option>
                    <option value="5">File Upload</option>
                    <option value="6">Number</option>
                    <option value="7">Date</option>
                  </select>
                </div>
              </div>

              <div class="field" id="max_score">
                <label class="label">Max score<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="number" step="any" v-model="form.max_score">
                </div>
              </div>

              <div class="field" id="question_options">
                <label class="label">Set Options<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.options" placeholder="1-10, 11-20">
                </div>
              </div>

              <div class="field" id="score_options">
                <label class="label">Set Scores<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.score" placeholder="1, 5">
                </div>
              </div>

              <div class="columns">
                <div class="column">
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_required">
                        <strong> Bidders must answer </strong>
                      </label>
                    </div>
                  </div>

                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_qa">
                        <strong> Goes through QA </strong>
                      </label>
                    </div>
                  </div>
                </div>

                <div class="column">
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_dd">
                        <strong> Goes through DD </strong>
                      </label>
                    </div>
                  </div>

                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_scored" @change="toggle_max_score">
                        <strong> Response is scored </strong>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div class="risk_submit">
                <button type="submit" class="button button-submit">
                  Update
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import prequal from "@/services/qed/prequal";

export default {
  name: "EditQuestion",
  data() {
    return {
      form: {
        "description": "",
        "trans_description": "",
        "section": this.$route.params.section_id,
        "answer_type": "",
        "is_required": "",
        "max_score": "",
        "is_scored": "",
        "is_qa": "",
        "is_dd": "",
        "options": "",
        "score": "",
      },
      question: {},
    }
  },
  methods: {
    toggle_max_score(){
      console.log(this.form.is_scored)
      if(this.form.is_scored === true){
        document.getElementById('max_score').style.display = 'block'
      }else if(this.form.is_scored === false){
        document.getElementById('max_score').style.display = 'none'
      }else{
        document.getElementById('max_score').style.display = 'none'
      }
    },
    toggle_options(){
      console.log(this.form.answer_type)
      if (parseInt(this.form.answer_type) === 2){
        document.getElementById('score_options').style.display = 'block'
        document.getElementById('question_options').style.display = 'block'
      }else{
        document.getElementById('score_options').style.display = 'none'
        document.getElementById('question_options').style.display = 'none'
      }
    },
    async update() {

      try {
        await prequal.update_question(this.form, this.$route.params.section_id, this.question.id)
        window.toast.fire({icon: 'success', title: "Question created successfully"})
        this.$router.push(`/qed/prequal/section/questions/${this.$route.params.section_id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_question(){
      try {
        let response = await prequal.question(this.$route.params.section_id, this.$route.params.id)
        this.question = response.data
        this.form.description = response.data['description']
        this.form.trans_description = response.data['trans_description']
        this.form.answer_type = response.data['answer_type']
        this.form.is_required = response.data['is_required']
        this.form.is_scored = response.data['is_scored']
        this.form.is_qa = response.data['is_qa']
        this.form.is_dd = response.data['is_dd']
        this.form.max_score = response.data['max_score']
        this.form.options = response.data['options']
        this.form.score = response.data['score']
        this.toggle_max_score()
        this.toggle_options()
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_question()
  },
  created() {
    // this.toggle_max_score()
    // this.toggle_options()
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>