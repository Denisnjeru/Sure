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
        <div class="column-details column is-4">
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Add Section</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">Section Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Translation Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.trans_name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Short Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.short_name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Description<span class="required">*</span></label>
                <div class="control">
                  <textarea class="input" v-model="form.description" required></textarea>
                </div>
              </div>

              <div class="field">
                <label class="label">Parent Section<span class="required">*</span></label>
                <div class="control">
                  <select v-model="form.parent_section" class="input" >
                    <option selected>Select Section</option>
                    <option v-for="section in sections" v-bind:key="section.id" :value="section.id">
                      {{ section.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="risk_submit">
                <button type="submit" class="button button-submit">
                  Create
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
  name: "CreateSection",
  data(){
    return{
      form: {
        "name": "",
        "trans_name": "",
        "short_name": "",
        "description": "",
        "parent_section": "",
        "category": this.$route.params.category_id
      },
      sections: [],
    }
  },
  methods: {
    async create(){
      try{
        await prequal.create_section(this.$route.params.category_id, this.form)
        window.toast.fire({icon: 'success', title: "Section created successfully"})
        this.$router.push(`/qed/prequalification/category/details/${this.$route.params.prequal_id}/${this.$route.params.category_id}`)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_defaults(){
      try {
        let response = await prequal.section_defaults(this.$route.params.category_id)
        this.sections = response.data['results']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_defaults()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>