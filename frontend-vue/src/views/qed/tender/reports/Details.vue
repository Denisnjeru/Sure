<template>
  <div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Tender Job > {{ tender.title }} > Reports
            </span>

      <div class="page__head--links">
        <div class="dropdown" id="job_options">
          <div class="dropdown-trigger">
            <button class="button is-primary" @click="show_job_options" aria-haspopup="true"
                    aria-controls="dropdown-menu4">
              <span><font-awesome-icon class="view__icon" icon="receipt"/> Tender Job Reports <font-awesome-icon
                  class="view__icon" icon="angle-down"/></span>
              <span class="icon is-small">
                <i class="angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu4" role="menu">
            <div class="dropdown-content">
<!--              <a class="dropdown-item" href="#" @click="generate_interim_report()">-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Interim Technical Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_qa_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                  Final QA Ranking Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Tender Job Summary Report-->
<!--              </a>-->
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item" @click="tender_participation_report()">
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Tender Participation Report
              </a>
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item" @click="supplier_details_report()">
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Tender Supplier Details
              </a>
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item" >
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Tender Category Suppliers
              </a>
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item"  @click="bidder_locations_report()">
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Bidder Locations &Contacts Report
              </a>
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item" @click="responsive_bidders_report()" >
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Responsive Bidders Report
              </a>
              <hr class="dropdown-divider">
              <a href="#" class="dropdown-item" @click="non_responsive_bidders_report()" >
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Non-Responsive Bidders Report
              </a>
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_prequalified_suppliers_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Prequalified Suppliers Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_job_bidder_payments_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Bidder Payments Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_responsive_bidders_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Responsive Bidders Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_non_responsive_bidders_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Non-Responsive Bidders Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_directors_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Directors Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" class="dropdown-item" @click="generate_dd_report()">-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                DD Ranking Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" @click="generate_participation_status_report()" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Participation Status Report-->
<!--              </a>-->
<!--              <hr class="dropdown-divider">-->
<!--              <a href="#" class="dropdown-item" >-->
<!--                <font-awesome-icon class="view__icon" icon="receipt"/>-->
<!--                Current Suppliers Report-->
<!--              </a>-->
              <hr class="dropdown-divider">
              <a href="#" @click="get_category_suppliers_report()" class="dropdown-item" >
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Category Suppliers Report
              </a><hr class="dropdown-divider">
              <a href="#" @click="get_current_suppliers_report()" class="dropdown-item" >
                <font-awesome-icon class="view__icon" icon="receipt"/>
                Current Suppliers Report
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page__content columns top_content" style="align-items: inherit !important;">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__instruction">
            {{ tender.title }} Categories
          </p>
          <div class="table-search__search">
            <font-awesome-icon class="table-search__search--icon" icon="search"/>
            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
          </div>
        </div>

        <v-server-table :columns="columns" :options="options">
          <template slot="Title" slot-scope="row">
            <span>{{ row.row.name }}</span>
          </template>

          <template slot="Closing Date" slot-scope="row">
            <span>{{ row.row.closing_date }}</span>
          </template>

          <template slot="Actions" slot-scope="row">

            <div class="dropdown" :id="'row_'+row.row.id">
              <div class="dropdown-trigger">
                <button class="button is-primary is-small" @click="show_category_options(row.row)" aria-haspopup="true"
                        aria-controls="dropdown-menu3">
                  <span><font-awesome-icon class="view__icon" icon="receipt"/> Reports <font-awesome-icon
                      class="view__icon" icon="angle-down"/></span>
                  <span class="icon is-small">
                            <i class="angle-down" aria-hidden="true"></i>
                          </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                <div class="dropdown-content">
                  <a @click="get_category_technical_report(row.row.id)" class="dropdown-item">
                    <font-awesome-icon class="view__icon" icon="receipt"/>
                    Technical Evaluation Report
                  </a>

                  <a @click="get_tender_summary_report(row.row.id)" class="dropdown-item">
                    <font-awesome-icon class="view__icon" icon="receipt"/>
                    Tender Summary Report
                  </a>
                  <router-link :to="'#'+row.id" class="dropdown-item">
                    <font-awesome-icon class="view__icon" icon="receipt"/>
                    Interim Report
                  </router-link>
                  <hr class="dropdown-divider">
                  <router-link :to="'#'" class="dropdown-item">
                    <font-awesome-icon class="view__icon" icon="receipt"/>
                    QA Ranking Report
                  </router-link>
                </div>
              </div>
            </div>
          </template>

        </v-server-table>

      </div>

    </div>
  </div>
</template>

<script>
import tender from "@/services/qed/tender";

export default {
  name: "Details",
  data() {
    return {
      tender: {},
      page: 1,
      columns: ['Title', 'Closing Date', 'Actions'],
      options: {
        perPageValues: [10],
        sortable: ['Title', 'Closing Date'],
        texts: {
          loadingError: 'Oops! Something went wrong'
        },
        async requestFunction(data) {
          console.log(data)
          try {
            let response = await tender.report_categories(this.page)
            let response_data = {
              count: response.data['count'],
              data: response.data['results']
            }
            return response_data;
          } catch (err) {
            console.log(err)
            return err
            // window.toast.fire({icon: 'error', title: err})
          }

        }
      }
    }
  },
  methods: {
    show_category_options(row) {
      let element = document.getElementById('row_' + row.id)
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
    async generate_qa_report(){
      try{
        let response = await tender.qa_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async tender_participation_report(){
      try{
        let response = await tender.tender_participation_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async supplier_details_report(){
      try{
        let response = await tender.supplier_details_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async bidder_locations_report(){
      try{
        let response = await tender.bidder_locations_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async responsive_bidders_report(){
      try{
        let response = await tender.responsive_bidders_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async non_responsive_bidders_report(){
      try{
        let response = await tender.non_responsive_bidders_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async generate_interim_report(){
      try{
        let response = await tender.interim_report(this.$route.params.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_category_technical_report(category_id){
      try{
        let response = await tender.category_technical_report_pdf(this.tender.id, category_id)
        if (response.status === 200){
          console.log(response.data)
          window.toast.fire({icon: 'success', title: "Report generated successfully"})
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async get_tender_summary_report(category_id){
      try{
        let response = await tender.tender_summary_report(this.tender.id, category_id)
        if (response.status === 200){
          console.log(response.data)
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async get_category_suppliers_report(){
      try{
        let response = await tender.category_suppliers_report(this.tender.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/tender/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_current_suppliers_report(){
      try{
        let response = await tender.category_suppliers_report(this.tender.id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "Report generation started"})
          this.$router.push(`/qed/prequal/report/progress/${this.$route.params.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    show_job_options() {
      let element = document.getElementById('job_options')
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
    async getTender(){
      try{
        let response = await tender.tender(this.$route.params.id)
        if (response.status === 200){
          this.tender = response.data
        }else{
          window.toast.fire({icon: 'error', title: "Network Error"})
        }
      }catch (err){
          window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.getTender()
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
  margin: 0 !important;
  //@include grid_column;
}

.top_content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom_content {
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  align-items: center;
}

.page .table-search[data-v-e49b950c] {
  padding: 12px 6px
}

.VueTables__table tbody td {
  padding: 5px 24px;
}

.is-primary {
  background-color: #073A82 !important;
}

.input {
  border-radius: 15px !important;
}

select {
  border-radius: 15px !important;
}

.textarea {
  border-radius: 15px !important;
}

.tabs li.is-active a {
  border-bottom-color: #073A82;
  color: #073A82;
}

.modal-card {
  width: 560px;
  background-color: #ffffff !important;
  border-radius: 12px;
}

.modal {
  z-index: 9999;
}

.modal-card-head {
  background-color: #ffffff !important;
  display: block
}

hr {
  margin: 0rem 0 !important;
}

.dropdown-content {
  position: fixed !important;
}
.page__content {
    position: relative;
    z-index: 0;
}
.dropdown-item {
    padding: 0.1rem 1rem;
    font-size: 12px;
}
.dropdown-item svg:not(:root).svg-inline--fa {
    overflow: visible;
    color: green;
}
</style>