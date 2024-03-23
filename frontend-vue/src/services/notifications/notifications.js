import api from '../../apiV1/api';

const notifications = {
    all_notifications_count() {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/api/all_count/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    all_notifications_list() {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/api/all/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    unread_notifications_count() {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/api/unread_count/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    unread_notifications_list() {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/api/unread_list/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    // assigned_notifications_list(){
    //     return new Promise((resolve, reject) => {
    //         api.get(`/notifications/live_assigned_notification_list/`,(data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    // mentioned_notifications_list(){
    //     return new Promise((resolve, reject) => {
    //         api.get(`/notifications/live_mentioned_notification_list/`,(data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    // participating_notifications_list(){
    //     return new Promise((resolve, reject) => {
    //         api.get(`/notifications/live_participating_notification_list/`,(data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    // review_requested_notifications_list(){
    //     return new Promise((resolve, reject) => {
    //         api.get(`/notifications/live_review_requested_notification_list/`,(data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    // starred_notifications_list(){
    //     return new Promise((resolve, reject) => {
    //         api.get(`/notifications/live_starred_notification_list/`,(data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    mark_all_as_read() {
        return new Promise((resolve, reject) => {
            api.get(`corenotification/mark-all-as-read/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    delete_notification(slug) {
        return new Promise((resolve, reject) => {
            api.delete(`core/notification/delete/${slug}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    mark_as_read(slug) {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/mark-as-read/${slug}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    mark_as_unread(slug) {
        return new Promise((resolve, reject) => {
            api.get(`core/notification/mark-as-unread/${slug}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default notifications;