<template>
    <div class="dashboard">
      <div class="page__head">
              <span class="page__head--title">
                  Submit Financial Responses
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
              {{ category.name }}
            </p>
            <div class="table-search__search">
                <router-link :to="'/supplier/tender/category/instructions/'+$route.params.category_id" class="button is-small is-primary">
                    Technical Envelope
                </router-link>
              <!-- <font-awesome-icon class="table-search__search--icon" icon="search"/> -->
              <!-- <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here"> -->
            </div>
          </div>
          
          <div class="notification is-primary" v-if="response_message">
            <button class="delete"></button>
            {{ response_message }}
        </div>

        <div class="columns" style="padding: 6px 24px;">
          <div class="column is-6">
            <span class="page__head--title"><strong>Job Title: </strong>{{ category.tender.title }}</span><br/>
            <span class="page__head--title"><strong>Opening Date: </strong>{{ category.opening_date }}</span><br/>
          </div>

          <div class="column is-6">
            <span class="page__head--title"><strong>Category Name: </strong>{{ category.name }}</span><br/>
            <span class="page__head--title"><strong>Closing Date: </strong>{{ category.closing_date }}</span><br/>
          </div>
        </div>

         <div class="columns" style="padding: 6px 24px;">
           <div class="column is-12">
            <span class="page__head--title">
              <strong>Instructions:</strong>
              <hr>
                <div class="field">
                  <span class="page__head--title" style="font-size: 12px">
                  <strong>1) Please download the template below, fill in the relevant column cells and upload back on the form below.</strong></span>
              </div>

              <div class="field">
                  <span class="page__head--title" style="font-size:12px">
                      <strong style="color:red;"><label>2) NB: </label>Note that any edits outside of the provisioned cells are likely to invalidate your bid!!</strong>
                  </span>
              </div>
              <p>{{category.instructions}}</p>
            </span>
            
            <div class="field">
                <button @click="generate_template()" class="button is-primary is-small">Download Items Template</button> 
                <a v-if="category.previous_bid_template" :href="category.previous_bid_template" class="button is-primary is-small is-pulled-right" download>Previous Bid Template</a>     
            </div>

            <form @submit.prevent="submit_items_template()" style="font-size: 12px">
                <div class="field">
                    <label>Filled Items Template</label>
                    <div class="control">
                        <input type="file" @change="selectTemplate($event)" class="input is-small" required/>
                    </div>
                </div>
                <button type="submit" class="button is-primary is-small">Submit</button>
            </form>
        
           </div>
         </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import tender from "@/services/supplier/tender";
  
  export default {
    name: "AdvancedTenderFinancialBid",
    data() {
      return {
        category: {},
        excel_url: "",
        response_message: null
      }
    },
    methods: {
        selectTemplate(event){
            this.excel_url = event.target.files[0]
        },
      async fetchData() {
        console.log(this.page)
      },
      async search() {
        console.log('search')
      },
      async generate_template(){
        try{
            let response = await tender.gen_items_template(this.$route.params.category_id)
            if (response.status == 200){
                window.toast.fire({icon: 'success', title: response.data['response_message']})
                let routeData = this.$router.resolve(
                    `/supplier/tender/category/item/template/generation/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
                window.open(routeData.href, '_blank');
            }else{
                window.toast.fire({icon: 'error', title: 'An error occured! Please try again!'})
            }
        }catch(err){
            window.toast.fire({icon: 'error', title: err})
        }
      },
      async getCategory() {
        try {
          let response = await tender.category_instructions(this.$route.params.category_id)
          this.category = response.data
        } catch (err) {
          window.toast.fire({icon: 'error', title: err})
        }
      },

      async submit_items_template(){
        let form = new FormData()
        if (this.excel_url) {
            form.append("excel_url", this.excel_url, this.excel_url.name)
        }
        try{
            let response = await tender.submit_advanced_financial_bid(form, this.$route.params.category_id)
            if (response.status === 200){
                this.response_message = response.data["response_message"]
                window.toast.fire({icon: 'success', title: response.data["response_message"]})
            }else{
                window.toast.fire({icon: 'error', title: "An error occured. Please try again!"})
            }
        }catch(err){
            this.response_message = err
            window.toast.fire({icon: 'error', title: err})
        }
      }
    },
    mounted() {
      this.getCategory()
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