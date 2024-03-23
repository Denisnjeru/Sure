import api from '../../apiV1/api';

const archive = {
    companies() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/archive/companies/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    categories(companyID) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/archive/company/${companyID}/categories/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    documents(categoryId, jobType){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/archive/documents/${categoryId}/${jobType}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default archive