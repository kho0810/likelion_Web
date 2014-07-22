$(document).ready(function() {
	$('.carousel').carousel ({
		interval: 1500,
		pause: "mouselaeve"
	});

	$('a[href^="#"]').on('click',function (e) {
		e.preventDefault();

		var target = this.hash,
		$target = $(target);

		$('html, body').stop().animate({
			'scrollTop': $target.offset().top
		}, 900, 'swing', function () {
			window.location.hash = target;
		});
	});

	$('#small_img img').fadeTo('fast', '0.5');
	$('#small_img img').hover(
		function() {
			$(this).fadeTo('fast', '1');
		},
		function(){
			$(this).fadeTo('fast', '0.5')
		}
		);

	$('#b').css('display', 'none');
	$('#c').css('display', 'none');
	slide('#a', '#b', '#c');

	$('#small_img a[href^="#"]').click(function (e) {
		e.preventDefault();
		var target = this.hash
		$('#big_img div').hide()
		$(target).fadeIn(1000)
	});

});

function slide(a, b, c) {
	$(a).delay(2000).fadeOut(1000);
	$(b).delay(2000).fadeIn(1000, function() {
		$(this).delay(2000).fadeOut(1000);
		slide(b, c, a);
	});
}