<template>
    <div class="side-nav">
        <div class="columns is-centered is-multiline">
            <div class="column is-centered is-12 brand">
                <router-link to="/">
                    <img class="brand__logo" src="@/assets/logo.png" alt="logo">
                </router-link>
            </div>
            <div class="column is-12 nav-links" v-if="userData">
                <router-link to="/">
                    <a class="button nav-links__link" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'dashboard')) === true }">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/dashboard-icon.png" alt="logo">
                                Dashboard
                            </span>
                        <span class="right">
                            <span class="right__active">
                                |
                            </span>
                        </span>
                    </a>
                </router-link>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'supplier'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'projectmanagement')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/project-management-icon.png" alt="logo">
                            Project Management
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                    <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content" v-if="userData.user_type === 'buyer'">
                            <div class="dropdown-item">
                                <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementtimeline')) === true }">Timeline</p>
                                <router-link to="/company/project_management/approved_gantt_chart">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementganttchartapproved')) === true }">Approved Gantt Chart</p>
                                </router-link>
                                <router-link to="/company/project_management/project_gantt_chart">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementganttchartproject')) === true }">Project Gantt Chart</p>
                                </router-link>
                                <router-link to="/company/project_management/meetings">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementmeeting')) === true }">Meetings</p>
                                </router-link>
                            </div>
                        </div>
                        <div class="dropdown-content" v-if="userData.user_type === 'qed'">
                            <div class="dropdown-item">
                                <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementganttchart')) === true }">Timeline</p>
                                <router-link to="/qed/project_management/approved_gantt_chart">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementganttchartapproved')) === true }">Approved Gantt Chart</p>
                                </router-link>
                                <router-link to="/qed/project_management/project_gantt_chart">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementganttchartproject')) === true }">Project Gantt Chart</p>
                                </router-link>
                                <router-link to="/qed/project_management/meetings">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'projectmanagementmeeting')) === true }">Meetings</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type === 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'sourcing')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/prequal-icon.png" alt="logo">
                            Sourcing
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                    <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content" v-if="userData.user_type === 'qed'">
                            <div class="dropdown-item">
                                <router-link to="/qed/prequalification/buyers">
                                    <p class="dropdown-item__link">Prequalification</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/qed/rfq/buyers">
                                    <p class="dropdown-item__link">RFQ</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/qed/tender/buyers">
                                    <p class="dropdown-item__link">Tender</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'companyprequal')) === true || ($options.filters.nameInRoute($route.name, 'supplierprequal')) === true }">
                    <span class="dropdown-trigger">
                        <router-link v-if="userData.user_type === 'supplier'" to="/supplier/prequal/ordered/categories">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/prequal-icon.png" alt="logo">
                                Prequalification
                            </span>
                        </router-link>
                        <router-link v-else to="/company/prequalifications">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/prequal-icon.png" alt="logo">
                                Prequalification
                            </span>
                        </router-link>
                        <span class="right">

                        </span>
                    </span>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'rfq')) === true }">
                    <span class="dropdown-trigger">
                        <router-link v-if="userData.user_type === 'supplier'" to="/supplier/list/rfqs">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/rfq-icon.png" alt="logo">
                                RFQ
                            </span>
                        </router-link>
                        <router-link v-else to="/company/rfqs">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/rfq-icon.png" alt="logo">
                                RFQ
                            </span>
                        </router-link>
                        <span class="right">

                        </span>
                    </span>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'tender')) === true }">
                    <span class="dropdown-trigger">
                        <router-link v-if="userData.user_type === 'supplier'" to="/supplier/tender/ordered/categories">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/tender-icon.png" alt="logo">
                                Tender
                            </span>
                        </router-link>
                        <router-link v-if="userData.user_type === 'buyer'" to="/company/tenders">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/tender-icon.png" alt="logo">
                                Tender
                            </span>
                        </router-link>
                        <span class="right">

                        </span>
                    </span>
                </a>

<!--                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'tender')) === true }">-->
<!--                    <span class="dropdown-trigger">-->
<!--                        <router-link v-if="userData.user_type === 'supplier'" to="/supplier/tender/ordered/categories">-->
<!--                            <span class="left">-->
<!--                                <img class="nav-links__link&#45;&#45;image" src="@/assets/icons/tender-icon.png" alt="logo">-->
<!--                                Tender-->
<!--                            </span>-->
<!--                        </router-link>-->
<!--                        <span class="left" v-else>-->
<!--                            <img class="nav-links__link&#45;&#45;image" src="@/assets/icons/tender-icon.png" alt="logo">-->
<!--                            Tender-->
<!--                        </span>-->
<!--                        <span class="right">-->
<!--                            <font-awesome-icon class="nav-links__link&#45;&#45;icon" icon="chevron-right" />-->
<!--                        </span>-->
<!--                    </span>-->
<!--                    <div class="dropdown-menu" id="dropdown-menu1" role="menu">-->
<!--                        <div class="dropdown-content">-->
<!--                            <div class="dropdown-item">-->
<!--                                <router-link to="/company/tenders">-->
<!--                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'companytenders')) === true }">Consolidated</p>-->
<!--                                </router-link>-->
<!--                                <router-link to="/company/tenders">-->
<!--                                    <p class="dropdown-item__link">Multi-Item</p>-->
<!--                                </router-link>-->
<!--                            </div>-->
<!--                        </div>                        -->
<!--                    </div>-->
<!--                </a>-->

                <a class="button nav-links__link dropdown is-hoverable" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'auction')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/auction-icon.png" alt="logo">
                            eAuction
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                    <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">
                                <router-link to="/buyer/list/reverse/auction" v-if="userData.user_type === 'buyer'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'reverse')) === true }">Reverse Auction</p>
                                </router-link>
                                <router-link to="/supplier/list/reverse/auction" v-if="userData.user_type === 'supplier'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'reverse')) === true }">Reverse Auction</p>
                                </router-link>
                                <p class="dropdown-item__link" v-if="userData.user_type === 'qed'" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedreverse3')) === true }">Reverse Auction</p> 
                                <router-link v-if="userData.user_type === 'qed'" to="/qed/list/buyers/reverse/auction">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'reverse')) === true }">Buyer</p> 
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/buyer/list/foward/auction" v-if="userData.user_type === 'buyer'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'foward')) === true }">Foward Auction</p> 
                                </router-link>
                                <router-link to="/supplier/list/foward/auction" v-if="userData.user_type === 'supplier'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'foward')) === true }">Foward Auction</p>
                                </router-link>
                                <p class="dropdown-item__link" v-if="userData.user_type === 'qed'" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedfoward3')) === true }">Foward Auction</p> 
                                <router-link v-if="userData.user_type === 'qed'" to="/qed/list/buyers/foward/auction">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'foward')) === true }">Buyer</p> 
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'auction')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/asset-disposal-icon.png" alt="logo">
                            Asset Disposal
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                    <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">
                                <router-link to="/buyer/list/risk-management">
                                    <p class="dropdown-item__link">Disposal Planning</p>
                                </router-link>
                                <router-link to="/buyer/list/risk-management">
                                    <p class="dropdown-item__link">Bidding</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.path, 'risk-management')) === true }">
                    <span class="dropdown-trigger">
                        <router-link v-if="userData.user_type === 'supplier'" to="/buyer/list/risk-management">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/risk-management-icon.png" alt="logo">
                                Risk Management
                            </span>
                        </router-link>
                        <router-link v-else to="/buyer/list/risk-management">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/risk-management-icon.png" alt="logo">
                                Risk Management
                            </span>
                        </router-link>
                        <span class="right">

                        </span>
                    </span>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'contracts')) === true }">
                    <span class="dropdown-trigger">
                        <router-link v-if="userData.user_type === 'supplier'" to="/supplier/contracts">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/contract-icon.png" alt="logo">
                                Contract
                            </span>
                        </router-link>
                        <span v-else class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/contract-icon.png" alt="logo">
                            Contract
                        </span>
                        <span class="right">
                            <font-awesome-icon v-if="userData.user_type !== 'supplier'" class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                    <div v-if="userData.user_type !== 'supplier'" class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">
                                <router-link to="/buyer/contracts/qed" v-if="userData.user_type === 'buyer'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'contractsqed')) === true }">QED Contract</p>
                                </router-link>
                                <router-link to="/qed/contracts/buyer" v-if="userData.user_type === 'qed'">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedcontracts')) === true }">QED Contract</p>
                                </router-link>
                                <router-link to="/buyer/contracts/supplier/jobs">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'contractssupplier')) === true }">Supplier Contract</p>
                                </router-link>
                                <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'contractstemplates')) === true }">Template</p>
                                <router-link to="/buyer/contracts/templates">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'contractstemplatestemplates')) === true }">Contract Template</p>
                                </router-link>
                                <router-link to="/buyer/contracts/sections">
                                    <p class="dropdown-item__link level2" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'contractstemplatessections')) === true }">Contract Section</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <a class="button nav-links__link" v-if="userData.user_type === 'supplier'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'archive')) === true }">
                    <span class="dropdown-trigger">
                        <router-link  to="/supplier/archive/companies">
                            <span class="left">
                                <img class="nav-links__link--image" src="@/assets/icons/archive-icon.png" alt="logo">
                                Archive
                            </span>
                        </router-link>
                        <span class="right">
                        </span>
                    </span>
                </a>
                <!-- <a class="button nav-links__link" href="https://e-procure.co.ke" v-if="userData.user_type !== 'supplier'">
                    <span class="left">
                        <img class="nav-links__link--image" src="@/assets/icons/eprocure-icon.png" alt="logo">
                        eProcure
                    </span>
                    <span class="right">
                    </span>
                </a>

                <a class="button nav-links__link" v-if="userData.user_type !== 'supplier'">
                    <span class="left">
                        <img class="nav-links__link--image" src="@/assets/icons/ecommerce-icon.png" alt="logo">
                        eCommerce
                    </span>
                    <span class="right">
                    </span>
                </a> -->
                <!-- <a class="button nav-links__link">
                    <span class="left">
                        <font-awesome-icon class="nav-links__link--icon" icon="file-invoice" />
                        Report
                    </span>
                    <span class="right">
                        <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                    </span>
                </a> -->
                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type === 'qed'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'bwqed')) === true }">
                  <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/buyer-world-icon.png" alt="logo">
                          Buyer World
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right"/>
                        </span>
                  </span>
                  <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                      <div class="dropdown-content">
                          <div class="dropdown-item" v-if="userData.user_type === 'qed'">
                              <router-link to="/qed/archive/buyers">
                                  <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedarchive')) === true }">Archive</p>
                              </router-link>
                          </div>
                      </div>
                  </div>
                </a>
                <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type === 'buyer'">
                  <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/supplier-world-icon.png" alt="logo">
                          Supplier World
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right"/>
                        </span>
                  </span>
                  <div class="dropdown-menu" id="dropdown-menu1" role="menu">
                      <div class="dropdown-content">
                          <div class="dropdown-item">
                            <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'CompanyPrequalLetterJobs')) === true }">Letters</p>
                                <router-link to="/company/prequal/letters/jobs">
                                    <p class="dropdown-item__link level2"
                                       :class="{ activeLink: ($options.filters.nameInRoute($route.name,
                                        'CompanyPrequalLetterJobs')) === true }">Prequalification</p>
                                </router-link>
                                <router-link to="/company/tender/letters/jobs">
                                    <p class="dropdown-item__link level2"
                                       :class="{ activeLink: ($options.filters.nameInRoute($route.name,
                                       'CompanyTenderLetterJobs')) === true }">Tender</p>
                                </router-link>
                          </div>
                          <div class="dropdown-item" v-if="userData.user_type === 'buyer'">
                              <router-link to="/company/archive/jobs">
                                  <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'companyarchivejobs')) === true }">Archive</p>
                              </router-link>
                          </div>
                      </div>
                  </div>
                </a>

                <a class="button nav-links__link dropdown is-hoverable" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'usermanagement')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/users-icon.png" alt="logo">
                            User Management
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right"/>
                        </span>
                    </span>
                    <div v-if="userData.user_type === 'supplier' && authPrivileges.some(privilege => privilege.title === 'MANAGE_USER')" class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">
                                <router-link to="/supplier/user/users">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'supplierusermanagementusers')) === true }">Users</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/supplier/user/roles">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'supplierusermanagementroles')) === true }">Roles</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/supplier/user/logs">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'supplierusermanagementlogs')) === true }">Logs</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <div v-if="userData.user_type === 'buyer'" class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">

                                <router-link to="/buyer/user/users">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'buyerusermanagementusers')) === true }">Users</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/buyer/user/roles">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'buyerusermanagementroles')) === true }">Roles</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/buyer/user/logs">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'buyerusermanagementlogs')) === true }">Logs</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <div v-if="userData.user_type === 'qed'" class="dropdown-menu" id="dropdown-menu1" role="menu">
                        <div class="dropdown-content">
                            <div class="dropdown-item">

                                <router-link to="/qed/user/users">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedusermanagementusers')) === true }">Users</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/qed/user/roles">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedusermanagementroles')) === true }">Roles</p>
                                </router-link>
                            </div>
                            <div class="dropdown-item">
                                <router-link to="/qed/user/logs">
                                    <p class="dropdown-item__link" :class="{ activeLink: ($options.filters.nameInRoute($route.name, 'qedusermanagementlogs')) === true }">Logs</p>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </a>

                <router-link class="button nav-links__link dropdown is-hoverable"
                           to="/qed/category/types"
                           v-if="userData.user_type === 'qed'"
                           :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'system')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/system-management-icon.png" alt="logo">
                            Category Management
                        </span>
                        <span class="right">
                        </span>
                    </span>
                </router-link>
                
                <!-- <a class="button nav-links__link dropdown is-hoverable" v-if="userData.user_type !== 'supplier'" :class="{ activeNav: ($options.filters.nameInRoute($route.name, 'system')) === true }">
                    <span class="dropdown-trigger">
                        <span class="left">
                            <img class="nav-links__link--image" src="@/assets/icons/system-management-icon.png" alt="logo">
                            System Management
                        </span>
                        <span class="right">
                            <font-awesome-icon class="nav-links__link--icon" icon="chevron-right" />
                        </span>
                    </span>
                </a> -->

                <a class="button nav-links__link" v-if="userData.user_type == 'supplier'">
                    <span class="left">
                        <img class="nav-links__link--image" src="@/assets/icons/videos-icon.png" alt="logo">
                        Tutorial Videos
                    </span>
                    <span class="right">
                    </span>
                </a>



            </div>
            <div class="column is-centered is-12">
                <div class="event">
                    <p class="event__title">Tendersure Event</p>
                    <p class="event__country">
                        <font-awesome-icon class="event__country--icon" icon="globe" />
                        <span class="event__country--name">World</span>
                    </p>
                    <p class="event__detail">Venue - 8.119.575</p>
                    <p class="event__detail">Time - 4.231.974</p>
                    <p class="event__detail">Invited - 439.217</p>

                    <div class="control">
                        <a class="button event__button">
                            <span>Share</span>
                            <font-awesome-icon class="event__button--icon" icon="arrow-circle-up" />
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: "SideNav",
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError', 'authPrivileges']),
        ...mapGetters('User',['userData',]),
    },
}
</script>


<style lang="scss" scoped>
.side-nav  {
    width: 100%;
    padding: $line-height $line-height/2;
}

.brand {
    width: 100%;
    @include grid_row;
    position: sticky;
    top: 0;
    z-index: 100;
    background-color: $color-white-main;

    &__logo {
        // height: $line-height*2.5;
        width: 100%;

        @media screen and (min-width: 1600px) {
            height: $line-height*2.5;
        }
    }
}

.nav-links {
    padding: 0;
    padding-left: $line-height/2;

    a {
        color: $color-black-main;
    }

    &__link {
        width: 100%;
        border-radius: $line-height/3;
        border: none;
        font-size: $font-size-small;
        padding: $line-height/2 $line-height/2;
        padding-right: 0;
        @include grid_row;
        margin: $line-height/6 0;
        background-color: transparent;

        @media screen and (min-width: 1600px) {
            font-size: $font-size-normal;
            padding: $line-height/1.25 $line-height/2;
            padding-right: 0;
        }

        &:hover {
            color: $color-blue-main;
        }

        &--icon {
            margin-right: $line-height/2;
            font-size: $font-size-text;
            min-width: $font-size-title;

            @media screen and (min-width: 1600px) {
                margin-right: $line-height/2;
                font-size: $font-size-normal;
                min-width: $font-size-major;
            }
        }

        &--image {
            margin-right: $line-height/4;
            font-size: $font-size-text;
            max-width: $line-height*0.9;
        }

        .left {
            @include grid_row;
            justify-content: left;
            align-items: center;

        }

        .right {
            &__active {
                margin-right: $line-height/3;
                font-weight: 600;
                display: none;
            }
        }
    }

    // .router-link-exact-active, .router-link-active {
    //     .nav-links__link {
    //         background-color: $color-blue-main;
    //         color: $color-green-light;
    //     }
    // }

    .dropdown-menu {
        width: 100%;
    }

    .dropdown-content {
        width: 100%;
        text-align: left;
        padding: 0 $line-height/2;
    }

    .dropdown-item {
        padding: 0 $line-height/4;

        &__link {
            color: $color-black-main;
            padding: $line-height/4 $line-height/4;
            font-size: $font-size-text;
            // border-radius: $line-height/4;

            @media screen and (min-width: 1600px) {
                font-size: $font-size-normal;
            }

            &:hover {
                color: $color-blue-main;
            }
        }

        .level2 {
            margin-left: $line-height;
            border-left: 1px solid $color-gray-medium;
            padding-left: $line-height/2;
        }

        .activeLink {
            color: green; //$color-green-main;
            // color: $color-green-light;
            // background-color: $color-blue-main;
        }
    }

    .dropdown-trigger {
        @include grid_row;
        align-items: center;
        width: 100%;
    }

    .activeNav {
        background-color: $color-baby-blue;
        color: green;

        .left {
            color: green;
            @include grid_row;
            justify-content: left;

        }
    }
}

.event {
    margin: 0 $line-height/2;
    margin-top: -$line-height/2;
    padding: $line-height/2;
    min-height: 20vh;
    border-radius: 15px;
    background: rgba(22, 170, 81, 0.04);

    @media screen and (min-width: 1600px) {
       padding: $line-height/1.5;
       margin-top: 0;
    }

    &__title {
        color: #121F3E;
        font-weight: 500;
        font-size: $font-size-text;

        @media screen and (min-width: 1600px) {
           font-size: $font-size-normal;
        }
    }

    &__country {
        font-size: $font-size-tiny;
        color: #1882FF;
        margin: $line-height/6 0;

        @media screen and (min-width: 1600px) {
            margin: $line-height/3 0;
        }

        &--icon {
            margin-right: $line-height/4;
        }
    }

    &__detail {
        font-size: $font-size-small;

        @media screen and (min-width: 1600px) {
            font-size: $font-size-text;
        }
    }

    &__button {
        width: 100%;
        margin: $line-height/3 0;
        color: $color-white-main;
        background-color: $color-green-main;
        font-weight: 600;
        padding: $line-height/3 $line-height/2;
        border-radius: $line-height/2;
        @include grid_row;
        justify-content: space-between;

        @media screen and (min-width: 1600px) {
            padding: $line-height/3 $line-height;
        }
    }
}
svg:not(:root).svg-inline--fa {
    overflow: visible;
    color: green;
}
</style>
