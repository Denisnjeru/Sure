<template>
    <div class="profile">
        <div class="page__head">
            <span class="page__head--title">
                Change Password
            </span>

            <div class="page__head--links">
                <router-link to="/profile">
                    <a class="page__head--link button button-link">
                        Profile
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns is-centered">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Change password</p>
                </div>
                <div class="column-details__content">
                    <form v-on:submit.prevent="updatePassword()" class="content__form--form">
                        <div class="field">
                            <label class="label">Current Password</label>
                            <div class="control has-icons-right">
                                <input v-if="showCurrentPassword === false" v-model="currentPassword" class="input" type="password" placeholder="Current Password">
                                <input v-else v-model="password" class="input" type="text">
                                <span class="icon is-small is-right password-icon-span">
                                    <font-awesome-icon v-if="showCurrentPassword === false" class="password-icon" icon="eye" @click="displayCurrentPassword()"/>
                                    <font-awesome-icon v-else class="password-icon" icon="eye-slash" @click="displayCurrentPassword()"/>
                                </span>
                            </div>
                            <br>
                            <label class="label">New Password</label>
                            <div class="control has-icons-right">
                                <input v-if="showPassword === false" v-model="password" class="input" type="password" placeholder="New Password">
                                <input v-else v-model="password" class="input" type="text">
                                <span class="icon is-small is-right password-icon-span">
                                    <font-awesome-icon v-if="showPassword === false" class="password-icon" icon="eye" @click="displayPassword()"/>
                                    <font-awesome-icon v-else class="password-icon" icon="eye-slash" @click="displayPassword()"/>
                                </span>
                            </div>
                            <p class="error" v-for="passwordError in passwordErrors" :key="passwordError">{{passwordError}}</p>
                            <p class="help">The new password must be at least 6 digits, contain at least one letter and at least one digit.</p>
                            
                            <label class="label">Confirm New Password</label>
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
                            <div class="column-details__content is-centered additions form-submit">     
                                <input type="submit" class="button button-submit" value="Submit">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
        </div>
    </div>
</template>

<script>
// import auth from '@/services/authentication/auth'

export default {
    name: 'Change Password',
    data() {
        return {
            currentPassword: '',
            password: '',
            confirmPassword: '',
            showPassword: false,
            showCurrentPassword: false,
            showConfirmPassword: false,
            passwordErrors: []
        }    
    },
    mounted() {
        this.getProfile()
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
        async getProfile() {
            
        },
        displayPassword: function() {
            this.showPassword = !this.showPassword
        },
        displayConfirmPassword: function() {
            this.showConfirmPassword = !this.showConfirmPassword
        },
        displayCurrentPassword: function() {
            this.showCurrentPassword = !this.showCurrentPassword
        },
        async updatePassword() {
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

            window.toast.fire({
                icon: 'success',
                title: 'Password Update Successfully'
            })
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

.password-icon-span {
    pointer-events: all !important;
}

.password-icon {
    color: $color-green-main;
    cursor: pointer;
}

.error {
    color: red;
    font-size: $font-size-small;
    margin-bottom: $line-height/8;
}

.label {
    font-weight: 500 !important;
    font-size: $font-size-text;
}
</style>
