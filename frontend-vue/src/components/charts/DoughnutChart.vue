<template>
  <div>
    <apexcharts :height="chartHeight" :options="chartOptions" :series="series"></apexcharts>
  </div>
</template>

<script>
  import VueApexCharts from 'vue-apexcharts'

  export default {
    props: ['colors', 'dates', 'values', 'chartHeight', 'labels'],
    name: 'apexLineChart',
    components: {
      apexcharts: VueApexCharts
    },
    data () {
        return {
            series: this.values,
            chartOptions: {
                chart: {
                    type: 'donut',
                },
                dataLabels: {
                    enabled: false,
                    formatter: function (val, opts) {
                        return opts.w.config.series[opts.seriesIndex]
                    },
                },                
                plotOptions: {
                    pie: {
                        startAngle: 0,
                        endAngle: 360,
                        expandOnClick: true,
                        offsetX: 0,
                        offsetY: 0,
                        customScale: 1,
                        dataLabels: {
                            offset: 0,
                            minAngleToShowLabel: 10
                        }, 
                        donut: {
                            hollow: {
                                size: '70%',
                            },
                            borderRadius: 5,
                            labels: {
                                show: true,
                                total: {
                                    showAlways: false,
                                    show: true,
                                    fontWeight: 500,
                                    fontSize: '14px',
                                    formatter: function (w) {
                                        return w.globals.seriesTotals.reduce((a, b) => {
                                        return a + b
                                        }, 0)
                                    }
                                },
                                value: {
                                    show: true,
                                    fontSize: '18px',
                                    fontFamily: 'Helvetica, Arial, sans-serif',
                                    fontWeight: 600,
                                    color: '#030229',
                                    formatter: function (val) {
                                        return val
                                    }
                                }
                            },
                            
                        }
                    }
                    
                },
                labels: this.labels,
                legend: {
                    position: 'right',
                    horizontalAlign: 'center',
                    verticalAlign: 'center',
                    // offsetX: 40
                },
                stroke: {
                    lineCap: 'round'
                },
                borderRadius: 5,
                colors: this.colors,
                responsive: [{
                    breakpoint: 1600,
                    options: {
                        chart: {
                            height: '160%'
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            },
        }
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    }
  }
</script>

<style lang="scss" scoped>
.apex-chart {
  width: 100%;
  background-color: red;
}
</style>
