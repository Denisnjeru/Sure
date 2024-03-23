<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
              {{rfq.title}} > RFQ Job > Reports
            </span>

            <div class="page__head--links">
              <div class="dropdown" id="job_options">
                <div class="dropdown-trigger">
                  <button class="button is-primary" @click="show_job_options" aria-haspopup="true"
                          aria-controls="dropdown-menu4">
                    <span><font-awesome-icon class="view__icon" icon="receipt"/> RFQ Reports <font-awesome-icon
                        class="view__icon" icon="angle-down"/></span>
                    <span class="icon is-small">
                      <i class="angle-down" aria-hidden="true"></i>
                    </span>
                  </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                  <div class="dropdown-content">
                    <a class="dropdown-item" href="#" @click="downloadJobSavingsReport()">
                      Job Savings Report
                    </a>
                    <hr class="dropdown-divider">
                    <a href="#" class="dropdown-item" >
                      Participation Summary Report
                    </a>
                  </div>
                </div>
              </div>
            </div>
        </div>

        <div class="page__head">
            <span class="page__head--title">
               RFQ Categories
            </span>

            <div class="page__head--links">
            </div>
        </div>
     
        <div class="page__content columns top_content" style="align-items: inherit !important;">
          <div class="column is-12 column-page">
            <div class="table-search">
              <p class="table-search__instruction">
                {{ rfq.title }} Categories
              </p>
              <div class="table-search__search">
                <font-awesome-icon class="table-search__search--icon" icon="search"/>
                <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
              </div>
            </div>

            <v-client-table :columns="columns" :options="options" :data="categories">
              <span slot="Category Name" slot-scope="{row}">
                <span>{{ row.name }}</span>
              </span>

              <span slot="Category Code" slot-scope="{row}">
                <span>{{ row.unique_reference }}</span>
              </span>

              <span slot="Closing Date" slot-scope="{row}">
                <span>{{ row.closing_date }}</span>
              </span>

              <span slot="Reports" slot-scope="{row}">

                <div class="dropdown" :id="'row_'+row.id">
                  <div class="dropdown-trigger">
                    <button class="button is-primary is-small" @click="show_category_options(row)" aria-haspopup="true"
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
                      <!-- <router-link :to="'#'+row.id" class="dropdown-item">
                        Financial Evaluation 
                      </router-link> -->
                      <a href="#" @click="downloadFinancialReport(row)" class="dropdown-item">
                        Financial Evaluation
                      </a>
                      <hr class="dropdown-divider">
                      <a href="#" @click="downloadParticipationSummary(row)" class="dropdown-item">
                        Participation Summary
                      </a>
                      <!-- <router-link :to="'#'" class="dropdown-item">
                        Participation Summary 
                      </router-link> -->
                    </div>
                  </div>
                </div>
              </span>
            </v-client-table>
          </div>
      </div>
    </div>
</template>

<script>
import rfq from "@/services/company/rfq";

export default {
  name: "JobReports",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Category Name', 'Category Code', 'Closing Date', 'Reports'],
      options: {
        sortable: ['Category Name','Category SCode'],
        perPageValues: [20],
        filterable: false,
      },
      categories: [],
      rfq: {},
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
    async search() {
      console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async getCategories() {
      try {
        let response = await rfq.categories(this.$route.params.rfq_id)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.categories)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getRfq() {
      try {
        let response = await rfq.rfq(this.$route.params.rfq_id)
        this.rfq = response.data
      } catch (err) {
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
    openModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    async downloadParticipationSummary(row){
      try{
        let response = await rfq.rfqDownloadParticipationSummary(this.$route.params.rfq_id, row.id)
        console.log(response)
        if(response.status === 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          try{
            window.open(reportUrl)
          }catch(err){
            window.toast.fire({icon: 'error', title: err})
          }
        }
        else{
           window.toast.fire({icon: 'error', title: 'Error downloading the report'})
        }

      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async downloadFinancialReport(row){
      try{
        let response = await rfq.rfqDownloadFinancialReport(this.$route.params.rfq_id, row.id)
        console.log(response)
        if(response.status === 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          try{
              window.open(reportUrl)
            }catch(err){
              window.toast.fire({icon: 'error', title: err})
            }
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async downloadJobSavingsReport(){
      try{
        let response = await rfq.rfqDownloadJobSummaryReport(this.$route.params.rfq_id)
        console.log(response)
        if(response.status === 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          try{
              window.open(reportUrl)
            }catch(err){
              window.toast.fire({icon: 'error', title: err})
            }
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },

  mounted() {
    this.getCategories()
    this.getRfq()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.page {
  &__content {
    position: relative;
    z-index: 20;

    .column-details {
      margin: 0 $line-height/4;
      box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
      border-radius: $line-height/2;
      padding: 0;
      margin-bottom: $line-height/2;

      &__head {
        background: $color-baby-blue;
        padding: $line-height $line-height;
        border-radius: $line-height/2 $line-height/2 0 0;

        &--title {
          color: rgba(18, 31, 62, 0.8);
          font-size: $font-size-title;
          font-weight: 600;
          margin-bottom: $line-height/6 !important;
        }

        &--desc {
          color: $color-black-medium;
          margin: $line-height/4 0;
        }
      }

      &__content {
        padding: $line-height/2 $line-height;
        margin-bottom: 0;

        .detail {
          padding: $line-height 0;
          border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

          &__title {
            font-weight: 600;
            margin-right: $line-height/2;
            color: $color-black-main;
          }

          &__text {
            color: $color-lightblue-text;
          }
        }

        .document {
          padding: $line-height 0;
          border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
          position: relative;
          z-index: 1;

          &__status {
            position: absolute;
            z-index: 20;
            padding: $line-height/6 $line-height/3;
            color: $color-lightblue-text;
            background: #F2F6FF;
            border: 1px solid #073A82;
            box-sizing: border-box;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: 10px;
            font-size: $font-size-small;
            left: 60%;
            display: none;
          }

          &__title {
            width: 100%;
            @include grid_row;

            &--name {
              font-weight: 600;
              color: $color-black-main;
            }

            &--icon {
              color: $color-gray-main;
            }

            .missing {
              color: $color-red-main;
            }
          }

          &__name {
            width: 100%;
            @include grid_row;
            align-items: center;
            margin-top: $line-height/3;
            background: #F8F8F8;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: $line-height/4 $line-height/2;
            font-size: $font-size-text;

            &--text {
              @include grid_row;
              align-items: center;

              .icon {
                margin-right: $line-height/4;
                height: $line-height;
              }
            }

            &--delete {

              .selected__icon {
                margin: 0 $line-height/4;

                &--img {
                  height: $line-height/1.2;
                  padding: $line-height/6;
                  background-color: $color-gray-main;
                  color: $color-white-main;
                  border-radius: 50%;
                  cursor: pointer;

                  &:hover {
                    background-color: $color-red-main;
                  }
                }
              }
            }
          }

          &:hover {
            .doc-missing {
              color: $color-red-main;
              cursor: pointer;
            }

            .document__status {
              display: block;
            }
          }
        }

        .risk_submit {
          padding: $line-height/2 0;
          margin: $line-height/1 0 50px;

          .button-submit {
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;
            font-size: $font-size-text;
          }

          &:hover {
            cursor: pointer;
          }
        }

        .show_bids {
          display: inline-block;
          color: $color-blue-main;

          .text {
            font-size: $font-size-text;
            font-weight: 600;
            padding: 12px;
          }
        }
      }
    }

  }
}

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