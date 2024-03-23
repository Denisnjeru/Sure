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
          <form v-on:submit.prevent="update()">
            <div class="column-details__head">
              <p class="column-details__head--title">Edit Job </p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">Job Title <span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.title">
                </div>
              </div>
              <div class="field">
                <label class="label">Job Code<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.unique_reference">
                </div>
              </div>

              <div class="field">
                <label class="label">Advert<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectAdvert($event)">
                </div>
                <p><small>Current: </small>{{ prequal.advert }}</p>
              </div>

              <div class="field">
                <label class="label">Current Suppliers<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectCurrentSuppliers($event)">
                </div>
                <p><small>Current: </small>{{ prequal.current_suppliers }}</p>
              </div>

              <div class="field">
                <label class="label">Bidding Instructions<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectBiddingInstructions($event)">
                </div>
                <p><small>Current: </small>{{ prequal.bidding_instructions }}</p>
              </div>

              <div class="field">
                <div class="control">
                  <label class="checkbox">
                    <input type="checkbox" v-model="form.show_bids">
                    <strong> Show supplier bids </strong>
                  </label>
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
import prequal from "@/services/company/prequal";

export default {
  name: "Edit",
  data(){
    return{
      form: {
        "title": "",
        "unique_reference": "",
        "show_bids": "",
        "advert": "",
        "current_suppliers": "",
        "bidding_instructions": ""
      },
      prequal: {},
    }
  },
  methods: {
    async update(){
      let form_data = new FormData();
      if (this.form.advert) {
        form_data.append("advert", this.form.advert, this.form.advert.name)
      }
      if (this.form.current_suppliers) {
        form_data.append("current_suppliers", this.form.current_suppliers, this.form.current_suppliers.name)
      }
      if (this.form.bidding_instructions) {
        form_data.append("bidding_instructions", this.form.bidding_instructions, this.form.bidding_instructions.name)
      }
      form_data.append("title", this.form.title);
      form_data.append("unique_reference", this.form.unique_reference);
      form_data.append("show_bids", this.form.show_bids);

      try{
        let response = await prequal.update(this.$route.params.id,form_data)
        window.toast.fire({icon: 'success', title: "Prequalification job created successfully"})
        this.$router.push(`/company/prequalification/details/${response.data['id']}`)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    selectAdvert(event){
      this.form.advert = event.target.files[0]
    },
    selectCurrentSuppliers(event){
      this.form.current_suppliers = event.target.files[0]
    },
    selectBiddingInstructions(event){
      this.form.bidding_instructions = event.target.files[0]
    },
    async get_prequal(){
      try{
        let response = await prequal.prequal(this.$route.params.id)
        this.prequal = response.data
        this.form.title = response.data['title']
        this.form.unique_reference = response.data['unique_reference']
        this.form.show_bids = response.data['show_bids']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_prequal()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
</style>