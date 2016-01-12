const EVENT_HANDLED = false;
const EVENT_NOT_HANDLED = true;

/**
 * jQuery for adding event listeners to HTML elements
 */
$(document).ready(
	() => {
		$('.submit-form').submit(() => {

			const category = $('.category-chooser option:selected').text().toLowerCase();
			const language = $('.language-chooser option:selected').text().toLowerCase();
			const day = $('.day-chooser option:selected').text();
			const month = $('.month-chooser option:selected').text();
			const year = $('.year-chooser option:selected').text();

			insert_loader_animation();

			get_json(category, year, month, day, language).done(
				result => {

					console.log('Received JSON result for ' + category + '.');
					if (category === 'persons') {
						var timeline_config = create_timeline_config();
						window.timeline = new TL.Timeline('timeline-embed', result, timeline_config);

						$('.tl-slidenav-content-container').on('click', function(event) {
							console.log('next or previous clicked, removing stupid styling ...');
							remove_unnecessary_direct_styling();
							add_necessary_styling();
						});

						remove_unnecessary_direct_styling();
						add_necessary_styling();

					} else if (category === 'companies') {
						console.log('now using companies result');

					} else if (category === 'series') {
						console.log('now using series result');
					}

				}
			).fail(
				result => {
					console.log('AJAX REQUEST FAILED!');
				}
			);

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

/**
 * This function retrieves JSON data from the server. The returned JSON data should be in the timeline.js JSON data format.
 */
function get_json(category, year, month, day, language) {
	var url = '';

	if (category === 'persons') {
		url += '/' + category + '/' + year + '/' + month + '/' + day + '/' + language;
	} else if (category === 'companies') {
		url += '/' + category + '/' + year + '/' + language;
	} else if (category === 'series') {
		url += '/' + category + '/' + year + '/' + language;
	} else {
		console.log('unknown category chosen');
	}

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
	$('#timeline-embed').html('<div class="flex-area"><img src="static/img/pacman_loader.gif" alt="loading ..."></div>');
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
