<template>
    <div class="notify">
        <div class="page__head">
            <span class="page__head--title">
                Notifications
            </span>

            <div class="page__head--links">
                <a class="page__head--link unread-link" @click.prevent="filterUnReadOnly()">
                    UNREAD(3)
                </a>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column column-page --scroll-box">
                <div class="notification-card">
                    <div class="media">
                        <ul>
                            <li v-for="notification in notifications"  v-bind:key="notification.id" :id="notification.id">
                                <div class="media-body">
                                    <div class="media-img">
                                        <div class="media-object">
                                            <img src="@/assets/logo.png">
                                        </div>
                                    </div>
                                    <div class="media-text">
                                        <a href="#" class="notification-mark-read" title="Mark as read">
                                            <span class="notification-card-title">{{ notification.verb }}</span>
                                        </a>
                                        <span class="mark_as_read">
                                            <span class="mark_as_read__mark_text" @click.prevent="markAsRead(notification.id)">Mark as Read </span>
                                            <font-awesome-icon  class="mark_as_read__delete" icon="trash-alt" @click.prevent="deleteNotification(notification.id)"/>
                                        </span>
                                        
                                        <p class="paragraph_text">
                                            {{ notification.description }}
                                        </p>

                                        <div class="notification-meta">
                                            <small class="timestamp">
                                                <timeago :datetime="notification.timestamp" :auto-update="30"/>
                                            </small>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import notifications from "@/services/notifications/notifications"

export default {
    name: 'notifications-page',
    data () {
        return{
            notifications: [],
        }
    },
    mounted(){
        this.fetchAllList()
    },
    methods:{
        async fetchAllList(){
            try{
                const response = await notifications.all_notifications_list()
                console.log('Fetching All Notifications !')
                console.log(response.data)
                this.notifications = response.data

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
        },
        async deleteNotification(note){
            try{
                await notifications.delete_notification(note)
                this.fetchAllList()
                this.$router.go(); // Refresh Page
            }catch(error){
                console.log(error)
            }
        },
        async filterUnReadOnly(){
            try{
                const response = await notifications.unread_notifications_list()
                console.log('Unread Notifications !')
                console.log(response.data)
                this.notifications = response.data
            }catch(error){
                console.log(error)
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@include page;
.page{
    .column-page{
        border-radius: 15px;
        padding: 12px 20px;
        margin-bottom: 12px;
        display: flex;
        flex-flow: column nowrap;
        justify-content: space-between;
        align-items: center;
    }
    &__head {
        .unread-link {
            font-size: 1em;
            font-weight: 500;
            color: $color-blue-main;
            transform: rotate(0.02deg);
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em #FEFEFE;
                transform: translateY(-0.25em);
            }
        }
        &--title {
            font-size: 25px;
            color: $color-lightblue-text;
            font-weight: 600;

            .title__active {
                color: $color-green-light;
            }

            @media screen and (max-width: 1600px) {
                font-size: $font-size-normal;
            }
        }
    }
    &__content {
        .--scroll-box {
            width: 300px;
            height: 900px;
            overflow-y: scroll;
            scrollbar-width: thin;
        }

        .notification-card{
            display: block;
            padding: 9.6px, 12px;
            color: #333333;
            background-color: $color-white-main;
            text-decoration: none;
            .media{
                align-items: flex-start;
                display: flex;
                text-align: inherit;

                .media-body{
                    padding-top: 5.6px;
                    border-bottom: 1px solid #eeeeee;
                    display: flex;
                    .media-img{
                        float: left;
                        padding-right: 20px;
                    }

                    .media-text{
                        display: block;
                        float: right;
                        width:90%;
                    }
                    .paragraph_text{
                        color: $color-black-light;
                    }
                }
                .media-object img {
                    width: 64px;
                }
            }

            .notification-mark-read{
                display: inline;

                .notification-card-title{
                    color: black;
                    font-size: 15px;
                    font-weight: 600;
                }
            }
            .mark_as_read{
                float: right;
                color: #121F3ECC;

                &__mark_text{
                    font-size: 15px;
                    font-weight: 500;
                    text-align: justify;
                }

                &__delete{
                    color: $color-gray-main;
                    margin-left: 1em;

                    &:hover, :focus {
                        box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                        transform: translateY(-0.25em);
                    }
                }
            }

            .notification-meta {
                padding-top: 10px;
                padding-bottom: 10px;
                .timestamp{
                    color: $color-black-light;
                    display: inline;
                }
                .more{
                    font-size: 0.875em;
                    font-weight: 600;
                    position: absolute;
                    right:2ch;
                    color: $color-blue-main;
                    display: inline;
                }
            }
        }
    }
}

</style>