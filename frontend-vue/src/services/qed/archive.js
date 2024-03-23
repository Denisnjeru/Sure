import api from '../../apiV1/api';

const archive = {
    buyers(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    jobs(page, dataPerPage, buyerId) {
        return new Promise((resolve, reject) => {
            api.get(`/qed/jobs/buyer/${buyerId}/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default archive