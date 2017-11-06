/* global chartData */

import $ from 'jquery'
import Highcharts from 'highcharts'

$(document).ready(() => {
    Highcharts.chart('plays-chart', {
        chart: {
            zoomType: 'x',
        },
        title: {
            text: 'Plays over time',
        },
        subtitle: {
            text: document.ontouchstart === undefined
                ? 'Click and drag in the plot area to zoom in'
                : 'Pinch the chart to zoom in',
        },
        xAxis: {
            type: 'datetime',
        },
        yAxis: {
            title: {
                text: 'Play count',
            },
        },
        legend: {
            enabled: false,
        },
        series: [{
            type: 'column',
            name: 'Played',
            data: chartData,
        }],
    })
})
