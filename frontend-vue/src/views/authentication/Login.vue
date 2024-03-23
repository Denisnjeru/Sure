<template>
    <div class="login">
        <div class="content">
            <Nav />
            <div class="myslider">
                <VueSlickCarousel :arrows="false" :dots="true" :autoplay="true" :autoplaySpeed="3000" class="myslider__carousel">
                    <div class="myslider__carousel--item item1">
                        <p class="myslider__carousel--title main-title">Source to Contract <br> Cloud Solution</p>
                        <p class="myslider__carousel--desc"></p>
                    </div>
                    <div class="myslider__carousel--item item2">
                        <p class="myslider__carousel--title">Our Promise</p>
                        <p class="myslider__carousel--desc">Efficiency, Transparency and Savings</p>
                    </div>
                    <div class="myslider__carousel--item item3">
                        <p class="myslider__carousel--title">The next generation of eProcurement</p>
                        <p class="myslider__carousel--desc"></p>
                    </div>
                </VueSlickCarousel>
            </div>
            <div class="content__row columns">
                <div class="column is-4 login-form">
                    <p class="column__title">{{ $t('message.value', { value: 'Login' }) }}</p>
                    <form v-on:submit.prevent="login()">
                        <div class="standard-height">
                            <div class="field">
                                <label class="label">Username</label>
                                <div class="control">
                                    <input v-model="username" class="input" type="text">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Password</label>
                                <div class="control has-icons-right">
                                    <input v-if="showPassword === false" v-model="password" class="input" type="password">
                                    <input v-else v-model="password" class="input" type="text">
                                    <span class="icon is-small is-right password-icon-span">
                                        <font-awesome-icon v-if="showPassword === false" class="password-icon" icon="eye" @click="displayPassword()"/>
                                        <font-awesome-icon v-else class="password-icon" icon="eye-slash" @click="displayPassword()"/>
                                    </span>
                                </div>
                                <div class="text-row">
                                    <label class="checkbox remember-me">
                                        <input type="checkbox">
                                        Remember me
                                    </label>
                                    <router-link to="reset-password">
                                        <span class="text-link">
                                            Forgot Password?
                                        </span>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                        <div class="control">
                            <input class="button submit-button" type="submit" value="Sign In">
                        </div>
                        <div class="text-row">
                            <span class="no-account">
                                Don't have an account?
                            </span>
                            <span class="text-link" @click="popupTwoFactor()">
                                Contact Tendersure Team?
                            </span>
                        </div>
                    </form>
                </div>
                <div class="column is-4 registration">
                    <p class="column__title">Supplier Registration</p>
                    <div class="standard-height">
                        <p class="registration__text">
                            If you are not a registered supplier, click the <span class="registration__text--highlight"> 'REGISTER NOW'</span> button below
                            to register your company. If you have already registered, please login with your username and password.
                        </p>
                    </div>
                    <div class="control">
                        <router-link to="register">
                            <a class="button submit-button">
                                Register Now
                            </a>
                        </router-link>
                    </div>
                </div>
                <div class="column is-4 help-info">
                    <p class="column__title">Helpdesk</p>
                    <div class="standard-height">
                        <!-- <p class="help-info__text">QED Solutions Ltd</p> -->
                        <div class="contacts">
                            <p class="contact">
                                QED Solutions Ltd
                            </p>
                            <p class="contact">
                                Phone: +254 709 557 000,
                            </p>
                            <p class="contact">
                                Email: help@tendersure.co.ke,
                            </p>
                            <p class="contact">
                                Hours: Mon - Fri: 8:00 AM to 5:00 PM
                            </p>
                        </div>
                    </div>
                    <Socials />
                </div>
            </div>            
        </div>
        <div class="myfooter">
            <Footer />
        </div>
        <div class="popup" v-if="popTwoFactor === true" v-prevent-parent-scroll>
                <span class="popup__details">
                    <div class="page__head">
                        <span class="page__head--title">
                            <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupTwoFactor()" />
                            &nbsp;&nbsp;
                            Verification code
                        </span>

                        <div class="page__head--links">
                            
                        </div>
                    </div>
                    <div class="page__content columns">
                        <div class="column is-12 column-page is-centered">
                            <form v-on:submit.prevent="">
                                <div class="field">
                                    <label class="label">Enter the code sent to your email</label>
                                    <div class="control">
                                        <input v-model="verificationCode" class="input" type="text">
                                    </div>
                                </div>
                                <div class="control">
                                    <input class="button submit-button" type="submit" value="Verify">
                                </div>
                                <div class="text-row">
                                    <span class="no-account">
                                       
                                    </span>
                                    <span class="text-link" @click="popupTwoFactor()">
                                        Resend Code
                                    </span>
                                </div>
                            </form>
                        </div>
                    </div>
                </span>
            </div>  
    </div>
</template>

<script>
import Nav from '@/components/authentication/Nav'
import Footer from '@/components/authentication/Footer'
import Socials from '@/components/authentication/Socials'
import { mapGetters } from 'vuex'

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            previousRoute: '',
            showPassword: false,
            popTwoFactor: false,
            verificationCode: ''
        }
    },
    components: {
        Nav,
        Footer,
        Socials
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
    },
    methods: {
        scrollToTop() {
            window.scrollTo(0,0);
        },
        popupTwoFactor() {
            this.popTwoFactor = !this.popTwoFactor
            if (this.popTwoFactor === true) {
                this.scrollToTop()
            }
        },
        displayPassword: function() {
            this.showPassword = !this.showPassword
        },
        async login(){
            const { username, password } = this
            this.$store.dispatch('Auth/login', {  username, password })
            .then(() => {
                if(this.authStatus === 2) {
                    this.$store.dispatch('User/getUser')
                    .then(() => {

                    })

                    this.$router.push('/');
                } 
                if(this.authStatus === 3) {
                    window.toast.fire({
                        icon: 'error',
                        title: this.authError //'Invalid credentials. Please try again.'
                    })
                }
            })            
        },
        beforeRouteEnter(to, from, next) {
            next(vm => {
                vm.previousRoute = from
            });
        },
    }
}
</script>

<style lang="scss" scoped>

.content {
    padding: $line-height 5%;
    position: relative;
    z-index: 20;

    .myslider {
        width: 100%;
        margin-top: $line-height;
        height: 50vh;

        &__carousel {
            width: 100%;

            &--title {
                font-weight: 700;
                font-size: $line-height;
                margin-bottom: $line-height/2 !important;

                @media screen and (min-width: 1600px) {
                    font-size: $line-height*1.5;
                    margin-bottom: $line-height !important;
                }
            }


            &--desc {
                font-weight: 500;
                font-size: $font-size-normal;

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-title;
                }
            }

            &--item {
                width: 100%;
                height: 50vh;
                color: $color-white-main;
                @include grid_column;
                display: flex !important;
                align-items: flex-start;
                justify-content: flex-end;
                padding: $line-height*2;
                padding-bottom: 10vh;
            }

            .main-title {
                color: $color-blue-main;
                line-height: $line-height*1.5;
            }

            .item1 {
                background-image: url('../../assets/homebg.png');
                background-position: center 80%;
                background-repeat: no-repeat;
                background-size: cover;
            }

            .item2 {
                background-image: url('../../assets/homebg1.png');
                background-position: center center;
                background-repeat: no-repeat;
                background-size: cover;
            }

            .item3 {
                background-image: url('../../assets/homebg2.png');
                background-position: center center;
                background-repeat: no-repeat;
                background-size: cover;
            }
        }
    }

    &__row {
        width: 100%;
        background-color: $color-white-main;
        margin: 0;
        margin-top: $line-height/3;
        z-index: -1;
        position: relative;
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: 15px;
        padding: $line-height $line-height;

        .column {
            padding: $line-height/2 $line-height;

            &:not(:first-child) {
                border-left: 2px solid #E8E8E8;
            }

            &__title {
                font-size: $font-size-title;
                font-weight: 700;
                margin-bottom: $line-height/2 !important;
                color: $color-blue-main;

                @media screen and (min-width: 1600px) {
                    font-size: $line-height;
                }
            }

            .submit-button {
                width: 100%;
                margin: $line-height/4 0;
                color: $color-white-main;
                background-color: $color-green-main;
                font-weight: 600;
                border-radius: $line-height/2;
            }
        }

        .login-form {
            padding-right: $line-height;

            @media screen and (min-width: 1600px) {
                padding-right: $line-height*3;
            }

            .label {
                color: $color-blue-main;
                font-weight: 500;
                font-size: $font-size-text;

                @media screen and (min-width: 1600px) { 
                    font-size: $font-size-normal;
                }
            }

            .input {
                border-radius: $line-height/2;
                border: 1px solid #D0D0D0;

                &:focus {
                    outline: none;
                    border: 1px solid #D0D0D0;
                }
            }

            .password-icon {
                color: $color-green-main;
                cursor: pointer;
            }

            .password-icon-span {
                pointer-events: all;
            }

            .remember-me {
                color: $color-blue-main;
            }

            .text-row {
                @include grid_row;
                margin: $line-height/3 0;
                font-size: $font-size-small;
                flex-wrap: nowrap;

                span {
                    white-space: nowrap
                }
            }

            .text-link {
                color: $color-green-main;
                cursor: pointer;
                text-align: right;
            }

            .no-account {
                color: $color-black-main;
                font-weight: 500;
            }
        }

        .registration {
            text-align: left;
            padding-left: $line-height;
            padding-right: $line-height;

            @media screen and (min-width: 1600px) {
                padding-left: $line-height*2;
                padding-right: $line-height*2;
            }

            &__text {
                color: $color-black-medium;
                padding: 5% 0;
                padding-bottom: 15%;       
                text-align: justify;        

                font-size: $font-size-text;

                &--highlight {
                    color: $color-green-main;
                }

                @media screen and (min-width: 1600px) { 
                    font-size: $font-size-normal;
                }
            }
        }

        .help-info {
            &__text {
                padding: 5% 0;
                padding-bottom: 3%;
                font-size: $font-size-text;

                @media screen and (min-width: 1600px) { 
                    font-size: $font-size-normal;
                }
            }

            .contacts {
                font-size: $font-size-text;
                padding: 5% 0;

                @media screen and (min-width: 1600px) { 
                    font-size: $font-size-normal;
                }

                .contact {
                    margin-bottom: $line-height/8;
                }
            }

            .socials {

                margin-top: $line-height/2;

                &__icon {

                    &--img {
                        height: $line-height/1.5;
                    }

                    cursor: pointer;
                
                    &:not(:first-child) {
                        margin-left: $line-height;
                    }
                }
            }
        }
    }
}

.standard-height {
    min-height: 200px !important;
}

.popup {
    position: absolute; 
    top: 0vh;
    width: 100%;
    height: 100%; 
    z-index: 90;
    background-color: rgba(0, 0, 0, 0.6); 
    @include grid_row;
    align-items: flex-start;
    transition: opacity .3s;
    
    &__details {
        // position: sticky;
        top: 20vh;
        height: auto;
        min-height: 50vh;
        background-color: $color-white-main;
        $width: 35%;
        width: $width;
        margin: 20vh calc((100% - #{$width})/2);
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: $line-height $line-height/3;

        .page__content {
            padding-top: $line-height*2;
        }

        .column-page {
            box-shadow: none;
            padding: 0 $line-height;
            border-radius: 0;
        }

        .page__head {
            &--title {
                font-size: $font-size-title;
                font-weight: 700;
                margin-bottom: $line-height/2 !important;
                color: $color-blue-main;

                @media screen and (min-width: 1600px) {
                    font-size: $line-height;
                }
            }

            &--back {
                cursor: pointer;
            }
        }

        .submit-button {
            width: 100%;
            margin: $line-height/4 0;
            color: $color-white-main;
            background-color: $color-green-main;
            font-weight: 600;
            border-radius: $line-height/2;
        }

        .label {
            color: $color-blue-main;
            font-weight: 500;
            font-size: $font-size-text;

            @media screen and (min-width: 1600px) { 
                font-size: $font-size-normal;
            }
        }

        .input {
            border-radius: $line-height/2;
            border: 1px solid #D0D0D0;

            &:focus {
                outline: none;
                border: 1px solid #D0D0D0;
            }
        }

        .text-row {
            @include grid_row;
            margin: $line-height/3 0;
            font-size: $font-size-small;
            flex-wrap: nowrap;

            span {
                white-space: nowrap
            }
        }

        .text-link {
            color: $color-blue-main;
            cursor: pointer;
            text-align: right;
        }
    }
}

</style>

