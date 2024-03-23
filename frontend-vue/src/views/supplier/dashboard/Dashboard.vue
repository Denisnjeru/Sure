<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard
            </span>
        </div>
        <div class="page__content columns">     
            <div class="stats">
                <router-link  class="stat" to="user/users">
                    <span class="stat__icon-container stat1">
                        <img src="@/assets/total-bidders.png" alt="total bidders" class="stat__icon-container--icon">
                    </span>
                    <span class="stat__info">
                        <span class="stat__info--title">Users</span>
                        <span class="stat__info--desc" v-if="dashboardStats">{{dashboardStats.users}}</span>
                        <span class="stat__info--desc" v-else>
                            <div class="snippet" data-title=".dot-pulse">
                            <div class="stage">
                                <div class="dot-pulse"></div>
                            </div>
                            </div>
                        </span>
                    </span>
                </router-link >                    
                <router-link class="stat" :to="'ongoingbids'">
                    <span class="stat__icon-container stat2">
                        <img src="@/assets/live.png" alt="live" class="stat__icon-container--icon">
                    </span>
                    <span class="stat__info">
                        <span class="stat__info--title">Ongoing Bids</span>
                        <span class="stat__info--desc" v-if="dashboardStats">{{dashboardStats.live_bids}}</span>
                        <!-- <span class="stat__info--desc" v-else>
                            <font-awesome-icon class="loading-icon" icon="circle-notch" />
                        </span> -->
                        <span class="stat__info--desc" v-else>
                            <div class="snippet" data-title=".dot-pulse">
                            <div class="stage">
                                <div class="dot-pulse"></div>
                            </div>
                            </div>
                        </span>
                    </span>
                </router-link>
                <router-link class="stat" :to="'closedbids'">
                    <span class="stat__icon-container stat3">
                        <img src="@/assets/lock.png" alt="live" class="stat__icon-container--icon">
                    </span>
                    <span class="stat__info">
                        <span class="stat__info--title">Closed Bids</span>
                        <span class="stat__info--desc" v-if="dashboardStats">{{dashboardStats.closed_bids}}</span>
                        <span class="stat__info--desc" v-else>
                            <div class="snippet" data-title=".dot-pulse">
                            <div class="stage">
                                <div class="dot-pulse"></div>
                            </div>
                            </div>
                        </span>
                    </span>
                </router-link>
                <router-link class="stat" :to="'/supplier/dashbard/letters'">
                    <span class="stat__icon-container stat4">
                        <img src="@/assets/list-interface.png" alt="live" class="stat__icon-container--icon">
                    </span>
                    <span class="stat__info">
                        <span class="stat__info--title">Award & Regret Letters</span>
                        <span class="stat__info--desc savings-desc" v-if="dashboardStats">{{dashboardStats.letters}}</span>
                        <span class="stat__info--desc" v-else>
                            <div class="snippet" data-title=".dot-pulse">
                            <div class="stage">
                                <div class="dot-pulse"></div>
                            </div>
                            </div>
                        </span>
                    </span>
                </router-link>
            </div>
            <br>
            <br>      
            <div class="column is-12 column-page">
                
                <div class="table-search">
                    <p class="table-search__title">
                        Companies With  Open Jobs
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="companies" :options="options" class="hasRowNo hasNoWrap">
                    <p class="row-no" v-if="companies.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    <p slot="company" class="hasLogo" slot-scope="{row}">
                        <img class="logo" :src="row.company_logo_url" alt="">
                        <span>{{row.company_name}}</span>
                    </p>

                    
                    <p slot="job"  slot-scope="{row}">
                        {{row.tenders}} Tenders {{row.prequals}} Prequalifications
                    </p>

                    <router-link class="link Active"  slot-scope="{row}" slot="view" :to="'/supplier/dashboard/company/'+row.id+'/jobs'">
                        Categories &nbsp; <font-awesome-icon icon="chevron-right" />
                    </router-link>

                </v-client-table>
                <div class="page__pagination" v-if="companies.length > 0">
                    <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getCompaniesWithOpenJobs()">
                    </pagination>
                </div>
            </div>
            
        </div>        
    </div>
</template>

<script>
import dashboard from '@/services/supplier/dashboard'
export default {
    name: 'SupplierDashboard',
    data() {
        return {
            columns: ['#', 'company', 'view'],
            options: {
                editableColumns:['company'],
                sortable: ['company', 'job'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            companies: [],
            dashboardStats: null
        }
    },
    mounted() {
        this.dataCount = 1
        this.getStats()
        this.getCompaniesWithOpenJobs()
    },
    methods: {
        async fetchData() {
            console.log(this.page);
        },
        async search() {
            console.log('search');
        },
        async getStats() {
            try {
                const response = await dashboard.stats()
                this.dashboardStats = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getCompaniesWithOpenJobs() {
            try {
                const response = await dashboard.companiesWithOpenJobs()
                this.companies = response.data.results
                this.dataCount =  response.data.count
            } catch (err) {
                console.log(err)
            }
        },
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}

.loading-icon {
    animation: rotation 3s linear infinite;
}

@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}

.dot-pulse {
  position: relative;
  left: -9999px;
  width: 10px;
  height: 6px;
  border-radius: 5px;
  background-color: #344767;
  color: #344767;
  box-shadow: 9999px 0 0 -5px #344767;
  animation: dotPulse 1.5s infinite linear;
  animation-delay: .25s;
}

.dot-pulse::before, .dot-pulse::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
  width: 10px;
  height: 6px;
  border-radius: 5px;
  background-color: #344767;
  color: #344767;
}

.dot-pulse::before {
  box-shadow: 9984px 0 0 -5px #344767;
  animation: dotPulseBefore 1.5s infinite linear;
  animation-delay: 0s;
}

.dot-pulse::after {
  box-shadow: 10014px 0 0 -5px #344767;
  animation: dotPulseAfter 1.5s infinite linear;
  animation-delay: .5s;
}

@keyframes dotPulseBefore {
  0% {
    box-shadow: 9984px 0 0 -5px #344767;
  }
  30% {
    box-shadow: 9984px 0 0 2px #344767;
  }
  60%,
  100% {
    box-shadow: 9984px 0 0 -5px #344767;
  }
}

@keyframes dotPulse {
  0% {
    box-shadow: 9999px 0 0 -5px #344767;
  }
  30% {
    box-shadow: 9999px 0 0 2px #344767;
  }
  60%,
  100% {
    box-shadow: 9999px 0 0 -5px #344767;
  }
}

@keyframes dotPulseAfter {
  0% {
    box-shadow: 10014px 0 0 -5px #344767;
  }
  30% {
    box-shadow: 10014px 0 0 2px #344767;
  }
  60%,
  100% {
    box-shadow: 10014px 0 0 -5px #344767;
  }
}


.stats {
    width: 100%;
    @include grid_row;
    justify-content: space-between;

    .stat {
        width: 22.5%;
        height: 12.5vh;
        background-color: $color-white-main;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
        border-radius: $line-height/2;
        padding: $line-height/1.5;
        @include grid_row;
        align-items: flex-end;

        &__icon-container {
            border-radius: $line-height/2;
            padding: $line-height/2.5 $line-height/2.5;
            @include grid_row;
            align-items: center;

            &--icon {
                height: $line-height/1.25;

                @media screen and (min-width: 1600px) {
                    height: $line-height;
                }
            }
        }

        .stat1 {
            background: linear-gradient(180deg, #4A4A4A 0%, #202020 100%);
        } 
        
        .stat2 {
            background: linear-gradient(180deg, #E93B77 0%, #DA1F63 100%);
        } 

        .stat3 {
            background: linear-gradient(180deg, #439DEE 0%, #1E78E9 100%);
        } 

        .stat4 {
            background: linear-gradient(180deg, #63B967 0%, #4BA64F 100%);
        } 

        &__info {
            @include grid_column;
            align-items: flex-end;

            &--title {
                font-weight: 300;
                font-size: 14px;
                text-align: right;
                color: #7B809A;

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-normal;
                }
            }

            &--desc {
                color: #344767;
                text-align: right;
                font-weight: 700;
                font-size: 18px;
                width: auto;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;

                @media screen and (min-width: 1600px) {
                    font-size: 20px;
                }
            }

            .savings-desc {
                font-size: $font-size-text;
                width: auto;

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-normal;
                }
            }
        }
    }
}
</style>
