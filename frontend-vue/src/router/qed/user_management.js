const routes = [
    {
        path: '/qed/user/users',
        name: 'QedUserManagementUsers',
        component: () => import('../../views/qed/system_management/users/Users.vue')
      },
      {
        path: '/qed/user/users/create',
        name: 'QedUserManagementUsersCreate',
        component: () => import('../../views/qed/system_management/users/CreateUser.vue')
      },
      {
        path: '/qed/user/users/:id/update',
        name: 'QedUserManagementUsersUpdate',
        component: () => import('../../views/qed/system_management/users/UpdateUser.vue')
      },
      {
        path: '/qed/user/roles',
        name: 'QedUserManagementRoles',
        component: () => import('../../views/qed/system_management/roles/Roles.vue')
      },
      {
        path: '/qed/user/roles/create',
        name: 'QedUserManagementRolesCreate',
        component: () => import('../../views/qed/system_management/roles/CreateRole.vue')
      },
      {
        path: '/qed/user/roles/:id/update',
        name: 'QedUserManagementRolesUpdate',
        component: () => import('../../views/qed/system_management/roles/UpdateRole.vue')
      },
      {
        path: '/qed/user/roles/:id/privileges',
        name: 'QedUserManagementRolesPrivileges',
        component: () => import('../../views/qed/system_management/roles/Privileges.vue')
      },
      {
        path: '/qed/user/logs',
        name: 'QedUserManagementLogs',
        component: () => import('../../views/qed/system_management/logs/Logs.vue')
      },
]

export default routes;