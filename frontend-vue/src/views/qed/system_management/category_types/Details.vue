<template>
<div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Category Types
            </span>

      <div class="page__head--links">
      </div>
    </div>

    <div class="page__content columns top_content" style="align-items: inherit !important;">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__instruction">
            Category Types
          </p>
          <div class="table-search__search">
            <font-awesome-icon class="table-search__search--icon" icon="search"/>
            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
          </div>
        </div>

        <v-server-table :columns="columns" :options="options">
          <template slot="Country" slot-scope="row">
            <span>{{ row.row.name }}</span>
          </template>

          <template slot="Criteria" slot-scope="row">
            <span v-if="row.row.criteria !== 'No criteria available'">
              <a :href="backend_url  + row.row.criteria.file_url" download="download">
                Download Criteria</a>
            </span>
            <span v-else>
              {{ row.row.criteria }}
            </span>
          </template>

          <template slot="Actions" slot-scope="row">

            <router-link v-if="row.row.criteria !== 'No criteria available'"
                         :to="'/qed/category/criteria/edit/'+$route.params.id+'/'+row.row.criteria.id" class="button is-small is-warning">
              <span><font-awesome-icon class="view__icon" icon="pencil-alt"/> Edit Criteria</span>
            </router-link>

            <router-link v-if="row.row.criteria === 'No criteria available'"
                         :to="'/qed/category/criteria/create/'+ $route.params.id + '/'+row.row.id" class="button is-small is-warning">
              <span><font-awesome-icon class="view__icon" icon="pencil-alt"/> Edit Criteria</span>
            </router-link>

            <router-link :to="'#'+row.id" class="button is-small is-danger" style="margin-left: 2px;">
              <span><font-awesome-icon class="view__icon" icon="trash-alt"/> Delete</span>
            </router-link>

<!--            <router-link :to="'#'+row.id" class="button is-small is-primary" style="margin-left: 2px;">-->
<!--              <span><font-awesome-icon class="view__icon" icon="eye"/> View</span>-->
<!--            </router-link>-->
          </template>

        </v-server-table>

      </div>

    </div>
  </div>
</template>

<script>
import category_types from "@/services/qed/category_types";

export default {
  name: "Details",
  data() {
    return {
      category_type: {},
      backend_url: process.env.VUE_APP_DOWNLOAD_URL,
      page: 1,
      columns: ['Country', 'Criteria', 'Actions'],
      options: {
        perPageValues: [10],
        sortable: ['Country', ],
        texts: {
          loadingError: 'Oops! Something went wrong'
        },
        async requestFunction(data) {
          console.log(data)
          try {
            let response = await category_types.category_type_countries(this.$route.params.id,this.page)
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
  methods: {
    async get_category_type(){
      try{
        let response = await category_types.category_type(this.$route.params.id)
        if (response.status === 200){
          this.category_type = response.data
        }else{
          window.toast.fire({icon: 'error', title: 'An error occured, please try again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_category_type()
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

.page .table-search[data-v-e49b950c] {
  padding: 12px 6px
}

.VueTables__table tbody td {
  padding: 5px 24px;
}

.is-primary {
  background-color: #073A82 !important;
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