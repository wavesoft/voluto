$(function() {

	/**
	 * Enable virtual radio buttons using data-radio-goup attribute
	 */
	$("input[data-radio-group]").click(function(e) {
		// Disable everything else in the group
		$("input[data-radio-group=" + $(this).data("radio-group") + "]:checked")
			.prop("checked", false);
		// Enable clicked item
		$(this).prop("checked", true);
	});

	/**
	 * Activate another checkbox when clicked
	 */
	$("input[data-link-check]").click(function(e) {
		// If we are checed, check the specified link
		if ($(this).is(":checked"))
			$($(this).data("link-check")).prop("checked", true);
	});

	/**
	 * Control the enabled state of another element
	 */
	$("input[data-link-enable]").each(function(i,e) {

		// Apply state on linked target
		$($(this).data("link-enable")).prop("disabled", !$(this).is(":checked"));

		// If we are checed, check the specified link
		$(e).click(function(e) {
			var disabled = !$(this).is(":checked"),
				target = $($(this).data("link-enable"));
			target.prop("disabled", disabled);
			if (disabled) $(target).prop("checked", false);
		});
		
	});

});