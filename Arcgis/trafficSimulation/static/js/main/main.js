


/***************************************************
****************** dojo导入模块 ********************
***************************************************/
//dojo
dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.layout.AccordionContainer");
dojo.require("dijit.layout.AccordionPane");
dojo.require("dijit.Toolbar");
dojo.require("dijit.form.Button");
dojo.require("dijit.form.DropDownButton");
dojo.require("dijit.Menu");
dojo.require("dijit.MenuItem");
//map
dojo.require("esri.map");
dojo.require("esri.dijit.HomeButton");

/***************************************************
****************** 声明全局变量 ********************
***************************************************/
var REFRESH_FREQUENCY;
var HEART_BEAT;
var map, routeTask, routeParams, routes = [];
var stopSymbol, barrierSymbol, routeSymbol;
var mapOnClick_addStops_connect;
var mapOnClick_addBarriers_connect;
var mapOnMouseMove_showCoordinate_connect;
var mapOnMouseDrag_showCoordinate_connect;
var wkid = 3857; //坐标系
//定义初始范围
var startExtent = new esri.geometry.Extent({
    "xmin": 9742886.90336549,
    "ymin": 5468988.56793551,
    "xmax": 9754958.5420921,
    "ymax": 5479290.80208165,
    "spatialReference": {"wkid": wkid}
});




alert(1);
