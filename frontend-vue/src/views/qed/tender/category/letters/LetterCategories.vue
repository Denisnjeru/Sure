<template>
  <div class="dashboard">
    <div class="page__head">
<!--      <div class="columns is-12">-->
        <div class="column is-5">
          <span class="page__head--title">
             Letters > Tender > Categories
          </span>
        </div>

        <div class="column is-7">
          <div class="page__head--links">
        <!--        check if letter exists-->

<!--        <div class="columns">-->
          <div class="column is-3">
            <template>
              <router-link v-if="tender_job.has_custom_letter === false"
                           :to="'/qed/tender/letters/custom/create/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                Custom Letter
              </router-link>
              <router-link v-else-if="tender_job.has_custom_letter === true"
                           :to="'/qed/tender/letters/custom/edit/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                Custom Letter
              </router-link>
            </template>
          </div>
          <div class="column is-3">
            <template>
              <router-link v-if="tender_job.has_dd_letter === false"
                  :to="'/qed/tender/letters/dd/create/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                DD Letter
              </router-link>
              <router-link v-else-if="tender_job.has_dd_letter === true"
                  :to="'/qed/tender/letters/dd/edit/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                DD Letter
              </router-link>
            </template>
          </div>
          <div class="column is-3">
            <template>
              <router-link v-if="tender_job.has_regret_letter === false"
                  :to="'/qed/tender/letters/regret/create/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                Regret Letter
              </router-link>
              <router-link v-else-if="tender_job.has_regret_letter === true"
                  :to="'/qed/tender/letters/regret/edit/'+this.$route.params.job_id"
                           style="margin-right: 2px" class="button is-primary is-small is-block">
                Regret Letter
              </router-link>
            </template>
          </div>
          <div class="column is-3">
            <template>
              <router-link v-if="tender_job.has_success_letter === false"
                  :to="'/qed/tender/letters/success/create/'+this.$route.params.job_id"
                           class="button is-primary is-small is-block">
                Success Letter
              </router-link>
              <router-link v-if="tender_job.has_success_letter === true"
                  :to="'/qed/tender/letters/success/edit/'+this.$route.params.job_id"
                           class="button is-primary is-small is-block">
                Success Letter
              </router-link>
            </template>
          </div>
<!--        </div>-->
      </div>
        </div>
<!--      </div>-->
    </div>

    <div class="page__content columns bottom_content">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__instruction">
            {{ tender_job.title }} Categories
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

          <span slot="Actions" slot-scope="{row}">
              <router-link :to="''+ tender_job.id +'/' + row.id" class="button is-primary is-small">
                <span><font-awesome-icon class="view__icon" icon="eye"/> View</span>
              </router-link>
            </span>
        </v-client-table>

      </div>
      <div class="page__pagination">
        <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getCategories()">
        </pagination>
      </div>
    </div>
  </div>
</template>

<script>
import tender from "@/services/qed/tender";

export default {
  name: "LetterCategories",
  data() {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 10,
      columns: ['Category Title', 'Category Code', 'Actions'],
      options: {
        sortable: ['Category Title', 'Category Code',],
        perPageValues: [20],
        filterable: false,
      },
      tender_job: {},
      categories: [],
      template_url: '',
    }
  },
  methods: {
    async getTender() {
      try {
        let response = await tender.tender_letter_details(this.$route.params.job_id)
        this.tender_job = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getCategories() {
      try {
        let response = await tender.categories(this.$route.params.job_id, this.page)
        this.categories = response.data['results']
        this.dataCount = response.data['count']
        console.log(this.dataPerPage)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getTender()
    this.getCategories()
  }
}
</script>
<style lang="scss" scoped>
@include page;

.page__content {
  margin: 0 !important;
  @include grid_column;
}

.is-primary {
  background-color: #073A82 !important;
}

//.VueTables__table tbody td {
//    padding: 5px 24px;
//}
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