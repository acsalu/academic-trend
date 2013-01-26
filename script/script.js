DEFAULT_START = 2000;
DEFAULT_END = 2012;
current_data = [];

String.prototype.trim = function() {
    return this.replace(/(^[\s]*)|([\s]*$)/g, "");
}


$(document).ready(function() {
	console.log("document is ready!");
	var $keyword = $('input[name="keyword"]');

	$('#search').click(function() {
		var trimmed = $keyword.val().trim();
		if (trimmed.length != 0) {
			$('#chart_div').html('<img id="loader" src="img/ajax-loader.gif">');
			fetchData(trimmed);
		}
	});
	
	$(document).keydown(function(key) {
		if (parseInt(key.which, 10) == 13)
			$('#search').click();
	});
	
	$('#compare').click(function() {
		var trimmed = $keyword.val().trim();
		if (trimmed.length != 0) {
			$('#chart_div').html('<img id="loader" src="img/ajax-loader.gif">');
			fetchData(trimmed);
		}
	});
});

function fetchData(keyword) {
	console.log("searching for " + keyword + "...");
	var url = "/query?q=" + keyword + "&start=" + DEFAULT_START + "&end=" + DEFAULT_END;
	console.log(url);
	$.getJSON(url, function(res) {
		console.log(res);
		drawChart(keyword, res);
	});
}


function drawChart(title, data) {
	current_data = [['Year', title]];
	for (var i = DEFAULT_START; i <= DEFAULT_END; ++i) {
		current_data.push([i.toString(), current_data[i - DEFAULT_START]]);
	}

	var data = google.visualization.arrayToDataTable(current_data);
	
	var options = {
	  title: 'Academic Trend'
	};
	
	$('#chart_div').html("");
	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}