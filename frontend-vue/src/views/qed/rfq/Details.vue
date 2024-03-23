<template>
  <div>
    <div class="dashboard">
      <div class="page__head">
            <span class="page__head--title">
               RFQ Job Details > 
            </span>

        <div class="page__head--links">

        </div>
      </div>

      <div class="page__content columns top_content" style="align-items: inherit !important;">
        <div class="column-details column">
            <div class="column-details__head">
              <p class="column-details__head--title">Job Title: {{ rfq.title }} </p>
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
              <template>
                <div class="field">
                  <label class="label">Upload Category Suppliers<span class="required"> *</span></label>
                  <div class="control">
                    <input class="input" type="file" @change="uploadCategorySuppliers($event)" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                  </div>
                </div>
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
                 <router-link :to="'/qed/rfq/job/reports/' + rfq.id" class="button is-primary is-block">
                  View Reports
                 </router-link>
                <!-- <a href="#" class="button is-primary is-block">View Reports</a> -->
              </div>
              <div class="column is-2">

              </div>
            </div>

            <!-- <div class="columns">
              <div class="column is-2">

              </div>
              <div class="column is-8">
                <a href="#" class="button is-primary is-block">Supplier Documents Update</a>
              </div>
              <div class="column is-2">

              </div>
            </div> -->

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
                <a href="#" class="button is-primary is-block">Send Job Notifications</a>
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
          <router-link :to="'/qed/rfq/create/category/' + rfq.id" class="button is-primary">
            Add Category
          </router-link>
        </div>
      </div>
      <div class="page__content columns bottom_content">
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
                <span slot="Category Title" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

            <span slot="Category Code" slot-scope="{row}">
                    <span> {{ row.unique_reference }}</span>
                </span>

            <span slot="Status" slot-scope="{row}">
                    <span v-if="row.status_open === true"> Open</span>
                    <span v-else > Closed</span>
                </span>

            <span slot="Actions" slot-scope="{row}">
              <template v-if="row.is_open === false && row.has_participants === true">
                <button class="button is-danger" style="margin-right: 2px">
                  <p><font-awesome-icon class="view__icon" icon="trash-alt"/></p>
                </button>
              </template>

              <template v-if="row.is_open === false">
                <router-link
                    :to="'/qed/rfq/edit/category/'+ rfq.id + '/' + row.id"
                    class="button is-primary" style="margin-right: 2px">
                    <p><font-awesome-icon class="view__icon" icon="pencil-alt"/></p>
                </router-link>
              </template>

              <router-link :to="'/qed/rfq/category/details/'+ rfq.id +'/' + row.id"
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
  </div>
</template>

<script>
import rfq from "@/services/qed/rfq";
import {mapGetters} from 'vuex'

export default {
  name: "RfqDetails",
  data() {
    return {
      page: 2,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Category Title', 'Category Code', 'Status', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Code', 'Status'],
        perPageValues: [20],
        filterable: false,
      },
      rfq: {},
      categories: [],
    }
  },
  computed: {
      ...mapGetters('Qed', ['selectedBuyer']),
  },    
  methods: {
    async search() {
      console.log('search');
    },
    async fetchData() {
      console.log(this.page);
    },
    async uploadCategorySuppliers(event){
      let f = event.target.files[0]
      let form_data = new FormData()
      form_data.append('category_suppliers', f, f.name)

      try{
        let response = await rfq.upload_category_suppliers(this.rfq.id, form_data)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: response.data['response_message']})
          this.$router.push(`/qed/rfq/cat/suppliers/progress/${this.rfq.id}/${response.data['task_id']}`)
        }else{
          window.toast.fire({icon: 'error', title: response.data['response_message']})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getRfq() {
      try {
        let response = await rfq.rfq(this.$route.params.id, this.selectedBuyer.id)
        this.rfq = response.data
        console.log(this.rfq)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await rfq.categories(this.$route.params.id)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
        console.log(this.dataPerPage)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    openModal() {
      document.getElementById('notifications').classList.add('is-active');
    },
    closeModal() {
      document.getElementById('notifications').classList.remove('is-active');
    },
  },
  mounted() {
    this.getRfq()
    this.getCategories()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.page{
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
.top_content{
  display: flex; justify-content: space-between; align-items: center;
}
.bottom_content{
  display: flex; flex-flow: column nowrap; justify-content: space-between;align-items: center;
}
.is-primary {
  background-color: #073A82 !important;
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