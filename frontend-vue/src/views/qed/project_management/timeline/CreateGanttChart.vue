<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                Create Gantt Chart
            </span>
            <div class="page__head--links">
            </div>
        </div>
        <form class="form" v-on:submit.prevent="createGanttChart()">
        <div class="page__content columns is-centered">
            <div class="column is-6 column-details">
                <!-- <div class="column-details__head">
                </div> -->
                <div class="column-details__content">     
                    <div class="field">
                        <label class="label">Buyer <span class="required">*</span></label>
                        <div class="control">
                            <v-select required v-model="selectedBuyer" :options="buyers" :reduce="buyer => buyer.id" label="company_name" placeholder="Select buyer"></v-select>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Job Title <span class="required">*</span></label>
                        <div class="control">
                            <v-select required v-model="selectedJob" :options="jobs" :reduce="job => job.id" label="title" placeholder="Select job"></v-select>
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Start Date <span class="required">*</span></label>
                        <div class="control">
                            <input required class="input" v-model="ganttChart.start_date" type="date">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Projected End Date <span class="required">*</span></label>
                        <div class="control">
                            <input required class="input" v-model="ganttChart.end_date" type="date">
                        </div>
                    </div> 
                </div>
            </div>
            <div class="column is-6 column-details">
                <!-- <div class="column-details__head">
                </div> -->
                <div class="column-details__content">                    
                    <div class="field file-upload">
                        <label class="label">Upload Approved Gantt Chart <span class="required">*</span></label>
                        <div class="control">
                            <input required type="file" id="approved_gantt_chart">
                        </div>
                    </div>  
                    <div class="field">
                        <span class="help">* Attach the sharable link to the actual gantt chart</span>
                        <label class="label">Project Gantt Chart <span class="required">*</span></label>
                        <div class="control">
                            <input required class="input" type="text" v-model="ganttChart.actual_gantt_chart">
                        </div>
                    </div> 
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
               <input type="submit" class="button button-submit" value="Create Gantt Chart">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import project_management from '@/services/qed/project_management'

export default {
    name: 'ProjectManagementGanttChartCreate',
    data() {
        return {
            ganttChart: {},
            buyers: [],
            selectedBuyer: null,
            jobs: [],
            selectedJob: null,
        }
    },
    watch: {
        selectedBuyer(newBuyer) {
            this.jobs = []
            this.getJobs(newBuyer)
        }
    },
    mounted() {
        this.getBuyers()
    },
    methods: {
        async search() {
            console.log('search');
        },
        async getBuyers(){
            try {
                const response = await project_management.buyers()
                this.buyers = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async getJobs(companyId){
            try {
                const response = await project_management.companyJobs(companyId)
                this.jobs = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async createGanttChart() {
            try {

                let form_data = new FormData()
                form_data.append("company", this.selectedBuyer)
                form_data.append("job", this.selectedJob)
                form_data.append("start_date", this.ganttChart.start_date)
                form_data.append("end_date", this.ganttChart.end_date)
                form_data.append("actual_gantt_chart", this.ganttChart.actual_gantt_chart)

                let approved_gantt_chart_file = document.getElementById("approved_gantt_chart").files[0];
                if (approved_gantt_chart_file !== undefined) {
                    form_data.append("approved_gantt_chart", approved_gantt_chart_file, approved_gantt_chart_file.name)
                }

                await project_management.createTimeline(form_data)
                window.toast.fire({
                    icon: 'success',
                    title: 'Gantt chart created successfully'
                })
                this.$router.push('/qed/project_management/approved_gantt_chart')
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: 'Error occurred while creating gantt chart'
                })
            }
        }

    }
}
</script>

<style lang="scss" scoped>
@include page;
@include form;

.page__content {
    padding: $line-height $line-height;
    margin-top: 0;

}

.page__head {
    padding-left: $line-height/2;

    &--title {
        margin-left: -10%;
    }
}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

.additions {
    margin-top: -$line-height*2.5;
}

.file-upload {
    margin-bottom: $line-height !important;
}

.column-details__content {
    margin-bottom: $line-height/3 !important;
}

// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

</style>
