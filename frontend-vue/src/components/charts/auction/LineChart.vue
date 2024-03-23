<template>
  <div>
    <apexchart width="100%" :height="chartHeight" type="line" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
    props: ['colors', 'dates', 'values', 'chartHeight', 'labels'],
  name: 'LineChart',
  data: function() {
    return {
      chartOptions: {
        chart: {
            height: 350,
            type: 'line',
            dropShadow: {
                enabled: true,
                color: '#000',
                top: 18,
                left: 7,
                blur: 10,
                opacity: 0.2
            },
            toolbar: {
                show: false
            }
        },
        xaxis: {
            type: 'datetime',
            categories: this.dates,
            labels: {
                style: {
                    colors: "#ffffff"
                }
            },
        },
        yaxis: {
            labels: {
                style: {
                    colors: "#ffffff"
                }
            },
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        grid: {
            borderColor: '#ffffff',
            strokeDashArray: 1,
            yaxis: {
                lines: {
                    show: true,
                    color: '#ffffff'
                }
            }
        },
        colors: ["#ffffff"],
        markers: {
            size: 3,
            colors: ['#ffffff']
        }
      },
      series: [
            {
              name: "Bidders",
              data: this.values
            },
      ]
    }
  },
  methods: {
     
  }
}
</script>
