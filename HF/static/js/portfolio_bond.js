const CalendarData = {
  labels: calendar_data[0],
  datasets: [
  {
    label: 'Купонный доход в месяц',
    data: calendar_data[1][0],
    backgroundColor: calendar_data[1][2],
    borderColor: calendar_data[1][1],
    borderWidth: 1
  },
  {
    label: 'Прочие выплаты в месяц',
    data: calendar_data[2][0],
    backgroundColor: calendar_data[2][2],
    borderColor: calendar_data[2][1],
    borderWidth: 1,
    hidden: true,
  }
  ]
};

const CalendarConfig = {
  type: 'bar',
  data: CalendarData,
  options: {
    scales: {
      y: {
        beginAtZero: true,
        stacked: true,
      },
      x: {
        stacked: true,
      }
    }
  },
};

const CalendarChart = new Chart(
    document.getElementById('CalendarChart'),
    CalendarConfig,

);



const MaturityData = {
  labels: maturity_chart_data[0],
  datasets: [
  {
    label: 'График погашения',
    data: maturity_chart_data[1],

    hoverOffset: 4
  }
  ]
};

const MaturityConfig = {
  type: 'doughnut',
  data: MaturityData,
};

const MaturityChart = new Chart(
    document.getElementById('MaturityChart'),
    MaturityConfig,

);


const SectorData = {
  labels: sector_chart_data[0],
  datasets: [
  {
    label: 'Сектора',
    data: sector_chart_data[1],

    hoverOffset: 4
  }
  ]
};

const SectorConfig = {
  type: 'doughnut',
  data: SectorData,
};

const SectorChart = new Chart(
    document.getElementById('SectorChart'),
    SectorConfig,

);


const RatingData = {
  labels: rating_chart_data[0],
  datasets: [
  {
    label: 'Кредитные рейтинги',
    data: rating_chart_data[1],
//    backgroundColor: rating_chart_data[2],
    hoverOffset: 4
  }
  ]
};

const RatingConfig = {
  type: 'doughnut',
  data: RatingData,
};

const RatingChart = new Chart(
    document.getElementById('RatingChart'),
    RatingConfig,

);
