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
        <div class="column-details column is-6">
          <form v-on:submit.prevent="update()">
            <div class="column-details__head">
              <p class="column-details__head--title">Update Due Diligence Question</p>
              <p class="column-details__head--desc">Supplier: {{ participant.supplier.company_name }}</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">

              <div class="columns">
                <div class="column is-12">
                  <div class="field">
                    <label class="label">Question<span class="required"> *</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="form.question" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Response<span class="required"> *</span></label>
                    <div class="control">
                      <textarea class="textarea" v-model="form.due_diligence_response" required></textarea>
                    </div>
                  </div>

                  <div class="field">
                    <div class="risk_submit">
                      <button type="submit" class="button button-submit">
                        Update
                      </button>
                    </div>
                  </div>

                </div>
              </div>


            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/qed/tender";

export default {
  name: "ConductDD",
  data() {
    return {
      defaults: [],
      participant: [],
      dd_question: [],
      form: {
        "question": "",
        "due_diligence_response": "",
      },
    }
  },
  methods: {
    async dd_question_response(){
      try{
        let response = await tender.dd_participant_question_response(
            this.$route.params.category_id, this.$route.params.participant_id, this.$route.params.question_id
        )
        this.participant = response.data['participant']
        this.dd_question = response.data['question']
        this.form.question = response.data['question'].question
        this.form.due_diligence_response = response.data['question'].due_diligence_response
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async update() {
      this.form['due_diligence_supplier'] = this.participant.id
      try {
        await tender.update_dd_supplier_question(
            this.form, this.$route.params.category_id, this.$route.params.participant_id, this.$route.params.question_id
        )
        window.toast.fire({icon: 'success', title: "Due diligence question updated successfully"})
        this.$router.push(
            `/qed/tender/dd/supplier/questions/${this.$route.params.category_id}/${this.$route.params.participant_id}`
        )
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.dd_question_response()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>