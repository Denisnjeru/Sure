<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Submit RFQ Responses
            </span>

            <div class="page__head--links">
<!--                    <router-link to="/company/create/prequalification" class="button is-primary">-->
<!--                        New Prequalification-->
<!--                    </router-link>-->
            </div>
        </div>
        <div class="page__content columns top-content">
            <div class="column-details column is-12" style="padding: 20px">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Request For Quotation Details
                    </p>
                </div>

              <div class="columns" style="padding: 6px 24px;">
                <div class="column is-6">
                  <span class="page__head--title"><strong>Job Title: </strong>{{ rfq.title }}</span><br/>
                  <span class="page__head--title"><strong>Opening Date: </strong>{{ category.opening_date }}</span><br/>
                  <br>
                  <span class="page__head--title">
                    <strong>Instructions:</strong>
                    <p>{{category.instructions}}</p>
                  </span>
                  <br>
                  <br>
                  <span class="page__head--title"><strong>Download RFQ Excel Template: </strong><br>
                    <a href="#" @click="generate_template()" class="button is-primary is-small">
                      <span><font-awesome-icon class="view__icon" icon="download"/> RFQ Price Template</span>
                    </a>
                  </span> 
                  <br/>
                </div>

                <div class="column is-6">
                  <span class="page__head--title"><strong>Category Name: </strong>{{ category.name }}</span><br/>
                  <span class="page__head--title"><strong>Closing Date: </strong>{{ category.closing_date }}</span><br/>
                </div>
              </div>
              <template v-if="response_document_url">
                <div class="column is-6" style="padding: 6px 24px;">
                  <span class="page__head--title"><strong>Current Response: </strong>
                    <input type="file" @change="uploadItemsTemplate($event)">
                  </span>
                  <br/>
                </div>
              </template>
              <template v-else>
                <div class="column is-6" style="padding: 6px 24px;">
                  <span class="page__head--title"><strong>Upload Filled Excel Template: </strong>
                  <div class="field">
                    <div class="control">
                      <input type="file" class="input is-small" @change="uploadItemsTemplate($event)">
                    </div>
                  </div>
                  </span>
                  <br/>
                </div>
              </template>
              
              <template v-if="category.supplier_participation_status">
                <button type="button" class="button submit-button is-small is-primary is-pulled-right" @click="submitAdvancedRFQ()">
                  <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Update</span>
                </button>
              </template>
              <template v-else>
                <button type="button" class="button submit-button is-small is-primary is-pulled-right" @click="submitAdvancedRFQ()">
                  <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Bid</span>
                </button>
              </template>
            </div>
        </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex';
import rfq from "@/services/company/rfq";
import supplierRfq from "@/services/supplier/rfq";

export default {
  name: "Instructions",
  data(){
    return{
      category: {},
      rfq: {},
      rfq_template:"",
      response_document_url:"",
    }
  },
  computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
    },
    
  methods:{
    async getRfq(){
        try{
            let response = await supplierRfq.rfqDetails(this.$route.params.category_id)
            this.category = response.data
            this.rfq=this.category.rfq
            console.log(this.category)
    
        }catch (err){
            window.toast.fire({icon: 'error', title: err})
        }
    },
    downloadRFQTemplate(category){
      let templateUrl = category.items_template
      if (templateUrl.length > 3){
        let file_url = process.env.VUE_APP_DOWNLOAD_URL + templateUrl.replace(/\//,"")
        console.log(file_url)
        window.open(file_url)
      }
      else{
        window.toast.fire({icon: "error", title: "File does not exist"})
      }
    },
    uploadItemsTemplate(event) {
      this.rfq_template = event.target.files[0]
    },
    async generate_template(){
        try{
            let response = await supplierRfq.gen_items_template(this.$route.params.category_id)
            if (response.status == 200){
                window.toast.fire({icon: 'success', title: response.data['response_message']})
                let routeData = this.$router.resolve(
                    `/supplier/rfq/category/item/template/generation/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
                window.open(routeData.href, '_blank');
            }else{
                window.toast.fire({icon: 'error', title: 'An error occured! Please try again!'})
            }
        }catch(err){
            window.toast.fire({icon: 'error', title: err})
        }
      },
    async submitAdvancedRFQ(){
        let formData = new FormData();
        formData.append("document_url", this.rfq_template, this.rfq_template.name)
        let content = formData
        console.log(content)
        try{
            let response = await rfq.rfqAdvancedSubmit(content,this.authUser.user_id,this.$route.params.category_id)
            console.log(response)
        }catch (err){
            window.toast.fire({icon: 'error', title: err})
        }
    },
    async getSupplierRFQResponse(){
      try{
            let response = await rfq.advancedSupplierRFQResponse(this.authUser.user_id,this.$route.params.category_id)
            this.response_document_url = response.data["results"][0].document_url
            console.log(this.response_document_url)
        }catch (err){
            window.toast.fire({icon: 'error', title: err})
        }
    }
  },
  mounted() {
    this.getRfq()
  },
  created() {

  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}
.is-primary{
  background-color: #073A82 !important;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
</style>