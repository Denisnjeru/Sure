<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Meeting Minutes
            </span>
            <div class="page__head--links">
                <router-link :to="'/qed/project_management/create_meetings'">
                    <a class="page__head--link button button-link">
                        Upload Meeting Minutes
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       List of Meeting Minutes
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="meetingMinutes" :options="options" class="hasRowNo">
                    <p class="row-no" v-if="meetingMinutes.length !== 0" slot="#" slot-scope="props">
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

                    <p slot="date" slot-scope="{row}">
                        {{row.date | formatDate}}
                    </p>


                    <span class="actions" slot="minutes" slot-scope="{row}">
                        <a :href="row.meeting_minutes">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="eye" />
                                View Minutes
                            </span>
                        </a>
                    </span>

                                        
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/qed/project_management/meetings/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete" @click="confirmDeleteMinutes(row)">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="meetingMinutes.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getMeetings()">
                </pagination>
            </div>
        </div>        
    </div>
</template>

<script>
import project_management from '@/services/qed/project_management'

export default {
    name: 'ProjectManagementMeetings',
    data() {
        return {
            columns: ['#', 'buyer', 'job', 'contact_person', 'date', 'minutes', 'actions'],
            options: {
                sortable: ['buyer', 'job'],
                editableColumns:[],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 1,
            dataPerPage: 20,
            meetingMinutes: [
                
            ]
        }
    },
    computed: {
        
    },
    mounted() {
        this.getMeetings()
    },
    methods: {
        async getMeetings() {
            try {
                const response = await project_management.meetings(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.meetingMinutes = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },
        confirmDeleteMinutes: function(minutes) {
            this.$swal({
                text: 'This meeting minutes will be permanently deleted',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Proceed',
                confirmButtonColor: 'red',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.deleteMinutes(minutes)    
                }
            });
        },
        async deleteMinutes(minutes) {           
            try {
                await project_management.deleteMeeting(minutes.id)                
            } catch (err) {
                window.toast.fire({
                    icon: 'success',
                    title: 'Meeting minutes deleted successfully'
                })
                this.getMeetings()
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
