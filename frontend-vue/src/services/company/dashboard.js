import api from '../../apiV1/api';

const dashboardStats = {
    stats(days) {
        return new Promise((resolve, reject) => {
            days = days || 14;

            api.get(`/buyer/dashboard/?days=${days}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    daily_bidders(days) {
        return new Promise((resolve, reject) => {
            days = days || 14;

            api.get(`/buyer/daily_bidders/?days=${days}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    jobs() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/jobs/jobs_list/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    liveJobs() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/jobs/live_jobs/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}
export default dashboardStats;