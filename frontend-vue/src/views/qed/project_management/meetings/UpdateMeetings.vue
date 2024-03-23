<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                Update Meeting Minutes
            </span>
            <div class="page__head--links">
            </div>
        </div>
        <form class="form" v-on:submit.prevent="updateMeetingMinutes()">
        <div class="page__content columns is-centered">
            <div class="column is-6 column-details">
                <!-- <div class="column-details__head">
                </div> -->
                <div class="column-details__content">                    
                    <div class="field">
                        <label class="label">Buyer {{selectedBuyer}} <span class="required">*</span></label>
                        <div class="control">
                            <v-select required v-model="selectedBuyer" :options="buyers" :reduce="buyer => buyer.id" label="company_name" placeholder="Select buyer"></v-select>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Job Title {{selectedJob}} <span class="required">*</span></label>
                        <div class="control">
                            <v-select required v-model="selectedJob" :options="jobs" :reduce="job => job.id" label="title" placeholder="Select job"></v-select>
                        </div>
                    </div> 
                </div>
            </div>
            <div class="column is-6 column-details">
                <!-- <div class="column-details__head">
                </div> -->
                <div class="column-details__content">                    
                    <div class="field file-upload">
                        <label class="label">Meeting Minutes <span class="required">*</span></label>
                        <div class="control">
                            <input type="file" id="meeting_minutes">
                        </div>
                        <span class="help">Current: <a :href="meeting.meeting_minutes">View minutes</a></span>
                    </div>  
                    <div class="field">
                        <label class="label">Date <span class="required">*</span></label>
                        <div class="control">
                            <input required class="input" type="date" v-model="meeting.date">
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
               <input type="submit" class="button button-submit" value="Update">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import project_management from '@/services/qed/project_management'

export default {
    name: 'ProjectManagementMeetingsCreate',
    data() {
        return {
            meeting: {},
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
        this.getMeeting()
    },
    methods: {
        async search() {
            console.log('search');
        },
        async getMeeting(){
            try {
                const response = await project_management.meeting(this.$route.params.id)
                this.meeting = response.data
                this.selectedBuyer = this.meeting.company
                this.selectedJob = this.meeting.job
            } catch (err) {
                console.log(err)
            }
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
        async updateMeetingMinutes(){
            try {

                let form_data = new FormData()
                form_data.append("company", this.selectedBuyer)
                form_data.append("job", this.selectedJob)
                form_data.append("date", this.meeting.date)

                let meeting_minutes_file = document.getElementById("meeting_minutes").files[0];
                if (meeting_minutes_file !== undefined) {
                    form_data.append("meeting_minutes", meeting_minutes_file, meeting_minutes_file.name)
                }
                
                await project_management.updateMeeting(this.$route.params.id, form_data)
                window.toast.fire({
                    icon: 'success',
                    title: 'Meeting updated successfully'
                })
                this.$router.push('/qed/project_management/meetings')
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: 'Error occurred while updating meeting'
                })
            }
        },

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
        margin-left: -$line-height*6;
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
    margin-bottom: $line-height/8 !important;
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
