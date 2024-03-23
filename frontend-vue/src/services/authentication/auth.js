import api from '../../apiV1/api';

const auth = {
    supplierRegister(content) {
        return new Promise((resolve, reject) => {
            api.post('/supplier/register/', content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    activateAccount(token) {
        return new Promise((resolve, reject) => {
            api.get(`/authentication/verify_email?token=${token}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    verifyToken(uidb64,token) {
        return new Promise((resolve, reject) => {
            api.get(`/authentication/password-reset/${uidb64}/${token}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    setPassword(content) {
        return new Promise((resolve, reject) => {
            api.patch(`/authentication/password-reset-complete`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    login(content) {
        return new Promise((resolve, reject) => {
            api.post('/authentication/login', content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    resetPassword(content) {
        return new Promise((resolve, reject) => {
            api.post('/authentication/request-reset-email/', content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    countryLocations(countryName) {
        return new Promise((resolve, reject) => {
            api.get(`/common/countries/${countryName}/locations/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    categoryTypes() {
        return new Promise((resolve, reject) => {
            api.get(`/common/category_types/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    companyProfile() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/profile/company/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateCompanyProfile(companyID, content) {
        return new Promise((resolve, reject) => {
            api.patch(`/supplier/profile/${companyID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierPrivileges() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/company/users/my_privileges/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    buyerPrivileges() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/users/my_privileges/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    logs(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/authentication/user_logs/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default auth
