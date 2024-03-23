<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Dashboard
            </span>

            <div class="page__head--links">
                <select class="page__head--link select-dropdown" v-model="days">
                    <option value="1" >Past Day</option>
                    <option value="7" >Past Week</option>
                    <option value="14" >Past 2 Weeks</option>
                    <option value="30" selected>Past Month</option>
                </select>
                <span class="page__head--link action-button" @click="printPage">
                    <font-awesome-icon class="action-button__icon" icon="print" />
                </span>
                <!-- <span class="page__head--link action-button">
                    <font-awesome-icon class="action-button__icon" icon="download" />
                </span> -->
            </div>
        </div>
        <div class="page__content columns" id="print">           
            <div class="column is-12 column-page">
                <div class="stats">
                    <div class="stat">
                        <span class="stat__icon-container stat1">
                            <img src="@/assets/total-bidders.png" alt="total bidders" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Total Bidders</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.total_bidders}}</span>
                        </span>
                    </div>                    
                    <router-link class="stat" :to="'livejobs'">
                        <span class="stat__icon-container stat2">
                            <img src="@/assets/live.png" alt="live" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Live Jobs</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.live_jobs}}</span>
                        </span>
                    </router-link>
                    <router-link class="stat" :to="'ourjobs'">
                        <span class="stat__icon-container stat3">
                            <img src="@/assets/list-interface.png" alt="live" class="stat__icon-container--icon">
                        </span>
                        <span class="stat__info">
                            <span class="stat__info--title">Our Jobs</span>
                            <span class="stat__info--desc" v-if="dashboardStats !== null">{{dashboardStats.our_jobs}}</span>
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
                    <div class="graph pie pie-1">
                        <p class="graph__title">Total Bidders</p>
                        <div class="pie__chart">
                            <DoughnutChart :height="'70%'" :colors="['#073A82', '#16AA51']" :values="dashboardStats.bidders" :labels="['Responsive', 'Non Responsive']"/>
                        </div>
                        <!-- <p class="labels">
                            <span class="labels__label">
                                <span class="labels__label--color color-1">
                                    <font-awesome-icon class="labels__label--color-icon" icon="circle" />
                                </span>
                                <span class="labels__label--name">Responsive</span>
                            </span>
                            <span class="labels__label">
                                <span class="labels__label--color color-2">
                                    <font-awesome-icon class="labels__label--color-icon" icon="circle" />
                                </span>
                                <span class="labels__label--name">Non-Responsive</span>
                            </span>
                        </p> -->
                    </div>
                    <div class="graph line">
                        <div class="line-graph">
                            <div class="line-graph__graph">
                                <span v-if="dailyBidders !== null">
                                    <LineChart :dates="dailyBidders.dates" :values="dailyBidders.bidder_count" :chartHeight="'120%'" />
                                </span>
                            </div>
                        </div>
                        <div class="line-details">
                            <p class="graph__title">Daily Bidders</p>
                            <p class="graph__desc">(+15%) increase in today sales.</p>
                        </div>
                    </div>
                    <div class="graph pie pie-2">
                        <p class="graph__title">Categories</p>
                        <div class="pie__chart">
                            <span v-if="dashboardStats !== null">
                                <DoughnutChart :height="350" :colors="['#073A82', '#16AA51', '#E91F63']" :values="dashboardStats.categories" :labels="['Goods', 'Services', 'Works']"/>
                            </span>
                        </div>
                        <!-- <p class="labels">
                            <span class="labels__label">
                                <span class="labels__label--color color-1">
                                    <font-awesome-icon class="labels__label--color-icon" icon="circle" />
                                </span>
                                <span class="labels__label--name">Goods</span>
                            </span>
                            <span class="labels__label">
                                <span class="labels__label--color color-2">
                                    <font-awesome-icon class="labels__label--color-icon" icon="circle" />
                                </span>
                                <span class="labels__label--name">Services</span>
                            </span>
                            <span class="labels__label">
                                <span class="labels__label--color color-3">
                                    <font-awesome-icon class="labels__label--color-icon" icon="circle" />
                                </span>
                                <span class="labels__label--name">Works</span>
                            </span>
                        </p> -->
                    </div>
                </div>
                <!-- <div class="dash-table">
                    <p class="dash-table__title">Top Bidders</p>
                    <v-client-table :columns="columns" :data="bidders" :options="options" class="hasRowNo hasNoWrap">
                        <p class="row-no" v-if="bidders.length !== 0" slot="#" slot-scope="props">
                            {{props.index}}
                        </p>
                        <p slot="supplier" class="hasLogo" slot-scope="{row}">
                            <img class="logo" src="@/assets/qed-logo.png" alt="">
                            <span>{{row.supplier}}</span>
                        </p>
                    </v-client-table>
                </div> -->
            </div>
        </div>        
    </div>
</template>

<script>
import DoughnutChart from '@/components/charts/DoughnutChart'
import LineChart from '@/components/charts/LineChart'
import dashboard from '@/services/company/dashboard'

export default {
    name: 'Dashboard',
    data() {
        return {
            columns: ['#', 'supplier', 'categories'],
            bidders: [
            ],
            dashboardStats: null,
            dailyBidders: null,
            days: 14
        }
    },
    components: {
        DoughnutChart,
        LineChart
    },
    mounted() {
        this.getStats()
        this.getDailyBidders()
    },
    watch: {
        days() {
            this.getDailyBidders()
        }
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
        async getDailyBidders() {
            try {
                this.dailyBidders = null
                const response = await dashboard.daily_bidders(this.days)
                this.dailyBidders = response.data.daily_bidders
            } catch (err) {
                console.log(err)
            }
        },
        printPage: function() {
            window.print();
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
        height: 40vh;
        background-color: $color-white-main;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
        border-radius: $line-height/2;
        padding: $line-height/1.5;
        @include grid_row;
        align-items: flex-end;

        &__title {
            text-align: left;
            font-weight: 700;
            font-size: $font-size-text;
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
            height: 30vh;
            width: 95%;
            margin: 0 2.5%;
            margin-top: -$line-height*1.25;
            background: linear-gradient(180deg, #63B967 0%, #4BA64F 100%);
            border-radius: $line-height/3;
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
