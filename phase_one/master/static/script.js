/* Custom Javascript for Gorbechov dashboard */

function read_hosts(){
	$.getJSON("/dashboard_hosts", (data)=>{
		$("#hosts_table tr.inserted").remove()
		$.each(data, (key,val)=>{
			var row_class = ''
			if (val['run_count'] == 15 || val['run_count'] == 5){
				row_class = "completed"
			}
			$("#hosts_table tr:last").after("<tr class='inserted " + row_class + "'><td>" + val['ip'] + "</td><td>" + val['run_count'] + "</td><td>" + val['last_run'] + "</td><td>" + val['status'] + "</td></tr>")
		})
	})
}

function read_status(){
	$("#data_loading").show()
	$.getJSON("/dashboard_status", (data) => {
		$("#data_table tr.inserted").remove()
		$.each(data, (key,val)=>{
			var row_class = ''
			if (val[1].indexOf('data') != -1){
				row_class = "completed"
			}
			$("#data_table tr:last").after("<tr class='inserted " + row_class + "'><td>" + val[0] + "</td><td>" + val[1] + "</td></tr>")
		})

		$("#data_loading").hide()
		read_count()
	})
}

function read_count(){
	$.get("/dashboard_count", data => {
		var completed_count = $("table#data_table tbody tr.completed").length

		$("#total_count").html(data + " total, " + Math.abs(1 * completed_count + 1 - 1 * data ) + " problem " )


	})
}

function show_all(){
	$(".completed").show()
}
function hide_all(){
	$(".completed").hide()
}

$(document).ready(()=>{
	
	read_hosts()
	read_status()


	setInterval(()=>{
		read_hosts()
		read_status()
	},30000)
})
