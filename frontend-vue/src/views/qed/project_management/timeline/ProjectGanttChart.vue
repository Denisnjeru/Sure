<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Project Gantt Charts
            </span>
            <div class="page__head--links">

            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       List of Project Gantt Charts
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="projectCharts" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="projectCharts.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    
                    <p slot="buyer" slot-scope="{row}">
                        {{row.company.company_name}}
                    </p>

                    <p slot="job" slot-scope="{row}">
                        {{row.job.title}}
                    </p>

                    <p slot="contact_person" slot-scope="{row}">
                        {{row.company.phone_number}}
                    </p>

                    <span class="actions" slot="gantt_chart" slot-scope="{row}">
                        <a :href="row.actual_gantt_chart">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="eye" />
                                Edit Gantt Chart
                            </span>
                        </a>
                    </span>
                                        
                    <span class="actions" slot="actions">
                        <span class="actions__delete" @click="confirmDeleteGantt(row)">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="projectCharts.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getProjectCharts()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import project_management from '@/services/qed/project_management'

export default {
    name: 'ProjectManagementGanttChartProject',
    data() {
        return {
            columns: ['#', 'buyer', 'job', 'contact_person', 'gantt_chart', 'actions'],
            options: {
                sortable: ['buyer', 'job'],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            projectCharts: []
        }
    },
    computed: {
        
    },
    mounted() {
        this.getProjectCharts()
    },
    methods: {
        async getProjectCharts() {
            try {
                const response = await project_management.timelines(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.projectCharts = response.data.results
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: 'Error retrieving gantt charts'
                })
            }
        },
        async search() {
            console.log('search');
        },
        confirmDeleteGantt: function(gantt) {
            this.$swal({
                text: 'This gantt chart will be permanently deleted',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.deleteGantt(gantt)    
                }
            });
        },
        async deleteGantt(gantt) {           
            try {
                await project_management.deleteTimeline(gantt.id)                
            } catch (err) {
                window.toast.fire({
                    icon: 'success',
                    title: 'Gantt chart deleted successfully'
                })
                this.getUsers()
            }
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}

</style>
