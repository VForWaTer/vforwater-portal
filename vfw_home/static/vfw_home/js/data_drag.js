/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

$(function() {
		    var clientFrameWindow = $('#wpstool').get(0).contentWindow;
            var test = document.getElementById("wpstool");
		    $("#workspace li").on('dragstart',function(event) {
		    	dragged = event.target;
		        var clientFrameWindow = $('#wpstool').get(0).contentWindow;
		        event.dataTransfer = event.originalEvent.dataTransfer;
		        event.dataTransfer.setData("data", dragged.id);
		    });
		    $("#workspace li").on('drag',function(event) {
		    	dragged = event.target;
		        event.dataTransfer = event.originalEvent.dataTransfer;
		        event.dataTransfer.setData("data", dragged.id);
		    });
		    $("#workspace li").on('dragend',function(event) {
		        document.getElementById("wpstool").contentWindow.document.getElementsByTagName("input")[1].value = dragged.id;
		    });

		    $("#wpstool").on('dragover',function() {
		    	console.log("drag over");
		    })



		    $('#wpstool').load(function()
		    {
		        var total = 0;
		        $(clientFrameWindow.document.body).find('*').on('dragenter',function(event)
		        {
		            event.preventDefault();
		            event.stopPropagation();
		            total +=1;
		        }).on('dragover',function(event)
		        {
		            event.preventDefault();
		            event.stopPropagation();
		            total +=1;
		        });


		        $(clientFrameWindow.document).find('body,html').on('drop',function(event) {
		            event.preventDefault();
		            event.stopPropagation();
		            total +=1;
		            total = 0;

		        });
		    });



		});
