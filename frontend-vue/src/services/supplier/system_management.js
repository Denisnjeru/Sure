import api from '../../apiV1/api';

const system_management = {
    users() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/company/users/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    user(userId) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/company/users/${userId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateUser(userId, content) {
        return new Promise((resolve, reject) => {
            api.put(`/supplier/company/users/${userId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createUser(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/company/users/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    roles() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/roles/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    role(roleId) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/roles/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRole(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/roles/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRole(roleId, content) {
        return new Promise((resolve, reject) => {
            api.put(`/supplier/roles/${roleId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRole(roleId) {
        return new Promise((resolve, reject) => {
            api.delete(`/supplier/roles/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rolePrivileges(roleId) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/role/privileges/${roleId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    assignRolePrivilege(roleId, content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/role/privileges/${roleId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRolePrivilege(roleId, privilegeId) {
        return new Promise((resolve, reject) => {
            api.delete(`/supplier/role/privileges/${roleId}/${privilegeId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default system_management