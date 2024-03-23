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
              <p class="column-details__head--title">Edit Category Type</p>
              <p class="column-details__head--desc">Fill in the required details</p>
          </div>

          <div class="column-details__content">
            <form @submit.prevent="updateCategoryType()">
              <div class="field">
                <label class="label">Category Type Name <span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.name">
                </div>
              </div>

              <div class="field">
                <label class="label">Category Type Code <span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.innitials">
                </div>
              </div>

              <div class="field">
                <label class="label">Grouping<span class="required">*</span></label>
                <div class="select is-fullwidth">
                  <select v-model="form.category_group">
                    <option>Select Category Group</option>
                    <option v-for="category_group in category_groups" :value="category_group.id" v-bind:key="category_group.id">
                      {{ category_group.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="field">
                <button type="submit" class="button is-primary">Update</button>
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
  name: "EditCategoryType",
  data(){
    return{
      category_groups: [],
      category_type: {},
      form: {
        'name': '',
        'innitials': '',
        'category_group': ''
      }
    }
  },
  methods: {
    async updateCategoryType(){
      try{
        let response = await category_types.update_category_type(this.form, this.category_type.id)
        console.log(response.status)
        if (response.status === 200){
          this.$router.push(`/qed/category/types`)
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again!!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategoryGroup(){
      try{
        let response = await category_types.category_groups()
        if (response.status === 200){
          this.category_groups = response.data['results']
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again!!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategoryType(){
      try{
        let response = await category_types.category_type(this.$route.params.category_type_id)
        console.log(response.status)
        if (response.status === 200){
          this.category_type = response.data
          this.form.name = response.data['name']
          this.form.innitials = response.data['innitials']
          this.form.category_group = response.data['category_group'].id
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getCategoryType()
    this.getCategoryGroup()
  }
}
</script>

<style lang="scss" scoped>
@include page;
</style>