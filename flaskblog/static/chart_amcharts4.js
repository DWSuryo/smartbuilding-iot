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
	chart.dataSource.url = source;
	chart.dataSource.parser = new am4core.CSVParser();
	chart.dataSource.parser.options.useColumnNames = true;
	chart.dateFormatter.inputDateFormat = "i";
	// updating source
	chart.dataSource.reloadFrequency = 20000;
	chart.dataSource.updateCurrentData = true;
	chart.dataSource.incremental = true;
	chart.dataSource.incrementalParams = {
		incremental: "y",
		something: "else"
	}
	chart.events.on("datavalidated", function(ev) {
		chart.series.each(function(series) {
		  series.appear();
		});
	});

	// Create x axes
	// var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
	var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
	categoryAxis.dataFields.category = "datetime";
	categoryAxis.tooltipDateFormat = "d MMMM, HH:mm:ss";
	//categoryAxis.dateFormats.setKey("day", "MMMM dt");
	//categoryAxis.dateFormats.setKey("second");
	categoryAxis.dateFormats.setKey("second", "HH:mm:ss");
	// categoryAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
	// categoryAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
	// categoryAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
	categoryAxis.skipEmptyPeriods = true; 
	//categoryAxis.periodChangeDateFormats.setKey("hour", "HH:mm:ss"); 

	// this makes the data to be grouped
	categoryAxis.groupData = true;
	categoryAxis.groupCount = 150;
	categoryAxis.skipEmptyPeriods = false; 
	
	


	//create series function
	function createseries(value, legend, position) {
		// Create y value axis
		var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
		valueAxis.paddingLeft = 0;
		valueAxis.paddingRight = 0;
		if (chart.yAxes.indexOf(valueAxis) != 0) {
			valueAxis.syncWithAxis = chart.yAxes.getIndex(0);
		  }

		//create series line
		var series = chart.series.push(new am4charts.LineSeries());
		series.dataFields.dateX = "tgl";
		series.dataFields.valueY = value;
		series.yAxis = valueAxis;
		series.name = legend;
		series.strokeWidth = 1.5;
		//cursor tooltips
		series.tooltipText = "{name}: [b]{valueY}[/]";

		valueAxis.renderer.line.strokeOpacity = 1;
		valueAxis.renderer.line.strokeWidth = 2;
		//valueAxis.renderer.line.stroke = series.stroke;
		valueAxis.renderer.labels.template.fill = series.stroke;
		valueAxis.renderer.opposite = position;
	}
	if(titlename=="DHT11"){
		createseries("temp", "Temperature (°C)", false);
		createseries("hum", "Humidity (%)", true);
	}
	else if(titlename=="Energy"){
		createseries("power", "Power (W)", false)
		createseries("energy", "Energy (kWh)", true);
	}
	
	// zoom
    
	// Make a panning cursor
	chart.cursor = new am4charts.XYCursor();
	chart.cursor.behavior = "panXY";
	chart.cursor.xAxis = categoryAxis;

	// Create a horizontal scrollbar with previe and place it underneath the date axis
	//chart.scrollbarX = new am4charts.XYChartScrollbar();
	chart.scrollbarX = new am4core.Scrollbar();
	chart.scrollbarX.parent = chart.bottomAxesContainer;
	//chart.scrollbarY = new am4core.Scrollbar();

	categoryAxis.start = 0.8;
	categoryAxis.keepSelection = true;

	// Add legend
	chart.legend = new am4charts.Legend();
}
// var c1 = createchart("chartdiv1","DHT11")
// var c2 = createchart("chartdiv2","Energy")
