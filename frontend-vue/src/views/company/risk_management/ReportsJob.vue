<template> 
    <div class="risk_job_reports">
        <div class="page__head">
            <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left" /> <span class="text">Back</span>
            </span>

            <div class="page__head--title">
                <router-link to="/buyer/add/risk-management">
                    <a class="page__head--link button button-link">
                        <span class="button-link__button-text">Risk Management Reports</span><font-awesome-icon icon="chevron-down"/>
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">January Risk Management 2022</p>
                    <p class="column-details__head--desc">Reports</p>
                </div>
                <div class="column-details__content">
                    <p class="detail">
                        <span class="detail__title">Job Title:</span>
                        <span class="detail__text">January Risk Management 2022</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Owner:</span>
                        <span class="detail__text">DEMO COMPANY HJ</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Sourcing Activity:</span>
                        <span class="detail__text">Risk Management</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Job Code:</span>
                        <span class="detail__text">RM001</span>
                    </p>
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Items in this Risk Management</p>
                    <p class="column-details__head--desc">Reports</p>
                </div>
                <div class="column-details__content">
                    <div class="table-search">
                        <p class="table-search__title">
                            <!-- Card Title Header -->
                        </p>
                        <div class="table-search__search">
                            <font-awesome-icon class="table-search__search--icon" icon="search"/>
                            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                        </div>
                    </div>
                    <v-client-table :data="data" :columns="columns" :options="options">
                        <p class = "row-no" v-if="data.length !== 0" slot="#" slot-scope="props">
                            {{ props.index }}
                        </p>

                        <a class= "row-link" v-if="data.length !== 0" slot="Reports"> 
                            <a class="button row-link__button-detail">
                                <font-awesome-icon class="row-link__button-detail__button-text" icon="file-alt"/><span class="row-link__button-detail__button-text">Reports</span><font-awesome-icon icon="chevron-down"/>
                            </a>
                        </a>
                    </v-client-table>
                    <div class="page__pagination">
                        <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                        </pagination>
                    </div>
                </div>
            </div>
        </div>
    </div>   
</template>

<script>
export default {
    name: 'risk-management-reports-buyer',
    data () {
        return{
            columns: ['#', 'Category Name', 'Closing Date', 'Reports'],
            data: [
                {
                    'Category Name':'G0005 - Supply of computers, laptops, tablets and accessories', 
                    'Closing Date':'April 6, 2022, 11 a.m.'
                },{
                    'Category Name':'G0006 - Supply of pharmaceutical dugs', 
                    'Closing Date':'April 6, 2022, 11 a.m.'
                },{
                    'Category Name':'G0005 - Provision of debt collection services', 
                    'Closing Date':'April 6, 2022, 11 a.m.'
                },
                {
                    'Category Name':'G0005 - Provision of security guarding services', 
                    'Closing Date':'April 6, 2022, 11 a.m.'
                },
            ],
            options: {
                headings : {

                },
                sortable:['#','Category Name', 'Bid Fee', 'Category Type', 'Status', 'Actions', 'More Actions'],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page{
    &__content{
        width: 100%;
        padding: $line-height $line-height;

        .column-details {
            margin: 0 $line-height/4;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: 0;
            margin-bottom: $line-height/2;

            &__head {
                background: $color-baby-blue;
                padding: $line-height/4 $line-height;
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
                margin-bottom: $line-height*20;

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

                    &__button-detail {

                        width: 200px;
                        color: $color-blue-main;
                        font-size: $font-size-text;
                        background-color: $color-white-main;
                        border: 1px solid $color-blue-main;
                        border-radius: 5px;
                        transform: rotate(0.02deg);

                        &__button-text{
                            display: inline;
                            margin-right: 1em;
                        }

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
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
            }
            &__content_documents{
                padding: $line-height*2 0;
                margin-bottom: $line-height;
                display: block;
                text-align: center;


                .detail_button {
                    padding: $line-height $line-height*2;

                    .button-detail {
                        width: 300.51px;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: none;                
                        font-size: $font-size-text;
                        border-radius: 5px;
                        box-sizing: border-box;
                        transform: rotate(0.02deg);


                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                }
            }
        }
    }

    .row-link{
        text-align: center;

        &__link{
            display: inline;
            margin-right: 0.5em;
            color: #4CAF50;
        }

        &__text{
            display: inline;
            color: $color-blue-main;
        }

        &__button-detail {
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
            border-radius: 5px;
            box-sizing: border-box;
            transform: rotate(0.02deg);

            &__button-text{
                display: inline;
                margin-right: 1em;
            }

            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }
    }
    .button-link{
        width: 100%;
        color: $color-white-main;
        background-color: $color-blue-main;
        border: none;                
        font-size: $font-size-text;
        border-radius: 5px;
        box-sizing: border-box;
        transform: rotate(0.02deg);

        &__button-text{
            display: inline;
            margin-right: 1em;
        }

        &:hover, :focus {
            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
            transform: translateY(-0.25em);
        }
    }
}
</style>