 const RadarData = {
  labels: [
    'Прозрачность',
    'Здоровье',
    'Эффективность',
    'Ликвидность',
    'Рост',
  ],
  datasets: [{
    label: title,
    data: radar_data,
    fill: true,
    backgroundColor: radar_color2,
    borderColor: radar_color1,
    pointBackgroundColor: radar_color1,
    pointBorderColor: radar_color1,
    pointHoverBackgroundColor: radar_color1,
    pointHoverBorderColor: radar_color1,
    pointRadius: 5,
    pointHoverRadius: 7,
  }, ]
};

const RadarConfig = {
  type: 'radar',
  data: RadarData,
  options: {
    plugins: {
      legend: {
        display: false
      }
    },
    elements: {
      line: {
        borderWidth: 5,
        tension: 0.3,
      }
    },
    scale: {
        r: {

            beginAtZero: true,
            max: 100,
            min: 0,
            ticks: {
              stepSize: 20
            }
        },
        x: {
          autoSkip: false,
          maxRotation: 90,
          minRotation: 90
        }
    }
  },
};

const RadarChart = new Chart(
    document.getElementById('RadarChart'),
    RadarConfig,
);





const NewRevenueData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Выручка',
        fill: true,
        borderColor: 'rgb(19, 99, 223)',
        backgroundColor: 'rgba(19, 99, 223, 0.1)',
        pointBackgroundColor: 'rgb(19, 99, 223)',
        lineTension: 0.25,
        data: revenue_data,
    },
    {
        label: 'Чистая прибыль',
        fill: true,
        borderColor: 'rgb(60, 207, 78)',
        backgroundColor: 'rgba(60, 207, 78, 0.1)',
        pointBackgroundColor: 'rgb(60, 207, 78)',
        lineTension: 0.25,
        data: net_profit_data,
    },
    {
        label: 'Операционная прибыль',
        fill: true,
        hidden: true,
        borderColor: 'rgb(255, 68, 68)',
        backgroundColor: 'rgba(255, 68, 68, 0.1)',
        pointBackgroundColor: 'rgb(255, 68, 68)',
        lineTension: 0.25,
        data: operation_profit_data,
    },
    {
        label: 'EBITDA',
        fill: true,
        hidden: true,
        borderColor: 'rgb(245, 131, 2)',
        backgroundColor: 'rgba(245, 131, 2, 0.1)',
        pointBackgroundColor: 'rgb(245, 131, 2)',
        lineTension: 0.25,
        data: ebitda_data,
    },

    {
        label: 'OCF',
        fill: true,
        hidden: true,
        borderColor: 'rgb(229, 33, 101)',
        backgroundColor: 'rgba(229, 33, 101, 0.1)',
        pointBackgroundColor: 'rgb(229, 33, 101)',
        lineTension: 0.25,
        data: ocf_data,
    },

    {
        label: 'FCF',
        fill: true,
        hidden: true,
        borderColor: 'rgb(144, 33, 229)',
        backgroundColor: 'rgba(144, 33, 229, 0.1)',
        pointBackgroundColor: 'rgb(144, 33, 229)',
        lineTension: 0.25,
        data: fcf_data,
    },

    ],
};

var NewRevenueChartOptions = {
    legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        },
        bezierCurve: true,
    },
    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: revenue_y_label,
             }
        }
    },


    responsive: true,

};

const NewRevenueСonfig = {
    type: 'line',
    data: NewRevenueData,
    options: NewRevenueChartOptions,
};

const NewRevenueChart = new Chart(
    document.getElementById('NewRevenueChart'),
    NewRevenueСonfig,
);





const GrowthData = {
    labels: ['CAGR-3 Выручка', 'CAGR-3 EBITDA', 'CAGR-3 Прибыль'],
    datasets: [
    {
        label: 'Эмитент',
        data: growth_data[0],
        backgroundColor: 'rgba(35, 148, 223, 0.5)',
        borderColor: 'rgb(35, 148, 223)',
        borderWidth: 2,
        barPercentage: 0.95,
        categoryPercentage: 0.9,
        borderRadius: 5,
        borderSkipped: false,
    },
    {
        label: 'Медианное значение по отрасли',
        data: growth_data[1],
        backgroundColor: 'rgba(113, 231, 214, 0.5)',
        borderColor: 'rgb(113, 231, 214)',
        borderWidth: 2,
        barPercentage: 0.95,
        categoryPercentage: 0.9,
        borderRadius: 5,
        borderSkipped: false,
    },


    ],

};

const GrowthСonfig = {
    type: 'bar',
    data: GrowthData,
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: '%',
                 }
            },
        },

        responsive: true,

    },
};

const GrowthChart = new Chart(
    document.getElementById('GrowthChart'),
    GrowthСonfig,
);

let width, height;

let gradient = Array.apply(null, Array(5)).map(function () {});


function getAreaGradient(ctx, chartArea, gr_id, colorStop) {
  const chartWidth = chartArea.right - chartArea.left;
  const chartHeight = chartArea.bottom - chartArea.top;
  if (!gradient[gr_id] || width !== chartWidth || height !== chartHeight) {

    width = chartWidth;
    height = chartHeight;
    gradient[gr_id] = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    for (let i = 0; i < colorStop.length; i++) {
      gradient[gr_id].addColorStop(colorStop[i][0], colorStop[i][1]);
    }

  }

  return gradient[gr_id];
}


const MarginData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'маржинальность по чистой прибыли',
        fill: true,

        backgroundColor: 'rgba(86, 190, 70, 0.1)',
        borderColor: 'rgb(86, 190, 70)',
        pointBackgroundColor: 'rgb(86, 190, 70)',
        borderWidth: 3,

        lineTension: 0.25,
        data: margin_values[0],
    },
    {
        label: 'среднее значение в отрасли',
        fill: true,
        borderColor: 'rgb(125, 125, 122)',
        backgroundColor: 'rgba(125, 125, 122, 0.1)',
        pointBackgroundColor: 'rgb(125, 125, 122)',
        lineTension: 0.25,
        borderWidth: 4,
        borderDash: [10,5],
        data: median_values[0],

    },


    ],
};

var MarginChartOptions = {
    plugins: {
        legend: {
            display: true,
            position: 'top',

            labels: {
              padding: 10,
            },

            bezierCurve: false,
        },
    },

    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: '%',
             }
        }
    },

    responsive: true,
};

const MarginСonfig = {
    type: 'line',
    data: MarginData,
    options: MarginChartOptions,
};

const MarginChart = new Chart(
    document.getElementById('MarginChart'),
    MarginСonfig,
);



const TurnoverData = {
    labels: turnover_labels,
    datasets: [
    {
        label: 'Оборачиваемость дебиторской задолженности',
        fill: true,

        backgroundColor: 'rgba(86, 190, 70, 0.1)',
        borderColor: 'rgb(86, 190, 70)',
        pointBackgroundColor: 'rgb(86, 190, 70)',
        borderWidth: 3,

        lineTension: 0.25,
        data: margin_values[3],
    },
    {
        label: 'среднее значение в отрасли',
        fill: true,
        borderColor: 'rgb(125, 125, 122)',
        backgroundColor: 'rgba(125, 125, 122, 0.1)',
        pointBackgroundColor: 'rgb(125, 125, 122)',
        lineTension: 0.25,
        borderWidth: 4,
        borderDash: [10,5],
        data: median_values[3],

    },


    ],
};

var TurnoverOptions = {
    plugins: {
        legend: {
            display: true,
            position: 'top',

            labels: {
              padding: 10,
            },

            bezierCurve: false,
        },
    },

    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: 'день',
             }
        }
    },

    responsive: true,
};

const TurnoverСonfig = {
    type: 'line',
    data: TurnoverData,
    options: TurnoverOptions,
};

const TurnoverChart = new Chart(
    document.getElementById('TurnoverChart'),
    TurnoverСonfig,
);



const ScoreData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Модель Альтмана',
        fill: true,

        backgroundColor: 'rgba(86, 190, 70, 0.1)',
        borderColor: 'rgb(86, 190, 70)',
        pointBackgroundColor: 'rgb(86, 190, 70)',
        borderWidth: 3,

        lineTension: 0.25,
        data: margin_values[6],
    },
    {
        label: 'нормальное значение',
        fill: true,
        borderColor: 'rgb(125, 125, 122)',
        backgroundColor: 'rgba(125, 125, 122, 0.1)',
        pointBackgroundColor: 'rgb(125, 125, 122)',
        lineTension: 0.25,
        borderWidth: 4,
        borderDash: [10,5],
        data: median_values[6],

    },
    ],
};

var ScoreOptions = {
    plugins: {
        legend: {
            display: true,
            position: 'top',

            labels: {
              padding: 10,
            },

            bezierCurve: false,
        },
    },

    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: false,
                text: '',
             }
        }
    },

    responsive: true,
};

const ScoreConfig = {
    type: 'line',
    data: ScoreData,
    options: ScoreOptions,
};

const ScoreChart = new Chart(
    document.getElementById('ScoreChart'),
    ScoreConfig,
);



var ProfitabilityOptions = {
    legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        },
        bezierCurve: true,
    },
    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: '%',
             }
        }
    },

    responsive: true,
};

const ProfitabilityData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Рентабельность активов',
        fill: true,
        borderColor: 'rgb(72, 61, 139)',
        backgroundColor: 'rgba(72, 61, 139, 0.1)',
        pointBackgroundColor: 'rgb(72, 61, 139)',
        lineTension: 0.25,
        data: roa_data,
    },
    {
        label: 'Рентабельность капитала',
        fill: true,
        borderColor: 'rgb(182, 69, 130)',
        backgroundColor: 'rgba(182, 69, 130, 0.1)',
        pointBackgroundColor: 'rgb(182, 69, 130)',
        lineTension: 0.25,
        data: roe_data,
    },

    ],
};

const ProfitabilityСonfig = {
    type: 'line',
    data: ProfitabilityData,
    options: ProfitabilityOptions,
};

const ProfitabilityChart = new Chart(
    document.getElementById('ProfitabilityChart'),
    ProfitabilityСonfig,
);



const AssetsLiabilitiesData = {
    labels: ['Краткосрочные', 'Долгосрочные'],
    datasets: [
    {
        label: 'Активы',
        data: assets_data,
        backgroundColor: '#2394DF',
        barPercentage: 1,
        categoryPercentage: 0.75,
    },
    {
        label: 'Обязательства',
        data: liabilities_data,
        backgroundColor: '#71E7D6',
        barPercentage: 1,
        categoryPercentage: 0.75,
    },
    ],
};

const AssetsLiabilitiesСonfig = {
    type: 'bar',
    data: AssetsLiabilitiesData,
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: revenue_y_label,
                 }
            },
        },

        responsive: true,

    },
};

const AssetsLiabilitiesChart = new Chart(
    document.getElementById('AssetsLiabilitiesChart'),
    AssetsLiabilitiesСonfig,
);



const DebtEbitdaData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Чистый долг',
        fill: true,
        borderColor: 'rgb(255, 68, 68)',
        backgroundColor: 'rgba(255, 68, 68, 0.1)',
        pointBackgroundColor: 'rgb(255, 68, 68)',
        lineTension: 0.25,
        data: net_debt_data,
    },
    {
        label: 'EBITDA',
        fill: true,
        borderColor: 'rgb(60, 207, 78)',
        backgroundColor: 'rgba(60, 207, 78, 0.1)',
        pointBackgroundColor: 'rgb(60, 207, 78)',
        lineTension: 0.25,
        data: ebitda_data,
    },
    {
        label: 'Капитал и резервы',
        fill: true,
        hidden: true,
        borderColor: 'rgb(19, 99, 223)',
        backgroundColor: 'rgba(19, 99, 223, 0.1)',
        pointBackgroundColor: 'rgb(19, 99, 223)',
        lineTension: 0.25,
        data: equity_data,
    },

    {
        label: 'Активы',
        fill: true,
        hidden: true,
        borderColor: 'rgb(245,131,2)',
        backgroundColor: 'rgba(245,131,2, 0.1)',
        pointBackgroundColor: 'rgb(245,131,2)',
        lineTension: 0.25,
        data: assets2_data,
    },

    ],
};

var DebtEbitdaChartOptions = {
    legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        },
        bezierCurve: true,
    },
    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: revenue_y_label,
             }
        }
    },

    responsive: true,
};

const DebtEbitdaСonfig = {
    type: 'line',
    data: DebtEbitdaData,
    options: DebtEbitdaChartOptions,
};

const DebtEbitdaChart = new Chart(
    document.getElementById('DebtEbitdaChart'),
    DebtEbitdaСonfig,
);



const LiquidityData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Коэффициент текущей ликвидности',
        fill: true,

        backgroundColor: 'rgba(86, 190, 70, 0.1)',
        borderColor: 'rgb(86, 190, 70)',
        pointBackgroundColor: 'rgb(86, 190, 70)',
        borderWidth: 3,

        lineTension: 0.25,
        data: margin_values[10],
    },
    {
        label: 'Среднее значение в отрасли',
        fill: true,
        borderColor: 'rgb(125, 125, 122)',
        backgroundColor: 'rgba(125, 125, 122, 0.1)',
        pointBackgroundColor: 'rgb(125, 125, 122)',
        lineTension: 0.25,
        borderWidth: 4,
        borderDash: [10,5],
        data: median_values[10],

    },
    ],
};

var LiquidityOptions = {
    plugins: {
        legend: {
            display: true,
            position: 'top',

            labels: {
              padding: 10,
            },

            bezierCurve: false,
        },
    },

    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: false,
                text: '',
             }
        }
    },

    responsive: true,
};

const LiquidityConfig = {
    type: 'line',
    data: LiquidityData,
    options: LiquidityOptions,
};

const LiquidityChart = new Chart(
    document.getElementById('LiquidityChart'),
    LiquidityConfig,
);


const TransparencyData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'Финансовые вложения',
        fill: true,
        borderColor: 'rgb(255, 68, 68)',
        backgroundColor: 'rgba(255, 68, 68, 0.1)',
        pointBackgroundColor: 'rgb(255, 68, 68)',
        lineTension: 0.25,
        data: margin_values[14],
    },
    {
        label: 'Денежные средства',
        fill: true,
        borderColor: 'rgb(60, 207, 78)',
        backgroundColor: 'rgba(60, 207, 78, 0.1)',
        pointBackgroundColor: 'rgb(60, 207, 78)',
        lineTension: 0.25,
        data: margin_values[15],
    },

    ],
};

var TransparencyOptions = {
    legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        },
        bezierCurve: true,
    },
    scales: {
        y: {
             beginAtZero: true,
             title: {
                display: true,
                text: revenue_y_label,
             }
        }
    },

    responsive: true,
};

const TransparencyСonfig = {
    type: 'line',
    data: TransparencyData,
    options: TransparencyOptions,
};

const TransparencyChart = new Chart(
    document.getElementById('TransparencyChart'),
    TransparencyСonfig,
);


const $element1 = document.getElementsByClassName('bond-about');
const $button1 = document.getElementsByClassName('li-1');

$button1[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element1[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element2 = document.getElementsByClassName('emitter-about');
const $button2 = document.getElementsByClassName('li-2');

$button2[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element2[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element3 = document.getElementsByClassName('payments-list');
const $button3 = document.getElementsByClassName('li-3');

$button3[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element3[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element4 = document.getElementsByClassName('revenue-income');
const $button4 = document.getElementsByClassName('li-4');

$button4[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element4[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element5 = document.getElementsByClassName('margin-data');
const $button5 = document.getElementsByClassName('li-5');

$button5[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element5[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element6 = document.getElementsByClassName('finance-health');
const $button6 = document.getElementsByClassName('li-6');

$button6[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element6[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});


const $element7 = document.getElementsByClassName('liquidity');
const $button7 = document.getElementsByClassName('li-7');

$button7[0].addEventListener('click', e => {
  // Прокрутим страницу к форме
  $element7[0].scrollIntoView({
    block: 'nearest', // к ближайшей границе экрана
    behavior: 'smooth', // и плавно
  });
});

var win_wigth = window.screen.width;

if (win_wigth < 900) {
    const collection = document.getElementsByClassName("pc-only");

    while(collection.length) {
        collection[0].remove();
    }
}

$("#net-profit-margin").on("click", function() {
    MarginChart.data.datasets[0].label = 'Маржинальность по чистой прибыли';
    MarginChart.data.datasets[0].data = margin_values[0];
    MarginChart.data.datasets[1].data = median_values[0];
    MarginChart.data.datasets[0].backgroundColor = 'rgba(86, 190, 70, 0.1)'
    MarginChart.data.datasets[0].borderColor = 'rgb(86, 190, 70)'
    MarginChart.data.datasets[0].pointBackgroundColor = 'rgb(86, 190, 70)'

    MarginChart.update();
});

$("#ebitda-margin").on("click", function() {
    MarginChart.data.datasets[0].label = 'Маржинальность по EBITDA';

    MarginChart.data.datasets[0].data = margin_values[1];
    MarginChart.data.datasets[1].data = median_values[1];

    MarginChart.data.datasets[0].backgroundColor = 'rgba(245, 131, 2, 0.1)'
    MarginChart.data.datasets[0].borderColor = 'rgb(245, 131, 2)'
    MarginChart.data.datasets[0].pointBackgroundColor = 'rgb(245, 131, 2)'
    MarginChart.update();
});

$("#ocf-margin").on("click", function() {
    MarginChart.data.datasets[0].label = 'Маржинальность по OCF';

    MarginChart.data.datasets[0].data = margin_values[2];
    MarginChart.data.datasets[1].data = median_values[2];

    MarginChart.data.datasets[0].backgroundColor = 'rgba(229, 33, 101, 0.1)'
    MarginChart.data.datasets[0].borderColor = 'rgb(8229, 33, 101)'
    MarginChart.data.datasets[0].pointBackgroundColor = 'rgb(229, 33, 101)'
    MarginChart.update();
});



$("#turnover-accounts-receivable").on("click", function() {
    TurnoverChart.data.datasets[0].label = 'Оборачиваемость дебиторской задолженности';
    TurnoverChart.data.datasets[0].data = margin_values[3];
    TurnoverChart.data.datasets[1].data = median_values[3];
    TurnoverChart.data.datasets[0].backgroundColor = 'rgba(86, 190, 70, 0.1)'
    TurnoverChart.data.datasets[0].borderColor = 'rgb(86, 190, 70)'
    TurnoverChart.data.datasets[0].pointBackgroundColor = 'rgb(86, 190, 70)'

    TurnoverChart.update();
});

$("#turnover-accounts-payable").on("click", function() {
    TurnoverChart.data.datasets[0].label = 'Оборачиваемость запасов';

    TurnoverChart.data.datasets[0].data = margin_values[4];
    TurnoverChart.data.datasets[1].data = median_values[4];

    TurnoverChart.data.datasets[0].backgroundColor = 'rgba(245, 131, 2, 0.1)'
    TurnoverChart.data.datasets[0].borderColor = 'rgb(245, 131, 2)'
    TurnoverChart.data.datasets[0].pointBackgroundColor = 'rgb(245, 131, 2)'
    TurnoverChart.update();
});

$("#turnover-current-assets").on("click", function() {
    TurnoverChart.data.datasets[0].label = 'Оборачиваемость дебиторской оборотных активов';

    TurnoverChart.data.datasets[0].data = margin_values[5];
    TurnoverChart.data.datasets[1].data = median_values[5];

    TurnoverChart.data.datasets[0].backgroundColor = 'rgba(229, 33, 101, 0.1)'
    TurnoverChart.data.datasets[0].borderColor = 'rgb(8229, 33, 101)'
    TurnoverChart.data.datasets[0].pointBackgroundColor = 'rgb(229, 33, 101)'
    TurnoverChart.update();
});



$("#altman-score").on("click", function() {
    ScoreChart.data.datasets[0].label = 'Модель Альтмана';
    ScoreChart.data.datasets[0].data = margin_values[6];
    ScoreChart.data.datasets[1].data = median_values[6];
    ScoreChart.data.datasets[0].backgroundColor = 'rgba(86, 190, 70, 0.1)'
    ScoreChart.data.datasets[0].borderColor = 'rgb(86, 190, 70)'
    ScoreChart.data.datasets[0].pointBackgroundColor = 'rgb(86, 190, 70)'

    ScoreChart.update();
});

$("#springate-score").on("click", function() {
    ScoreChart.data.datasets[0].label = 'Модель Спрингейта';

    ScoreChart.data.datasets[0].data = margin_values[7];
    ScoreChart.data.datasets[1].data = median_values[7];

    ScoreChart.data.datasets[0].backgroundColor = 'rgba(245, 131, 2, 0.1)'
    ScoreChart.data.datasets[0].borderColor = 'rgb(245, 131, 2)'
    ScoreChart.data.datasets[0].pointBackgroundColor = 'rgb(245, 131, 2)'
    ScoreChart.update();
});

$("#lis-score").on("click", function() {
    ScoreChart.data.datasets[0].label = 'Модель Лисса';

    ScoreChart.data.datasets[0].data = margin_values[8];
    ScoreChart.data.datasets[1].data = median_values[8];

    ScoreChart.data.datasets[0].backgroundColor = 'rgba(229, 33, 101, 0.1)'
    ScoreChart.data.datasets[0].borderColor = 'rgb(8229, 33, 101)'
    ScoreChart.data.datasets[0].pointBackgroundColor = 'rgb(229, 33, 101)'
    ScoreChart.update();
});

$("#tuffler-score").on("click", function() {
    ScoreChart.data.datasets[0].label = 'Модель Таффлера';

    ScoreChart.data.datasets[0].data = margin_values[9];
    ScoreChart.data.datasets[1].data = median_values[9];

    ScoreChart.data.datasets[0].backgroundColor = 'rgba(144, 33, 229, 0.1)'
    ScoreChart.data.datasets[0].borderColor = 'rgb(144, 33, 229)'
    ScoreChart.data.datasets[0].pointBackgroundColor = 'rgb(144, 33, 229)'
    ScoreChart.update();
});


$("#current-liquidity").on("click", function() {
    LiquidityChart.data.datasets[0].label = 'Коэффициент текущей ликвидности';
    LiquidityChart.data.datasets[0].data = margin_values[10];
    LiquidityChart.data.datasets[1].data = median_values[10];
    LiquidityChart.data.datasets[0].backgroundColor = 'rgba(86, 190, 70, 0.1)'
    LiquidityChart.data.datasets[0].borderColor = 'rgb(86, 190, 70)'
    LiquidityChart.data.datasets[0].pointBackgroundColor = 'rgb(86, 190, 70)'

    LiquidityChart.update();
});

$("#fast-liquidity").on("click", function() {
    LiquidityChart.data.datasets[0].label = 'Коэффициент быстрой ликвидности';

    LiquidityChart.data.datasets[0].data = margin_values[11];
    LiquidityChart.data.datasets[1].data = median_values[11];

    LiquidityChart.data.datasets[0].backgroundColor = 'rgba(245, 131, 2, 0.1)'
    LiquidityChart.data.datasets[0].borderColor = 'rgb(245, 131, 2)'
    LiquidityChart.data.datasets[0].pointBackgroundColor = 'rgb(245, 131, 2)'
    LiquidityChart.update();
});

$("#cash-liquidity").on("click", function() {
    LiquidityChart.data.datasets[0].label = 'Коэффициент абсолютной ликвидности';

    LiquidityChart.data.datasets[0].data = margin_values[12];
    LiquidityChart.data.datasets[1].data = median_values[12];

    LiquidityChart.data.datasets[0].backgroundColor = 'rgba(229, 33, 101, 0.1)'
    LiquidityChart.data.datasets[0].borderColor = 'rgb(8229, 33, 101)'
    LiquidityChart.data.datasets[0].pointBackgroundColor = 'rgb(229, 33, 101)'
    LiquidityChart.update();
});

$("#operating-capital").on("click", function() {
    LiquidityChart.data.datasets[0].label = 'Доля операционного оборотного капитала в активах';

    LiquidityChart.data.datasets[0].data = margin_values[13];
    LiquidityChart.data.datasets[1].data = median_values[13];

    LiquidityChart.data.datasets[0].backgroundColor = 'rgba(144, 33, 229, 0.1)'
    LiquidityChart.data.datasets[0].borderColor = 'rgb(144, 33, 229)'
    LiquidityChart.data.datasets[0].pointBackgroundColor = 'rgb(144, 33, 229)'
    LiquidityChart.update();
});