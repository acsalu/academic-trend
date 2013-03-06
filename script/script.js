DEFAULT_START = 1995;
DEFAULT_END = 2010;
current_data = null;

String.prototype.trim = function() {
    return this.replace(/(^[\s]*)|([\s]*$)/g, "");
}


$(document).ready(function() {
	console.log("document is ready!");
	var $keyword = $('input[name="keyword"]');

	$('#search').click(function() {
		var trimmed = $keyword.val().trim();
		if (trimmed.length != 0) {
			current_data = null;
			$('#chart_div').html('<img id="loader" src="img/ajax-loader.gif">');
			fetchData(trimmed);
		}
	});
	
	
	$('#compare').click(function() {
		var trimmed = $keyword.val().trim();
		if (trimmed.length != 0) {
			$('#chart_div').html('<img id="loader" src="img/ajax-loader.gif">');
			fetchData(trimmed);
		}
	});
	
	$(document).keydown(function(key) {
		if (parseInt(key.which, 10) == 13)
			if (current_data) $('#compare').click();
			else $('#search').click();
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
	
	console.log(current_data);	
	if (!current_data) console.log("current data is an empty array.");
	
	if (!current_data) {
		current_data = [['Year', title]];		
		for (var i = DEFAULT_START; i <= DEFAULT_END; ++i) {
			current_data.push([i.toString(), data[i - DEFAULT_START]]);
		}
	} else {
		current_data[0].push(title);
		for (var i = 0; i < data.length; ++i)
			current_data[i + 1].push(data[i]);
	}
	
	var data = google.visualization.arrayToDataTable(current_data);
	
	var options = {
	  title: 'Result',
	  lineWidth: 3
	};
	
	$('#chart_div').html("");
	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}