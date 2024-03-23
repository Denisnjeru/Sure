<template>
    <div class="register">
        <div class="content">
            <Nav />
            <div class="content__row columns is-centered">
                <div class="register__form column is-8">
                    <form v-on:submit.prevent="register()">
                        <div class="columns">
                            <div class="column is-6 register__form--section">
                                <p class="section-title">Company Details</p>
                                <div class="field">
                                    <label class="label">Company Type <span class="required">*</span></label>
                                    <div class="control">
                                        <v-select v-model="selectedCompanyType" :options="companyTypes" :reduce="type => type.value" label="name" placeholder="Select company type"></v-select>
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Company name <span class="required">*</span></label>
                                    <div class="control">
                                        <input required v-model="supplier.company_name" class="input" type="text" placeholder="Enter company name">
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Country <span class="required">*</span></label>
                                    <div class="select  country_select" >
                                        <country-select v-model="country" :country="supplier.country" :countryName="true" topCountry="KE" />
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Phone Number <span class="required">*</span></label>
                                    <div class="control">
                                        <input required v-model="supplier.phone_number" class="input" type="text" placeholder="Phone Number: Format +254 700 000 000">
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Physical Address <span class="required">*</span></label>
                                    <div class="control">
                                        <input required v-model="supplier.address" class="input" type="text" placeholder="P.O. Box address">
                                    </div>
                                </div>
                            </div>
                            <div class="column is-6 register__form--section">
                                <p class="section-title"><br></p>
                                <div class="field">
                                    <label class="label">Email Address <span class="required">*</span></label>
                                    <div class="control">
                                        <input required v-model="supplier.email" class="input" type="text" placeholder="Enter email address">
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label"> Location<span class="required">*</span></label>
                                    <div class="control">
                                        <input v-model="supplier.location" class="input" type="text" placeholder="Enter location">
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Contact Name <span class="required">*</span></label>
                                    <div class="control">
                                        <input v-model="supplier.contact_name" class="input" type="text" placeholder="First & Last Name">
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">
                                        <span v-if="country === 'Kenya'">KRA PIN Number</span>
                                        <span v-else>Tax Identification Number</span>
                                        <span class="required">*</span>
                                    </label>
                                    <div class="control">
                                        <input required v-model="supplier.kra_pin_number" class="input" type="text" placeholder="Enter Tax Identification Number">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="columns">
                            <div class="column is-12 general-details">
                                <div class="field">
                                    <label class="label">Categories of Interest <span class="required">*</span></label>
                                    <div class="control">
                                        <v-select v-model="selectedCategories" :options="categories" :reduce="category => category.id" label="name" multiple placeholder="Select categories of interest "></v-select>
                                        <!-- <textarea class="textarea" placeholder="List down categories of your interest"></textarea> -->
                                    </div>
                                </div>
                                <div class="field">
                                    <label class="label">Supply Locations<span class="required">*</span></label>
                                    <div class="control">
                                        <v-select v-model="selectedLocations" :options="locations" multiple placeholder="Select supply locations"></v-select>
                                    </div>
                                </div>
                                <div class="selected">
                                    <span class="selected__location" v-for="selectedLocation in selectedLocations" :key="selectedLocation">
                                        {{selectedLocation}}
                                        <span class="selected__icon">
                                            <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="" @click="removeSelectedLocation(selectedLocation)">
                                        </span>
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="columns register__submit is-vcentered">
                            <div class="column is-6">
                                <div class="text-row">
                                    <span>
                                        You have an account?
                                    </span>
                                    <router-link to="login">
                                        <span class="text-link">
                                            Sign In
                                        </span>
                                    </router-link>
                                </div>
                            </div>
                            <div class="column is-6">
                                <div class="control">
                                    <input class="button submit-button" type="submit" value="Sign Up" :class="{ active: supplier.kra_pin_number !== null }">
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div class="myfooter">
            <Footer />
        </div>
    </div>
</template>

<script>
import Nav from '@/components/authentication/Nav'
import Footer from '@/components/authentication/Footer'
import auth from '@/services/authentication/auth'

export default {
    name: 'Register',
    data() {
        return {
            page: 1,
            supplier: {
                'kra_pin_number': null
            },
            country: 'Kenya',
            locations: [],
            categories: [],
            selectedLocations: null,
            selectedCategories: null,
            companyTypes: [
                {
                    "name": 'Sole proprietor',
                    "value": 1
                },
                {
                    "name": 'Limited Company',
                    "value": 2
                },
                {
                    "name": 'Partnership',
                    "value": 3
                },
            ],
            selectedCompanyType: null
        }
    },
    components: {
        Nav,
        Footer
    },
    mounted() {
        this.getLocations('Kenya')
        this.getCategoryTypes()
    },
    watch: {
        country(newCountry) {
            this.supplier.location = ""
            this.selectedLocations = null
            this.getLocations(newCountry)
        }
    },
    methods: {
        removeSelectedLocation: function(location) {
            let locationIndex = this.selectedLocations.indexOf(location);
            if (locationIndex > -1) {
                this.selectedLocations.splice(locationIndex, 1)
            }
        },
        async getLocations(countryName) {
            try {
                const response = await auth.countryLocations(countryName)
                this.locations = response.data.locations.map(a => a.name);
            } catch (err) {
                console.log(err)
            }
        },
        async getCategoryTypes() {
            try {
                const response = await auth.categoryTypes()
                console.log(response)
                this.categories = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async register() {
            try {
                this.supplier.country = this.country

                if (this.country === 'Kenya') {
                    if (this.selectedCompanyType === 'sole-proprietor') {
                        if (this.supplier.kra_pin_number.charAt(0) !== 'A') {
                            window.toast.fire({
                                icon: 'error',
                                title: 'Invalid tax identification number'
                            })
                            return
                        }
                    }

                    if (this.selectedCompanyType === 'limited-company') {
                        if (this.supplier.kra_pin_number.charAt(0) !== 'P') {
                            window.toast.fire({
                                icon: 'error',
                                title: 'Please verify the tax identification number is correct'
                            })
                            return
                        }
                    }
                }

                this.supplier.category_type_ids = this.selectedCategories
                this.supplier.supply_locations = this.selectedLocations
                this.supplier.supplier_type = this.selectedCompanyType
                await auth.supplierRegister(this.supplier)
                this.$swal({
                    icon: 'success',
                    title: 'Registration successful',
                    text: 'Please check your email for an activation link',
                    showConfirmButton: false,
                });
                this.$router.push('/login')
            } catch (err) {
                console.log(err.response)
                // let error = Object.entries(err.response.data)
                // this.$swal({
                //     icon: 'error',
                //     title: 'Oops...',
                //     text: error,
                //     showConfirmButton: false,
                // });
            }
        }
    }
}
</script>

<style lang="scss" scoped>

.content {
    padding: $line-height 5%;
    position: relative;
    z-index: 20;

    &__row {
        min-height: 70vh;

        .register__form {
            background: $color-white-main;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: 15px;
            margin: $line-height*2 0;
            padding: $line-height $line-height*2;

            .label {
                // color: $color-black-main;
                font-weight: 500;
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

                &:focus {
                    outline: none;
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

            .input {
                padding: $line-height $line-height/2;

            }

            &--section {
                padding-right: $line-height;

                @media screen and (min-width: 1600px) {
                    padding-right: $line-height*2;
                }

                .section-title {
                    color: $color-black-main;
                    font-size: $font-size-title;
                    font-weight: 500;
                }
            }

            .selected {
                margin: $line-height/3 0;
                @include grid_row;
                justify-content: flex-start;

                &__location {
                    background-color: $color-blue-main;
                    padding: $line-height/4 $line-height/3;
                    color: $color-white-main;
                    border-radius: $line-height/1.5;
                    @include grid_row;
                    justify-content: space-between;
                    align-items: center;
                    // width: $line-height*5;
                    margin-left: $line-height/3;

                    font-size: $font-size-text;

                    @media screen and (min-width: 1600px) {
                        font-size: $font-size-normal;
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
            }
        }

        .register__submit {
            margin: $line-height 0;

            .text-row {
                @include grid_row;
                justify-content: flex-start;
                margin: $line-height/3 0;
                font-size: $font-size-text;
                flex-wrap: nowrap;
                font-weight: 500;
                color: $color-black-main;

                span {
                    white-space: nowrap
                }
            }

            .text-link {
                color: $color-green-main;
                cursor: pointer;
                text-align: right;
                margin: 0 $line-height/2;
            }

            .submit-button {
                width: 100%;
                margin: $line-height/4 0;
                color: $color-white-main;
                background-color: $color-gray-main;
                font-weight: 600;
                border-radius: $line-height/2;
            }

            .active {
                background-color: $color-green-main;
            }
        }
    }
}

.general-details {
    .field {
        padding-right: 12px;




        .vs__dropdown-toggle {
            margin-left: 0 !important;
        }
    }
}


</style>
