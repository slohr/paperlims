
    function requiredFieldValidator(value) {
        if (value == null || value == undefined || !value.length) {
          return {valid: false, msg: "This is a required field"};
        } else {
          return {valid: true, msg: null};
        }
    }
    var grid;
    var data = [];
    var columns = [
        {id: "project", name: "Project", field: "project", width: 120, cssClass: "cell-title", editor: Slick.Editors.Text, validator: requiredFieldValidator},
        {id: "desc", name: "Description", field: "description", width: 100, editor: Slick.Editors.LongText}
    ];

    var options = {
        editable: true,
        enableAddRow: true,
        enableCellNavigation: true,
        asyncEditorLoading: false,
        autoEdit: false,
        forceFitColumns: true
    };

    $(function () {
        for (var i = 0; i < 500; i++) {
          var d = (data[i] = {});
          d["project"] = "Project " + i;
          d["description"] = "This is a description.\n  It can be multiline";
        }
        grid = new Slick.Grid("#myGrid", data, columns, options);
        grid.setSelectionModel(new Slick.CellSelectionModel());
        grid.onAddNewRow.subscribe(function (e, args) {
          var item = args.item;
          grid.invalidateRow(data.length);
          data.push(item);
          grid.updateRowCount();
          grid.render();
        });
        grid.onCellChange.subscribe(function (e, args) {
         //({ row: number, cell: number, item: any })
            console.log(args);
         });
    })
