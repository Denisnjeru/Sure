<template>
    <div>
         <div class="dashboard">
            <div class="page__head">
                <span class="page__head--title">
                   Invited Suppliers
                </span>
                <div class="page__head--links">
                  <div class="dropdown" id="job_options">
                    <div class="dropdown-trigger">
                      <button class="button is-primary is-small" @click="show_job_options" aria-haspopup="true"
                              aria-controls="dropdown-menu4">
                        <span><font-awesome-icon class="view__icon" icon="receipt"/> Invite From <font-awesome-icon
                            class="view__icon" icon="angle-down"/></span>
                        <span class="icon is-small">
                          <i class="angle-down" aria-hidden="true"></i>
                        </span>
                      </button>
                    </div>
                    <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                      <div class="dropdown-content">
                        <a class="dropdown-item" href="#" @click="openModal()">
                          Email List
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
            <div class="page__content columns">
                <div class="column is-12 column-page">
                    <div class="table-search">
                        <p class="table-search__instruction">
    
                        </p>
                        <div class="table-search__search">
                            <font-awesome-icon class="table-search__search--icon" icon="search" />
                            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                        </div>
                    </div>
    
                  <v-client-table :columns="columns" :options="options" :data="invited_bidders">
                    <span slot="Company Name" slot-scope="{row}">
                        <span v-if="row.supplier"> {{ row.supplier.company_name }}</span>
                        <span v-else> {{row.email}} </span>
                    </span> 
                    <span slot="Contact Name" slot-scope="{row}">   
                      <span v-if="row.supplier"> {{ row.supplier.contact_name }}</span>
                      <span v-else> N/A </span>
                    </span>            
                    <span slot="Phone Number" slot-scope="{row}">  
                      <span v-if="row.supplier"> {{ row.supplier.phone_number }}</span>
                      <span v-else> N/A </span>
                    </span>
                    <span slot="Actions" slot-scope="" class="is-justify-content-right">
                      <router-link to="#" class="button is-danger is-small" style="margin-right: 2px;">
                          <p><font-awesome-icon class="view__icon" icon="trash-alt"/></p>
                      </router-link>
                      <router-link to="#" class="button is-primary is-small">
                        <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>
                      </router-link>
                    </span>
                  </v-client-table>
    
                </div>
                <div class="page__pagination">
                    <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                    </pagination>
                </div>
            </div>
    
        </div>
        <div class="columns">
          <div class="column is-6">
            <div class="modal" id="invitees">
              <div class="modal-background"></div>
              <div class="modal-card">
                <header class="modal-card-head is-danger">
                  <div class="columns">
                    <div class="column is-10">
                      <h4>Add Supplier Emails</h4>
                      <small>
                        Input supplier emails separated by commas
                      </small>
                    </div>
                    <div class="column is-2">
                      <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
                    </div>
                  </div>
                </header>
                <section class="modal-card-body" style="padding: 2%">
                  <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
                    <div class="columns" id="broadcast_invitees">
                      <div class="column is-12">
                        <div class="container">
                          <form>
                            <div class="field">
                              <label style="font-weight: bold">Emails *</label>
                              <div class="control">
                                <textarea class="textarea" name="description" v-model="emails"></textarea>
                              </div>
                            </div>
                            <div class="field">
                              <a class="button is-block is-primary" @click="inviteSuppliers()">Send</a>
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
    import rfq from "@/services/company/rfq";
    
    export default {
      name: "Invitees",
      components:{
      },
      data () {
        return {
          page: 1,
          dataCount: 0,
          dataPerPage: 0,
          columns: ['Company Name', 'Contact Name', 'Phone Number', 'Actions'],
          options: {
            sortable: ['Company Name',],
            perPageValues: [20],
            filterable: false,
          },
          invited_bidders: [],
          emails: [],
        }
      },
      methods: {
        async search() {
          console.log('search');
        },
        async fetchData() {
            console.log('this.page');
        },
        async get_invited_bidders(){
          try{
            let response = await rfq.rfqInvitedBidders(this.$route.params.rfq_id, this.$route.params.category_id)
            console.log(response.data.data)
            this.invited_bidders = response.data.data
            this.dataCount = response.data['count']
            this.dataPerPage = response.data['count']
          }catch (err){
            window.toast.fire({icon: 'error', title: err})
          }
        },
        async inviteSuppliers(){
          if(!this.emails){
            alert("Please add a supplier's email")
            return
          }
          let content = {
            "emails": this.emails,
          }
          try{
            let response = await rfq.rfqInviteSuppliers(content,this.$route.params.rfq_id, this.$route.params.category_id)
            console.log(response.data)
            if (response.status === 201){
              window.toast.fire({icon: 'success', title: response.data['response_message']})
            }else{
              window.toast.fire({icon: 'error', title: "error"})
            }
          }catch (err){
            window.toast.fire({icon: 'error', title: err})
          }
        },
        openModal() {
          document.getElementById('invitees').classList.add('is-active');
        },
        closeModal() {
          document.getElementById('invitees').classList.remove('is-active');
        },
        show_job_options() {
          let element = document.getElementById('job_options')
          if (element.classList.contains('is-active')) {
            element.classList.remove('is-active')
          } else {
            element.classList.add('is-active')
          }
        },
      },
      mounted() {
        this.get_invited_bidders()
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
      margin-left: 36%; width: 560px; background-color: #ffffff !important; border-radius: 12px;
    }
    .modal{
      z-index: 9999;
    }
    .modal-card-head{
      background-color: #ffffff !important; display: block
    }
    </style>