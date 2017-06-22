(function ($) {

  function RemoteModel(options) {
    // private
    var PAGESIZE = 50;
    var data = [];
    var searchstr = "";
    var sortcol = null;
    var sortdir = 1;
    var h_request = null;
    var req = null; // ajax request
    var geturl = null;
    var posturl = null;

    // events
    var onDataLoading = new Slick.Event();
    var onDataLoaded = new Slick.Event();


    function init() {
        if(options!==undefined) {
            if(options.geturl!==undefined) {
                geturl = options.geturl;
            } else {
                throw new Error("RemoteModel requires at least 'geturl' to be specified.");
            }
            url = options.url;
        } else {
            throw new Error("RemoteModel options are required.");
        }
    }


    function isDataLoaded(from, to) {
      for (var i = from; i <= to; i++) {
        if (data[i] == undefined || data[i] == null) {
          return false;
        }
      }

      return true;
    }


    function clear() {
      for (var key in data) {
        delete data[key];
      }
      data.length = 0;
    }


    function fetchData(from, to) {
      if (req) {
        req.abort();
        for (var i = req.fromPage; i <= req.toPage; i++)
          data[i * PAGESIZE] = undefined;
      }

      if (from < 0) {
        from = 0;
      }

      if (data.length > 0) {
        to = Math.min(to, data.length - 1);
      }

      var fromPage = Math.floor(from / PAGESIZE);
      var toPage = Math.floor(to / PAGESIZE);

      while (data[fromPage * PAGESIZE] !== undefined && fromPage < toPage)
        fromPage++;

      while (data[toPage * PAGESIZE] !== undefined && fromPage < toPage)
        toPage--;


      if (fromPage > toPage || ((fromPage == toPage) && data[fromPage * PAGESIZE] !== undefined)) {
        // TODO:  look-ahead
        onDataLoaded.notify({from: from, to: to});
        return;
      }

      if (sortcol != null) {
        geturl += ("&sortby=" + sortcol + ((sortdir > 0) ? "+asc" : "+desc"));
      }

      if (h_request != null) {
        clearTimeout(h_request);
      }

      h_request = setTimeout(function () {
        for (var i = fromPage; i <= toPage; i++)
          data[i * PAGESIZE] = null; // null indicates a 'requested but not available yet'

        onDataLoading.notify({from: from, to: to});

        req = $.ajax({
          url: geturl,
          cache: true,
          success: onSuccess,
          error: function () {
            onError(fromPage, toPage)
          }
        });
        req.fromPage = fromPage;
        req.toPage = toPage;
      }, 50);
    }


    function onError(fromPage, toPage) {
      alert("error loading pages " + fromPage + " to " + toPage);
    }

    function onSuccess(resp) {
      var from = resp.start
      var to = from + resp.data.length;

      //data.length = Math.min(parseInt(resp.data),1000); // limitation of the API


      for (var i = 0; i < resp.data.length; i++) {
        var item = resp.data[i];

        data[from + i - 1] = item;
        data[from + i - 1].index = from + i;
      }
      data.length = resp.data.length;

      req = null;

      var hasData = data.length > 0 ? true : false;
      onDataLoaded.notify({from: from, to: to, hasData: hasData});
    }


    function reloadData(from, to) {
      for (var i = from; i <= to; i++)
        delete data[i];

      fetchData(from, to);
    }


    function setSort(column, dir) {
      sortcol = column;
      sortdir = dir;
      clear();
    }

    function setSearch(str) {
      searchstr = str;
      clear();
    }


    init();

    return {
      // properties
      "data": data,
      "options": options,

      // methods
      "clear": clear,
      "isDataLoaded": isDataLoaded,
      "fetchData": fetchData,
      "reloadData": reloadData,
      "setSort": setSort,
      "setSearch": setSearch,

      // events
      "onDataLoading": onDataLoading,
      "onDataLoaded": onDataLoaded
    };
  }

  // Slick.Data.RemoteModel
  $.extend(true, window, {
    "CoreSlick": {
        "Data": {
            "RemoteModel": RemoteModel
        }
    }
  });
})(jQuery);