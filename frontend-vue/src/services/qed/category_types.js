import api from '../../apiV1/api';

const category_types = {
    category_types(page) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/category/type/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_groups() {
        return new Promise((resolve, reject) => {
            api.get(`/qed/category/groups/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_type(id) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/category/type/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_type_countries(category_type_id, page) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/criteria/country/${category_type_id}/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_category_type(content) {
        return new Promise((resolve, reject) => {
            api.post(`/qed/category/type/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_category_type(form, id) {
        return new Promise((resolve, reject) => {
            api.put(`/qed/category/type/${id}/`, form, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    location(location_id) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/criteria/locations/${location_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_category_type_criteria(form_data) {
        return new Promise((resolve, reject) => {
            api.post(`/qed/category_type/criteria/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_category_type_criteria(id, form_data) {
        return new Promise((resolve, reject) => {
            api.put(`/qed/category_type/criteria/${id}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_type_criteria(criteria_id){
        return new Promise((resolve, reject) => {
            api.get(`/qed/category_type/criteria/${criteria_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    }
}
export default category_types;