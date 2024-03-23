<template>
    <div class="profile">
        <div class="page__head">
            <span class="page__head--title">
                Edit My Profile
            </span>

            <div class="page__head--links">
                <span class="page__head--link text-link" v-if="profile.supplier_company">
                    {{profile.supplier_company.company_name}}
                </span>
            </div>
        </div>
        <form v-on:submit.prevent="updateProfile()">
        <div class="page__content columns" v-if="profile.supplier_company">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Mandatory Details</p>
                    <p class="column-details__head--desc">Entered on registration</p>
                </div>
                <div class="column-details__content">
                    <div class="field">
                        <label class="label">Company Name <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" v-model="profile.supplier_company.company_name" type="text" placeholder="Enter company name">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Country <span class="required">*</span></label>
                        <div class="select  country_select" >
                            <country-select v-model="profile.supplier_company.country" :country="profile.supplier_company.country" :countryName="true" topCountry="KE" />
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">
                            <span v-if="profile.supplier_company.country === 'Kenya'">KRA PIN Number</span>
                            <span v-else>Tax Identification Number</span>
                            <span class="required">*</span>
                        </label>
                        <div class="control">
                            <input class="input" v-model="profile.supplier_company.tax_pin_number" type="text" placeholder="Enter KRA PIN">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Contact Name <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" v-model="profile.supplier_company.contact_name" type="text" placeholder="Enter contact name">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Phone Number <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" v-model="profile.supplier_company.phone_number" type="text" placeholder="Phone Number: Format +254 700 000 000">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Physical Address <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" v-model="profile.supplier_company.address" type="text" placeholder="P.O. Box address">
                        </div>
                    </div>
                    <!-- <div class="field">
                        <label class="label">Categories of Interest <span class="required">*</span></label>
                        <div class="control">
                            <textarea class="textarea" placeholder="List down categories of your interest"></textarea>
                        </div>
                    </div>
                    <div class="selected">
                        <span class="selected__item category">
                            Supply and maintenace of CCTV and acess control systems
                            <span class="selected__icon">
                                <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                            </span>                                        
                        </span>
                    </div>
                    <div class="field">
                        <label class="label">Supply Locations<span class="required">*</span></label>
                        <div class="select">
                            <select>
                                <option>Select your supply location</option>
                                <option>Nairobi</option>
                                <option>Kiambu</option>
                            </select>
                        </div>                                    
                    </div>
                    <div class="selected">
                        <span class="selected__item location">
                            Nairobi
                            <span class="selected__icon">
                                <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                            </span>                                        
                        </span>
                    </div> -->
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
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.registration_cert_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.registration_cert_url" target="_blank" download class="name download-link">Company Registration Document (Download) </a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('registration_cert_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="registration_cert_url" type="file" placeholder="Choose a file…">
                            </div>
                        </div>
                        <!-- <span class="document__status">Choose File</span> -->
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_pin_url === null?'doc-missing':'doc-available'">
                                <span v-if="profile.supplier_company.country === 'Kenya'">KRA PIN Certificate</span>
                                <span v-else>PIN Certificate</span>
                            </span>
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.kra_pin_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.kra_pin_url" target="_blank" download class="name download-link">
                                    <span v-if="profile.supplier_company.country === 'Kenya'">KRA PIN Certificate</span>
                                    <span v-else>PIN Certificate</span> 
                                    (Download)
                                </a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('kra_pin_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="kra_pin_url" type="file" placeholder="Choose a file…">
                            </div>
                        </div>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_compliance_url === null?'doc-missing':'doc-available'">Tax Compliace Certificate</span>
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.kra_compliance_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.kra_compliance_url" target="_blank" download class="name download-link">Tax Compliace Certificate (Download)  - expires on {{this.profile.kra_compliance_expiry_date}}</a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('kra_compliance_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="kra_compliance_url" type="file" placeholder="Choose a file…">
                            </div>
                        </div>
                        <div class="field expiry">
                            <label class="label">Set Tax Compliance Expiry date: <span class="required">*</span></label>
                            <div class="control">
                                <input class="input" type="date" v-model="kra_compliance_expiry_date" placeholder="Tax Compliance Expiry date">
                            </div>
                            <p class="help">Kindly pick a date for the expiry of your document</p>
                        </div>
                    </div>                    
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.kra_trading_licence_url === null?'doc-missing':'doc-available'">Trading License</span>
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.kra_trading_licence_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.kra_trading_licence_url" target="_blank" download class="name download-link">Trading License (Download) - expires on {{this.profile.kra_trading_licence_expiry_date}}</a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('kra_trading_licence_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="kra_trading_licence_url" type="file" placeholder="Choose a file…">
                            </div>
                        </div>
                        <div class="field expiry">
                            <label class="label">Set Trading Licence Expiry date: <span class="required">*</span></label>
                            <div class="control">
                                <input class="input" type="date" v-model="kra_trading_licence_expiry_date" placeholder="Tax Compliance Expiry date">
                            </div>
                            <p class="help">Kindly pick a date for the expiry of your document</p>
                        </div>
                    </div>                    
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.cr_12_document_url === null?'doc-missing':'doc-available'">CR12 Document</span>
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.cr_12_document_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/adobe.png" class="icon">
                                <a :href="profile.cr_12_document_url" target="_blank" download class="name download-link">CR12 Document (Download). </a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('cr_12_document_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="cr_12_document_url" type="file" placeholder="Choose a file…">
                            </div>
                        </div>
                    </div>
                    <div class="document">
                        <p class="document__title">
                            <span class="document__title--name" :class="profile.logo_url === null?'doc-missing':'doc-available'">Logo</span>
                            <span class="document__title--icon">
                                <!-- <font-awesome-icon class="icon" icon="folder-plus" /> -->
                            </span>
                        </p>
                        <span class="document__name" v-if="profile.logo_url !== null">
                            <span class="document__name--text">
                                <img src="@/assets/image.png" class="icon">
                                <a :href="profile.logo_url" target="_blank" download class="name download-link">Logo (Download) </a>
                            </span>
                            <span class="document__name--delete" @click="removeDocument('logo_url')">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="field file">
                            <div class="control">
                                <input class="input" id="logo_url" type="file" value="Choose image" placeholder="Choose image">
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note">Note that updates made on your profile will be used in future jobs. Past jobs maintain old profile information.</p>
            </div>
            <div class="column is-3">
                <input class="button button-submit" type="submit" value="Update Profile">
            </div>
        </div>
        </form>
    </div>
</template>

<script>
import auth from '@/services/authentication/auth'

export default {
    name: 'UpdateProfile',
    data() {
        return {
            profile: {},
            registration_cert: null,
            logo: null,
            kra_pin: null,
            kra_compliance: null,
            kra_trading_licence: null,
            cr_12_document: null,
            kra_compliance_expiry_date: null,
            kra_trading_licence_expiry_date: null,
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
            try {
                let form_data = new FormData()

                form_data.append("id", this.profile.id)
                form_data.append("company_name", this.profile.supplier_company.company_name)
                form_data.append("contact_name", this.profile.supplier_company.contact_name)
                form_data.append("phone_number", this.profile.supplier_company.phone_number)

                let registration_cert_url_file = document.getElementById("registration_cert_url").files[0];
                if (registration_cert_url_file !== undefined) {
                    form_data.append("registration_cert_url", registration_cert_url_file, registration_cert_url_file.name)
                }

                let kra_pin_url_file = document.getElementById("kra_pin_url").files[0];
                if (kra_pin_url_file !== undefined) {
                    form_data.append("kra_pin_url", kra_pin_url_file, kra_pin_url_file.name)
                }

                let kra_compliance_url_file = document.getElementById("kra_compliance_url").files[0];
                if (kra_compliance_url_file !== undefined) {
                    form_data.append("kra_compliance_url", kra_compliance_url_file, kra_compliance_url_file.name)

                    if (this.kra_compliance_expiry_date === null) {
                        window.toast.fire({
                            icon: 'error',
                            title: 'Please enter the Tax Compliance expiry date.'
                        })
                    } else {
                        form_data.append("kra_compliance_expiry_date", this.kra_compliance_expiry_date)
                    }
                }

                let kra_trading_licence_url_file = document.getElementById("kra_trading_licence_url").files[0];
                if (kra_trading_licence_url_file !== undefined) {
                    form_data.append("kra_trading_licence_url", kra_trading_licence_url_file, kra_trading_licence_url_file.name)

                    if (this.kra_trading_licence_expiry_date === null) {
                        window.toast.fire({
                            icon: 'error',
                            title: 'Please enter the Tax Compliance expiry date.'
                        })
                    } else {
                        form_data.append("kra_trading_licence_expiry_date", this.kra_trading_licence_expiry_date)
                    }
                }

                let cr_12_document_url_file = document.getElementById("cr_12_document_url").files[0];
                if (cr_12_document_url_file !== undefined) {
                    form_data.append("cr_12_document_url", cr_12_document_url_file, cr_12_document_url_file.name)
                }

                let logo_url_file = document.getElementById("logo_url").files[0];
                if (logo_url_file !== undefined) {
                    form_data.append("logo_url", logo_url_file, logo_url_file.name)
                }

                console.log(form_data)

                await auth.updateCompanyProfile(this.profile.id, form_data)
                window.toast.fire({
                    icon: 'success',
                    title: 'Company profile updated successfully'
                })
                this.getProfile()

            } catch (err) {
                console.log(err)
            }
        },
        async removeDocument(document) {
            try {
                let form_data = new FormData()
                if (document === 'registration_cert_url') {
                    form_data.append("registration_cert_url", "")
                }

                if (document === 'kra_pin_url') {
                    form_data.append("kra_pin_url", "")
                }

                if (document === 'kra_compliance_url') {
                    form_data.append("kra_compliance_url", "")
                    form_data.append("kra_compliance_expiry_date", "")
                }

                if (document === 'kra_trading_licence_url') {
                    form_data.append("kra_trading_licence_url", "")
                    form_data.append("kra_trading_licence_expiry_date", "")
                }

                if (document === 'cr_12_document_url') {
                    form_data.append("cr_12_document_url", "")
                }

                if (document === 'logo_url') {
                    form_data.append("logo_url", "")
                }

                await auth.updateCompanyProfile(this.profile.id, form_data)
                
                window.toast.fire({
                    icon: 'success',
                    title: 'Company profile updated successfully'
                })
                this.getProfile()

            } catch (err) {
                console.log(err)
            }
        }
    }
}
</script>

<style lang="scss" scoped>
.page {
    &__head {
        @include grid_row;
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
        position: sticky;
        top: 13vh;
        background-color: $color-white-main;
        z-index: 200;

        &--title {
            color: rgba(18, 31, 62, 0.8);
            font-size: $font-size-text;
            font-weight: 500;
            margin-bottom: $line-height/6 !important;
        }

        &--links {
            @include grid_row;
            align-items: center;

            .text-link {
                color: $color-blue-main;
                font-size: $font-size-normal;
                font-weight: 500;
            }

            .button-link {
                color: $color-white-main;
                background-color: $color-blue-main;
                border: none;                
                font-size: $font-size-text;
            }
        }

        &--link {
            margin: 0 $line-height/4;
        }
    }

    &__content {
        width: 100%;
        padding: $line-height $line-height;
        margin-bottom: $line-height;

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

                .label {
                    font-weight: 500;
                    margin-right: $line-height/2;
                    color: $color-black-main;
                    font-size: $font-size-text;
                }

                .select {
                    width: 100%;
                }

                .input, select, textarea {
                    width: 100%;
                    border-radius: $line-height/2;
                    border: 1px solid #D0D0D0;
                    font-size: $font-size-text;  
                    color: $color-black-main; 
                    z-index: 1;             

                    &:focus {
                        outline: none;
                    }
                }

                .selected {
                    margin: $line-height/3 0;

                    &__item {
                        background-color: $color-blue-main;
                        padding: $line-height/4 $line-height/3;
                        color: $color-white-main;
                        border-radius: $line-height/1.5;
                        @include grid_row;
                        justify-content: space-between;
                        align-items: center;
                        width: $line-height*5;

                        font-size: $font-size-small;

                        @media screen and (min-width: 1600px) { 
                            font-size: $font-size-text;
                        }
                    }

                    &__icon {
                        margin: 0 $line-height/4;

                        &--img {
                            height: $line-height;
                            padding: $line-height/6;
                            background-color: $color-blue-main;
                            color: $color-white-main;
                            border-radius: 50%;
                            cursor: pointer;
                        }
                    }

                    .category {
                        width: 100%;
                    }
                }

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
                    padding: $line-height/2 0;
                    padding-bottom: 0;
                    border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
                    position: relative;
                    z-index: 1;

                    &__status {
                        position: absolute;
                        z-index: 20;
                        padding: $line-height/6 $line-height/3;.country_select {
                            select {
                                height: auto;
                                padding: 12px;

                                option:first {
                                    color: red !important;
                                }
                            }
                        }
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

                        .upload {
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
                        cursor: pointer;
                        
                        &:hover {
                            color: $color-green-main;
                        }

                        &--text {
                            @include grid_row;
                            align-items: center;

                            .name {
                                font-size: $font-size-text;
                            }

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

                    .file {
                        margin: $line-height/3 0;
                        // display: block;
                        display: none;

                        .input {
                            border: none;
                            padding-bottom: 0;
                            padding-top: 0;
                        }
                    }

                    .expiry {
                        display: none;
                        // display: block;
                    }

                    &:hover {
                        .doc-available {
                            // color: $color-green-main;
                            cursor: pointer;
                        }

                        .doc-missing {
                            color: $color-red-main;
                            cursor: pointer;
                        }

                        .document__status {
                            display: block;
                        }

                        .file {
                            display: block;
                        }

                        .expiry {
                            display: block;
                        }
                    }
                }

                .expiry {
                    margin: $line-height/3 $line-height/2;

                    .label {
                        color: $color-gray-main;
                        font-size: $font-size-text;
                        font-weight: 500;
                    }

                    .help {
                        color: $color-gray-main;
                    }
                }
            }
        }
    }

    .additions {
        padding: $line-height $line-height;

        .note {
            color: $color-lightblue-text;
            font-weight: 600;
        }

        .button-submit {
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
        }
    }
}

.country_select {
    select {
        height: auto;
        padding: 12px;

        option:first {
            color: red !important;
        }
    }
}

.download-link {
    color: $color-green-main;

    &:hover {
        color: $color-green-main;
    }
}
</style>
