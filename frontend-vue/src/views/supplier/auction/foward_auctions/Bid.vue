<template>
    <div class="bid_auction">
    </div>
</template>
<script>
export default {
    name: 'risk-auction-participate-supplier',
    data () {}
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
                padding: $line-height $line-height;
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
            width: 300.51px;
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
        width: 300.51px;
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