const EVENT_HANDLED = false;
const EVENT_NOT_HANDLED = true;

DAYS_OF_MONTHS = [
	1,2,3,4,5,6,7,8,9,
	10,11,12,13,14,15,16,17,18,19,
	20,21,22,23,24,25,26,27,28,29,
	30,31
];
MONTH = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

YEARS = [];
LANGUAGES = [
	'English',
	'German'
];

current_date = new Date();
current_year = current_date.getFullYear();

for (var year = 1900; year <= current_year; year++) {
	YEARS.push(year);
}



// BUILD THE  SELECT BOXES, TO ADD AND REMOVE THEM DYNAMICALLY
years_select = build_years_select();
months_select = build_months_select();
days_select = build_days_select();
languages_select = build_languages_select();


// start of event handling code
$(document).ready(
	() => {
		show_selects_for_category('persons');

		$('.category-chooser').change(
			() => {
				category = $('.category-chooser').val().toLowerCase();
				show_selects_for_category(category);
			}
		);

		$('.submit-form').submit(() => {
			const category = $('.category-chooser option:selected').text().toLowerCase();
			const language = $('.language-chooser option:selected').text().toLowerCase();
			
			var raw_day = $('.day-chooser option:selected').text();
			if(raw_day.length === 1) {
				raw_day = '0' + raw_day;
			} else {
				raw_day = raw_day;
			}
			const day = raw_day;
			
			var raw_month = $('.month-chooser option:selected').val();
			console.log(raw_month);
			if(raw_month.length === 1) {
				raw_month = '0' + raw_month;
			} else {
				raw_month = raw_month;
			}
			const month = raw_month;
			
			const year = $('.year-chooser option:selected').text();

			insert_loader_animation();

			console.log('Getting JSON for ' + category);

			if (category === 'persons') {
				get_json_with_complete_date(category, year, month, day, language).done(
				result => {
					console.log('Received JSON result for:|' + category + '|.');
					console.log(result);

					var timeline_config = create_timeline_config();
					window.timeline = new TL.Timeline('timeline-embed', result, timeline_config);

					$('.tl-slidenav-content-container').on('click', function(event) {
						remove_unnecessary_direct_styling();
						add_necessary_styling();
					});

					remove_unnecessary_direct_styling();
					add_necessary_styling();

					$('.ajax_loader_animation').remove();
				}).fail(
					result => {
						console.log('AJAX REQUEST FAILED!');
					}
				);
			}

			if (category === 'foundations' || category === 'series') {
				get_json(category, year, language).done(
					result => {
						if (category === 'foundations') {
							console.log('RENDERING FOUNDATIONS');
							$('.result-container').empty();
							_.each(result.result, (one_foundation, index, list) => {
								foundations_html = build_foundation_item_html(one_foundation);
								$('.result-container').append(foundations_html);
							});

						} else if (category === 'series') {
							console.log('RENDERING SERIES');
							$('.result-container').empty();
							_.each(result.result, (one_series, index, list) => {
								series_html = build_series_item_html(one_series);
								$('.result-container').append(series_html);
							});
						}
						$('.ajax_loader_animation').remove();
					}
				).fail(
					result => {
						console.log('AJAX REQUEST FAILED!');
					}
				);
			}

			return EVENT_HANDLED;
		});

		$('.tl-slidenav-content-container').click(() => {
			setTimeout(() => {
				remove_unnecessary_direct_styling();
				add_necessary_styling();
				alert('ALERT');
			}, 1);
		});
	}
);

function build_foundation_item_html(one_foundation) {
	return '<div class="foundation-item">'+
			'<p><a href="' + one_foundation.url + '">Link</a></p>' +
			'<p>Name:' + one_foundation.name + '</p>' +
			'<p>Start Date:' + one_foundation.start_date + '</p>' + 
			'<p>Type of Business:' + one_foundation.type + '</p>' + 
			'<p>Revenue:' + one_foundation.revenue + '</p>' + 
			'<p><img class="foundation-item-image" src="' + one_foundation.image_url + '" alt="IMAGE"></img></p>' +
			'<p>Summary: ' + one_foundation.summary + '</p>' +
		'</div>';
}

function build_series_item_html(one_series) {
	return '<div class="series-item">'+
			'<p><a href="' + one_series.url + '">Link</a></p>' +
			'<p>Start Date:' + one_series.start_date + '</p>' + 
			'<p>Name:' + one_series.name + '</p>' +
			'<p>Episode Count:' + one_series.episode_count + '</p>' +
			'<p>Producer:<a href="' + one_series.producer_url + '">Producer</a></p>' +
			'<p><img class="series-item-image" src="' + one_series.image_url + '" alt="IMAGE"></img></p>' +
			'<p>Summary: ' + one_series.summary + '</p>' +
		'</div>';
}

function show_selects_for_category(category) {
	children = $(".chooser-area > div")
	child_count = children.length;

	for(var child_index = 1; child_index < child_count - 1; child_index++) {
		children.eq(child_index).remove();
	}

	if (category === 'persons') {
		children.eq(0).after(languages_select);
		children.eq(0).after(days_select);
		children.eq(0).after(months_select);
		children.eq(0).after(years_select);

	} else {
		children.eq(0).after(languages_select);
		children.eq(0).after(years_select);
	}
}

function daysInMonth(month, year) {
	return new Date(year, month, 0).getDate();
}

function build_years_select() {
	years_options = ''
	_.each(YEARS, (element, index, list) => {
		years_options += '<option value="' + index + '">' + element + '</option>\n';
	});
	years_select = $(
		'<div>' +
			'<label>Year: </label>' +
			'<select class="year-chooser mini-input">' +
				years_options +
			'</select>' +
		'</div>'
	);
	return years_select;
}

function build_months_select() {
	months_options = ''
	_.each(MONTH, (element, index, list) => {
		months_options += '<option value="' + (index + 1) + '">' + element + '</option>\n';
	});
	months_select = $(
		'<div>' +
			'<label>Month: </label>' +
			'<select class="month-chooser mini-input">' +
				months_options +
			'</select>' +
		'</div>'
	);
	return months_select;
}

function build_days_select() {
	days_options = ''
	_.each(DAYS_OF_MONTHS, (element, index, list) => {
		days_options += '<option value="' + (index + 1) + '">' + element + '</option>\n';
	});
	days_select = $(
		'<div>' +
			'<label>Day: </label>' +
			'<select class="day-chooser mini-input">' +
				days_options +
			'</select>' +
		'</div>'
	);
	return days_select;
}

function build_languages_select() {
	languages_options = ''
	_.each(LANGUAGES, (element, index, list) => {
		languages_options += '<option value="' + index + '">' + element + '</option>\n';
	});
	languages_select = $(
		'<div>' +
			'<label>Language: </label>' +
			'<select class="language-chooser" class="mini-input">' +
				languages_options +
			'</select>' +
		'</div>'
	);
	return languages_select;
}

/**
 * This function retrieves JSON data from the server. The returned JSON data should be in the timeline.js JSON data format.
 */
function get_json_with_complete_date(category, year, month, day, language) {
	var url = '/' + category + '/' + year + '/' + month + '/' + day + '/' + language;
	console.log('Getting JSON from REST URL: ' + url);

	return $.ajax({
		type: 'GET',
		url: url,
		data: {},
		contentType: 'application/json;charset=UTF-8'
	});
}
function get_json(category, year, language) {
	var url = '/' + category + '/' + year + '/' + language;
	console.log('Getting JSON from REST URL: ' + url);

	return $.ajax({
		type: 'GET',
		url: url,
		data: {},
		contentType: 'application/json;charset=UTF-8'
	});
}

/**
 * This function returns a configuration object for timeline.js.
 */
function create_timeline_config() {
	return {
		width:              '100%',
		height:             '600px',
		//source:             'path_to_json/or_link_to_googlespreadsheet',
		embed_id:           'timeline-embed',               //OPTIONAL USE A DIFFERENT DIV ID FOR EMBED
		start_at_end:       false,                          //OPTIONAL START AT LATEST DATE
		start_at_slide:     '0',                            //OPTIONAL START AT SPECIFIC SLIDE
		start_zoom_adjust:  '3',                            //OPTIONAL TWEAK THE DEFAULT ZOOM LEVEL
		hash_bookmark:      true,                           //OPTIONAL LOCATION BAR HASHES
		font:               'Bevan-PotanoSans',             //OPTIONAL FONT
		debug:              true,                           //OPTIONAL DEBUG TO CONSOLE
		lang:               'en',                           //OPTIONAL LANGUAGE
		//maptype:            'watercolor'                   //OPTIONAL MAP STYLE
		//css:                'path_to_css/timeline.css',     //OPTIONAL PATH TO CSS
		//js:                 'path_to_js/timeline-min.js'    //OPTIONAL PATH TO JS
	}
}

/**
 * This function inserts an animation to show that the AJAX request is being processed on the server side.
 */
function insert_loader_animation() {
	$('#timeline-embed').html('<div class="flex-area ajax_loader_animation"><img src="static/img/pacman_loader.gif" alt="loading ..."></div>');
}

/**
 * This function removes unnecessary direct styling of HTML elements, which causes bad layout of some elements of the timeline.
 */
function remove_unnecessary_direct_styling() {
	// tl-media-item tl-media-youtube tl-media-shadow

	$('.tl-media-youtube').removeAttr('width');
	$('.tl-media-youtube').removeAttr('height');
	$('.tl-media-youtube').removeAttr('style');

	$('.tl-media-item').removeAttr('width');
	$('.tl-media-item').removeAttr('height');
	$('.tl-media-item').removeAttr('style');

	$('.tl-media').removeAttr('width');
	$('.tl-media').removeAttr('height');
	$('.tl-media').removeAttr('style');

	$('.tl-slide-content').removeAttr('width');
	$('.tl-slide-content').removeAttr('height');
	$('.tl-slide-content').removeAttr('style');

	// pattern: $("#myParagraph").css({
	//	"backgroundColor":"black",
	//	"color":"white"
	//});

	//tl-media-item tl-media-youtube tl-media-shadow
	//$('.tl-slide-content .tl-text-content').css('box-sizing', '');
	//document.getElementById('mydiv').style.removeProperty('-moz-user-select')
}

function add_necessary_styling() {
	$('.tl-media-image').css({
		'max-width': '200px',
		'max-height': '200px'
	});
}
