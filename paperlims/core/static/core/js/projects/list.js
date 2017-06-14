
    function requiredFieldValidator(value) {
        if (value == null || value == undefined || !value.length) {
          return {valid: false, msg: "This is a required field"};
        } else {
          return {valid: true, msg: null};
        }
    }

    var list_loader = new CoreSlick.Data.RemoteModel({
        geturl:Urls.projects_json()
    });

    var grid;

    var columns = [
        {
            id: "name",
            name: "Name",
            field: "name",
            width: 120,
            cssClass: "cell-title",
            saveOnEdit: true,
            editor: Slick.Editors.Text,
            validator: requiredFieldValidator
        },
        {
            id: "description",
            name: "Description",
            field: "description",
            width: 100,
            editor: Slick.Editors.LongText
        }
    ];

    var grid_options = {
        editable: false,
        enableAddRow: false,
        enableCellNavigation: true,
        asyncEditorLoading: false,
        autoEdit: false,
        forceFitColumns: true,
        multiSelect:false
    };
    var loadingIndicator = null;
    $(function () {
        var ttp = [];
        grid = new Slick.Grid("#myGrid", list_loader.data, columns, grid_options);
        $("#myGrid").data('slickgrid', grid);
        grid.onViewportChanged.subscribe(function (e, args) {
            var vp = grid.getViewport();
            list_loader.fetchData(vp.top, vp.bottom);
        });

        var rowSelection = new Slick.RowSelectionModel();

        grid.setSelectionModel(rowSelection);

        grid.onSelectedRowsChanged.subscribe(function(e,args) {
            var selectedRows = grid.getSelectedRows();
            console.log(selectedRows);
        });

        grid.onCellChange.subscribe(function (e, args) {
         //({ row: number, cell: number, item: any })
            var column = args.grid.getColumns()[args.cell]

            //console.log(args);
            //console.log(column);
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
        });

        grid.onViewportChanged.notify();

    })
