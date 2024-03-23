<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard
            </span>

            <div class="page__head--links">
                <select class="page__head--link select-dropdown">
                    <option value="monthy" >Past Day</option>
                    <option value="monthy" >Past Week</option>
                    <option value="monthy" selected>Past Month</option>
                    <option value="monthy" >Past 3 Months</option>
                    <option value="monthy" >Past 3 Months</option>
                </select>
                <span class="page__head--link action-button">
                    <font-awesome-icon class="action-button__icon" icon="print" />
                </span>
                <span class="page__head--link action-button">
                    <font-awesome-icon class="action-button__icon" icon="download" />
                </span>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="stats">
                    <router-link class="stat" :to="'buyers'">
                        <span class="stat__icon-container stat1">
                            <img src="@/assets/total-bidders.png" alt="total bidders" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Buyers</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.buyers}}</span>
                            <span class="stat__info--desc savings-desc" v-else>-</span>
                        </span>
                    </router-link>                    
                    <router-link class="stat" :to="'suppliers'">
                        <span class="stat__icon-container stat2">
                            <img src="@/assets/live.png" alt="live" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Suppliers</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.suppliers}}</span>
                            <span class="stat__info--desc savings-desc" v-else>-</span>
                        </span>
                    </router-link>
                    <router-link class="stat" :to="'/qed/jobs/buyers/'">
                        <span class="stat__icon-container stat3">
                            <img src="@/assets/list-interface.png" alt="live" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Jobs</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.jobs}}</span>
                            <span class="stat__info--desc savings-desc" v-else>-</span>
                        </span>
                    </router-link>
                    <router-link class="stat" :to="'savings'">
                        <span class="stat__icon-container stat4">
                            <img src="@/assets/save-money.png" alt="live" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Savings</span>
                            <span class="stat__info--desc savings-desc">-</span>
                        </span>
                    </router-link>
                </div>
                <div class="graphs">
                    <div class="graph line">
                        <div class="line-graph line-1">
                            <div class="line-graph__graph">
                                <span v-if="monthlySupplierRegistration !== null">
                                    <BarChart :dates="monthlySupplierRegistration.supplier_registration.dates" :values="monthlySupplierRegistration.supplier_registration.reg_count" :chartHeight="'145%'" />
                                </span>
                            </div>
                        </div>
                        <div class="line-details">
                            <p class="graph__title">Monthly Supplier Registration</p>
                            <p class="graph__desc">Supplier Registration Per Month (Last 12 Months)</p>
                        </div>
                    </div>
                    <div class="graph line ">
                        <div class="line-graph line-2">
                            <div class="line-graph__graph">
                                <span v-if="monthlyBids !== null">
                                    <LineChart :dates="monthlyBids.monthly_bids.dates" :values="monthlyBids.monthly_bids.bids_count" :chartHeight="'145%'" />
                                </span>
                            </div>
                        </div>
                        <div class="line-details">
                            <p class="graph__title">Bids(Last Six Months)</p>
                            <p class="graph__desc">Bids Per Month (Last 6 Months)</p>
                        </div>
                    </div>
                </div>
                <div class="dash-table">
                    <p class="dash-table__title">Live jobs</p>
                    <v-client-table :columns="columns" :data="liveJobs" :options="options" class="hasRowNo hasNoWrap">
                        <p class="row-no" v-if="liveJobs.length !== 0" slot="#" slot-scope="props">
                            {{props.index}}
                        </p>
                        <p slot="company" class="hasLogo" slot-scope="{row}">
                            <img class="logo" :src="row.company.company_logo_url" alt="">
                            <span>{{row.company.company_name}}</span>
                        </p>

                        <p class="link" slot="job"  slot-scope="{row}">
                            {{row.title}}
                        </p>

                        <p class="capitalize" slot="type" slot-scope="{row}">
                            {{row.sourcing_activity}}
                        </p>

                        <p class="small-centered" slot="responsive_Bidders" slot-scope="{row}">
                            {{row.responsive_bidders}}
                        </p>

                    </v-client-table>
                </div>
            </div>
        </div>        
    </div>
</template>

<script>
const LineChart = () => import('@/components/charts/LineChart')
const BarChart = () => import('@/components/charts/BarChart')
import dashboard from '@/services/qed/dashboard'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'company', 'job', 'type', 'responsive_Bidders'],
            options: {
                editableColumns:['company'],
                sortable: ['company', 'job'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            dashboardStats: null,
            liveJobs: [],
            monthlySupplierRegistration: null,
            monthlyBids: null
        }
    },
    components: {
        LineChart,
        BarChart
    },
    mounted() {
        this.getStats()
        this.getLiveJobs()
        this.getSupplierRegistration()
        this.getMonthlyBids()
    },
    methods: {
        async getStats() {
            try {
                const response = await dashboard.stats()
                this.dashboardStats = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getSupplierRegistration() {
            try {
                const response = await dashboard.monthlySupplierRegistration()
                this.monthlySupplierRegistration = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getMonthlyBids() {
            try {
                const response = await dashboard.monthlyBids()
                this.monthlyBids = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getLiveJobs() {
            try {
                const response = await dashboard.liveJobs()
                this.liveJobs = response.data.results
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

.select-dropdown {
    padding: $line-height/2;
    border: none;
    border-radius: $line-height/6;
    background-color: #F7F9FA;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1), 0px 4px 10px rgba(0, 0, 0, 0.1);

    &:focus {
        outline: none;
    }
}

.action-button {
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1), 0px 4px 10px rgba(0, 0, 0, 0.1);    
    padding: $line-height/3 $line-height/2;
    cursor: pointer;
    border-radius: $line-height/6;

    &:hover {
        background-color: #e1eaee;
    }

    &__icon {
        font-size: $font-size-small;
    }
}

.column-page {
    box-shadow: none !important;
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

.graphs {
    margin: $line-height*1.5 0;
    width: 100%;
    @include grid_row;
    justify-content: space-between;

    .graph {
        height: 45vh;
        background-color: $color-white-main;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
        border-radius: $line-height/2;
        padding: $line-height/1.5;
        @include grid_row;
        align-items: flex-end;

        &__title {
            text-align: left;
            font-weight: 700;
            font-size: $font-size-normal;
            line-height: 140%;
            color: #344767;
        }

        &__desc {
            font-family: 'Roboto';
            font-style: normal;
            font-weight: 400;
            font-size: $font-size-small;
            color: #7B809A;
        }
    }

    .pie {
        width: 22.5%;
        @include grid_column;
        justify-content: flex-start;
        align-items: center;

        &__chart {
            height: 22.5vh;
        }
    }

    .line {
        width: 49%;
        @include grid_column;
        justify-content: flex-start;
        align-items: flex-start;

        .line-graph {
            height: 35vh;
            width: 95%;
            margin: 0 2.5%;
            margin-top: -$line-height*1.25;
            border-radius: $line-height/3;
        }

        .line-1 {
            background: linear-gradient(180deg, #E93B77 0%, #DA1F63 100%);
        }

        .line-2 {
            background: linear-gradient(180deg, #63B967 0%, #4BA64F 100%);
        }

        .line-details {
            width: 95%;
            margin: $line-height/2 2.5%;
        }
    }

    .labels {

        .color-1 {
            color: #073A82;
        }

        .color-2 {
            color: #4CAF50;
        }

        .color-3 {
            color: #E91F63;
        }

        &__label {
            margin-right: $line-height/6;

            &--color {
                &-icon {
                    margin: 0 $line-height/6;
                    font-size: $font-size-tiny;
                }
            }

            &--name {
                font-size: $font-size-tiny;
                font-weight: 400;
                color: #030229;
                opacity: 0.7;
            }
        }
    }
}

.dash-table {
    width: 100%;

    &__title {
        text-align: left;
        font-weight: 700;
        font-size: $font-size-text;
        line-height: 140%;
        color: #344767;
        margin-bottom: $line-height;
    }
}
</style>
