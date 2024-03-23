<template>
    <div class="reset-password">
        <div class="content">
            <Nav />
            <div class="content__row columns is-centered">
                <div class="content__form column is-5-desktop is-4-fullhd">
                    <p class="content__form--title">Change Password</p>
                    <p class="content__form--desc">
                        Your new password must be different from previous used passwords.
                    </p>
                    <form class="content__form--form">
                        <div class="field">
                            <label class="label">Old Password</label>
                            <div class="control has-icons-right">
                                <input class="input" type="password" placeholder="Password">
                                <span class="icon is-small is-right">
                                    <font-awesome-icon class="password-icon" icon="eye" />
                                    <!-- <font-awesome-icon class="password-icon" icon="eye-slash" /> -->
                                </span>
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">New Password</label>
                            <div class="control has-icons-right">
                                <input class="input" type="password" placeholder="Password">
                                <span class="icon is-small is-right">
                                    <font-awesome-icon class="password-icon" icon="eye" />
                                    <!-- <font-awesome-icon class="password-icon" icon="eye-slash" /> -->
                                </span>
                            </div>
                            <p class="help">The new password must be at least 6 digits, contain at least one letter and at least one digit.</p>
                            <div class="control has-icons-right">
                                <input class="input" v-model="confirmPassword" type="password" placeholder="Confirm Password">
                                <span class="icon is-small is-right">
                                    <font-awesome-icon class="password-icon" icon="eye" />
                                    <!-- <font-awesome-icon class="password-icon" icon="eye-slash" /> -->
                                </span>
                            </div>
                        </div>
                        <div class="control">
                            <router-link to="login">
                                <a class="button submit-button" :class="{ active: confirmPassword !== '' }">
                                    Change Password
                                </a>
                            </router-link>
                        </div>
                    </form>
                    <div class="columns help-info">
                        <div class="column is-3">
                            <p class="content__form--title">Help Desk</p>
                        </div>
                        <div class="column is-9">
                            <p class="help-info__text">QED Solutions Ltd</p>
                            <div class="contacts">
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

                            <Socials />
                        </div>
                    </div>
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
import Socials from '@/components/authentication/Socials'
export default {
  name: 'ResetPassword',
  data() {
    return {
        confirmPassword: '',
    }    
  },
  components: {
    Nav,
    Footer,
    Socials
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

        .content__form {
            background: $color-white-main;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: 15px;
            margin: $line-height*2 0;
            padding: $line-height $line-height*2;

            &--title {
                color: $color-black-main;
                font-size: $font-size-title;
                font-weight: 500;
                text-align: center;

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-major;
                }
            }

            &--desc {
                color: $color-black-main;
                text-align: center;
            }

            &--form {
                padding: $line-height/2 0;
                border-bottom: 0.5px solid #E5E5E5;

                .label {
                    color: $color-black-main;
                    font-weight: 500;
                }

                .input {
                    width: 100%;
                    border-radius: $line-height/2;
                    border: 1px solid #D0D0D0;
                    font-size: $font-size-text;  
                    color: $color-black-main;   
                    padding: $line-height $line-height/2;           

                    &:focus {
                        outline: none;
                    }
                }

                .help {
                    font-size: $font-size-text;
                }

                .password-icon {
                    color: $color-green-main;
                }

                .submit-button {
                    width: 100%;
                    margin: $line-height/4 0;
                    color: $color-white-main;
                    background-color: $color-gray-main;
                    font-weight: 600;
                    padding: $line-height/2 0;
                    border-radius: $line-height/2;
                }

                .active {
                    background-color: $color-green-main;
                }
            }

            .help-info {
                padding: $line-height 0;
                font-size: $font-size-text;

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-normal;
                }

                &__text {
                    padding-bottom: $line-height/2;
                    margin-bottom: 0;
                }

                .contacts {
                    .contact {
                        margin-bottom: $line-height/6;
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
}



</style>

