<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Meeting Minutes
            </span>
            <div class="page__head--links">
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

                    <p slot="job_title" slot-scope="{row}">
                        {{row.job.title}}
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
            columns: ['#', 'job_title', 'date', 'minutes'],
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
