<template>
<div class="dashboard">
    <div class="page__head">
      <span class="page__head--title">
         Tender > {{ category.name }} > Invited Suppliers
      </span>

      <div class="page__head--links">
        <button type="button" class="button is-primary" @click="openModal()" style="margin-right: 2px">Invite (Email List)</button>
        <button type="button" class="button is-primary">Invite (System)</button>
      </div>
    </div>

  <div class="page__content columns top_content" style="align-items: inherit !important;">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__instruction">
            Suppliers
          </p>
          <div class="table-search__search">
            <font-awesome-icon class="table-search__search--icon" icon="search"/>
            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
          </div>
        </div>

        <v-server-table ref="invited_suppliers" :columns="columns" :options="options">
          <template slot="CompanyName" slot-scope="row">
            <span>{{ row.row.supplier.company_name }}</span>
          </template>

          <template slot="Email" slot-scope="row">
            <span>{{ row.row.email }}</span>
          </template>

          <template slot="Actions" slot-scope="row">
            <a :href="''+row.row.id">Revoke Invite</a>
          </template>

        </v-server-table>
      </div>
  </div>

  <div class="modal" id="email_invite_bidders">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important;">
            <div class="columns">
              <div class="column is-6">
                <strong>Invite Bidders</strong><br>
<!--                <small>Fill in the required fields</small>-->
              </div>
              <div class="column is-6">
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
              </div>
            </div>

          </header>
          <section class="modal-card-body" style="padding: 2%">
            <form @submit.prevent="submitEmailInvites()">

              <div class="field">
                <label class="label">Emails *</label>
                <div class="control">
                  <textarea class="textarea" type="datetime-local" v-model="form.emails"
                            placeholder="Enter comma separated email addresses" required></textarea>
                </div>
              </div>

            </form>
          </section>

          <section class="modal-card-body">
            <button type="button" @click="submitEmailInvites()" class="button is-fullwidth is-primary">Submit</button>
          </section>
        </div>
      </div>
</div>
</template>

<script>
import tender from "@/services/company/tender";

export default {
  name: "InvitedSuppliers",
  data(){
    return{
      form: {
        "category": this.$route.params.category_id,
        "emails": ""
      },
      page: 1,
      category: {},
      columns: ['CompanyName', 'Email', 'Actions'],
      options: {
        perPageValues: [10],
        sortable: ['Company Name', 'Email'],
        texts: {
          loadingError: 'Oops! Something went wrong'
        },
        async requestFunction(data) {
          console.log(data)
          try {
            let response = await tender.invited_suppliers(
                this.$route.params.tender_id, this.$route.params.category_id,this.page)
            let response_data = {
              count: response.data['count'],
              data: response.data['results']
            }
            return response_data;
          } catch (err) {
            console.log(err)
            window.toast.fire({icon: 'error', title: err})
            return err
          }

        }
      }
    }
  },
  methods:{
    openModal() {
      console.log('got here')
      document.getElementById('email_invite_bidders').classList.add('is-active');
    },
    closeModal() {
      console.log('got here')
      document.getElementById('email_invite_bidders').classList.remove('is-active');
    },
    async submitEmailInvites(){
      try{
        let response = await tender.email_invite_suppliers(
            this.$route.params.tender_id, this.$route.params.category_id, this.form
        )
        if (response.status === 200){
          this.closeModal()
          this.$refs["invited_suppliers"].getData()
          window.toast.fire({icon: 'success', title: 'Invites are being sent'})
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again!'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategory(){
      try{
        let response = await tender.category(
            this.$route.params.tender_id, this.$route.params.category_id,
        )
        this.category = response.data
      }catch (err){
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
.is-primary {
  background-color: #073A82 !important;
}
.textarea {
  border-radius: 15px !important;
}
.modal-card-head {
  background-color: #ffffff !important;
  display: block
}
.modal-card {
  width: 560px;
  background-color: #ffffff !important;
  border-radius: 12px;
}

.modal {
  z-index: 9999;
}
</style>