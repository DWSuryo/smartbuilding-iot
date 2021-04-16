// Data from: https://data.giss.nasa.gov/gistemp/
// Mean from: https://earthobservatory.nasa.gov/world-of-change/DecadalTemp

window.addEventListener('load', setup);

async function setup() {
    const ctx = document.getElementById('room1').getContext('2d');
    const dataTemps = await getData();
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
        labels: dataTemps.time,
        datasets: [
            {
            label: 'Temperature (°C)',
            data: dataTemps.temps,
            fill: false,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderWidth: 1
            },
            {
            label: 'Humidity (%)',
            data: dataTemps.hums,
            fill: false,
            borderColor: 'rgba(99, 132, 255, 1)',
            backgroundColor: 'rgba(99, 132, 255, 0.5)',
            borderWidth: 1
            },
            {
            label: 'energy (kWh)',
            data: dataTemps.kwhs,
            fill: false,
            borderColor: 'rgba(99, 255, 132, 1)',
            backgroundColor: 'rgba(99, 255, 132, 0.5)',
            borderWidth: 1
            }
        ]
        },
        options: {
            animation: {
                duration: 0 // general animation time
            },
        }
    });
    setTimeout (function() { setup(); }, 5000);
}

async function getData() {
    const response = await fetch('sensor_room1.csv');
    // const response = await fetch('https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv');
    //const response = await fetch('C:/Users/Dito Wicaksono/webdevproject/modul6/static/ZonAnn.Ts+dSST.csv');
    //const response = await fetch('ZonAnn.Ts+dSST.csv')
    const data = await response.text();
    const time = [];
    const temps = [];
    const hums = [];
    const kwhs = [];
    const rows = data.split('\n').slice(1);
    rows.forEach(row => {
        const cols = row.split(',');
        time.push(cols[1]);
        temps.push(14 + parseFloat(cols[2]));
        hums.push(14 + parseFloat(cols[3]));
        kwhs.push(14 + parseFloat(cols[4]));
    });
    return { time, temps, hums, kwhs };
}
