var lightChart;
var tempChart;
var humidityChart;

function renderLDRChart(lightIntensity, labels){
    var ctx3 = document.getElementById("chart3").getContext('2d');
    lightChart = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Light Intensity',
                    data: lightIntensity,
                    borderColor: '#c56015',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
    });
}

function renderHumidityChart(humidity, labels){
    var ctx2 = document.getElementById("chart2").getContext('2d');

    
    humidityChart = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'humidity (%)',
                    data: humidity,
                    borderColor: '#3b6431',
                    borderWidth: 1,
                    fill: false
                },
            ]
        },
    });
}

function renderTempChart(temp, labels) {
    var ctx = document.getElementById("chart").getContext('2d');
    
    
    tempChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'temperature (Degree Celcius)',
                    data: temp,
                    borderColor: '#3c0e7b',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
    });
}


function getHistoricalTempAndHumidity() {
        var dht11Data = {}
        dht11Data.temperatures = []
        dht11Data.humidity = []
        dht11Data.datetime = []
        $.ajax({
                url: "/api/dht11-data",
                async: false,
                success: function(results){
                            for(var i = 0; i < results.length; i++){
                                dht11Data.temperatures.push(results[i].temperature)
                                dht11Data.humidity.push(results[i].humidity)
                                dht11Data.datetime.push(results[i].datetime)
                            }
                        },
                
                type: 'GET'
            });

        return dht11Data
    };


function getHistoricalLightIntensity(){
        var LDRData = {}
        LDRData.lightIntensity = []
        LDRData.datetime = []
        $.ajax({
                url: "/api/ldr-data",
                async: false,
                success: function(results){
                            for(var i = 0; i < results.length; i++){
                                LDRData.lightIntensity.push(results[i].light_intensity)
                                LDRData.datetime.push(results[i].datetime)
                            }
                        },
                
                type: 'GET'
            });

        return LDRData
};

function renderCharts(){
    var dht11Data = getHistoricalTempAndHumidity();
    var ldrdata = getHistoricalLightIntensity();


    renderLDRChart(ldrdata.lightIntensity, ldrdata.datetime);
    renderTempChart(dht11Data.temperatures, dht11Data.datetime);
    renderHumidityChart(dht11Data.humidity, dht11Data.datetime);
}


function updateCharts(){

    tempChart.destroy();
    lightChart.destroy();
    humidityChart.destroy();

    $("canvas#chart").remove();
    $("canvas#chart2").remove();
    $("canvas#chart3").remove();

    $("div#temp-chart").append('<canvas class="w-100" height="400" id="chart"></canvas>');
    $("div#humidity-chart").append('<canvas class="w-100" height="400" id="chart2"></canvas>');
    $("div#light-chart").append('<canvas class="w-100" height="400" id="chart3"></canvas>');

    renderCharts();
}


function getLEDStatus(){
    $.ajax({
        url: "/api/led-status",
        success: function(results){
                    console.log(results);
                    if (results['led_status'] == true){
                        $('#led_status').html('LED is on');
                    }
                    else{
                        $('#led_status').html('LED is off');
                    }
                },
        type: 'GET'
    });
};


$(document).ready(function() {
    getLEDStatus();
    renderCharts();
    setInterval(getCurrentLDRData, 1000 * 5);
    setInterval(getCurrentDHT11Data, 1000 * 5);
});

function getCurrentDHT11Data(){
    $.ajax({
        url: "/api/latest-dht11-reading",
        success: function(results){
                    $('#temperature').html(results.temperature + " &deg;C");
                    $('#humidity').html(results.humidity + " %");
                },
        
        type: 'GET'
    });
};

function getCurrentLDRData(){
    $.ajax({
        url: "/api/latest-ldr-reading",
        success: function(results){
                    $('#light').html(results.light_intensity);
                },
        type: 'GET'
    });
};


function callLedOnAPI(){
    $.ajax({
        url: "/api/led-on",
        success: function(results){
                    getLEDStatus();
                },
        type: 'GET'
    });
};

function callLedOffAPI(){
    $.ajax({
        url: "/api/led-off",
        success: function(results){
                    getLEDStatus();
                },
        type: 'GET'
    });
};
