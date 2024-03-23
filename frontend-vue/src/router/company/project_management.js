const routes = [
    {
        path: '/company/project_management/approved_gantt_chart',
        name: 'ProjectManagementGanttChartApproved',
        component: () => import('../../views/company/project_management/timeline/ApprovedGanttChart.vue')
    },
    {
        path: '/company/project_management/project_gantt_chart',
        name: 'ProjectManagementGanttChartProject',
        component: () => import('../../views/company/project_management/timeline/ProjectGanttChart.vue')
    },
    {
        path: '/company/project_management/meetings',
        name: 'ProjectManagementMeetings',
        component: () => import('../../views/company/project_management/meetings/Meetings.vue')
    },
]

export default routes;