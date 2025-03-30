
const RevenueData = {
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

    ],
};

var RevenueChartOptions = {
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

const RevenueСonfig = {
    type: 'line',
    data: RevenueData,
    options: RevenueChartOptions,
};

const RevenueChart = new Chart(
    document.getElementById('RevenueChart'),
    RevenueСonfig,
);






const MarginData = {
    labels: revenue_x_labels,
    datasets: [
    {
        label: 'по чистой прибыли',
        fill: true,
        borderColor: 'rgb(0, 193, 43)',
        backgroundColor: 'rgba(0, 193, 43, 0.1)',
        pointBackgroundColor: 'rgb(0, 193, 43)',
        lineTension: 0.25,
        data: margin_income_data,
    },
    {
        label: 'по операционной прибыли',
        fill: true,
        borderColor: 'rgb(255, 124, 0)',
        backgroundColor: 'rgba(255, 124, 0, 0.1)',
        pointBackgroundColor: 'rgb(255, 124, 0)',
        lineTension: 0.25,
        data: margin_operation_data,
    },
    {
        label: 'по EBITDA',
        fill: true,
        hidden: true,
        borderColor: 'rgb(211, 0, 104)',
        backgroundColor: 'rgba(211, 0, 104, 0.1)',
        pointBackgroundColor: 'rgb(211, 0, 104)',
        lineTension: 0.25,
        data: margin_ebitda_data,
    },

    ],
};

var MarginChartOptions = {
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

const MarginСonfig = {
    type: 'line',
    data: MarginData,
    options: MarginChartOptions,
};

const MarginChart = new Chart(
    document.getElementById('MarginChart'),
    MarginСonfig,
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



const GrowthRevenueData = {
    labels: ['CAGR за 1 год', 'CAGR 3 год', 'CAGR 5 год'],
    datasets: [{
        label: '',
        data: cagr_revenue_data,
        backgroundColor: ['#2394DF', '#71E7D6', '#B74583'],
        barPercentage: 1,
        categoryPercentage: 1,
    }],
};

const GrowthRevenueСonfig = {
    type: 'bar',
    data: GrowthRevenueData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            },
        },

    },
};

const RevenueGrowthChart = new Chart(
    document.getElementById('RevenueGrowthChart'),
    GrowthRevenueСonfig,
);



const GrowthIncomeData = {
    labels: ['CAGR за 1 год', 'CAGR 3 год', 'CAGR 5 год'],
    datasets: [{
        label: '',
        data: cagr_income_data,
        backgroundColor: ['#2394DF', '#71E7D6', '#B74583'],
        barPercentage: 1,
        categoryPercentage: 1,
    }],
};

const GrowthIncomeСonfig = {
    type: 'bar',
    data: GrowthIncomeData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            },
        },

    },
};

const IncomeGrowthChart = new Chart(
    document.getElementById('IncomeGrowthChart'),
    GrowthIncomeСonfig,
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
    labels: ['Текущие обязательства', 'Текущая ликвидность', 'Быстрая ликвидность', 'Абсолютная ликвидность'],
    datasets: [{
        label: '',
        data: liquidity_data,
        backgroundColor: ['rgba(255, 31, 1, 0.2)', 'rgba(92, 179, 25, 0.2)', 'rgba(92, 179, 25, 0.2)', 'rgba(92, 179, 25, 0.2)'],
        borderColor: ['rgb(255, 31, 1)', 'rgb(92, 179, 25)', 'rgb(92, 179, 25)', 'rgb(92, 179, 25)'],
        barPercentage: 0.5,
        borderWidth: 3,
        categoryPercentage: 1,
    }],
};

const LiquidityСonfig = {
    type: 'bar',
    data: LiquidityData,
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

const LiquidityChart = new Chart(
    document.getElementById('LiquidityChart'),
    LiquidityСonfig,
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