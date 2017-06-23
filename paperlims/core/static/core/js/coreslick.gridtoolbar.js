(function ($) {
  // register namespace
  $.extend(true, window, {
    "CoreSlick": {
      "GridToolbar": GridToolbar
    }
  });


  function GridToolbar(container,options) {
    var _grid;
    var _self = this;
    var _handler = new Slick.EventHandler();
    var _defaults = {
      dynamic: true,
      cssClass: null,
      elementId: "gridtoolbar"
    };
    var $container;
    var uid = "slickgridtoolbar_" + Math.round(1000000 * Math.random());
    var $recordActionView;

    var _options = $.extend(true, {}, _defaults, options);

    function init(grid) {
      if (container instanceof jQuery) {
        $container = container;
      } else {
        $container = $(container);

      }

        console.log(_options);
      if ($container.length < 1) {
        throw new Error("SlickGrid Toolbar requires a valid container, " + container + " does not exist in the DOM.");
      }

      $container
          .empty()
          .addClass(uid)
          .addClass("ui-widget");

        $buttonGroup = $('<div>').addClass('btn-group').appendTo($container);
        $recordActionView = $('<a>').appendTo($buttonGroup);
        $recordActionDelete = $('<a>').appendTo($buttonGroup);

      $recordActionView
        .on('click',function(){
            onViewPressed.notify();
        })
        .addClass("btn btn-default").text('View');

      $recordActionDelete
        .on('click',function(){
            onDeletePressed.notify();
        })
        .addClass("btn btn-default").text('Delete');

      if(_options.dynamic) {
        $recordActionView.css("display", "none");
        $recordActionDelete.css("display", "none");
      }

      _grid = grid;
      _handler
        .subscribe(_grid.onSelectedRowsChanged, handleSelectedRowsChanged)
        .subscribe(_grid.onClick, handleClick)
        .subscribe(_grid.onDblClick, handleDblClick);
    }

    function destroy() {
      _handler.unsubscribeAll();
    }

    // events
    var onViewPressed = new Slick.Event();
    var onDeletePressed = new Slick.Event();

    function handleSelectedRowsChanged(e, args) {
        var selectedRows = _grid.getSelectedRows();
        if(_options.dynamic) {
            if(selectedRows.length===0) {
                $recordActionView.hide();
                $recordActionDelete.hide();
            } else {
                $recordActionDelete.show();
                if(selectedRows.length===1) {
                    $recordActionView.show();
                } else {
                    $recordActionView.hide();
                }
            }
        }
    }

    function handleClick(e, args) {
        console.log("handling click in toolbar plugin");
        console.log(args);
    }

    function handleDblClick(e, args) {
        console.log("handling double click in toolbar plugin");
        console.log(args);
    }

    $.extend(this, {
      "init": init,
      "destroy": destroy,
      "onViewPressed": onViewPressed,
      "onDeletePressed": onDeletePressed
    });
  }
})(jQuery);