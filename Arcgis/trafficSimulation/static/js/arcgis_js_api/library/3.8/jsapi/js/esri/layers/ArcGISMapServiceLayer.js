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
define("esri/layers/ArcGISMapServiceLayer","dojo/_base/declare dojo/_base/lang dojo/_base/array dojo/has esri/kernel esri/lang esri/request esri/SpatialReference esri/geometry/Extent esri/layers/LayerInfo".split(" "),function(b,c,k,e,l,g,m,n,h,p){b=b(null,{declaredClass:"esri.layers.ArcGISMapServiceLayer",constructor:function(a,b){this.layerInfos=[];var f=this._params={},d=this._url.query?this._url.query.token:null;d&&(f.token=d)},_load:function(){m({url:this._url.path,content:c.mixin({f:"json"},
this._params),callbackParamName:"callback",load:this._initLayer,error:this._errorHandler})},spatialReference:null,initialExtent:null,fullExtent:null,description:null,units:null,_initLayer:function(a,b){try{this._findCredential();(this.credential&&this.credential.ssl||a&&a._ssl)&&this._useSSL();this.description=a.description;this.copyright=a.copyrightText;this.spatialReference=a.spatialReference&&new n(a.spatialReference);this.initialExtent=a.initialExtent&&new h(a.initialExtent);this.fullExtent=a.fullExtent&&
new h(a.fullExtent);this.units=a.units;this.maxRecordCount=a.maxRecordCount;this.maxImageHeight=a.maxImageHeight;this.maxImageWidth=a.maxImageWidth;this.supportsDynamicLayers=a.supportsDynamicLayers;var f=this.layerInfos=[],d=a.layers,c=this._defaultVisibleLayers=[];k.forEach(d,function(a,b){f[b]=new p(a);a.defaultVisibility&&c.push(a.id)});this.visibleLayers||(this.visibleLayers=c);this.version=a.currentVersion;this.version||(this.version="capabilities"in a||"tables"in a?10:"supportedImageFormatTypes"in
a?9.31:9.3);this.capabilities=a.capabilities;g.isDefined(a.minScale)&&!this._hasMin&&this.setMinScale(a.minScale);g.isDefined(a.maxScale)&&!this._hasMax&&this.setMaxScale(a.maxScale)}catch(e){this._errorHandler(e)}}});e("extend-esri")&&c.setObject("layers.ArcGISMapServiceLayer",b,l);return b});