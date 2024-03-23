import api from '../../apiV1/api';

const system_management = {
    users(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/users/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    user(userId) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/users/${userId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateUser(userId, content) {
        return new Promise((resolve, reject) => {
            api.put(`/qed/users/${userId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createUser(content) {
        return new Promise((resolve, reject) => {
            api.post(`/qed/users/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteUser(userId) {
        return new Promise((resolve, reject) => {
            api.delete(`/qed/users/${userId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    roles(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/roles/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    role(roleId) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/roles/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRole(content) {
        return new Promise((resolve, reject) => {
            api.post(`/qed/roles/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRole(roleId, content) {
        return new Promise((resolve, reject) => {
            api.put(`/qed/roles/${roleId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRole(roleId) {
        return new Promise((resolve, reject) => {
            api.delete(`/qed/roles/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rolePrivileges(roleId) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/role/privileges/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    assignRolePrivilege(roleId, content) {
        return new Promise((resolve, reject) => {
            api.post(`/qed/role/privileges/${roleId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRolePrivilege(roleId, privilegeId) {
        return new Promise((resolve, reject) => {
            api.delete(`/qed/role/privileges/${roleId}/${privilegeId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default system_management