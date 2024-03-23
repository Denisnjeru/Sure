import api from '../../apiV1/api';

const dashboardStats = {
    stats() {
        return new Promise((resolve, reject) => {
            api.get(`/qed/dashboard/stats/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    liveJobs() {
        return new Promise((resolve, reject) => {
            api.get(`qed/dashboard/live_jobs/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    monthlyBids() {
        return new Promise((resolve, reject) => {
            api.get(`qed/dashboard/monthly_bids/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    monthlySupplierRegistration() {
        return new Promise((resolve, reject) => {
            api.get(`qed/dashboard/monthly_registration/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    jobs() {
        return new Promise((resolve, reject) => {
            api.get(`qed/dashboard/jobs/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}
export default dashboardStats;