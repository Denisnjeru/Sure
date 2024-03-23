import api from '../../apiV1/api';

const archive = {
    jobs() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/jobs/jobs_list/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default archive