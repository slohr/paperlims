
$(document).ready(function () {

	$('body').on('dragenter',function() {
		if(object.record_status !== 'locked' && (typeof variable === 'undefined' || readonly)) {
			$('#file_upload').removeClass('hidden');
		} else {
			$.notify({
				message: 'File upload has been disabled.'
			},{
				type: 'danger'
			});
		}
	});

	$('#add_files').on('click',function() {
		if(object.record_status !== 'locked' && (typeof variable === 'undefined' || readonly)) {
			$('#file_upload').removeClass('hidden');
		} else {
			$.notify({
				message: 'File upload has been disabled.'
			},{
				type: 'danger'
			});
		}
	});

    var list_loader = new CoreSlick.Data.RemoteModel({
        geturl:Urls.datafiles_json()
    });

    var grid;

    var columns = [
        {
            id: "id",
            name: "ID",
            field: "id",
            width: 120,
            cssClass: "cell-title"
        },

        {
            id: "name",
            name: "Name",
            field: "name",
            width: 120,
            cssClass: "cell-title"
        },
        {
            id: "date_created",
            name: "Date Created",
            field: "date_created",
            width: 120,
            cssClass: "cell-title"
        },

        {
            id: "description",
            name: "Description",
            field: "description",
            width: 100
        }
    ];

    var grid_options = {
        editable: false,
        enableAddRow: false,
        enableCellNavigation: true,
        asyncEditorLoading: false,
        autoEdit: false,
        forceFitColumns: true,
        multiSelect:true
    };
    var loadingIndicator = null;


    var ttp = [];
    grid = new Slick.Grid("#myGrid", list_loader.data, columns, grid_options);
    $("#myGrid").data('slickgrid', grid);
    grid.onViewportChanged.subscribe(function (e, args) {
        var vp = grid.getViewport();
        list_loader.fetchData(vp.top, vp.bottom);
    });

    var rowSelection = new Slick.RowSelectionModel();

    var recordActionView = $('#recordActionView');
    var recordActionDelete = $('#recordActionDelete');

    grid.setSelectionModel(rowSelection);

    var gridToolbar = new CoreSlick.GridToolbar("#mygridtoolbar");

    gridToolbar.onViewPressed.subscribe(function(e,args) {
        console.log("view pressed");
        var selectedRows = grid.getSelectedRows();
        var row = grid.getDataItem(selectedRows[0]);
        location.href = Urls.datafiles_detail(row.id);

        console.log(selectedRows);
    });

    gridToolbar.onDeletePressed.subscribe(function(e,args) {
        console.log("delete pressed");
        var selectedRows = grid.getSelectedRows();
        console.log(selectedRows);
    });

    grid.registerPlugin(gridToolbar);

    grid.onDblClick.subscribe(function(e,args) {
        console.log(args);
        var row = grid.getDataItem(args.row);
        location.href = Urls.datafiles_detail(row.id);
    });

    grid.onCellChange.subscribe(function (e, args) {
        var column = args.grid.getColumns()[args.cell]

        if(column.hasOwnProperty('saveOnEdit') & column.saveOnEdit) {
            console.log("doing update");
        }
    });

    list_loader.onDataLoading.subscribe(function () {
        if (!loadingIndicator) {
            loadingIndicator = $("<span class='loading-indicator'><label>Loading...</label></span>").appendTo(document.body);
            var $g = $("#myGrid");
            loadingIndicator
                    .css("position", "absolute")
                    .css("top", $g.position().top + $g.height() / 2 - loadingIndicator.height() / 2)
                    .css("left", $g.position().left + $g.width() / 2 - loadingIndicator.width() / 2);
        }
        loadingIndicator.show();
    });

    list_loader.onDataLoaded.subscribe(function (e, args) {
        console.log("inside onDataLoaded subscription");
        for (var i = args.from; i <= args.to; i++) {
            grid.invalidateRow(i);
        }
        grid.updateRowCount();
        grid.render();
        loadingIndicator.fadeOut();

        if (!args.hasData) {
            grid.invalidateAllRows();
            var nodataIndicator = $('<div class="nodata-indicator">No Data</div>');
            $('.grid-canvas').replaceWith(nodataIndicator);
        }
    });

    grid.onViewportChanged.notify();

	replaceSizeMessage = function(file,message) {
		_ref1 = file.previewElement.querySelectorAll("[data-dz-size]");
		for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
			node = _ref1[_j];
			node.innerHTML = message;
		}
	};

	var dropzone_datafile = new Dropzone('div#to_be_uploaded_datafile',{
		url: Urls.datafiles_upload(),
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
		var csrftoken = Cookies.get('csrftoken');

		console.log("using token " + csrftoken);
		formData.append("csrfmiddlewaretoken", csrftoken);
		formData.append("content_type",$("#contentType").val());
		formData.append("project_id",$("#projectId").val());
	});

	dropzone_datafile.on("reset", function() {
		dropzone_datafile.removeAllFiles(true);
		$('#done_upload').removeClass('hidden');
	});

	dropzone_datafile.on("success",function() {
		console.log('success');
		setTimeout(function() {
			dropzone_datafile.processQueue();
		}, 0);
	});

	dropzone_datafile.on("queuecomplete",function() {
		$('#done_upload').removeClass('hidden');
        list_loader.clear();
        list_loader.fetchData(1,10);
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
		$('#file_upload').addClass('hidden');
		$('#add_files').removeClass('hidden');
	});


});