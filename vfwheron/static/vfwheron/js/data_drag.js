$(function() {
		    var clientFrameWindow = $('#wpstool').get(0).contentWindow;
            var test = document.getElementById("wpstool");
		    $("#workspace li").on('dragstart',function() {
		    	dragged = event.target;
		        console.log("Drag Started");
		        var clientFrameWindow = $('#wpstool').get(0).contentWindow;
		    });
		    $("#workspace li").on('dragend',function() {
		        console.log("Drag End");
		        document.getElementById("wpstool").contentWindow.document.getElementsByTagName("input")[1].value = dragged.id;		
		    });
		    
		    $("#wpstool").on('dragover',function() {
		    	colsole.log("drag over");
		    })
		    
		    
		    
		    $('#wpstool').load(function()
		    {
		        var total = 0;
		        $(clientFrameWindow.document.body).find('*').on('dragenter',function(event)
		        {
		            event.preventDefault();
		            event.stopPropagation();
		            console.log('Drag Enter');
		            total +=1;
		        }).on('dragover',function(event)
		        {
		            event.preventDefault();
		            event.stopPropagation();
		            console.log('Drag Over');
		            total +=1;
		        });

		
		        $(clientFrameWindow.document).find('body,html').on('drop',function(event) {
		            event.preventDefault();
		            event.stopPropagation();
		            console.log('Drop event ' + dragged.id);
		            total +=1;
		            console.log("Total Events Fired = "+total);
		            total = 0;
		            
		            var iframe = document.getElementById("wpstool");
		            var elmnt = iframe.contentWindow.document.getElementByTagName("input")[0];
		            elmnt.value = dragged.id;
		            
		        });
		    });
		    
		    

		});