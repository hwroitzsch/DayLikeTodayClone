
DAYS_OF_MONTHS = []
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
]
YEARS = []
LANGUAGES = [
	'English',
	'German'
]

current_date = new Date();
current_year = current_date.getFullYear();

for (var year = 1900; year <= current_year; year++) {
	YEARS.push(year);
}

_.each(MONTH, (element, index, list) => {
	DAYS_OF_MONTHS[index] = 31;
});

// BUILD THE  SELECT BOXES, TO ADD AND REMOVE THEM DYNAMICALLY
years_select = build_years_select();
months_select = build_months_select();
days_select = build_days_select();
languages_select = build_languages_select();


// start of event handling code
$(document).ready(

	() => {
		$('.category-chooser').change(
			() => {
				category = $('.category-chooser').val().toLowerCase();
				show_selects_for_category(category);
			}
		);
	}
);

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

	} else if (category === 'companies' || category === 'series') {
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
		months_options += '<option value="' + index + '">' + element + '</option>\n';
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
		days_options += '<option value="' + index + '">' + element + '</option>\n';
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

// einbauen:

/*
kategorie auswaehlbar machen
	year (serien, companies) oder volles datum (personen)

*/
