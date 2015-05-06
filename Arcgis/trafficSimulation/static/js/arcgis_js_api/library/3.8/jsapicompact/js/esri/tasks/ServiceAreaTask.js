/*
 COPYRIGHT 2009 ESRI

 TRADE SECRETS: ESRI PROPRIETARY AND CONFIDENTIAL
 Unpublished material - all rights reserved under the
 Copyright Laws of the United States and applicable international
 laws, treaties, and conventions.

 For additional information, contact:
 Environmental Systems Research Institute, Inc.
 Attn: Contracts and Legal Services Department
 380 New York Street
 Redlands, California, 92373
 USA

 email: contracts@esri.com
 */
//>>built
define("esri/tasks/ServiceAreaTask","dojo/_base/declare dojo/_base/lang dojo/has esri/kernel esri/request esri/geometry/normalizeUtils esri/tasks/Task esri/tasks/ServiceAreaSolveResult".split(" "),function(a,b,f,g,l,m,n,p){a=a(n,{declaredClass:"esri.tasks.ServiceAreaTask",_eventMap:{"solve-complete":["result"]},constructor:function(k){this._url.path+="/solveServiceArea";this._handler=b.hitch(this,this._handler);this.registerConnectEvents()},__msigns:[{n:"solve",c:3,a:[{i:0,p:["facilities.features",
"pointBarriers.features","polylineBarriers.features","polygonBarriers.features"]}],e:2}],_handler:function(k,a,e,c,d){try{var b=new p(k);this._successHandler([b],"onSolveComplete",e,d)}catch(h){this._errorHandler(h,c,d)}},solve:function(a,f,e,c){var d=c.assembly;a=this._encode(b.mixin({},this._url.query,{f:"json"},a.toJson(d&&d[0])));var g=this._handler,h=this._errorHandler;return l({url:this._url.path,content:a,callbackParamName:"callback",load:function(a,b){g(a,b,f,e,c.dfd)},error:function(a){h(a,
e,c.dfd)}})},onSolveComplete:function(){}});m._createWrappers(a);f("extend-esri")&&b.setObject("tasks.ServiceAreaTask",a,g);return a});