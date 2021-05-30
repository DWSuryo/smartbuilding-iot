function createchart(id, titlename, source){
	// Create chart instance
	var chart = am4core.create(id, am4charts.XYChart);

	//Padding
	chart.paddingRight = 20;
	chart.paddingLeft = 0;

	//Chart title
	var title = chart.titles.create();
	title.text = titlename;
	title.fontSize = 20;
	title.marginBottom = 10;
	title.tooltipText = "Stonks";

	// Set up data source
	// chart.dataSource.url = "static/sensor_date.csv";
	chart.dataSource.url = source;
	//chart.dataSource.url = "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv";
	chart.dataSource.parser = new am4core.CSVParser();
	chart.dataSource.parser.options.useColumnNames = true;
	chart.dateFormatter.inputDateFormat = "i";

	// Create x axes
	// var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
	var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
	categoryAxis.dataFields.category = "datetime";
	categoryAxis.tooltipDateFormat = "HH:mm:ss, d MMMM";
	//categoryAxis.dateFormats.setKey("day", "MMMM dt");
	//categoryAxis.dateFormats.setKey("second");
	categoryAxis.dateFormats.setKey("second", "ss");
	// categoryAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
	// categoryAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
	// categoryAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
	categoryAxis.skipEmptyPeriods = true; 
	//categoryAxis.periodChangeDateFormats.setKey("hour", "HH:mm:ss"); 

	// this makes the data to be grouped
	categoryAxis.groupData = true;
	categoryAxis.groupCount = 150;
	
	// Create y value axis
	var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
	valueAxis.paddingLeft = 0;
	valueAxis.paddingRight = 0;

	

	//create series function
	function createseries(value, legend) {
		//create series line
		var series = chart.series.push(new am4charts.LineSeries());
		series.dataFields.dateX = "tgl";
		series.dataFields.valueY = value;
		
		series.name = legend;
		series.strokeWidth = 3;
		//cursor tooltips
		series.tooltipText = "{name}: {dateX}: [b]{valueY}[/]";
	}
	if(titlename=="DHT11"){
		// createseries("AAPL.Open", "Open");
		// createseries("AAPL.High", "High");
		// createseries("AAPL.Low", "Low");
		createseries("temp", "Temperature (°C)");
		createseries("hum", "Humidity (%)");
	}
	else if(titlename=="Energy"){
		// createseries("AAPL.Close", "Close");
		createseries("power", "Power (W)")
		createseries("energy", "Energy (kWh)");
	}
	
	// zoom
    
	// Make a panning cursor
	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "panXY";
	chart.cursor.xAxis = categoryAxis;
	//chart.cursor.snapToSeries = series1;

	// Create a horizontal scrollbar with previe and place it underneath the date axis
	//chart.scrollbarX = new am4charts.XYChartScrollbar();
	chart.scrollbarX = new am4core.Scrollbar();
	// //chart.scrollbarX.series.push(series1);
	chart.scrollbarX.parent = chart.bottomAxesContainer;
	//chart.scrollbarY = new am4core.Scrollbar();

	categoryAxis.start = 0.8;
	categoryAxis.keepSelection = true;

	// Add legend
	chart.legend = new am4charts.Legend();
}
// var c1 = createchart("chartdiv1","DHT11")
// var c2 = createchart("chartdiv2","Energy")
