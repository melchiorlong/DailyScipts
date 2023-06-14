import * as echarts from 'echarts';

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

myChart.showLoading();
$.get(
  '/Users/tianlong/PycharmProjects/GV_GitLab/personal_tianlong_server/DailyScipts/DailyTest/Echarts_JS/data.json',
  function (data) {
    myChart.hideLoading();
    myChart.setOption(
      (option = {
        tooltip: {
          trigger: 'item',
          triggerOn: 'mousemove'
        },
        series: [
          {
            type: 'tree',
            data: [data],
            top: '18%',
            bottom: '14%',
            layout: 'radial',
            symbol: 'emptyCircle',
            symbolSize: 7,
            initialTreeDepth: 3,
            animationDurationUpdate: 750,
            emphasis: {
              focus: 'descendant'
            }
          }
        ]
      })
    );
  }
);

option && myChart.setOption(option);
