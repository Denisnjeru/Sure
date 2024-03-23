<template>
<div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Category Types
            </span>

      <div class="page__head--links">
        <router-link to="/qed/category/types/create" class="button is-primary is-pulled-right">New Category Type</router-link>
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
          <template slot="Title" slot-scope="row">
            <span>{{ row.row.name }}</span>
          </template>

          <template slot="Initials" slot-scope="row">
            <span>{{ row.row.innitials }}</span>
          </template>

          <template slot="Group" slot-scope="row">
            <span>{{ row.row.category_group.name }}</span>
          </template>

          <template slot="Actions" slot-scope="row">

            <div class="dropdown" :id="'row_'+row.row.id">
              <div class="dropdown-trigger">
                <button class="button is-primary is-small" @click="show_category_options(row.row)" aria-haspopup="true"
                        aria-controls="dropdown-menu3">
                  <span>Actions <font-awesome-icon
                      class="view__icon" icon="angle-down"/></span>
                  <span class="icon is-small">
                            <i class="angle-down" aria-hidden="true"></i>
                          </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                <div class="dropdown-content">
                  <router-link :to="'/qed/category/types/edit/'+row.row.id" class="dropdown-item">
                    <span><font-awesome-icon class="view__icon" icon="pencil-alt"/> Edit</span>
                  </router-link>
                  <hr class="dropdown-divider">
                  <router-link :to="'#'+row.id" class="dropdown-item">
                    <span><font-awesome-icon class="view__icon" icon="trash-alt"/> Delete</span>
                  </router-link>
                  <hr class="dropdown-divider">
                  <router-link :to="'/qed/category/type/'+row.row.id" class="dropdown-item">
                    <span><font-awesome-icon class="view__icon" icon="eye"/> View</span>
                  </router-link>
                </div>
              </div>
            </div>
          </template>

        </v-server-table>

      </div>

    </div>
  </div>
</template>

<script>
import category_types from "@/services/qed/category_types";

export default {
  name: "CategoryTypeList",
  data() {
    return {
      page: 1,
      columns: ['Title', 'Initials', 'Group', 'Actions'],
      options: {
        perPageValues: [10],
        sortable: ['Title', 'Initials', 'Group'],
        texts: {
          loadingError: 'Oops! Something went wrong'
        },
        async requestFunction(data) {
          console.log(data)
          try {
            let response = await category_types.category_types(this.page)
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
    show_category_options(row) {
      let element = document.getElementById('row_' + row.id)
      if (element.classList.contains('is-active')) {
        element.classList.remove('is-active')
      } else {
        element.classList.add('is-active')
      }
    },
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