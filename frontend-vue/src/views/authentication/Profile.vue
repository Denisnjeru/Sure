<template>
    <div class="profile">
        <div class="page__head">
            <span class="page__head--title">
                My Profile
            </span>

            <div class="page__head--links">
                <router-link to="/change-password">
                <span class="page__head--link text-link">
                    Change Password
                </span>
                </router-link>
                <router-link to="/update-profile">
                    <a class="page__head--link button button-link">
                        Edit Profile
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Mandatory Details</p>
                    <p class="column-details__head--desc">Entered on registration</p>
                </div>
                <div class="column-details__content" v-if="profile.supplier_company">
                    <p class="detail">
                        <span class="detail__title">Company Name:</span>
                        <span class="detail__text">{{profile.supplier_company.company_name}}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Contact Name:</span>
                        <span class="detail__text">{{profile.supplier_company.contact_name}}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Tax Identification Number:</span>
                        <span class="detail__text">{{profile.supplier_company.tax_pin_number}}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Phone Number:</span>
                        <span class="detail__text">{{profile.supplier_company.phone_number}}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Email Adress:</span>
                        <span class="detail__text">{{profile.supplier_company.email}}</span>
                    </p>
                    <p class="detail">
                        <span class="detail__title">Postal Adress:</span>
                        <span class="detail__text">{{profile.supplier_company.address}}</span>
                    </p>
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Profile Details</p>
                    <p class="column-details__head--desc">Documents</p>
                </div>
                <div class="column-details__content">
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.registration_cert_url === null?'doc-missing':'doc-available'">Company Registration Document</span>
                            <span class="document__title--icon" :class="profile.registration_cert_url === null?'missing':'available'">
                                <font-awesome-icon v-if="profile.registration_cert_url === null" class="icon" icon="folder-plus" />
                                <font-awesome-icon v-else class="icon" icon="folder-minus" />
                            </span>
                        </p>
                        <span class="document__status" v-if="profile.registration_cert_url === null">Not Uploaded</span>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.cr_12_document_url === null?'doc-missing':'doc-available'">Company CR12</span>
                            <span class="document__title--icon" :class="profile.cr_12_document_url === null?'missing':'available'">
                                <font-awesome-icon v-if="profile.cr_12_document_url === null" class="icon" icon="folder-plus" />
                                <font-awesome-icon v-else class="icon" icon="folder-minus" />
                            </span>
                        </p>
                        <span class="document__status" v-if="profile.cr_12_document_url === null">Not Uploaded</span>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_pin_url === null?'doc-missing':'doc-available'">KRA PIN Certificate </span>
                            <span class="document__title--icon" :class="profile.kra_pin_url === null?'missing':'available'">
                                <font-awesome-icon v-if="profile.kra_pin_url === null" class="icon" icon="folder-plus" />
                                <font-awesome-icon v-else class="icon" icon="folder-minus" />
                            </span>
                        </p>
                        <span class="document__status" v-if="profile.kra_pin_url === null">Not Uploaded</span>
                        <span class="document__name" v-else>
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <span class="name">KRA PIN Certificate (Download)</span>
                            </span>
                            <span class="document__name--delete">
                                <span class="selected__icon">
                                   
                                    <!-- <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt=""> -->
                                </span> 
                            </span>
                        </span>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_compliance_url === null?'doc-missing':'doc-available'">Tax Compliace Certificate</span>
                            <span class="document__title--icon" :class="profile.kra_compliance_url === null?'missing':'available'">
                                <font-awesome-icon v-if="profile.kra_compliance_url === null" class="icon" icon="folder-plus" />
                                <font-awesome-icon v-else class="icon" icon="folder-minus" />
                            </span>
                        </p>
                        <span class="document__status" v-if="profile.kra_compliance_url === null">Not Uploaded</span>
                        <span class="document__name" v-else>
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.kra_compliance_url" class="name">Download </a>
                            </span>
                            <span class="document__name--delete">
                                <span class="selected__icon">
                                    Expires on: {{profile.kra_compliance_expiry_date}}
                                    <!-- <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt=""> -->
                                </span> 
                            </span>
                        </span>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_trading_licence_url === null?'doc-missing':'doc-available'">Trading License</span>
                            <span class="document__title--icon" :class="profile.kra_trading_licence_url === null?'missing':'available'">
                                <font-awesome-icon v-if="profile.kra_trading_licence_url === null" class="icon" icon="folder-plus" />
                                <font-awesome-icon v-else class="icon" icon="folder-minus" />
                            </span>
                        </p>
                        <span class="document__status" v-if="profile.kra_trading_licence_url === null">Not Uploaded</span>
                        <span class="document__name" v-else>
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <span class="name">Trading License (Gempack Dot Net Enterprises).pdf </span>
                            </span>
                            <span class="document__name--delete">
                                <span class="selected__icon">
                                    Expires on: {{profile.kra_trading_licence_expiry_date}}
                                    <!-- <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt=""> -->
                                </span> 
                            </span>
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note">Note that updates made on your profile will be used in future jobs. Past jobs maintain old profile information.</p>
            </div>
        </div>
    </div>
</template>

<script>
import auth from '@/services/authentication/auth'

export default {
    name: 'Profile',
    data() {
        return {
            profile: {}
        }    
    },
    mounted() {
        this.getProfile()
    },
    methods: {
        async getProfile() {
            try {
                const response = await auth.companyProfile()
                this.profile = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async updateProfile() {
            
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page {

    &__head {
        position: sticky;
        top: 13vh;
        background-color: $color-white-main;
        z-index: 200;
    }

    &__content {
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
                    font-size: $font-size-text;
                    font-weight: 600;
                    margin-bottom: 0 !important;
                }

                &--desc {
                    color: $color-black-medium;
                    margin: 0;
                    font-size: $font-size-text;
                }
            }

            &__content {
                padding: $line-height/2 $line-height;
                margin-bottom: $line-height*2;

                .detail {
                    padding: $line-height/2 0;
                    border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

                    &__title {
                        font-weight: 500;
                        margin-right: $line-height/2;
                        color: $color-black-main;
                        font-size: $font-size-text;
                    }

                    &__text {
                        color: $color-lightblue-text;
                        font-size: $font-size-text;
                    }
                }

                .document {
                    padding: $line-height/2.5 0;
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
                        margin-top: -$line-height/3;
                    }                    

                    &__title {
                        width: 100%;
                        @include grid_row;

                        &--name {
                            font-weight: 500;
                            color: $color-black-main;
                            font-size: $font-size-text;
                        }

                        &--icon {
                            color: $color-gray-main;
                        }

                        .missing {
                            color: $color-red-main;
                        }

                        .available {
                            color: $color-green-main;
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

                            .name {
                                font-size: $font-size-small;
                            }

                            .icon {
                                margin-right: $line-height/4;
                                height: $line-height;
                            }
                        }

                        &:hover {
                            color: $color-green-main;
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
                        cursor: pointer;
                        
                        .doc-available {
                            color: $color-green-main;
                            cursor: pointer;
                        }

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
        }
    }

    .additions {
        padding: $line-height/6 $line-height;
        margin: $line-height/8 0;

        .note {
            color: $color-lightblue-text;
            font-weight: 600;
        }
    }
}
</style>
