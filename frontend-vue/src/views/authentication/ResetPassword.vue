<template>
    <div class="reset-password">
        <div class="content">
            <Nav />
            <div class="content__row columns is-centered">
                <div class="content__form column is-5-desktop is-4-fullhd">
                    <p class="content__form--title">Reset Password</p>
                    <p class="content__form--desc">
                        Enter the email associated with your account and we
                        will send an email with instructions to reset
                        your password
                    </p>
                    <form class="content__form--form" v-on:submit.prevent="resetPassword()">
                        <div class="field">
                            <label class="label">Email</label>
                            <div class="control">
                                <input class="input" v-model="email" type="email" placeholder="Enter email address">
                            </div>
                        </div>
                        <div class="control">
                            <input class="button submit-button" :class="{ active: email !== '' }" type="submit" value="Reset">
                        </div>
                    </form>
                    <div class="columns help-info">
                        <div class="column is-3">
                            <p class="content__form--title">Help Desk</p>
                        </div>
                        <div class="column is-9">
                            <!-- <p class="help-info__text"></p> -->
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
import auth from '@/services/authentication/auth'
import Socials from '@/components/authentication/Socials'

export default {
  name: 'ResetPassword',
  data() {
    return {
        email: '',
    }    
  },
  components: {
    Nav,
    Footer,
    Socials
  },
  created() {
    this.logout()
  },
  methods: {
    logout: function() {
        this.$store.dispatch('Auth/logout')
        this.$store.dispatch('User/logout')
    },
    async resetPassword() {
        try {
            let payload = {
                "email": this.email,
                "redirect_url": 'http://localhost:8080/set-password'
            }
            await auth.resetPassword(payload)
            window.toast.fire({
                icon: 'success',
                title: 'Reset password email sent'
            })
        } catch (err) {
            console.log(err.response) 
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

        .content__form {
            background: $color-white-main;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: 15px;
            margin: $line-height*2 0;
            padding: $line-height $line-height*2;

            &--title {
                text-align: center;
                font-size: $font-size-title;
                font-weight: 700;
                margin-bottom: $line-height/2 !important;
                color: $color-blue-main;

                @media screen and (min-width: 1600px) {
                    font-size: $line-height;
                }

                @media screen and (min-width: 1600px) {
                    font-size: $font-size-major;
                }
            }

            &--desc {
                color: $color-black-main;
                text-align: center;
                font-size: $font-size-text;
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

                .content__form--title {
                    font-size: $font-size-normal;
                }

                &__text {
                    padding-bottom: $line-height/2;
                    margin-bottom: 0;
                }

                .contacts {
                    .contact {
                        margin-bottom: $line-height/8;
                        font-size: $font-size-text;
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

