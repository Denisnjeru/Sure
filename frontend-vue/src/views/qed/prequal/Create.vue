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
              <p class="column-details__head--title">Add New Job to {{selectedBuyer.company_name}}</p>
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
                <label class="label">Job Country<span class="required">*</span></label>
                <div class="select is-fullwidth">
                  <select v-model="form.criteria_country">
                    <option>Select Country</option>
                    <option v-for="country in criteria_countries" v-bind:key="country.id" :value="country.id">
                      {{ country.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="field">
                <label class="label">Advert<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectAdvert($event)">
                </div>
              </div>

              <div class="field">
                <label class="label">Current Suppliers<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectCurrentSuppliers($event)">
                </div>
              </div>

              <div class="field">
                <label class="label">Bidding Instructions<span class="required"></span></label>
                <div class="control">
                  <input class="input" type="file" @change="selectBiddingInstructions($event)">
                </div>
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
                <button type="submit" class="button is-primary" style="width: 100%">
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
import {mapGetters} from 'vuex'

export default {
  name: "Create",
  data(){
    return{
      criteria_countries: [],
      form: {
        "title": "",
        "unique_reference": "",
        "show_bids": "",
        "advert": "",
        "current_suppliers": "",
        "bidding_instructions": "",
        "criteria_country": "",
      },
    }
  },
  computed: {
    ...mapGetters('Qed', ['selectedBuyer']),
  },
  methods: {
    async create(){
      let form_data = new FormData();
      if (this.form.advert) {
        form_data.append("advert", this.form.advert, this.form.advert.name)
      }
      if (this.form.current_suppliers) {
        form_data.appsend("current_suppliers", this.form.current_suppliers, this.form.current_suppliers.name)
      }
      if (this.form.bidding_instructions) {
        form_data.append("bidding_instructions", this.form.bidding_instructions, this.form.bidding_instructions.name)
      }
      form_data.append("title", this.form.title);
      form_data.append("unique_reference", this.form.unique_reference);
      form_data.append("show_bids", this.form.show_bids);
      form_data.append("criteria_country", this.form.criteria_country);

      try{
        let response = await prequal.create(form_data, this.selectedBuyer.id)
        window.toast.fire({icon: 'success', title: "Prequalification job created successfully"})
        this.$router.push(`/qed/prequalification/details/${response.data['id']}`)
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
    async get_criteria_countries(){
      try{
        let response = await prequal.criteria_countries()
        if (response.status === 200){
          this.criteria_countries = response.data['results']
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Try Again.'})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
  },
  mounted() {
    this.get_criteria_countries()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
.is-primary{
  background-color: #073A82 !important;
}
</style>