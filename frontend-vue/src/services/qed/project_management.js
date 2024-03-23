import api from '../../apiV1/api';

const project_management = {
    buyers() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/list/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    companyJobs(companyId) {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/jobs/company/${companyId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createTimeline(content) {
        return new Promise((resolve, reject) => {
            api.post(`/projectmanagement/timelines/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    timelines(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/projectmanagement/timelines/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteTimeline(timelineId) {
        return new Promise((resolve, reject) => {
            api.delete(`/projectmanagement/timelines/${timelineId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createMeeting(content) {
        return new Promise((resolve, reject) => {
            api.post(`/projectmanagement/meetings/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    meetings(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/projectmanagement/meetings/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    meeting(meetingId) {
        return new Promise((resolve, reject) => {
            api.get(`/projectmanagement/meetings/${meetingId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateMeeting(meetingId, content) {
        return new Promise((resolve, reject) => {
            api.patch(`/projectmanagement/meetings/${meetingId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteMeeting(meetingId) {
        return new Promise((resolve, reject) => {
            api.delete(`/projectmanagement/meetings/${meetingId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default project_management