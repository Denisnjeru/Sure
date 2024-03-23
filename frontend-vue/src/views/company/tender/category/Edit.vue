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
        <div class="column-details column is-12">
          <form v-on:submit.prevent="update">
            <div class="column-details__head">
              <p class="column-details__head--title">Edit Category</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">

              <div class="columns">
                <div class="column">
                  <div class="field">
                    <label class="label">Category Title <span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="form.name" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Category Number<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="form.unique_reference" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Opening Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="form.opening_date" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Closing Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="form.closing_date" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Supporting Documents<span class="required"></span></label>
                    <div class="control">
                      <input class="input" multiple="multiple" type="file" @change="selectSupportingDocuments($event)">
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

                <div class="column">
                  <div class="field">
                    <label class="label">Bid Fee Currency<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="form.currency" class="input" required>
                        <option selected>Select Currency</option>
                        <option v-for="currency in defaults.currencies" v-bind:key="currency.id" :value="currency.id">
                          {{ currency.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Bid Fee<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="number" v-model="form.bid_charge" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Category Type<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="form.category_type" class="input" required>
                        <option selected>Select Category Type</option>
                        <option v-for="category_type in defaults.category_types" v-bind:key="category_type.id" :value="category_type.id">
                          {{ category_type.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Pass Score<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="number" v-model="form.pass_score" required>
                    </div>
                  </div>

                  <!-- <div class="field">
                    <label class="label">Question Template<span class="required"></span></label>
                    <a href="#" class="button button-submit is-small">Download Template</a>
                    <a href="#" style="margin-left: 2px" v-if="category.questions_template" class="button button-submit is-small">Current Template</a>
                    <div class="control" style="margin-top:2%;">
                      <input class="input" type="file" @change="selectQuestionTemplate($event)">
                    </div>
                  </div> -->

                  <label class="label">Actions</label>
                  <div class="columns">
                    <div class="column">
                      <div class="field">
                        <div class="control">
                          <label class="checkbox">
                            <input type="checkbox" v-model="form.send_participant_list_to_supplier">
                            <strong> Send Participant List To Suppliers </strong>
                          </label>
                        </div>
                      </div>
                    </div>

                    <div class="column">
                      <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.invite_only">
                        <strong> Invite Only ? </strong>
                      </label>
                    </div>
                  </div>
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
import tender from "@/services/company/tender";

export default {
  name: "Edit",
  data() {
    return {
      defaults: [],
      category: {},
      form: {
        "name": "",
        "bid_charge": "",
        "unique_reference": "",
        "pass_score": "",
        "opening_date": "",
        "closing_date": "",
        "currency": "",
        // "questions_template": "",
        "send_participant_list_to_supplier": "",
        "category_type": "",
        "invite_only": "",
        "tender": "",
        "supporting_documents": ""
      },
    }
  },
  methods: {
    async update() {
      let form_data = new FormData();
      // if (this.form.questions_template) {
      //   form_data.append("questions_template", this.form.questions_template, this.form.questions_template.name)
      // }
      if (this.form.current_suppliers) {
        form_data.append("supporting_documents", this.form.supporting_documents, this.form.supporting_documents.name)
      }

      form_data.append("name", this.form.name);
      form_data.append("unique_reference", this.form.unique_reference);
      form_data.append("opening_date", this.form.opening_date);
      form_data.append("closing_date", this.form.closing_date);
      form_data.append("send_participant_list_to_supplier", this.form.send_participant_list_to_supplier);
      form_data.append("bid_charge", this.form.bid_charge);
      form_data.append("currency", this.form.currency);
      form_data.append("category_type", this.form.category_type);
      form_data.append("pass_score", this.form.pass_score);
      form_data.append("invite_only", this.form.invite_only);
      form_data.append("tender", this.form.tender);

      try {
        let response = await tender.update_category(form_data, this.$route.params.tender_id, this.$route.params.category_id)
        window.toast.fire({icon: 'success', title: "Tender category created successfully"})
        this.$router.push(`/company/tender/category/details/${this.$route.params.tender_id}/${response.data['id']}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    selectSupportingDocuments(event) {
      this.form.supporting_documents = event.target.files
    },
    selectQuestionTemplate(event) {
      this.form.questions_template = event.target.files[0]
    },

    async get_defaults(){
      try {
        let response = await tender.defaults()
        this.defaults = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_category(){
      try{
        let response = await tender.category(this.$route.params.tender_id, this.$route.params.category_id)
        this.category = response.data
        this.form.name = response.data['name']
        this.form.unique_reference = response.data['unique_reference']
        this.form.opening_date = response.data['opening_date']
        this.form.closing_date = response.data['closing_date']
        this.form.send_participant_list_to_supplier = response.data['send_participant_list_to_supplier']
        this.form.bid_charge = response.data['bid_charge']
        this.form.currency = response.data['currency'].id
        this.form.category_type = response.data['category_type'].id
        this.form.pass_score = response.data['pass_score']
        this.form.invite_only = response.data['invite_only']
        this.form.tender = response.data['tender'].id
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_defaults()
    this.get_category()
  },
  created() {
  },
}
</script>

<style lang="scss" scoped>
@include page;
.input {
  border-radius: 15px !important;
}
select {
  border-radius: 15px !important;
}

.textarea{
  border-radius: 15px !important;
}
</style>