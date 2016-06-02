$(function() {
  $("#round_trip_search").click(function() {
    $.ajax({
      type: "GET",
      url: $SCRIPT_ROOT + "/index-round-trip",
      contentType: "application/json; charset=utf-8",
      data: {
        From: $('input[name="From1"]').val(),
        to: $('input[name="to1"]').val(),
        d_date: $('input[name="d_date1"]').val(),
        r_date: $('input[name="r_date1"]').val(),
        volume: $('select[name="volume1"]').val(),
        cabin_class: $('select[name="cabin_class1"]').val()
      },
      success: function(response) {
        $('#round_trip_result').html(response);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert(errorThrown);
      }
    });
  });
});

$(function() {
  $("#one_way_search").click(function() {
    $.ajax({
      type: "GET",
      url: $SCRIPT_ROOT + "/index-one-way",
      contentType: "application/json; charset=utf-8",
      data: {
        From: $('input[name="From2"]').val(),
        to: $('input[name="To2"]').val(),
        d_date: $('input[name="d_date2"]').val(),
        volume: $('select[name="volume2"]').val(),
        cabin_class: $('select[name="cabin_class2"]').val()
      },
      success: function(response) {
        $('#one_way_result').html(response);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert(errorThrown);
      }
    });
  });
});

// page-picker.html
	var $pickerLib = $('.ui-picker-lib'),
	    pickerMap,
	    pickerMarker;

	function initPickerMap () {
		pickerMap = new google.maps.Map(document.getElementById('ui_picker_map_wrap'), {
			center: {
				lat: 0,
				lng: 0
			},
			disableDefaultUI: true,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			zoom: 15
		});

		pickerMarker = new google.maps.Marker({
			map: pickerMap,
			position: {lat: 0, lng: 0}
		});
	};

	if ((typeof google != 'undefined') && $('.ui-picker-map-wrap').length) {
		initPickerMap();
	};

	if (typeof jQuery.ui != 'undefined') {
		// draggable
			$('.ui-picker-draggable-handler').draggable({
				addClasses: false,
				appendTo: 'body',
				cursor: 'move',
				cursorAt: {
					top: 0,
					left: 0
				},
				delay: 100,
				helper: function () {
					return $('<div class="tile tile-brand-accent ui-draggable-helper"><div class="tile-side pull-left"><div class="avatar avatar-sm"><strong>' + $('.ui-picker-selected:first .ui-picker-draggable-avatar strong').html() + '</strong></div></div><div class="tile-inner text-overflow">' + $('.ui-picker-selected:first .ui-picker-info-title').html() + '</div></div>');
				},
				start: function (event, ui) {
					var draggableCount = $('.ui-picker-selected').length;

					if (draggableCount > 1) {
						$('.ui-draggable-helper').append('<div class="avatar avatar-brand avatar-sm ui-picker-draggable-count">' + draggableCount + '</div>');
					};
				},
				zIndex: 100
			});

		// droppable
			$('.ui-picker-nav .nav a').droppable({
				accept: '.ui-picker-draggable-handler',
				addClasses: false,
				drop: function(event, ui) {
					$('body').snackbar({
						content: 'Dropped on "' + $(this).html() + '"'
					});
				},
				hoverClass: 'ui-droppable-helper',
				tolerance: 'pointer'
			});

		// selectable
			$pickerLib.selectable({
				cancel: '.ui-picker-draggable-handler',
				filter: '.ui-picker-selectable-handler',
				selecting: function (event, ui) {
					var $selectingParent = $(ui.selecting).parent();

					$selectingParent.addClass('tile-brand-accent ui-picker-selected');

					$('.ui-picker-info').addClass('ui-picker-info-active').removeClass('ui-picker-info-null');
					$('.ui-picker-info-desc-wrap').html($selectingParent.find('.ui-picker-info-desc').html());
					$('.ui-picker-info-title-wrap').html($selectingParent.find('.ui-picker-info-title').html());

					var pickerMapLatLng = new google.maps.LatLng($selectingParent.find('.ui-picker-map-lat').html(), $selectingParent.find('.ui-picker-map-lng').html());

					pickerMap.setCenter(pickerMapLatLng);
					pickerMarker.setMap(pickerMap);
					pickerMarker.setPosition(pickerMapLatLng);
				},
				unselecting: function (event, ui) {
					var $unselectingParent = $(ui.unselecting).parent();

					$unselectingParent.removeClass('tile-brand-accent ui-picker-selected');

					if (!$('.ui-picker-selected').length) {
						$('.ui-picker-info').addClass('ui-picker-info-null');
						$('.ui-picker-info-desc-wrap').html('');
						$('.ui-picker-info-title-wrap').html('');
						pickerMarker.setMap(null);
					} else {
						var $first = $($('.ui-picker-selected')[0]);

						$('.ui-picker-info-desc-wrap').html($first.find('.ui-picker-info-desc').html());
						$('.ui-picker-info-title-wrap').html($first.find('.ui-picker-info-title').html());

						var firstLatLng = new google.maps.LatLng($first.find('.ui-picker-map-lat').html(), $first.find('.ui-picker-map-lng').html());

						pickerMap.setCenter(firstLatLng);
						pickerMarker.setMap(pickerMap);
						pickerMarker.setPosition(firstLatLng);
					};
				}
			});
	};

	$(document).on('click', '.ui-picker-info-close', function () {
		$('.ui-picker-info').removeClass('ui-picker-info-active');
	});

// ui-picker.html
  $('#datepicker_Fei1').pickdate({
    cancel: 'Clear',
    closeOnCancel: false,
    closeOnSelect: false,
    container: '',
    firstDay: 0,
    format: 'dd/mmm/yyyy',
    formatSubmit: 'yyyy-mm-dd',
    onClose: function () {
      $('body').snackbar({
        content: 'Depart date selected'
      });
    },
    onOpen: function () {
      $('body').snackbar({
        content: 'Please select depart date'
      });
    },
    selectMonths: true,
    selectYears: 5,
    min: true
  });

$('#datepicker_Fei2').pickdate({
  cancel: 'Clear',
  closeOnCancel: false,
  closeOnSelect: false,
  container: '',
  firstDay: 0,
  format: 'dd/mmm/yyyy',
  formatSubmit: 'yyyy-mm-dd',
  onClose: function () {
    $('body').snackbar({
      content: 'Return date selected'
    });
  },
  onOpen: function () {
    $('body').snackbar({
      content: 'Please select return date'
    });
  },
  selectMonths: true,
  selectYears: 5,
  min: true
});

$('#datepicker_Fei3').pickdate({
  cancel: 'Clear',
  closeOnCancel: false,
  closeOnSelect: false,
  container: '',
  firstDay: 0,
  format: 'dd/mmm/yyyy',
  formatSubmit: 'yyyy-mm-dd',
  onClose: function () {
    $('body').snackbar({
      content: 'Depart date selected'
    });
  },
  onOpen: function () {
    $('body').snackbar({
      content: 'Please select depart date'
    });
  },
  selectMonths: true,
  selectYears: 5,
  min: true
});
$('#ui_datepicker_example_1').pickdate();

	$('#ui_datepicker_example_2').pickdate({
		cancel: 'Clear',
		closeOnCancel: false,
		closeOnSelect: true,
		container: '',
		firstDay: 1,
		format: 'You selecte!d: dddd, d mm, yy',
		formatSubmit: 'dd/mmmm/yyyy',
		ok: 'Close',
		onClose: function () {
			$('body').snackbar({
				content: 'Datepicker closes'
			});
		},
		onOpen: function () {
			$('body').snackbar({
				content: 'Datepicker opens'
			});
		},
		selectMonths: true,
		selectYears: 10,
		today: ''
	});

	$('#ui_datepicker_example_3').pickdate({
		disable: [
			[2016,0,12],
			[2016,0,13],
			[2016,0,14]
		],
		today: ''
	});

	$('#ui_datepicker_example_4').pickdate({
		disable: [
			new Date(2016,0,12),
			new Date(2016,0,13),
			new Date(2016,0,14)
		],
		today: ''
	});

	$('#ui_datepicker_example_5').pickdate({
		disable: [
			2, 4, 6
		],
		today: ''
	});

	$('#ui_datepicker_example_6').pickdate({
		disable: [
			{
				from: [2016,0,12],
				to: 2
			}
		],
		today: ''
	});

	$('#ui_datepicker_example_7').pickdate({
		disable: [
			true,
			3,
			[2016,0,13],
			new Date(2016,0,14)
		],
		today: ''
	});

	$('#ui_datepicker_example_8').pickdate({
		disable: [
			{
				from: [2016,0,10],
				to: [2016,0,30]
			},
			[2016,0,13, 'inverted'],
			{
				from: [2016,0,19],
				to: [2016,0,21],
				inverted: true
			}
		],
		today: ''
	});

	$('#ui_datepicker_example_9').pickdate({
		max: [2016,0,30],
		min: [2016,0,10],
		today: ''
	});

	$('#ui_datepicker_example_10').pickdate({
		max: new Date(2016,0,30),
		min: new Date(2016,0,10),
		today: ''
	});

	$('#ui_datepicker_example_11').pickdate({
		max: true,
		min: -10,
		today: ''
	});

// ui-progress.html
	$('.finish-loading').on('click', function(e) {
		e.stopPropagation();
		$($(this).attr('data-target')).addClass('el-loading-done');
	});

	$('#ui_el_loading_example_wrap .tile-active-show').each(function (index) {
		var $this = $(this),
		    timer;

		$this.on('hide.bs.tile', function(e) {
			clearTimeout(timer);
		});

		$this.on('show.bs.tile', function(e) {
			if (!$('.el-loading', $this).hasClass('el-loading-done')) {
				timer = setTimeout(function() {
					$('.el-loading', $this).addClass('el-loading-done');
					$this.prepend('<div class="tile-sub"><p>Additional information<br><small>Aliquam in pharetra leo. In congue, massa sed elementum dictum, justo quam efficitur risus, in posuere mi orci ultrices diam.</small></p></div>');
				}, 6000);
			};
		});
	});

// ui-snackbar.html
	var snackbarText = 1;

	$('#ui_snackbar_toggle_1').on('click', function () {
		$('body').snackbar({
			content: 'Simple snackbar ' + snackbarText + ' with some text',
			show: function () {
				snackbarText++;
			}
		});
	});

	$('#ui_snackbar_toggle_2').on('click', function () {
		$('body').snackbar({
			content: '<a data-dismiss="snackbar">Dismiss</a><div class="snackbar-text">Simple snackbar ' + snackbarText + ' with some text and a simple <a href="javascript:void(0)">link</a>.</div>',
			show: function () {
				snackbarText++;
			}
		});
	});
