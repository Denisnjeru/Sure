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
              <p class="column-details__head--title">Add Category Type Criteria</p>
              <p class="column-details__head--desc">Fill in the required details</p>
          </div>

          <div class="column-details__content">
            <form @submit.prevent="createCategoryCriteria()">
              <div class="field">
                <label class="label">Category Type <span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="category_type.name" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Category Type Code <span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="category_type.innitials" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Country<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="location.name" disabled readonly>
                </div>
              </div>

              <div class="field">
                <label class="label">Evaluation Criteria File<span class="required"> *</span></label>
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
  name: "CreateCategoryCriteria",
  data(){
    return{
      location: {},
      category_type: {},
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
    async getLocation(){
      try{
        let response = await category_types.location(this.$route.params.location_id)
        if (response.status){
          this.location = response.data
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategoryType(){
      try{
        let response = await category_types.category_type(this.$route.params.category_type_id)
        if (response.status){
          this.category_type = response.data
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },

    async createCategoryCriteria(){
      let form_data = new FormData();
      if (this.form.file_url) {
        form_data.append("file_url", this.form.file_url, this.form.file_url.name)
      }
      form_data.append("criteria_country", this.location.id);
      form_data.append("category_type", this.category_type.id);
      console.log(this.form)
      try{
        let response = await category_types.create_category_type_criteria(form_data)
        if (response.status === 201){
          window.toast.fire({icon: 'success', title: 'Criteria updated'})
          this.$router.push(`/qed/category/type/${this.category_type.id}`)
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    }
  },
  mounted() {
    this.getLocation()
    this.getCategoryType()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.is-primary {
  background-color: #073A82 !important;
}
</style>