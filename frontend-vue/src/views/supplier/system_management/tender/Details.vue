<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Tender Jobs > {{ tender.title }}
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
            <template v-if="tender.has_participants === false && tender.is_open === false">
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
            <p class="column-details__head--desc">Job Actions </p>
            <hr>
          </div>
          <!-- Form Details -->
          <div class="column-details__content">
            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">View Reports</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">Supplier Documents Update</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">Zip Files</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

            <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a @click="openModal" class="button is-primary is-block">Send Job Notifications</a>
              </div>
              <div class="column is-2">

              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               Categories belonging to this job
            </span>

        <div class="page__head--links">
          <router-link :to="'/company/tender/create/category/' + tender.id" class="button is-primary">
            Add Category
          </router-link>
        </div>
      </div>
      <div class="page__content columns bottom_content">
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

          <v-client-table :columns="columns" :options="options" :data="categories">
                <span slot="Category Title" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

            <span slot="Category Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

            <span slot="Status" slot-scope="{row}">
                    <span v-if="row.is_open === true"> Open</span>
                    <span v-if="row.is_open === false"> Closed</span>
                </span>

            <span slot="Actions" slot-scope="{row}">
              <template v-if="row.is_open === false && row.has_participants === true">
                <button class="button is-danger is-small" style="margin-right: 2px">
                  <p><font-awesome-icon class="view__icon" icon="trash-alt"/></p>
                </button>
              </template>

              <template v-if="row.is_open === false">
                <router-link
                    :to="'/company/tender/edit/category/'+tender.id + '/' + row.id"
                    class="button is-primary is-small" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                </router-link>

                <template>
                  <button v-if="row.has_dd_instance === false" @click="open_dd_confirm_alert(row)"
                          class="button is-primary is-small" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="hammer"></font-awesome-icon> DD</p>
                  </button>
                  <router-link :to="'/company/tender/dd/details/'+row.id" v-else-if="row.has_dd_instance === true"
                               class="button is-primary is-small" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="shield-alt"></font-awesome-icon> DD</p>
                </router-link>
                </template>


                <button v-if="row.has_qa_instance === false"
                        @click="open_qa_confirm_alert(row)"
                        class="button is-primary is-small" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="shield-alt"></font-awesome-icon> QA</p>
                </button>

                <router-link :to="'/company/tender/qa/instructions/'+row.id" v-else-if="row.has_qa_instance === true"
                             class="button is-primary is-small" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="shield-alt"></font-awesome-icon> QA</p>
                </router-link>

              </template>

              <router-link :to="'/company/tender/category/details/'+ tender.id +'/' + row.id"
                           class="button is-primary is-small">
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
      <div class="column is-6"></div>
      <div class="column is-6">
        <div class="modal" id="notifications">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head is-danger">
          <div class="columns">
            <div class="column is-6">
              <h5>Job Notifications</h5>
            </div>
            <div class="column is-6">
              <button class="delete is-pulled-right" @click="closeModal" aria-label="close"></button>
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
                          <option value="success">Success</option>
                          <option value="info">Info</option>
                          <option value="warning">Warning</option>
                          <option value="error">Error</option>
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
                          <option value="success">Success</option>
                          <option value="info">Info</option>
                          <option value="warning">Warning</option>
                          <option value="error">Error</option>
                        </select>
                      </div>
                    </div>

                    <div class="field">
                      <label style="font-weight: bold">Type *</label><br>
                      <div class="select is-fullwidth">
                        <select name="type">
                          <option selected disabled>Select Type</option>
                          <option >Paid</option>
                          <option >Potential</option>
                          <option >Qualified</option>
                          <option >Unqualified</option>
                          <option >Non-Responsive</option>
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
      columns: ['Category Title', 'Category Code', 'Status', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Code', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      tender: {},
      categories: [],
    }
  },
  methods: {
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
    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    openModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
    async getPrequal() {
      try {
        let response = await tender.tender(this.$route.params.id)
        this.tender = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await tender.categories(this.page)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.dataPerPage)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async initiate_qa(row) {
      let content = {
        "category": row.id,
        "title": row.name
      }
      try {
        let response = await tender.initiate_qa(content, row.id)
        console.log(response)
        window.toast.fire({icon: 'success', title: 'Quality assurance initiated successfully'})
        this.$router.push(`/company/tender/qa/instructions/${row.id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async initiate_dd(row) {
      let content = {
        "category": row.id,
        "title": row.name
      }
      try {
        let response = await tender.initiate_dd(content, row.id)
        console.log(response)
        window.toast.fire({icon: 'success', title: 'Due diligence initiated successfully'})
        this.$router.push(`/company/tender/dd/details/${row.id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    open_qa_confirm_alert(row) {
      let self = this
      this.$swal.fire({
        title: 'Quality Assurance',
        icon: 'info',
        html:
            'Are you sure you want to initiate the quality assurance process ??',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonColor: '#073A82',
        confirmButtonText:
            '<i class="fa fa-thumbs-up"></i> Confirm',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        cancelButtonText:
            '<i class="fa fa-thumbs-down"></i>Cancel',
        cancelButtonAriaLabel: 'Thumbs down',
      }).then(function (isConfirm) {
        if (isConfirm) {
          self.initiate_qa(row)
        }
      })
    },
    open_dd_confirm_alert(row) {
      let self = this
      this.$swal.fire({
        title: 'Due Diligence',
        icon: 'info',
        html:
            'Are you sure you want to initiate the due diligence process ??',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonColor: '#073A82',
        confirmButtonText:
            '<i class="fa fa-thumbs-up"></i> Confirm',
        confirmButtonAriaLabel: 'Thumbs up, great!',
        cancelButtonText:
            '<i class="fa fa-thumbs-down"></i>Cancel',
        cancelButtonAriaLabel: 'Thumbs down',
      }).then(function (isConfirm) {
        if (isConfirm) {
          self.initiate_dd(row)
        }
      })
    },
  },
  mounted() {
    this.getPrequal()
    this.getCategories()
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
  margin-left: 36%; width: 560px; background-color: #ffffff !important; border-radius: 12px;
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
hr {
  margin: 0.5rem 0 !important;
}
</style>