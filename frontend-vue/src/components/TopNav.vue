<template>
    <div class="topNav">
        <div class="left">
            <div class="company-logo" v-if="authUser.user_type === 'buyer'">
                <img class="img" :src="authUser.company_logo" alt="">
            </div>
            <div class="company-logo" v-else>
                <img class="img" src="@/assets/qed-logo.png" alt="">
            </div>
            <div class="dropdown is-hoverable company-name">
                <div class="dropdown-trigger">
                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu4">
                    <span class="name" v-if="authUser.user_type !== 'qed'">{{authUser.company_name}}</span>
                    <span class="name" v-else>QED Solutions</span>
                    <span class="icon is-small">
                        <font-awesome-icon icon="chevron-down" />
                    </span>
                    </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                    <div class="dropdown-content">
                    <div class="dropdown-item">
                        <li>Test</li>
                    </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="right">
            <div class="basket right__item" v-if="authUser.user_type === 'supplier'">
                <router-link to="/supplier/dashboard/cart" class="basket__icon">
                    <font-awesome-icon class="basket__icon--icon" icon="shopping-basket" />
                </router-link>
            </div>
            <div class="dropdown  dropdown-notifications" v-click-outside="onClickOutside" v-on:click="popShowNotifications()">
                <div class="dropdown-trigger">
                    <div class="notifications right__item">
                        <span class="notifications__icon">
                            <font-awesome-icon  class="notifications__icon--icon" icon="bell" />
                            <sup class="notifications__count-two">{{ unread_count }}</sup>
                        </span>
                    </div>
                </div>
                <div v-if="showNotifications" class="dropdown-container --scroll-box">
                    <div class="dropdown-toolbar">
                        <h3 class="dropdown-toolbar-notifications-title"> 
                            <font-awesome-icon class="notifications__icon left" icon="bell" /> 
                            <span class="notifications__icon-title">Notifications</span>
                            <span class="notifications__count">Unread({{ unread_count }})</span>
                        </h3>
                    </div>
                    <div class="--scroll-box">
                        <NotificationDropDownVue  v-for="notification in notifications"
                                    :key="notification.id"
                                    :notification="notification"
                                    @read="markAsRead(notification.id)"
                        />
                        <li v-if="!hasUnread" class="notification-empty">
                            You don't have any unread notifications.
                        </li>
                    </div>
                    <router-link class="button button-link" to="/notifications">
                        <div class="button-link__button-text" align="center">See All</div>
                    </router-link>
                </div>
            </div>
            <div class="dropdown is-hoverable right__item user">
                <div class="dropdown-trigger">
                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu4">
                    <span class="user-details">
                        <img class="pic" src="@/assets/user.png" alt="">
                        <span class="info">
                            <span class="name">{{authUser.first_name}} {{authUser.last_name}}</span>
                            <br>
                            <span class="type" v-if="authUser !== null">{{authUser.user_type}}</span>
                        </span>
                    </span>
                    <span class="icon is-small">
                        <font-awesome-icon icon="chevron-down" />
                    </span>
                    </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                    <div class="dropdown-content">
                    <div class="dropdown-item">
                        <router-link to="/profile">
                            <span><font-awesome-icon icon="user" /> Profile</span>
                        </router-link>
                        <br>
                        <a @click="logout()"><font-awesome-icon icon="caret-square-right" /> Logout</a>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import notifications from "@/services/notifications/notifications"
import NotificationDropDownVue from './notifications/NotificationDropDown.vue'

export default {
    name: "TopNav",
    data(){
        return{
            showNotifications: false,
            unread_count:0,
            notifications: [],
        }
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
        hasUnread () {
            return this.unread_count > 0
        }
    },
    mounted(){
        this.getUnreadCount()
        this.fetchUnreadList()
    },
    methods: {
        logout: function() {
            this.$store.dispatch('Auth/logout')
            this.$store.dispatch('User/logout')
            this.$router.push('/login')
        },
        popShowNotifications () {
            this.showNotifications = !this.showNotifications
            console.log(this.notifications)
        },
        onClickOutside () {
            this.showNotifications = false
        },
        async getUnreadCount(){
            try{
                const response = await notifications.unread_notifications_count()
                this.unread_count = response.data.unread_count
            } catch(error){
                console.log(error)
            }
        },
        async fetchUnreadList(){
            try{
                const response = await notifications.unread_notifications_list()
                console.log('Fetching Unread Notifications !')
                console.log(response.data)
                this.notifications = response.data
            }catch(error){
                console.log(error)
            }
        },
        async AllMarkRead(){
            try{
                await notifications.mark_all_as_read()
                this.showNotifications = !this.showNotifications
                this.getUnreadCount()
            }catch(error){
                console.log(error)
            }
        },
        async markAsRead(note){
            try{
                await notifications.mark_as_read(note)
            }catch(error){
                console.log(error)
            }
        }
    },
    components:{
        NotificationDropDownVue
    }
}
</script>

<style lang="scss" scoped>
.topNav {
    width: 100%;
    padding: $line-height;
    @include grid_row;
    align-items: center;
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.05);
    background-color: $color-white-main;
    z-index: 100;
}

.company-name {    

    .dropdown-trigger .button {        
        background: #F2F7FF;
        color: $color-blue-main;
        font-size: $font-size-small;
        padding: $line-height/8 $line-height;
        border: none;
        border-radius: $line-height/2;
    }

    .name {
        margin-right: $line-height/2;
    }
}

.company-logo {
    @include grid_row;
    align-items: center;
    .img {
        height: $line-height*1.5;
        margin-right: $line-height/3;
    }
}

.left {
    @include grid_row;
    align-items: center;
    justify-content: flex-start;
}

.right {
    @include grid_row;
    align-items: center;

    &__item {
        padding: 0 $line-height/2;

        &:not(:last-child) {
            border-right: 2px solid #F2F6FF;
        }
    }

    .basket {
        &__icon {
            background-color: #F2F7FF;
            color: $color-blue-main;
            border-radius: $line-height/4;

            &--icon {
                margin: 6px;
            }
        }
    }

    .notifications {
        &__icon {
            &--icon {
                color: $color-blue-main;
                font-size: $font-size-major;
            }
        }
    }

    .user {
        background: #F2F7FF;
        border-radius: $line-height/2;
        padding: 0 $line-height/4;
        margin: 0 $line-height/2;

        .button {      
            background-color: transparent;
            color: $color-blue-main;
            font-size: $font-size-small;
            border: none;            
            @include grid_row;
            align-items: flex-start;
            padding: 0 $line-height/4;
            margin-bottom: $line-height/2;
            margin-top: $line-height/3;

            .user-details {
                @include grid_row;
                align-items: center;
                align-items: flex-start;
                margin-right: $line-height/2;

                .pic {
                    height: $line-height*2;
                    width: $line-height*2;
                }

                .info {
                    text-align: left;

                    .name {
                        color: $color-black-main;
                        font-weight: 500;
                    }

                    .type {
                        color: $color-green-main;
                        font-size: $font-size-small;
                        text-transform: capitalize;
                    }
                }
            }
        }
    }
    .dropdown-container{
        cursor: pointer;
        position: relative;
        display: inline-block;
        
    }
    .dropdown-toolbar {
        padding-top: 6px;
        padding-left: 20px;
        padding-right: 20px;
        padding-bottom: 5px;
        background-color: #fff;
        border-bottom: 1px solid rgba(0, 0, 0, 0.15);
        border-radius: 4px 4px 0 0;
    }
    .dropdown-toolbar .dropdown-toolbar-actions {
        float: right;
    }
    .dropdown-toolbar .dropdown-toolbar-title {
        margin: 0;
        font-size: 14px;
    }
    .dropdown-toolbar .dropdown-toolbar-notifications-title{
        margin: 0;
        font-size: 14px;
    }
    .dropdown-notifications .dropdown-toolbar{
        padding: 9.6px 12px;
    }
    .dropdown-notifications .dropdown-footer {
        padding: 1.6px 12px;
    }
    .dropdown-notifications .dropdown-toolbar {
        background: #fff;
    }
    .dropdown-notifications .dropdown-footer {
        background: #eeeeee;
        padding: 9.6px 20px;
    }
    .dropdown-container > .dropdown-menu {
        position: static;
        z-index: 1000;
        float: none!important;
        padding: 10px 0;
        margin: 0;
        border: 0;
        background: transparent;
        border-radius: 0;
        -webkit-box-shadow: none;
        box-shadow: none;
        max-height: 330px;
        overflow-y: auto;
    }
    .dropdown-container > .dropdown-menu + .dropdown-menu {
        padding-top: 0;
    }
    .dropdown-menu > li > a {
        overflow: hidden;
        white-space: nowrap;
        word-wrap: normal;
        text-decoration: none;
        text-overflow: ellipsis;
        -o-text-overflow: ellipsis;
        -webkit-transition: none;
        -o-transition: none;
        transition: none;
    }
    .dropdown-menu .notification{
        padding: 9.6px 12px;
    }
    .dropdown-notifications > .dropdown-container,
    .dropdown-notifications > .dropdown-menu {
        width: 450px;
        max-width: 450px;
    }
    .dropdown-notifications .dropdown-menu {
        padding: 0;
    }
    .dropdown-footer {
        padding: 2.5px 20px;
        border-top: 1px solid #ccc;
        // border-top: 1px solid rgba(0, 0, 0, 0.15);
        border-radius: 0 0 4px 4px;
    }
    .dropdown-footer-hover{
        & :hover{
            background: #ccc;
        }
    }

    .dropdown-notifications {
        cursor: pointer;
        .dropdown-container {
            display: block;
            position: absolute;
            background-color: #fff;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 20;
            margin-top: 4.2vh;
            margin-left: -20ch;
            width: 40ch;
            padding: $line-height/2;
            border-radius: 10px;

            .--scroll-box {
                height: 600px;
                overflow-y: scroll;
                scrollbar-width: thin;
            }

        }
    
        .notification-icon.hide-count:after {
            display: none;
        }
    
        .dropdown-toolbar .dropdown-toolbar-actions {
            margin-top: -2px;
            font-size: 13px;
        }
    
        .notification-mark-read {
            float: right;
            float: right;
            color: #333;
            opacity: 0.4;
        
            &:hover {
                opacity: .8;
            }
        }
    
        .notification-action {
            margin-top: 5px;
            margin-bottom: 2px;
        }
    
        .notification .media-body {
            padding-top: 0px;
        }
    
        .media-object img {
            width: 64px;
        }
    }
    .notications-dropdown {
        cursor: pointer;
        position: relative;
        display: inline-block;

        &__content {
            display: block;
            position: absolute;
            background-color: #f1f1f1;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 20;
            margin-top: 4.2vh;
            margin-left: -20ch;
            width: 44ch;
            padding: $line-height/2;
        }
    }
    .notifications {
        display: block;
        margin-right: $line-height/2;

        &__icon, &__count {
            display: inline;
        } 

        &__icon {
            color: $color-blue-main;
            font-size: $font-size-title;
            vertical-align:text-top;
        }

        &__icon-title{
            right: -2ch;
            font-weight: 600;
            color: $color-lightblue-text;
            position: relative;
        }

        &__count {
            color: $color-blue-main;
            font-weight: 600;
            position: absolute;
            right:2ch;
        }
        &__count-two {
            color: $color-blue-main;
            font-weight: 400;
            position: absolute;
            margin-top: -2px;
            font-size: 75%;
        }
    }
    .notification-empty{
        display: block;
        padding: 9.6px 12px;
        border-bottom: 1px solid #eeeeee;
        color: #333333;
        background-color: $color-white-main;
        text-decoration: none;
    }
    .button-link{
        width: 100%;
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
            color: $color-white-main;
        }

        &:hover, :focus {
            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
            transform: translateY(-0.25em);
        }
    }
}

</style>
