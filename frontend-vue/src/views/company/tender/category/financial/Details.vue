<template>
<div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Tender Jobs > {{ tender.title }} > {{ category.name }} > Financial Details
            </span>

        <div class="page__head--links">
          <router-link class="button is-primary is-small" :to="'/company/tender/category/details/'+tender.id+'/'+category.id">
            Technical Details
          </router-link>
        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title: </p>
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <p><strong>Sourcing Activity:</strong> Tender</p>
            <hr>
            <p><strong>Job Code:</strong> {{ tender.unique_reference }}</p>
            <hr>
            <p v-if="tender.is_open === true"><strong>Approval Status:</strong> Open</p>
            <p v-else><strong>Approval Status:</strong> Closed</p>
            <hr>
            <p><strong>Opening Date:</strong> {{ category.opening_date }}</p>
            <hr>
            <p><strong>Closing Date:</strong> {{ category.closing_date }}</p>
            <hr>
            <p><strong>Pass Mark:</strong> {{ category.pass_score }}%</p>
            <hr>
            <template v-if="category.has_participants === false && category.is_open === false">
                <div class="field">
                  <label class="label">Import Items From Excel<span class="required"> *</span></label>
                  <a download="download" :href="category.items_template" class="button is-primary is-small">
                    <span><font-awesome-icon class="view__icon" icon="download"/> Items Template</span>
                  </a>
                  <div class="control">
                    <br>
                    <input class="input" type="file">
                  </div>
                </div>
                <hr>
              </template>
          </div>

        </div>

        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Actions</p>
          </div>
          <!-- Form Details -->
          <div class="column-details__content">

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-small is-block">Refresh Scores</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
<!--                <a href="#" @click="openNotificationsModal" class="button is-primary is-block">Send Category Notifications</a>-->
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
            <span class="page__head--title column is-4">
               Items
            </span>

            <div class="page__head--links column is-8" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">

                </div>
                <div class="column is-6">
<!--                  <router-link to="#" class="button is-primary is-block">-->
<!--                    Add Item-->
<!--                  </router-link>-->
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

              <v-client-table :columns="item_columns" :options="item_options" :data="items">
                <span slot="#NO" slot-scope="{row}">
                    <span> {{ row.number }}</span>
                </span>

                <span slot="Item Description" slot-scope="{row}">
                    <span> {{ row.description }}</span>
                </span>

                <span slot="Reserve Price" slot-scope="{row}">
                    <span> {{ row.current_price }}</span>
                </span>

<!--                <span slot="Actions">-->
<!--                  <span class="actions__delete">-->
<!--                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>-->
<!--                  </span>-->

<!--                  <router-link to="#"-->
<!--                               class="button is-primary is-small" style="margin-right: 2px;">-->
<!--                      <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>-->
<!--                  </router-link>-->

<!--                  <router-link to="#"-->
<!--                               class="button is-primary is-small">-->
<!--                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>-->
<!--                  </router-link>-->
<!--                </span>-->
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="itemDataCount" v-model="itemPage" :per-page="itemDataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>

        </div>

        <div class="column-details column">
          <div class="page__head">
              <span class="page__head--title column is-4">
                 Participants
              </span>


                <div class="page__head--links column is-8" style="display: inline !important;">
                    <button type="button" class="button is-primary is-small is-pulled-right" @click="close_category()" v-if="category.is_open === true">
                      Close Category
                    </button>

                    <template v-else>
                      <div class="columns">
                        <div class="column is-6">
<!--                          <router-link :to="'/company/tender/letters/'+tender.id+'/'+category.id" class="button is-primary is-fullwidth" style="margin-right: 2px">-->
<!--                            Letters-->
<!--                          </router-link>-->
                        </div>

                        <div class="column is-6">
                          <button type="button" class="button is-small is-primary" @click="openModal">
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
                <span slot="Supplier" slot-scope="{row}">
                  <template>
                    <span>{{ row.company_name }}</span>
                  </template>
                </span>

                <span slot="Contact" slot-scope="{row}">
                  <template>
                    <span> {{ row.contact_name }}</span>
                  </template>
                </span>

                <span slot="Actions">
<!--                  <template v-if="category.is_open === false && category.has_qa_instance === true">-->
<!--                     <router-link :to="'/company/tender/conduct/qa/'+ category.id +'/' + row.id"-->
<!--                               class="button is-primary is-small">-->
<!--                      <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Conduct QA</p>-->
<!--                    </router-link>-->
<!--                  </template>-->
                </span>
              </v-client-table>

            <div class="page__pagination">
              <pagination :records="participantDataCount" v-model="participantPage" :per-page="participantDataPerPage" @paginate="fetchData()">
              </pagination>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" id="open_tender">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important;">
            <div class="columns">
              <div class="column is-6">
                <strong>Open Category</strong><br>
                <small>Fill in the required fields</small>
              </div>
              <div class="column is-6">
                <button class="delete is-small is-pulled-right" @click="closeModal" aria-label="close"></button>
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
            <button class="button is-fullwidth is-small is-primary" @click="open_category()">Submit</button>
          </section>
        </div>
      </div>

  </div>
</template>

<script>
import tender from "@/services/company/tender";

export default {
  name: "FinancialDetails",
  data() {
    return {
      participantPage: 1,
      participantDataCount: 0,
      participantDataPerPage: 10,

      itemPage: 1,
      itemDataCount: 0,
      itemDataPerPage: 10,
      participant_columns: ['Supplier', 'Contact', 'Quotation',],
      item_columns: ['#NO', 'Item Description', 'Reserve Price'],
      participant_options: {
        sortable: ['Supplier',],
        perPageValues: [10],
        filterable: false,
      },
      item_options: {
        sortable: ['#NO','Item Description'],
        perPageValues: [10],
        filterable: false,
      },
      tender: {},
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
      document.getElementById('open_tender').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('open_tender').classList.remove('is-active');
    },

    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    async getCategory() {
      try {
        let response = await tender.minimized_category_details(this.$route.params.tender_id, this.$route.params.category_id)
        this.category = response.data
        this.tender = this.category.tender
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getParticipants() {
      try {
        let response = await tender.financial_participants(
          this.$route.params.tender_id, this.$route.params.category_id, this.participantPage, this.participantDataPerPage)
        this.participants = response.data['results']
        this.participantDataCount = response.data['count']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getItems() {
      try {
        let response = await tender.items(
          this.$route.params.tender_id, this.$route.params.category_id, this.itemPage, this.itemDataPerPage)
        this.items = response.data['results']
        this.itemDataCount = response.data['count']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async close_category(){
      try{
        let response = await tender.close_category(this.tender.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async open_category(){
      try{
        let response = await tender.open_category(this.open_form, this.tender.id, this.category.id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.open_form.closing_date = ""
        this.closeModal()
        this.getCategory()
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.getCategory()
    this.getParticipants()
    this.getItems()
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
  margin: 0 !important;
  //@include grid_column;
}

.page__head{
  padding: 1px 30px;
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
  padding-top: 1px;
}

.page .table-search[data-v-e49b950c] {
    padding: 12px 6px
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

.textarea{
  border-radius: 15px !important;
}
.tabs li.is-active a {
    border-bottom-color: #073A82;
    color: #073A82;
}
.modal-card{
   width: 560px; background-color: #ffffff !important; border-radius: 12px;
}
.modal{
  z-index: 9999;
}
.modal-card-head{
  background-color: #ffffff !important; display: block
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
hr{
  margin: 0.5rem 0 !important;
}
</style>