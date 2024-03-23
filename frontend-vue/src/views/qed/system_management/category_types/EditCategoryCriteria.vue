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
          <div class="column-details__head">
              <p class="column-details__head--title">Edit Category Type Criteria</p>
              <p class="column-details__head--desc">Fill in the required details</p>
          </div>

          <div class="column-details__content">
            <form @submit.prevent="updateCategoryCriteria()">
              <div class="field">
                <label class="label">Category Type <span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="criteria.category_type.name" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Category Type Code <span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="criteria.category_type.innitials" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Country<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="criteria.criteria_country.name" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Evaluation Criteria File<span class="required"> *</span></label>
                <a class="button is-small is-primary is-pulled-right" download="download" :href="criteria.file_url">Current Template </a>
                <br>
                <div class="control">
                  <input class="input" type="file" @change="selectFile($event)">
                </div>
              </div>

              <div class="field">
                <button type="submit" class="button is-primary">Submit</button>
              </div>
            </form>
          </div>

        </div>
      </div>
    </div>
</div>
</template>

<script>
import category_types from "@/services/qed/category_types";

export default {
  name: "EditCategoryCriteria",
  data(){
    return{
      criteria: {},
      backend_url: process.env.VUE_APP_DOWNLOAD_URL,
      form: {
        'criteria_country': '',
        'category_type': '',
        'file_url': ''
      }
    }
  },
  methods:{
    selectFile(event){
      this.form.file_url = event.target.files[0]
    },
    async getCategoryTypeCriteria(){
      try{
        let response = await category_types.category_type_criteria(this.$route.params.criteria_id)
        if (response.status){
          this.criteria = response.data
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },

    async updateCategoryCriteria(){
      let form_data = new FormData();
      if (this.form.file_url) {
        form_data.append("file_url", this.form.file_url, this.form.file_url.name)
      }
      form_data.append("criteria_country", this.criteria.criteria_country.id);
      form_data.append("category_type", this.criteria.category_type.id);
      console.log(this.form)
      try{
        let response = await category_types.update_category_type_criteria(this.$route.params.criteria_id, form_data)
        if (response.status === 200){
          window.toast.fire({icon: 'success', title: 'Criteria updated'})
          this.$router.push(`/qed/category/type/${this.$route.params.category_type_id}`)
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    }
  },
  mounted() {
    this.getCategoryTypeCriteria()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.is-primary {
  background-color: #073A82 !important;
}
</style>