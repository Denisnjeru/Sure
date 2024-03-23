<template>
    <div class="reset-password">
        <div class="content">
            <Nav />
            <div class="content__row columns is-centered">
                <div class="content__form column is-5-desktop is-5-fullhd">
                    <p class="content__form--title">Create Password</p>
                    <br>
                    <p class="content__form--desc">
                        Enter the email associated with your account and we
                        will send an email with instructions to reset
                        your password
                    </p>
                    <form class="content__form--form" v-on:submit.prevent="setPassword()">
                        <div class="field">
                            <label class="label">Password</label>
                            <div class="control has-icons-right">
                                <input v-if="showPassword === false" v-model="password" class="input" type="password" placeholder="Password">
                                <input v-else v-model="password" class="input" type="text">
                                <span class="icon is-small is-right password-icon-span">
                                    <font-awesome-icon v-if="showPassword === false" class="password-icon" icon="eye" @click="displayPassword()"/>
                                    <font-awesome-icon v-else class="password-icon" icon="eye-slash" @click="displayPassword()"/>
                                </span>
                            </div>
                            <p class="error" v-for="passwordError in passwordErrors" :key="passwordError">{{passwordError}}</p>
                            <p class="help">The new password must be at least 6 digits, contain at least one letter and at least one digit.</p>
                            
                            <label class="label">Confirm Password</label>
                            <div class="control has-icons-right">
                                <input v-if="showConfirmPassword === false" v-model="confirmPassword" class="input" type="password" placeholder="Confirm Password">
                                <input v-else v-model="confirmPassword" class="input" type="text">
                                <span class="icon is-small is-right password-icon-span">
                                    <font-awesome-icon v-if="showConfirmPassword === false" class="password-icon" icon="eye" @click="displayConfirmPassword()"/>
                                    <font-awesome-icon v-else class="password-icon" icon="eye-slash" @click="displayConfirmPassword()"/>
                                </span>
                            </div>
                        </div>
                        <div class="control">
                                <input class="button submit-button" :class="{ active: passwordErrors.length === 0 }" type="submit" value="Reset Password">
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
import auth from '@/services/authentication/auth'
import Socials from '@/components/authentication/Socials'

export default {
  name: 'SetPassword',
  data() {
    return {
        password: '',
        confirmPassword: '',
        showPassword: false,
        showConfirmPassword: false,
        passwordErrors: []
    }    
  },
  components: {
    Nav,
    Footer,
    Socials
  },
  created() {
    this.verifyToken()
  },
  watch: {
    password() {
        console.log(this.password)
        if (this.password.length < 8) {
            if (this.passwordErrors.find(element => element === 'Password must be at least 8 characters.') === undefined) {
                this.passwordErrors.push('Password must be at least 8 characters.')
            }
        } else {
            const index = this.passwordErrors.indexOf('Password must be at least 8 characters.');
            if (index > -1) {
                this.passwordErrors.splice(index, 1); 
            }
        }
        
    },
    confirmPassword(newConfirmPassword) {
        if (newConfirmPassword !== this.password) {
            if (this.passwordErrors.find(element => element === 'Confirm password and Password must be similar.') === undefined) {
                this.passwordErrors.push('Confirm password and Password must be similar.')
            }
        } else {
            const index = this.passwordErrors.indexOf('Confirm password and Password must be similar.');
            if (index > -1) {
                this.passwordErrors.splice(index, 1); 
            }
        }
    }
  },
  methods: {
    displayPassword: function() {
        this.showPassword = !this.showPassword
    },
    displayConfirmPassword: function() {
        this.showConfirmPassword = !this.showConfirmPassword
    },
    async verifyToken() {
        try { 
            await auth.verifyToken(this.$route.params.uidb64,this.$route.params.token);            
            
        } catch (err) {
            if (err.response) {
                window.toast.fire({
                    icon: 'error',
                    title: err.response.data.error
                })    
                this.$router.push('/reset-password');            
            }
        }
    },
    async setPassword() {
        try { 

            if (this.confirmPassword === '') {
                if (this.passwordErrors.find(element => element === 'Confirm password cannot be empty.') === undefined) {
                    this.passwordErrors.push('Confirm password cannot be empty.')
                }
                return
            } else {
                const index = this.passwordErrors.indexOf('Confirm password cannot be empty.');
                if (index > -1) {
                    this.passwordErrors.splice(index, 1); 
                }
            }
            

            if (this.confirmPassword !== this.password) {
                if (this.passwordErrors.find(element => element === 'Confirm password and Password must be similar.') === undefined) {
                    this.passwordErrors.push('Confirm password and Password must be similar.')
                }
                return
            } else {
                const index = this.passwordErrors.indexOf('Confirm password and Password must be similar.');
                if (index > -1) {
                    this.passwordErrors.splice(index, 1); 
                }
            }

            let payload = {
                "password": this.password,
                "token": this.$route.params.token,
                "uidb64": this.$route.params.uidb64
            }
            const response = await auth.setPassword(payload); 
            window.toast.fire({
                icon: 'success',
                title: response.data.success
            })    
            this.$router.push('/login');           
            
        } catch (err) {
            if (err.response) {
                window.toast.fire({
                    icon: 'error',
                    title: err.response.data.detail
                })    
                this.$router.push('/reset-password');            
            }
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
                text-align: justify;
                font-size: $font-size-normal;
            }

            .error {
                color: red;
                font-size: $font-size-small;
                margin-bottom: $line-height/8;
            }

            &--form {
                padding: $line-height/2 0;
                border-bottom: 0.5px solid #E5E5E5;

                .label {
                    color: $color-blue-main;
                    font-weight: 500;
                    font-size: $font-size-normal;

                    @media screen and (min-width: 1600px) { 
                        font-size: $font-size-normal;
                    }
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
                    color: $color-black-main;
                    font-size: $font-size-small;
                    font-weight: 500;
                }

                .password-icon {
                    color: $color-green-main;
                    cursor: pointer;
                }

                .password-icon-span {
                    pointer-events: all;
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

