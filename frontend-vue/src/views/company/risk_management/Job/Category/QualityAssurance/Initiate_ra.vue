<template>
    <div class="risk-job-add">
        <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <router-link to="/buyer/list/risk-management"><font-awesome-icon icon="chevron-left" />  <span class="text">Back</span></router-link>
                </span>
            </span>
        </div>
        <div class="page__content">
            <div class="columns is-centered">
                <div class="column-details column is-4">
                    <form v-on:submit.prevent="create_risk_assessment()">
                        <div class="column-details__head">
                            <p class="column-details__head--title">Add New Risk Assessment</p>
                            <p class="column-details__head--desc">Fill in the required details</p>
                        </div>
                        <!-- Form Details -->
                        <div class="column-details__content">
                            <div class="field">
                                <label class="label">Title <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter Job Title" v-model="riskassessment.title">
                                </div>
                            </div>
                            <div class="risk_submit">
                                <input type="submit"  class="button button-submit" value="Create">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import risk_management from '@/services/company/risk_management'

export default {
    name:'add-risk-assessment-buyer',
    data() {
        return{
            riskassessment: {
                "title": '',
            },
            error_text: '',
        }
    },
    components:{
    },
    mounted:{
    },
    created:{
    },
    methods:{
        async create_risk_assessment(){
            try {
                if (this.riskassessment.title !== ''){
                    const response = await risk_management.createRiskAssessment(this.riskassessment, this.$route.params.categoryId)
                    
                    if(response.status == 201){
                        console.log(response.data)
                        window.toast.fire({icon: 'success', title: "Risk Assessment created successfully"})
                        this.$router.push("/buyer/add/ra/instructions/"+this.$route.params.categoryId+"/${response.data['id']}/risk-management/")
                    }else{
                        window.toast.fire({icon: 'error', title: "Error creating risk assessment"})
                    } 
                } else {
                    // No Title
                    if(this.risk.title == ''){
                        this.error_text = 'Please add risk assessment !'
                    }
                    // No Unique Reference
                    if(this.risk.unique_reference == ''){
                        this.error_text = 'Please add risk assessment !'
                    }
                    window.toast.fire({icon: 'error', title: this.error_text})

                }
            } catch (error) {
                console.log(error)
            }
        }
    },
}
</script>

<style lang="scss" scoped>
    .page {

        .nav-links__link {
            color: $color-blue-main;

            .text {
                font-size: font-size-major;
                font-weight: 600;
            }

            &:hover {
                cursor: pointer;
            }
        }

        &__content {
            padding: $line-height 5%;
            position: relative;
            z-index: 20; 
        
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
                margin-bottom: 0;

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

                .risk_submit {
                    padding: $line-height/2 0;
                    margin: $line-height/1 0 50px;
                    
                    .button-submit {
                        width: 100%;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: none;                
                        font-size: $font-size-text;
                    }

                    &:hover, :focus {
                        cursor: pointer;
                        transform: translateY(-0.25em);
                    }
                }
                
                .show_bids {
                    display: inline-block;
                    color: $color-blue-main;

                    .text {
                        font-size: $font-size-text;
                        font-weight: 600;
                        padding: 12px;
                    }
                }
            }
        }

        }

    }
</style>