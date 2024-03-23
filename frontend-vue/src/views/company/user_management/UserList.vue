<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Company Users
            </span>

            <div class="page__head--links">
                    <router-link to="/company/create/user" class="button is-primary">
                        Add New User
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

              <v-client-table :columns="columns" :options="options" :data="users">
                <span slot="Name" slot-scope="{row}">
                    <span> {{ row.first_name }} {{ row.last_name }}</span>
                </span>

                <span slot="Email" slot-scope="{row}">
                    <span> {{ row.email }}</span>
                </span>

                <span slot="Status" slot-scope="{row}">
                    <span v-if="row.is_active === true"> Active</span>
                    <span v-else>In-Active</span>
                </span>

                <span slot="Role" slot-scope="{row}">
                    <span> {{ row.buyer_role.name }}</span>
                </span>

                <span slot="Last Login" slot-scope="{row}">
                    <span> {{ row.last_login }}</span>
                </span>

                <span slot="Resend Invitation Email">
                    <button type="button" class="button is-primary is-block">Send</button>
                </span>

                <span slot="Actions" slot-scope="{row}">
<!--                  <span class="actions__edit">-->
<!--                      <font-awesome-icon class="actions__icon" icon="pen-alt" />-->
<!--                  </span>-->
<!--                  <span class="actions__delete">-->
<!--                      <font-awesome-icon class="actions__icon" icon="trash-alt" />-->
<!--                  </span>-->
                  <button type="button" v-if="row.is_active === true" class="button is-success" >Activate</button>
                  <button type="button" v-else class="button is-warning" >De-Activate</button>
<!--                  <button @click="prequalDetails(row)" class="button is-primary is-small">-->
<!--                    <p><font-awesome-icon class="view__icon" icon="eye"></font-awesome-icon> Categories</p>-->
<!--                  </button>-->
                </span>

                <span slot="Date Joined" slot-scope="{row}">
                    <span> {{ row.date_joined }}</span>
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
  name: "UserList",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Name', 'Email', 'Status', 'Role', 'Last Login', 'Resend Invitation Email', 'Actions', 'Date Joined'],
      options: {
        sortable: ['Name', 'Email', 'Status', 'Role', 'Last Login',],
        perPageValues: [20],
        filterable: false,
      },
      users: []
    }
  },
  methods: {
    // prequalDetails(row){
    //   this.$router.push(`/company/prequalification/details/${row.id}`)
    // },
    async search() {
        console.log('search');
    },
    async getUsers(){
      try{
        let response = await user_management.users()
        this.users = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.getUsers()
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