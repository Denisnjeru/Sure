<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Tender Jobs > {{ tender.title }} > {{ category.name }}
            </span>

        <div class="page__head--links">
        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
          <div class="column-details__head">
            <p class="column-details__head--title">Job Title: </p>
            <p class="column-details__head--desc">Fill in the required details</p>
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
                  <label class="label">Import Questions From Excel<span class="required"> *</span></label>
                  <a download="download" href="#" class="button is-primary">
                    <span><font-awesome-icon class="view__icon" icon="download"/> Questions Template</span>
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
                <a href="#" class="button is-primary is-block">Refresh Scores</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" @click="openNotificationsModal" class="button is-primary is-block">Send Category Notifications</a>
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
               Question Sections
            </span>

            <div class="page__head--links column is-8" style="display: inline !important;">
              <div class="columns">
                <div class="column is-6">

                </div>
                <div class="column is-6">
                  <router-link :to="'/company/tender/create/section/' + tender.id + '/' + category.id" class="button is-primary is-block">
                    Add Section
                  </router-link>
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

              <v-client-table :columns="section_columns" :options="section_options" :data="sections">
                <span slot="Section" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

                <span slot="#Qs" slot-scope="{row}">
                    <span> {{ row.question_count }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <span class="actions__delete">
                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>
                  </span>

                  <router-link :to="'/company/tender/edit/section/'+tender.id+'/'+category.id+'/'+row.id"
                               class="button is-primary is-small" style="margin-right: 2px;">
                      <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                  </router-link>

                  <router-link :to="'/company/tender/section/questions/' + row.id"
                               class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> View</p>
                  </router-link>
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
              <span class="page__head--title column is-4">
                 Participants
              </span>


                <div class="page__head--links column is-8" style="display: inline !important;">
                    <button type="button" class="button is-primary is-pulled-right" @click="close_category()" v-if="category.is_open === true">
                      Close Category
                    </button>

                    <template v-else>
                      <div class="columns">
                        <div class="column is-6">
                          <router-link :to="'/company/tender/letters/'+tender.id+'/'+category.id" class="button is-primary is-fullwidth" style="margin-right: 2px">
                            Letters
                          </router-link>
                        </div>

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
                  <template v-if="category.is_open === true && category.show_bids">
                    <span>{{ row.company_name }}</span>
                  </template>
                  <template v-if="category.is_open === false">
                    <span>{{ row.company_name }}</span>
                  </template>
                   <template>
                    <span></span>
                  </template>
                </span>

                <span slot="Contact" slot-scope="{row}">
                  <template v-if="category.is_open === true && category.show_bids">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template v-if="category.is_open === false">
                    <span> {{ row.contact_name }}</span>
                  </template>
                  <template>
                    <span></span>
                  </template>

                </span>

                <span slot="Actions" slot-scope="{row}">
<!--                  <span class="actions__edit">-->
<!--                      <font-awesome-icon class="actions__icon" icon="pen-alt"/>-->
<!--                  </span>-->
<!--                  <span class="actions__delete">-->
<!--                      <font-awesome-icon class="actions__icon" icon="trash-alt"/>-->
<!--                  </span>-->

                  <template v-if="category.is_open === false && category.has_qa_instance === true">
                     <router-link :to="'/company/tender/conduct/qa/'+ category.id +'/' + row.id"
                               class="button is-primary is-small">
                      <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Conduct QA</p>
                    </router-link>
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
                <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
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
            <button class="button is-fullwidth is-primary" @click="open_category()">Submit</button>
          </section>
        </div>
      </div>

    <div class="columns">
      <div class="column is-12">
        <div class="modal" id="notifications">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head is-danger">
          <div class="columns">
            <div class="column is-6">
              <h5>Category Notifications</h5>
            </div>
            <div class="column is-6">
              <button class="delete is-pulled-right" @click="closeNotificationsModal" aria-label="close"></button>
            </div>
          </div>

        </header>
        <section class="modal-card-body" style="padding: 2%">
          <div class="tabs">
            <ul>
              <li class="is-active" id="broadcast_tab" @click="show_content('broadcast_notifications')"><a>Broadcast
                Notifications</a></li>
              <li id="email_tab" @click="show_content('email_notifications')"><a>Email Notifications</a></li>
              <li id="sms_tab" @click="show_content('sms_notifications')"><a>SMS Notifications</a></li>
            </ul>
          </div>
          <div class="tab-content" id="tab-content" style="padding-left: 20px; padding-right: 20px">
            <div class="columns" id="broadcast_notifications">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">Level *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select Level</option>
                          <option value="Success">Success</option>
                          <option value="Info">Info</option>
                          <option value="Warning">Warning</option>
                          <option value="Error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Action *</label>
                      <div class="control">
                        <input type="text" class="input" name="action">
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Description *</label>
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

            <div class="columns" id="email_notifications" style="display: none;">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">Level *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select Level</option>
                          <option value="Success">Success</option>
                          <option value="Info">Info</option>
                          <option value="Warning">Warning</option>
                          <option value="Error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="type">
                          <option selected disabled>Select Type</option>
                          <option value="paid">Paid</option>
                          <option value="potential">Potential</option>
                          <option value="qualified"> Qualified </option>
                          <option value="unqualified"> Unqualified </option>
                          <option value="specific"> Specific </option>
                          <option value="responsive">Responsive</option>
                          <option value="non-responsive">Non-Responsive</option>
                        </select>
                      </div>
                    </div>

                    <div class ="hidden_div"  hidden>
                        <label>Bidder *</label>
                        <select name="specific-bidder" id="specific-bidder" multiple>
                          <option v-for="participant in participants" v-bind:key="participant.id" :value="participant.email">{{ participant.company_name }}</option>
                        </select>
                    </div>

                    <div class="select" id="hidden_div_potential" hidden>
                        <label>Type</label>
                        <select name="selection_potential" id="selection_potential"  onchange="toggleFieldsSelection()">
                            <option value="Default">Default</option>
                            <option value="Custom" selected="selected">Custom</option>
                            <option value="Reminder">Reminder</option>
                            <option value="Extension">Extension</option>
                        </select>
                    </div>

                    <div class="select" id="hidden_div_non_responsive" hidden>
                        <select name="nonresponsive_selection" id="nonresponsive_selection" style="max-width: 100%;" onchange="toggleFieldsNonresponsiveSelection()">
                            <option value="Custom" selected="selected">Custom</option>
                            <option value="Reminder">Reminder</option>
                        </select>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Action *</label>
                      <div class="control">
                        <input type="text" class="input" name="action">
                      </div>
                    </div>

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
                      <label>Attach Files *</label>
                      <div class="control">
                        <input type="file" multiple name="files" required>
                      </div>
                    </div>

                    <div class="field">
                      <a  class="button is-block is-primary">Send</a>
                    </div>
                  </form>
                </div>
              </div>
            </div>

            <div class="columns" id="sms_notifications" style="display: none">
              <div class="column is-12">
                <div class="container">
                  <form>
                    <div class="field">
                      <label style="font-weight: bold">To *</label><br>
                      <div class="select is-fullwidth">
                        <select name="level">
                          <option selected disabled>Select</option>
                          <option >All</option>
                          <option >Potential</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Content *</label>
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

        <section class="modal-card-body">
          <!--            <button class="button is-fullwidth is-primary">Submit</button>-->
        </section>
      </div>
    </div>
      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/company/tender";

export default {
  name: "Details",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      participant_columns: ['Company', 'Contact', 'Actions'],
      section_columns: ['Section', '#Qs', 'Actions'],
      participant_options: {
        sortable: ['Company',],
        perPageValues: [20],
        filterable: false,
      },
      section_options: {
        sortable: ['Section',],
        perPageValues: [20],
        filterable: false,
      },
      tender: {},
      category: {},
      participants: [],
      sections: [],
      open_form: {
        "closing_date": ""
      },
    }
  },
  methods: {
    openNotificationsModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeNotificationsModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    show_content(tab) {
      if (tab === 'broadcast_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'block'
        document.getElementById('email_notifications').style.display = 'none'
        document.getElementById('sms_notifications').style.display = 'none'

        document.getElementById('broadcast_tab').classList.add('is-active')
        document.getElementById('email_tab').classList.remove('is-active')
        document.getElementById('sms_tab').classList.remove('is-active')
      } else if (tab === 'email_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'none'
        document.getElementById('email_notifications').style.display = 'block'
        document.getElementById('sms_notifications').style.display = 'none'

        document.getElementById('broadcast_tab').classList.remove('is-active')
        document.getElementById('email_tab').classList.add('is-active')
        document.getElementById('sms_tab').classList.remove('is-active')
      } else if (tab === 'sms_notifications') {
        document.getElementById('broadcast_notifications').style.display = 'none'
        document.getElementById('email_notifications').style.display = 'none'
        document.getElementById('sms_notifications').style.display = 'block'

        document.getElementById('broadcast_tab').classList.remove('is-active')
        document.getElementById('email_tab').classList.remove('is-active')
        document.getElementById('sms_tab').classList.add('is-active')
      }
    },
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
        let response = await tender.category(this.$route.params.tender_id, this.$route.params.category_id)
        this.category = response.data
        this.tender = this.category.tender
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        this.participants = this.category.participants
        this.sections = this.category.sections
        console.log(this.dataPerPage)
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