const EVENT_HANDLED = false;
const EVENT_NOT_HANDLED = true;

$(document).ready(
	() => {
		$('#submit-form').submit(function() {
			//const day = $('#day-chooser').val();
			const day = $('#day-chooser option:selected').text();
			const month = $('#month-chooser option:selected').text();
			const language = $('#language-chooser option:selected').text();

			get_json(month, day, language).done(
				result => {
					console.log(result);
					var timeline_config = create_timeline_config();
					window.timeline = new TL.Timeline('timeline-embed', result);
					console.log(window.timeline);
					//window.timeline = new TL.Timeline('timeline-embed', result, timeline_config);
				}
			).fail(
				result => {
					console.log('AJAX REQUEST FAILED!');
				}
			);

			return EVENT_HANDLED;
		});
	}
);

function get_json(month, day, language) {
	const url = '/' + 'what_happened' + '/' + month + '/' + day + '/' + language;
	
	return $.ajax({
		type: 'GET',
		url: url,
		data: {},
		contentType: 'application/json;charset=UTF-8'
	});
}

function create_timeline_config() {
	return {
		width:              '100%',
		height:             '600px',
		//source:             'path_to_json/or_link_to_googlespreadsheet',
		embed_id:           'timeline-embed',               //OPTIONAL USE A DIFFERENT DIV ID FOR EMBED
		start_at_end:       false,                          //OPTIONAL START AT LATEST DATE
		start_at_slide:     '4',                            //OPTIONAL START AT SPECIFIC SLIDE
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