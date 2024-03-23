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
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Add Due Diligence Question</p>
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
                        Create
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
import prequal from "@/services/company/prequal";

export default {
  name: "AddPerSupplierQuestion",
  data() {
    return {
      defaults: [],
      participant: [],
      form: {
        "question": "",
        "due_diligence_response": "",
      },
    }
  },
  methods: {
    async get_participant(){
      try{
        let response = await prequal.dd_participant(
            this.$route.params.category_id, this.$route.params.participant_id
        )
        this.participant = response.data
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async create() {
      this.form['due_diligence_supplier'] = this.participant.id
      try {
        await prequal.create_dd_supplier_question(
            this.form, this.$route.params.category_id, this.$route.params.participant_id
        )
        window.toast.fire({icon: 'success', title: "Due diligence question added successfully"})
        this.$router.push(
            `/company/prequal/dd/supplier/questions/${this.$route.params.category_id}/${this.$route.params.participant_id}`
        )
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_participant()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>