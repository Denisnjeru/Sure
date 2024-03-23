<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               RFQ Jobs > {{rfq.title}} > {{ category.name }}
            </span>

        <div class="page__head--links">
        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title:{{ rfq.title }} </p>
            <p class="column-details__head--desc">Fill in the required details</p>
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <p><strong>Sourcing Activity:</strong> Request for Quotation</p>
            <hr>
            <p><strong>Job Code:</strong> {{ rfq.unique_reference }}</p>
            <hr>
            <p v-if="rfq.is_open === true"><strong>Approval Status:</strong> Open</p>
            <p v-else><strong>Approval Status:</strong> Closed</p>
            <hr>
            <p><strong>Opening Date:</strong> {{ category.opening_date }}</p>
            <hr>
            <p><strong>Closing Date:</strong> {{ category.closing_date }}</p>
            <hr>
          </div>

        </div>

        <div class="column-details column">
          <div class="column-details__head" style="background: white;">
            <p class="column-details__head--title">Actions</p>
            <p class="column-details__head--desc">Category Actions </p>
            <hr>
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
             <div class="columns">
              <div class="column is-2">
              </div>
              <div class="column is-8">
                <router-link :to="'/qed/rfq/invited/suppliers/'+rfq.id+'/'+category.id" class="button is-primary is-fullwidth" style="margin-right: 2px">
                    Invite Suppliers  
                </router-link>
              </div>
              <div class="column is-2">
              </div>
            </div>
            <div class="columns">
              <div class="column is-2">
              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">Refresh Scores</a>
              </div>
              <div class="column is-2">
              </div>
            </div>

            <div class="columns">
              <div class="column is-2">
              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block" @click="openNotificationsModal()">Send Category Notifications</a>
              </div>
              <div class="column is-2">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="page__head">
            <span class="page__head--title column is-6">
               RFQ Items
            </span>

            <div class="page__head--links column is-6" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">
                  <button type="button" class="button is-primary is-pulled-right" @click="downloadCurrentPriceTemplate()">
                      Prices Template
                  </button>
                </div>
                <div class="column is-6">
                  <button type="button" class="button is-primary is-pulled-right" @click="openImportModal">
                      Import Prices
                    </button>
                </div>
              </div>
            </div>
          </div>
          <div class="page__content columns bottom_content">
            <div class="table-search">
                <p class="table-search__instruction">

                </p>
                <div class="table-search__search">
                  <font-awesome-icon class="table-search__search--icon" icon="search"/>
                  <input @keyup.enter="search()" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="item_columns" :data="items">
                <span slot="No." slot-scope="{row}">
                  {{ row.item_number }}
                </span>
                <span slot="Item" slot-scope="{row}">
                  <span> {{ row.item_description }} </span>
                </span>
                <span slot="Reserve" slot-scope="{row}">
                  <span> {{ row.current_price }} </span>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>

        </div>

        <div class="column-details column">
          <div class="page__head">
              <span class="page__head--title column is-6">
                 Participants
              </span>
                <div class="page__head--links column is-6" style="display: inline !important;">
                    <button type="button" class="button is-primary is-pulled-right" @click="closeCategory()" v-if="category.status_open === true">
                      Close Category
                    </button>

                    <template v-else>
                      <div class="columns">
                        <div class="column is-6">
                          <button type="button" class="button is-primary" @click="openModal">
                            Open Category
                          </button>
                        </div>
                      </div>
                  </template>

                </div>
          </div>
          <div class="page__content columns bottom_content">
            <div class="table-search">
                <p class="table-search__instruction">
                </p>
                <div class="table-search__search">
                  <font-awesome-icon class="table-search__search--icon" icon="search"/>
                  <input @keyup.enter="search()" class="table-search__search--input" type="text"
                         placeholder="Search here">
                </div>
              </div>

              <v-client-table :columns="participant_columns" :options="participant_options" :data="participants">
                <span slot="Company" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                    <span>{{ row.company_name }}</span>
                  </template>
                  <template v-if="category.status_open === false">
                    <span>{{ row.company_name }}</span>
                  </template>
                   <template>
                    <span></span>
                  </template>
                </span>

                <span slot="Contact Name" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template v-if="category.status_open === false">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template>
                    <span></span>
                  </template>

                </span>

                <span slot="Actions" slot-scope="{row}">
                  <template v-if="category.status_open === true">
                   <span>{{row.phone_number}}</span>
                  </template>
                  <template v-else>
                    <button class="button is-primary is-small" @click="downloadSupplierResponse(row)" aria-haspopup="true" aria-controls="dropdown-menu3">
                        <span>Report</span>
                        <span class="icon is-small">
                          <i class="angle-down" aria-hidden="true"></i>
                        </span>
                  </button>
                  </template>
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" id="open_rfq">
        <div class="modal-background"></div>
        <div class="modal-card" style="margin-left: 37%; background-color: #DBE9FE !important; border-radius: 12px">
          <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important; display: block">
            <div class="columns">
              <div class="column is-6">
                <p class="modal-card-title">Open RFQ</p>
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
              </div>
            </div>
            <div class="columns">
              <div class="column">
                <p>Fill in the required fields</p>
              </div>
            </div>
          </header>
          <section class="modal-card-body" style="padding: 2%">
            <form>
              <div class="field">
                <label class="label">New Closing Date *</label>
                <div class="control">
                  <input class="input" type="datetime-local" v-model="open_form.closing_date" required>
                </div>
              </div>
            </form>
          </section>

          <section class="modal-card-body">
            <button class="button is-fullwidth is-primary" @click="openCategory()">Submit</button>
          </section>
        </div>
    </div>
    
    <div class="columns">
      <div class="column is-4">
          <div class="modal" id="import_prices">
            <div class="modal-background"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <h5 class="modal-card-title">Import Current Prices</h5>
                <button class="delete" aria-label="close"></button>
              </header>
              <section class="modal-card-body">
                <input type="file" name="" id="">
              </section>
              <footer class="modal-card-foot">
                <button class="button is-success">Submit</button>
              </footer>
            </div>
        </div>
      </div>

    </div>


    <div class="columns">
      <div class="column is-6">
        <div class="modal" id="notifications">
          <div class="modal-background"></div>
          <div class="modal-card">
            <header class="modal-card-head is-danger">
              <div class="columns">
                <div class="column is-12">
                  <h5>RFQ Category Notifications</h5>
                </div>
                <div class="column is-2">
                  <button class="delete is-pulled-right" @click="closeNotificationsModal" aria-label="close"></button>
                </div>
              </div>

            </header>
            <section class="modal-card-body" style="padding: 2%">
              <div class="tabs">
                <ul>
                  <li class="is-active" id="reminder_tab" ><a>Reminder Notification</a></li>
                  <li id="extension_tab"><a>Extension Notification</a></li>
                  <li id="custom_tab"><a>Custom Notifications</a></li>
                </ul>
              </div>
              <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
                <div class="columns" id="reminder_notifications">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Invited Suppliers</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                <div class="columns" id="extension_notifications" style="display: none;">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Invited Suppliers</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                <div class="columns" id="custom_notifications" style="display: none;">
                  <div class="column is-12">
                    <div class="container">
                      <form>
                        <div class="field">
                          <label style="font-weight: bold">Subject *</label>
                          <div class="control">
                            <input type="text" class="input" name="subject">
                          </div>
                        </div>

                        <div class="field">
                          <label style="font-weight: bold">Message *</label>
                          <div class="control">
                            <textarea class="textarea" name="description"></textarea>
                          </div>
                        </div>
                        <div class="field">
                          <a  class="button is-block is-primary">Send</a>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import rfq from "@/services/qed/rfq";

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      participant_columns: ['Company', 'Contact Name', 'Actions'],
      item_columns: ['No.', 'Item', 'Reserve'],
      participant_options: {
        sortable: ['Company',],
        perPageValues: [20],
        filterable: false,
      },
      item_options: {
        sortable: ['Item',],
        perPageValues: [20],
        filterable: false,
      },
      rfq: {},
      category: {},
      participants: [],
      items: [],
      open_form: {
        "closing_date": ""
      },
    }
  },
  methods: {
    openModal() {
      console.log('got here')
      document.getElementById('open_rfq').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('open_rfq').classList.remove('is-active');
    },
    openNotificationsModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeNotificationsModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    openImportModal(){
      document.getElementById('import_prices').classList.add('is-active');
    },
    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    async getCategory() {
      try {
        let response = await rfq.rfqCategoryDetails(this.$route.params.rfq_id, this.$route.params.category_id)
        this.category = response.data
        this.rfq = this.category.rfq
        this.items = this.category.items
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.category)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getParticipants(){
      try {
        let response = await rfq.rfqGetParticipants(this.$route.params.rfq_id, this.$route.params.category_id)
        this.participants = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }

    },
    async closeCategory(){
      try{
        let response = await rfq.closeRFQCategory(this.rfq.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async openCategory(){
      try{
        let response = await rfq.openRFQCategory(this.open_form, this.rfq.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.open_form.closing_date = ""
        this.closeModal()
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async downloadSupplierResponse(row){
      try{
        let response = await rfq.rfqDownloadSupplierResponse(this.$route.params.rfq_id, this.$route.params.category_id, row.id)
        
        if(response.status == 200){
          let reportUrl = process.env.VUE_APP_DOWNLOAD_URL + response.data.report
          console.log(process.env.VUE_APP_DOWNLOAD_URL)
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
     async downloadCurrentPriceTemplate(){
      try{
        let response = await rfq.rfqDownloadCurrentSupplierTemplate(this.$route.params.rfq_id,this.$route.params.category_id)
        console.log(response)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "File download initiated"})
          this.$router.push(`/qed/rfq/category/download/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
   async uploadCurrentPriceTemplate(){
      try{
        let response = await rfq.rfqUploadCurrentSupplierTemplate(this.$route.params.rfq_id,this.$route.params.category_id)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: "File upload initiated"})
          this.$router.push(`/qed/rfq/category/upload/progress/${this.$route.params.category_id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: "Report generation error"})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getCategory()
    this.getParticipants()
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

.is-primary {
  background-color: #073A82 !important;
}

hr{
  margin: 0.5rem 0 !important;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
</style>