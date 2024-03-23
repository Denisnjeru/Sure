const routes = [
    {
        path: '/qed/project_management/create_gantt_chart',
        name: 'QedProjectManagementGanttChartCreate',
        component: () => import('../../views/qed/project_management/timeline/CreateGanttChart.vue')
    },
    {
        path: '/qed/project_management/approved_gantt_chart',
        name: 'QedProjectManagementGanttChartApproved',
        component: () => import('../../views/qed/project_management/timeline/ApprovedGanttChart.vue')
    },
    {
        path: '/qed/project_management/project_gantt_chart',
        name: 'QedProjectManagementGanttChartProject',
        component: () => import('../../views/qed/project_management/timeline/ProjectGanttChart.vue')
    },
    {
        path: '/qed/project_management/meetings',
        name: 'QedProjectManagementMeetings',
        component: () => import('../../views/qed/project_management/meetings/Meetings.vue')
    },
    {
        path: '/qed/project_management/create_meetings',
        name: 'QedProjectManagementMeetingsCreate',
        component: () => import('../../views/qed/project_management/meetings/CreateMeetings.vue')
    },
    {
        path: '/qed/project_management/meetings/:id/update',
        name: 'QedProjectManagementMeetingsUpdate',
        component: () => import('../../views/qed/project_management/meetings/UpdateMeetings.vue')
    },
]

export default routes;