<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard > Buyers > <span class="title__active">QED Solutions Limited</span>
            </span>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-details">
                <div class="column-details__head head-row">
                    <span class="head-row__left head-row__row">
                        <img class="logo head-row__image" src="@/assets/qed-logo.png" alt="">
                        <h3 class="column-details__head--title">QED Solutions Limited</h3>
                    </span>

                    <span class="head-row__right head-row__row">
                        <router-link to="/qed/buyers/1/users/create">
                            <a class="button head-row__row--button blue-button">
                                View Asset Disposals
                            </a>
                        </router-link>
                        <router-link to="/qed/buyers/1/users/create">
                            <a class="button head-row__row--button blue-button">
                               View Auctions
                            </a>
                        </router-link>
                        <router-link to="/qed/buyers/1/users/create">
                            <a class="button head-row__row--button blue-button">
                               View Jobs
                            </a>
                        </router-link>
                    </span>
                </div>
                <div class="column-details__content content-row">
                    <div class="content-row__2">
                        <p class="detail">
                            <span class="detail__title">Initials:</span>
                            <span class="detail__text">QST</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">KRA PIN:</span>
                            <span class="detail__text">P0514110079F</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">Country:</span>
                            <span class="detail__text">Kenya</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">System Users:</span>
                            <span class="detail__text">3</span>
                        </p>
                    </div>
                    <div class="content-row__2">
                        <p class="detail">
                            <span class="detail__title">Contact person:</span>
                            <span class="detail__text">John Doe</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">Phone:</span>
                            <span class="detail__text">0722121212</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">Jobs:</span>
                            <span class="detail__text">2</span>
                        </p>
                        <p class="detail">
                            <span class="detail__title">Roles:</span>
                            <span class="detail__text">
                                <a>Administrator</a>
                                &nbsp;-&nbsp;
                                <a class="Active">All roles</a>
                            </span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="page__head">
            <span class="page__head--title">
                Users
            </span>
            <div class="page__head--links">
                <router-link to="/qed/buyers/1/users/create">
                    <a class="page__head--link button button-link">
                        Add New User
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Company Users
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="users" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="users.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <router-link :to="'/qed/buyers/' + row.id + '/buyer'" class="standard-column link" slot="name" slot-scope="{row}">
                        {{row.name}}
                    </router-link>

                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/qed/buyers/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete" @click="deleteUser()">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>
     
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getBuyers()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
    name: 'QedBuyers',
    data() {
        return {
            columns: ['#', 'name', 'email', 'creation_date', 'last_login', 'actions'],
            options: {
                sortable: ['company', 'initial'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            users: [
                {
                    "id": 1,
                    "name": 'John Doe',
                    "email": 'johndoe@qedsolutions.co.ke',
                    "creation_date": "Feb. 9, 2022, 12:37 p.m.",
                    "last_login": "June. 9, 2022,9:37 a.m."
                }
            ]
        }
    },
    computed: {
        ...mapGetters('Auth', ['authUser']),
    },
    mounted() {
        this.getBuyer()
    },
    methods: {
        selectJob: function() {
        },
        async getBuyer() {
            try {
                console.log()
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        deleteUser() {
            this.$swal({
                text: 'This user will be permanently deleted',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    alert('done')             
                }
            });
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}

</style>
