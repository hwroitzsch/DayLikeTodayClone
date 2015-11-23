const EVENT_HANDLED = false;
const EVENT_NOT_HANDLED = true;

$(document).ready(
	() => {
		$('#submit-form').submit(function() {
			//const day = $('#day-chooser').val();
			const day = $('#day-chooser option:selected').text();
			const month = $('#month-chooser option:selected').text();
			const language = $('#language-chooser option:selected').text();

			// console.log(day);
			// console.log(month);
			// console.log(language);

			get_json(month, day, language).done(
				result => {
					console.log("received data!");
					console.log(result);
				}
			).fail(
				result => {
					console.log('AJAX REQUEST FAILED!');
				}
			);

			//var timeline_json = get_json(); // you write this part
		
			// two arguments: the id of the Timeline container (no '#')
			// and the JSON object or an instance of TL.TimelineConfig created from
			// a suitable JSON object
			
			//window.timeline = new TL.Timeline('timeline-embed', timeline_json);

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