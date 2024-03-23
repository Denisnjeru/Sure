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
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Add New Request for Quotation</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">

              <div class="columns">
                <div class="column">
                  <div class="field">
                    <label class="label">RFQ Type<span class="required">*</span></label>
                    <div class="control" style="margin-left:10px;">
                      <label class="radio">
                        <input  type="radio" id="basic" value="basic" v-model="category.rfq_type">
                        Basic
                      </label>
                      <label class="radio">
                        <input type="radio" id="advanced" value="advanced" v-model="category.rfq_type">
                        Advanced
                      </label>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Category Name <span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="category.name" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Category Code<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="category.unique_reference" required>
                    </div>
                  </div>
                   <div class="field">
                    <label class="label">Category Type<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="category.category_type" class="input" required>
                        <option selected>Select Category Type</option>
                        <option v-for="category_type in defaults.category_types" v-bind:key="category_type.id" :value="category_type.id">
                          {{ category_type.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Currency<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="category.currency" class="input" required>
                        <option selected>Select Currency</option>
                        <option v-for="currency in defaults.currencies" v-bind:key="currency.id" :value="currency.id">
                          {{ currency.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Inclusive VAT<span class="required">*</span></label>
                    <div class="control" style="margin-left:10px;">
                      <label class="radio">
                        <input type="radio" id="yes" value="True" v-model="category.vatable">
                        Yes
                      </label>
                      <label class="radio">
                        <input type="radio" id="no" value="False" v-model="category.vatable">
                        No
                      </label>
                    </div>
                  </div>
                  <div class="field" v-show="category.vatable === 'True'">
                    <label class="label">VAT Rate<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" name="vat_rate" type="number" v-model="category.vat_rate" >
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

                <div class="column">
                  <div class="field">
                    <label class="label">Opening Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="category.opening_date" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Closing Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="category.closing_date" required>
                    </div>
                  </div>
                   <div class="field">
                    <label class="label">Supporting Document</label>
                    <div class="control" style="margin-top:2%;">
                      <input class="input" type="file">
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Excel Template<span class="required"></span></label>
                    <a href="#" @click="downloadRFQTemplate()" class="button is-primary is-small">
                      <span><font-awesome-icon class="view__icon" icon="download"/> RFQ Template</span>
                    </a>
                    <div class="control" style="margin-top:2%;">
                      <input class="input" type="file" @change="selectItemsTemplate($event)">
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Instructions <span class="required"></span></label>
                    <div class="control" style="margin-top:2%;">
                      <textarea class="textarea" v-model="category.instructions"></textarea>
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
import rfq from "@/services/company/rfq";

export default {
  name: "Create",
  data() {
    return {
      defaults: [],
      currentStatus: 0,
      category: {
        "name": "",
        "unique_reference": "",
        "opening_date": "",
        "closing_date": "",
        "category_type": "",
        "instructions":"",
        "currency":"",
        "items_template":"",
        "vatable":"",
        "vat_rate":"",
        "rfq_type":"",
      },
    }
  },

  methods: {
    async create() {
      let form_data = new FormData();
      if (this.category.items_template) {
        form_data.append("items_template", this.category.items_template, this.category.items_template.name)
      }

      form_data.append("name", this.category.name);
      form_data.append("unique_reference", this.category.unique_reference);
      form_data.append("opening_date", this.category.opening_date);
      form_data.append("closing_date", this.category.closing_date);
      form_data.append("category_type", this.category.category_type);
      form_data.append("instructions", this.category.instructions);
      form_data.append("currency", this.category.currency);
      form_data.append("vatable", this.category.vatable);
      form_data.append("vat_rate", this.category.vat_rate);
      form_data.append("rfq_type", this.category.rfq_type);
      
      try {
        let response = await rfq.rfqCategoryCreate(form_data, this.$route.params.id)
        console.log(response.data)
        window.toast.fire({icon: 'success', title: "RFQ job category created successfully"})
        this.$router.push('/company/rfq/category/details/'+ this.$route.params.id + '/' + response.data['id'])
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    selectTechnicalDocuments(event){
      this.category.technical_documents = event.target.files[0]
    },
    selectSupportingDocuments(event) {
      this.category.supporting_documents = event.target.files[0]
    },
    selectItemsTemplate(event) {
      this.category.items_template = event.target.files[0]
    },
    async get_defaults(){
      try {
        let response = await rfq.defaults()
        this.defaults = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    downloadRFQTemplate(){
      let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + "media/templates/RFQ_Template_V2.xlsx"
      try{
        window.open(reportUrl)
        }
      catch(err){
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
  .input {
    border-radius: 15px !important;
  }
  select {
    border-radius: 15px !important;
  }
  
  .textarea{
    border-radius: 15px !important;
  }
  .is-primary{
    background-color: #073A82 !important;
  }
</style>