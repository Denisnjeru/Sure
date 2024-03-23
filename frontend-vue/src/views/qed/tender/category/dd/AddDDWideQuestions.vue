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
              <p class="column-details__head--desc">This question will be added to all participants.</p>
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
import tender from "@/services/qed/tender";

export default {
  name: "AddDDWideQuestions",
  data() {
    return {
      defaults: [],
      participant: [],
      form: {
        "question": "",
      },
    }
  },
  methods: {
    async create() {
      try {
        await tender.create_dd_wide_question(
            this.form, this.$route.params.category_id
        )
        window.toast.fire({icon: 'success', title: "Due diligence question added successfully"})
        this.$router.push(
            `/qed/tender/dd/details/${this.$route.params.category_id}`
        )
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>