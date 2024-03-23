<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Company Roles
            </span>

            <div class="page__head--links">
                    <router-link to="/company/create/role" class="button is-primary">
                        Add New Role
                    </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Users
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="roles">
                <span slot="Role" slot-scope="{row}">
                    <span> {{ row.name }}</span>
                </span>

                <span slot="Description" slot-scope="{row}">
                    <span> {{ row.description }}</span>
                </span>

                <span slot="Actions">
                  <span class="actions__edit">
                      <font-awesome-icon class="actions__icon" icon="pen-alt" />
                  </span>
                  <span class="actions__delete">
                      <font-awesome-icon class="actions__icon" icon="trash-alt" />
                  </span>

<!--                  <button @click="prequalDetails(row)" class="button is-primary is-small">-->
<!--                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Categories</p>-->
<!--                  </button>-->
                </span>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import user_management from "@/services/company/user_management";

export default {
  name: "RoleList",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Role', 'Description', 'Actions'],
      options: {
        sortable: ['Role', 'Description',],
        perPageValues: [20],
        filterable: false,
      },
      roles: []
    }
  },
  methods: {
    async search() {
        console.log('search');
    },
    async getRoles(){
      try{
        let response = await user_management.roles()
        this.roles = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getRoles()
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
</style>