import api from '../../apiV1/api';

const user_management = {
    users() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/users/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    roles() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/roles/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_user(content) {
        return new Promise((resolve, reject) => {
            api.post(`/buyer/users/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_role(content) {
        return new Promise((resolve, reject) => {
            api.post(`/buyer/roles/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default user_management;