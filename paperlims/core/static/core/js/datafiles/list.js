$(document).ready(function () {

	replaceSizeMessage = function(file,message) {
		_ref1 = file.previewElement.querySelectorAll("[data-dz-size]");
		for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
			node = _ref1[_j];
			node.innerHTML = message;
		}
	};

	var dropzone_datafile = new Dropzone('div#to_be_uploaded_datafile',{
		url: '/datafiles/upload',
		previewsContainer: "#to_be_uploaded_datafile",
		autoProcessQueue: false,
		addRemoveLinks: true,
		parallelUploads: 1,
		maxFilesize:4024
	});

	dropzone_datafile.on("addedfile", function(file) {
		$('#to_be_uploaded_datafile').removeClass('hidden');
		$('#upload_files').removeClass('hidden');
		$('#cancel_upload').removeClass('hidden');

	});

	dropzone_datafile.on("sending",function(file, xhr, formData) {
		var csrftoken = getCookie('csrftoken');
		console.log("using token " + csrftoken);
		formData.append("csrfmiddlewaretoken", csrftoken);
	});

	dropzone_datafile.on("reset", function() {
		dropzone_datafile.removeAllFiles(true);
		$('#done_upload').removeClass('hidden');
	});

	dropzone_datafile.on("dragover", function(event) {
		console.log('drag over');
		$('a[href="#projectfiles"]').tab('show');
	});

	dropzone_datafile.on("success",function() {
		console.log('success');
		setTimeout(function() {
			dropzone_datafile.processQueue();
		}, 0);
	});

	dropzone_datafile.on("queuecomplete",function() {
		$('#done_upload').removeClass('hidden');
	});

	dropzone_datafile.on("uploadprogress",function(file,uploadProgress) {
		if(uploadProgress >= 100) {
			replaceSizeMessage(file,'Processing...');
		}
	});

	dropzone_datafile.on("complete",function(file,uploadProgress) {
		if(file.status === Dropzone.ERROR) {
			replaceSizeMessage(file,'Error');
		} else {
			replaceSizeMessage(file,'Done');
		}
	});

	$('#upload_files').on('click',function() {
		dropzone_datafile.processQueue();
	});

	$('#cancel_upload').on('click',function() {
		dropzone_datafile.removeAllFiles(true);
	});

	$('#done_upload').on('click',function() {
		dropzone_datafile.removeAllFiles(true);
		$('#upload_files').addClass('hidden');
		$('#cancel_upload').addClass('hidden');
		$('#done_upload').addClass('hidden');
	});


});