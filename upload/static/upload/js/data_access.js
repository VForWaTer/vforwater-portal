$(function() {
	clearURL = "{% url 'upload:clear_database' %}";

	/* 1. OPEN THE FILE EXPLORER WINDOW */
	$(".js-upload-files").click(function() {
		$("#fileupload").click();
	});

	/* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
	$("#fileupload").fileupload({

		dataType : 'json',
		done : function(e, data) { /* 3. PROCESS THE RESPONSE FROM THE SERVER */
			if (data.result.is_valid) {
				$("#workspace div").prepend(
					"<strong><a href='" + data.result.url + "'>" + data.result.name + "</a></strong>")
				}
			}
		});
});
