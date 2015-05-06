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
require({cache:{"url:esri/dijit/analysis/templates/FindHotSpots.html":'\x3cdiv class\x3d"esriAnalysis"\x3e\n  \x3cdiv data-dojo-type\x3d"dijit/layout/ContentPane" style\x3d"margin-top:0.5em; margin-bottom: 0.5em;"\x3e\n    \x3cdiv data-dojo-attach-point\x3d"_hotspotsToolContentTitle" class\x3d"analysisTitle"\x3e\n         \x3ctable class\x3d"esriFormTable" \x3e \n            \x3ctr\x3e\n              \x3ctd class\x3d"esriToolIconTd"\x3e\x3cdiv class\x3d"findHotSpotsIcon"\x3e\x3c/div\x3e\x3c/td\x3e\n              \x3ctd class\x3d"esriAlignLeading"\x3e${i18n.findHotSpots}\x3c/td\x3e\n              \x3ctd\x3e\n                \x3cdiv class\x3d"esriFloatTrailing" style\x3d"padding:0;"\x3e\n                    \x3cdiv class\x3d"esriFloatLeading"\x3e\n                      \x3ca href\x3d"#" class\x3d\'esriFloatLeading helpIcon\' esriHelpTopic\x3d"toolDescription"\x3e\x3c/a\x3e\n                    \x3c/div\x3e\n                    \x3cdiv class\x3d"esriFloatTrailing"\x3e\n                      \x3ca href\x3d"#" data-dojo-attach-point\x3d"_closeBtn" title\x3d"${i18n.close}" class\x3d"esriAnalysisCloseIcon"\x3e\x3c/a\x3e\n                    \x3c/div\x3e              \n                \x3c/div\x3e  \n              \x3c/td\x3e\n            \x3c/tr\x3e\n         \x3c/table\x3e\n    \x3c/div\x3e\n    \x3cdiv style\x3d"clear:both; border-bottom: #333 thin solid; height:1px;width:100%;"\x3e\x3c/div\x3e\n  \x3c/div\x3e\n  \x3cdiv data-dojo-type\x3d"dijit/form/Form" data-dojo-attach-point\x3d"_form" readOnly\x3d"true"\x3e\n     \x3ctable class\x3d"esriFormTable"  data-dojo-attach-point\x3d"_hotspotsTable"\x3e \n       \x3ctbody\x3e\n        \x3ctr\x3e\n          \x3ctd  colspan\x3d"3" class\x3d"sectionHeader" data-dojo-attach-point\x3d"_hotspotsToolDescription" \x3e\x3c/td\x3e\n        \x3c/tr\x3e\n        \x3c!--\x3ctr data-dojo-attach-point\x3d"_pointFieldTd"\x3e\n           \x3ctd colspan\x3d"3"\x3e\n             \x3clabel class\x3d"esriFloatLeading esriTrailingMargin025"\x3e${i18n.oneLabel}\x3c/label\x3e\n             \x3clabel class\x3d""\x3e${i18n.chooseAttributeLabel}\x3c/label\x3e\n           \x3c/td\x3e\n        \x3c/tr\x3e--\x3e\n        \x3ctr\x3e\n          \x3ctd colspan\x3d"2"\x3e\n            \x3clabel data-dojo-attach-point\x3d"_labelOne" class\x3d"esriFloatLeading esriTrailingMargin025"\x3e${i18n.oneLabel}\x3c/label\x3e\n            \x3clabel data-dojo-attach-point\x3d"_polylabel" class\x3d""\x3e${i18n.chooseAttributeLabel}\x3c/label\x3e\n            \x3cselect class\x3d"longTextInput"  style\x3d"margin-top:10px;" data-dojo-type\x3d"dijit/form/Select" data-dojo-attach-point\x3d"_analysFieldSelect" data-dojo-attach-event\x3d"onChange:_handleFieldChange"\x3e\x3c/select\x3e\n          \x3c/td\x3e\n          \x3ctd class\x3d"shortTextInput"\x3e\n            \x3ca href\x3d"#" class\x3d\'esriFloatTrailing helpIcon\' data-dojo-attach-point\x3d"_analysisFieldHelpLink" esriHelpTopic\x3d"AnalysisFieldPoly"\x3e\x3c/a\x3e \n          \x3c/td\x3e \n        \x3c/tr\x3e\n        \x3ctr data-dojo-attach-point\x3d"_optionsRow"\x3e\n          \x3ctd colspan\x3d"3"\x3e\n            \x3cdiv class\x3d"optionsClose" style\x3d"width:99%" data-dojo-attach-point\x3d"_optionsDiv"\x3e\n              \x3cdiv class\x3d"dijitTreeExpando" data-dojo-attach-event\x3d"onclick:_handleOptionsBtnClick"\x3e\x3clabel class\x3d"esriLeadingMargin2 noWrapLabel"\x3e${i18n.Options}\x3c/label\x3e\x3c/div\x3e\n              \x3ctable class\x3d"esriFormTable optionsTable"\x3e\n                \x3ctbody\x3e\n                  \x3ctr\x3e\n                    \x3ctd colspan\x3d"2"\x3e\n                        \x3clabel class\x3d"longTextInput"\x3e${i18n.defineBoundingLabel}\x3c/label\x3e\n                    \x3c/td\x3e                    \n                  \x3c/tr\x3e\n                  \x3ctr\x3e\n                    \x3ctd style\x3d"width:95%"\x3e\n                      \x3cselect class\x3d"longTextInput esriMediumlabel2"  style\x3d"width:100%;table-layout:fixed;" data-dojo-type\x3d"dijit/form/Select" data-dojo-attach-point\x3d"_boundingAreaSelect" data-dojo-attach-event\x3d"onChange:_handleBoundingSelectChange"\x3e\x3c/select\x3e                      \n                    \x3c/td\x3e\n                    \x3ctd style\x3d"width:8%"\x3e\n                      \x3cbutton data-dojo-type\x3d"dijit/form/ToggleButton" class\x3d"esriboundingButton" data-dojo-props\x3d"showLabel:false,iconClass:\'toolbarIcon polygonIcon\',style:\'width:16px;\'" data-dojo-attach-event\x3d"onClick:_handleBoundingBtnClick"\x3e\x3c/button\x3e\n                    \x3c/td\x3e \n                    \x3ctd class\x3d"shortTextInput"\x3e\n                       \x3ca href\x3d"#" class\x3d\'esriFloatTrailing helpIcon\' esriHelpTopic\x3d"BoundingPolygonLayer"\x3e\x3c/a\x3e \n                    \x3c/td\x3e \n                   \n                  \x3c/tr\x3e      \n                  \x3ctr\x3e\n                    \x3ctd colspan\x3d"2"\x3e\n                        \x3clabel class\x3d"longTextInput"\x3e${i18n.provideAggLabel}\x3c/label\x3e\n                    \x3c/td\x3e                    \n                  \x3c/tr\x3e\n                  \x3ctr\x3e\n                    \x3ctd colspan\x3d"2"\x3e\n                        \x3cselect class\x3d"longTextInput"  data-dojo-type\x3d"dijit/form/Select" data-dojo-attach-point\x3d"_aggAreaSelect" data-dojo-attach-event\x3d"onChange:_handleAggAreaSelectChange"\x3e\x3c/select\x3e\n                    \x3c/td\x3e   \n                    \x3ctd class\x3d"shortTextInput"\x3e\n                      \x3ca href\x3d"#" class\x3d\'esriFloatTrailing helpIcon\' esriHelpTopic\x3d"AggregationPolygonLayer"\x3e\x3c/a\x3e \n                    \x3c/td\x3e \n                 \n                  \x3c/tr\x3e                               \n                \x3c/tbody\x3e\n              \x3c/table\x3e\n            \x3c/div\x3e\n          \x3c/td\x3e\n        \x3c/tr\x3e\n        \x3ctr\x3e\n          \x3ctd colspan\x3d"2"\x3e\n            \x3clabel class\x3d"esriFloatLeading esriTrailingMargin025"\x3e${i18n.twoLabel}\x3c/label\x3e\n            \x3clabel class\x3d"longTextInput"\x3e${i18n.outputLayerLabel}\x3c/label\x3e\n          \x3c/td\x3e\n          \x3ctd class\x3d"shortTextInput"\x3e\n            \x3ca href\x3d"#" class\x3d\'esriFloatTrailing helpIcon\' esriHelpTopic\x3d"OutputLayerName"\x3e\x3c/a\x3e \n          \x3c/td\x3e             \n        \x3c/tr\x3e\n        \x3ctr\x3e\n          \x3ctd colspan\x3d"3"\x3e\n            \x3cinput type\x3d"text" data-dojo-type\x3d"dijit/form/ValidationTextBox" data-dojo-props\x3d"required:true" class\x3d"longTextInput esriLeadingMargin05" data-dojo-attach-point\x3d"_outputLayerInput" value\x3d"${i18n.hotspots}"\x3e\x3c/input\x3e\n          \x3c/td\x3e                \n        \x3c/tr\x3e\n        \x3ctr\x3e\n          \x3ctd colspan\x3d"3"\x3e\n             \x3cdiv data-dojo-attach-point\x3d"_chooseFolderRow"\x3e\n               \x3clabel style\x3d"width:9px;font-size:smaller;"\x3e${i18n.saveResultIn}\x3c/label\x3e\n               \x3cinput class\x3d"longInput" dojoAttachPoint\x3d"_webMapFolderSelect" dojotype\x3d"dijit/form/ComboBox" trim\x3d"true" style\x3d"width:60%;height:auto"\x3e\x3c/input\x3e\n             \x3c/div\x3e              \n          \x3c/td\x3e\n        \x3c/tr\x3e                                              \n      \x3c/tbody\x3e         \n     \x3c/table\x3e\n   \x3c/div\x3e\n  \x3cdiv style\x3d"padding:5px;margin-top:5px;border-top:solid 1px #BBB;"\x3e\n    \x3cdiv style\x3d"width:100%;padding:0.5em 0 0.5em 0"\x3e\n      \x3ca class\x3d"esriFloatTrailing esriSmallFont"  href\x3d"#" data-dojo-attach-point\x3d"_showCreditsLink" data-dojo-attach-event\x3d"onclick:_handleShowCreditsClick"\x3e${i18n.showCredits}\x3c/a\x3e\n     \x3clabel data-dojo-attach-point\x3d"_chooseExtentDiv"class\x3d"esriSelectLabel" style\x3d"font-size:smaller;"\x3e\n       \x3cinput type\x3d"radio" data-dojo-attach-point\x3d"_useExtentCheck" data-dojo-type\x3d"dijit/form/CheckBox" data-dojo-props\x3d"checked:true" name\x3d"extent" value\x3d"true"/\x3e\n         ${i18n.useMapExtent}\n     \x3c/label\x3e\n    \x3c/div\x3e\n    \x3cbutton data-dojo-type\x3d"dijit/form/Button" type\x3d"submit" data-dojo-attach-point\x3d"_saveBtn" class\x3d"esriLeadingMargin4 esriAnalysisSubmitButton" data-dojo-attach-event\x3d"onClick:_handleSaveBtnClick"\x3e\n        ${i18n.runAnalysis}\n    \x3c/button\x3e\n  \x3c/div\x3e\n  \x3cdiv data-dojo-type\x3d"dijit/Dialog" title\x3d"${i18n.creditTitle}" data-dojo-attach-point\x3d"_usageDialog" style\x3d"width:40em;"\x3e\n    \x3cdiv data-dojo-type\x3d"esri/dijit/analysis/CreditEstimator"  data-dojo-attach-point\x3d"_usageForm"\x3e\x3c/div\x3e\n  \x3c/div\x3e    \n\x3c/div\x3e\n'}});
define("esri/dijit/analysis/FindHotSpots","require dojo/_base/declare dojo/_base/lang dojo/_base/array dojo/_base/connect dojo/_base/Color dojo/_base/json dojo/has dojo/i18n dojo/json dojo/string dojo/dom-style dojo/dom-attr dojo/dom-construct dojo/query dojo/dom-class dijit/_WidgetBase dijit/_TemplatedMixin dijit/_WidgetsInTemplateMixin dijit/_OnDijitClickMixin dijit/_FocusMixin dijit/registry dijit/form/Button dijit/form/CheckBox dijit/form/Form dijit/form/Select dijit/form/TextBox dijit/form/ToggleButton dijit/form/ValidationTextBox dijit/layout/ContentPane dijit/form/ComboBox dijit/Dialog esri/kernel esri/lang esri/dijit/analysis/AnalysisBase esri/toolbars/draw esri/dijit/PopupTemplate esri/layers/FeatureLayer esri/map esri/dijit/analysis/utils esri/dijit/analysis/CreditEstimator dojo/text!esri/dijit/analysis/templates/FindHotSpots.html".split(" "),
function(m,r,f,h,n,s,e,t,u,G,g,l,p,H,I,d,v,w,x,y,z,J,K,L,M,N,O,P,Q,R,S,T,A,B,C,q,D,E,U,k,V,F){m=r([v,w,x,y,z,C],{declaredClass:"esri.dijit.analysis.FindHotSpots",templateString:F,basePath:m.toUrl("esri/dijit/analysis"),widgetsInTemplate:!0,analysisLayer:null,analysisField:null,aggregationPolygonLayer:null,boundingPolygonLayer:null,outputLayerName:null,showSelectFolder:!1,showChooseExtent:!0,showHelp:!0,returnFeatureCollection:!1,showCredits:!0,isProcessInfo:!0,i18n:null,map:null,toolName:"FindHotSpots",
helpFileName:"FindHotSpots",resultParameter:"HotSpotsResultLayer",constructor:function(a,b){this._pbConnects=[];a.containerNode&&(this.container=a.containerNode)},destroy:function(){this.inherited(arguments);h.forEach(this._pbConnects,n.disconnect);delete this._pbConnects},postMixInProperties:function(){this.inherited(arguments);f.mixin(this.i18n,u.getLocalization("esri","jsapi").findHotSpotsTool);this.set("drawLayerName",this.i18n.blayerName)},postCreate:function(){this.inherited(arguments);d.add(this._form.domNode,
"esriSimpleForm");this._outputLayerInput.set("validator",f.hitch(this,this.validateServiceName));this._buildUI()},startup:function(){},_onClose:function(a){a&&this._featureLayer&&(this.map.removeLayer(this._featureLayer),h.forEach(this.boundingPolygonLayers,function(a,c){a===this._featureLayer&&(this._boundingAreaSelect.removeOption({value:c+1,label:this._featureLayer.name}),this.boundingPolygonLayers.splice(c,1))},this));this._toolbar.deactivate();this.emit("close",{save:!a})},_handleShowCreditsClick:function(a){a.preventDefault();
a={};var b;this._form.validate()&&(a.AnalysisLayer=e.toJson(k.constructAnalysisInputLyrObj(this.analysisLayer)),"0"!==this._analysFieldSelect.get("value")&&(a.AnalysisField=this._analysFieldSelect.get("value")),this._isPoint&&"0"===this._analysFieldSelect.get("value")&&("-1"!==this._boundingAreaSelect.get("value")&&(b=this.boundingPolygonLayers[this._boundingAreaSelect.get("value")-1],a.BoundingPolygonLayer=e.toJson(k.constructAnalysisInputLyrObj(b))),"-1"!==this._aggAreaSelect.get("value")&&(b=this.aggregationPolygonLayers[this._aggAreaSelect.get("value")-
1],a.AggregationPolygonLayer=e.toJson(k.constructAnalysisInputLyrObj(b)))),this.returnFeatureCollection||(a.OutputName=e.toJson({serviceProperties:{name:this._outputLayerInput.get("value")}})),this.showChooseExtent&&!this.get("DisableExtent")&&this._useExtentCheck.get("checked")&&(a.Context=e.toJson({extent:this.map.extent._normalize(!0)})),this.getCreditsEstimate(this.toolName,a).then(f.hitch(this,function(a){this._usageForm.set("content",a);this._usageDialog.show()})))},_handleSaveBtnClick:function(a){if(this._form.validate()){this._saveBtn.set("disabled",
!0);a={};var b={},c;a.AnalysisLayer=e.toJson(k.constructAnalysisInputLyrObj(this.analysisLayer));"0"!==this._analysFieldSelect.get("value")&&(a.AnalysisField=this._analysFieldSelect.get("value"));this._isPoint&&"0"===this._analysFieldSelect.get("value")&&("-1"!==this._boundingAreaSelect.get("value")&&(c=this.boundingPolygonLayers[this._boundingAreaSelect.get("value")-1],a.BoundingPolygonLayer=e.toJson(k.constructAnalysisInputLyrObj(c))),"-1"!==this._aggAreaSelect.get("value")&&(c=this.aggregationPolygonLayers[this._aggAreaSelect.get("value")-
1],a.AggregationPolygonLayer=e.toJson(k.constructAnalysisInputLyrObj(c))));this.returnFeatureCollection||(a.OutputName=e.toJson({serviceProperties:{name:this._outputLayerInput.get("value")}}));this.showChooseExtent&&!this.get("DisableExtent")&&this._useExtentCheck.get("checked")&&(a.Context=e.toJson({extent:this.map.extent._normalize(!0)}));this.returnFeatureCollection&&(c={outSR:this.map.spatialReference},this.showChooseExtent&&(c.extent=this.map.extent._normalize(!0)),a.context=e.toJson(c));a.isProcessInfo=
this.isProcessInfo;b.jobParams=a;b.itemParams={description:this.i18n.itemDescription,tags:g.substitute(this.i18n.itemTags,{layername:this.analysisLayer.name,fieldname:!a.AnalysisField?"":a.AnalysisField}),snippet:this.i18n.itemSnippet};this.showSelectFolder&&(b.itemParams.folder=this._webMapFolderSelect.item?this.folderStore.getValue(this._webMapFolderSelect.item,"id"):"");this.execute(b)}},_save:function(){},_buildUI:function(){this._loadConnections();this.signInPromise.then(f.hitch(this,k.initHelpLinks,
this.domNode,this.showHelp,{analysisGpServer:this.analysisGpServer}));if(this.analysisLayer){if("esriGeometryPolygon"===this.analysisLayer.geometryType)this._isPoint=!1,p.set(this._hotspotsToolDescription,"innerHTML",g.substitute(this.i18n.hotspotsPolyDefine,{layername:this.analysisLayer.name})),l.set(this._optionsRow,"display","none"),p.set(this._analysisFieldHelpLink,"esriHelpTopic","AnalysisFieldPoly");else if("esriGeometryPoint"===this.analysisLayer.geometryType||"esriGeometryMultipoint"===this.analysisLayer.geometryType)this._isPoint=
!0,p.set(this._hotspotsToolDescription,"innerHTML",g.substitute(this.i18n.hotspotsPointDefine,{layername:this.analysisLayer.name})),d.add(this._analysFieldSelect.domNode,"esriLeadingMargin1"),l.set(this._optionsRow,"display",""),p.set(this._analysisFieldHelpLink,"esriHelpTopic","AnalysisFieldPoint"),this._outputLayerInput.set("value",g.substitute(this.i18n.outputLayerName,{layername:this.analysisLayer.name}));this.set("AnalyisFields",this.analysisLayer);"esriGeometryPolygon"===this.analysisLayer.geometryType&&
this._outputLayerInput.set("value",g.substitute(this.i18n.outputLayerName,{layername:this._analysFieldSelect.getOptions(0).label}))}this.outputLayerName&&this._outputLayerInput.set("value",this.outputLayerName);this.boundingPolygonLayers&&(this._boundingAreaSelect.addOption({value:"-1",label:this.i18n.defaultBoundingOption,selected:!0}),h.forEach(this.boundingPolygonLayers,function(a,b){"esriGeometryPolygon"===a.geometryType&&this._boundingAreaSelect.addOption({value:b+1,label:a.name,selected:!1})},
this));this.aggregationPolygonLayers&&(this._aggAreaSelect.addOption({value:"-1",label:this.i18n.defaultAggregationOption,selected:!0}),h.forEach(this.aggregationPolygonLayers,function(a,b){"esriGeometryPolygon"===a.geometryType&&this._aggAreaSelect.addOption({value:b+1,label:a.name,selected:!1})},this));l.set(this._chooseFolderRow,"display",!0===this.showSelectFolder?"block":"none");this.showSelectFolder&&this.getFolderStore().then(f.hitch(this,function(a){this.folderStore=a;this._webMapFolderSelect.set("store",
a);this._webMapFolderSelect.set("value",this.portalUser.username)}));l.set(this._chooseExtentDiv,"display",!0===this.showChooseExtent?"block":"none");l.set(this._showCreditsLink,"display",!0===this.showCredits?"block":"none")},_handleFieldChange:function(a){"0"===this._analysFieldSelect.get("value")?(this._outputLayerInput.set("value",g.substitute(this.i18n.outputLayerName,{layername:this.analysisLayer.name})),this._isPoint&&d.remove(this._optionsDiv,"disabled")):(this._outputLayerInput.set("value",
g.substitute(this.i18n.outputLayerName,{layername:this._analysFieldSelect.getOptions(a).label})),this._isPoint&&(d.add(this._optionsDiv,"disabled"),d.contains(this._optionsDiv,"optionsOpen")&&(d.remove(this._optionsDiv,"optionsOpen"),d.add(this._optionsDiv,"optionsClose"))))},_handleOptionsBtnClick:function(){d.contains(this._optionsDiv,"disabled")||(d.contains(this._optionsDiv,"optionsClose")?(d.remove(this._optionsDiv,"optionsClose"),d.add(this._optionsDiv,"optionsOpen")):d.contains(this._optionsDiv,
"optionsOpen")&&(d.remove(this._optionsDiv,"optionsOpen"),d.add(this._optionsDiv,"optionsClose")))},_handleBoundingSelectChange:function(a){this._aggAreaSelect.set("disabled","-1"!==this._boundingAreaSelect.get("value"))},_handleAggAreaSelectChange:function(a){this._boundingAreaSelect.set("disabled","-1"!==this._aggAreaSelect.get("value"));this._aggAreaSelect.get("value")},_handleBoundingBtnClick:function(a){a.preventDefault();this.emit("drawtool-activate",{});this._featureLayer||this._createBoundingPolyFeatColl();
this._toolbar.activate(q.POLYGON)},_loadConnections:function(){this.on("start",f.hitch(this,"_onClose",!1));this._connect(this._closeBtn,"onclick",f.hitch(this,"_onClose",!0))},_createBoundingPolyFeatColl:function(){var a;a={layerDefinition:null,featureSet:{features:[],geometryType:"esriGeometryPolygon"}};a.layerDefinition={currentVersion:10.11,copyrightText:"",defaultVisibility:!0,relationships:[],isDataVersioned:!1,supportsRollbackOnFailureParameter:!0,supportsStatistics:!0,supportsAdvancedQueries:!0,
geometryType:"esriGeometryPolygon",minScale:0,maxScale:0,objectIdField:"OBJECTID",templates:[],type:"Feature Layer",displayField:"TITLE",visibilityField:"VISIBLE",name:this.drawLayerName,hasAttachments:!1,typeIdField:"TYPEID",capabilities:"Query",allowGeometryUpdates:!0,htmlPopupType:"",hasM:!1,hasZ:!1,globalIdField:"",supportedQueryFormats:"JSON",hasStaticData:!1,maxRecordCount:-1,indexes:[],types:[],drawingInfo:{renderer:{type:"simple",symbol:{color:[0,0,0,255],outline:{color:[0,0,0,255],width:3,
type:"esriSLS",style:"esriSLSSolid"},type:"esriSFS",style:"esriSFSNull"},label:"",description:""},transparency:0,labelingInfo:null,fixedSymbols:!0},fields:[{alias:"OBJECTID",name:"OBJECTID",type:"esriFieldTypeOID",editable:!1},{alias:"Title",name:"TITLE",length:50,type:"esriFieldTypeString",editable:!0},{alias:"Visible",name:"VISIBLE",type:"esriFieldTypeInteger",editable:!0},{alias:"Description",name:"DESCRIPTION",length:1073741822,type:"esriFieldTypeString",editable:!0},{alias:"Type ID",name:"TYPEID",
type:"esriFieldTypeInteger",editable:!0}]};new D({title:"{title}",description:"{description}"});this._featureLayer=new E(a,{id:this.drawLayerName});this.map.addLayer(this._featureLayer);n.connect(this._featureLayer,"onClick",f.hitch(this,function(a){this.map.infoWindow.setFeatures([a.graphic])}))},_addFeatures:function(a){this.emit("drawtool-deactivate",{});this._toolbar.deactivate();var b=[],c={},d=new esri.symbol.SimpleFillSymbol(esri.symbol.SimpleFillSymbol.STYLE_NULL,new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_SOLID,
new s([0,0,0]),4));a=new esri.Graphic(a,d);this.map.graphics.add(a);c.description="blayer desc";c.title="blayer";a.setAttributes(c);b.push(a);this._featureLayer.applyEdits(b,null,null);if(0===this.boundingPolygonLayers.length||this.boundingPolygonLayers[this.boundingPolygonLayers.length-1]!==this._featureLayer)b=this.boundingPolygonLayers.push(this._featureLayer),c=this._boundingAreaSelect.getOptions(),this._boundingAreaSelect.removeOption(c),c=h.map(c,function(a){a.selected=!1;return a}),this._boundingAreaSelect.addOption({value:b,
label:this._featureLayer.name,selected:!0}),this._boundingAreaSelect.addOption(c)},_setAnalysisGpServerAttr:function(a){a&&(this.analysisGpServer=a,this.set("toolServiceUrl",this.analysisGpServer+"/"+this.toolName))},_setAnalysisLayerAttr:function(a){this.analysisLayer=a},_setAnalyisFieldsAttr:function(a){a=a.fields;var b,c;this._isPoint&&this._analysFieldSelect.addOption({value:"0",label:this.i18n.noAnalysisField});h.forEach(a,function(a,d){-1!==h.indexOf(["esriFieldTypeSmallInteger","esriFieldTypeInteger",
"esriFieldTypeSingle","esriFieldTypeDouble"],a.type)&&(b={value:a.name,label:B.isDefined(a.alias)&&""!==a.alias?a.alias:a.name},this.analysisField&&b.label===this.analysisField&&(b.selected="selected",c=a.name),this._analysFieldSelect.addOption(b))},this);c&&this._analysFieldSelect.set("value",c)},_setMapAttr:function(a){this.map=a;this._toolbar=new q(this.map);n.connect(this._toolbar,"onDrawEnd",f.hitch(this,this._addFeatures))},_getMapAttr:function(){return this.map},_setDrawLayerNameAttr:function(a){this.drawLayerName=
a},_getDrawLayerNameAttr:function(){return this._featureLayer.name},_getDrawLayerAttr:function(){return this._featureLayer},_getDrawToolbarAttr:function(){return this._toolbar},_setDisableRunAnalysisAttr:function(a){this._saveBtn.set("disabled",a)},validateServiceName:function(a){var b=/(:|&|<|>|%|#|\?|\\|\"|\/|\+)/.test(a);return 0===a.length||0===g.trim(a).length?(this._outputLayerInput.set("invalidMessage",this.i18n.requiredValue),!1):b?(this._outputLayerInput.set("invalidMessage",this.i18n.invalidServiceName),
!1):98<a.length?(this._outputLayerInput.set("invalidMessage",this.i18n.invalidServiceNameLength),!1):!0},_setShowSelectFolderAttr:function(a){this.showSelectFolder=a},_getShowSelectFolderAttr:function(){return this.showSelectFolder},_setShowChooseExtentAttr:function(a){this.showChooseExtent=a},_getShowChooseExtentAttr:function(){return this.showChooseExtent},_setShowHelpAttr:function(a){this.showHelp=a},_getShowHelpAttr:function(){return this.showHelp},_setReturnFeatureCollectionAttr:function(a){this.returnFeatureCollection=
a},_getReturnFeatureCollectionAttr:function(){return this.returnFeatureCollection},_setShowCreditsAttr:function(a){this.showCredits=a},_getShowCreditsAttr:function(){return this.showCredits},_setDisableExtentAttr:function(a){this._useExtentCheck.set("checked",!a);this._useExtentCheck.set("disabled",a)},_getDisableExtentAttr:function(){this._useExtentCheck.get("disabled")},_connect:function(a,b,c){this._pbConnects.push(n.connect(a,b,c))},onDrawToolActivate:function(){},onDrawToolDeactivate:function(){},
onSave:function(){},onClose:function(){}});t("extend-esri")&&f.setObject("dijit.analysis.FindHotSpots",m,A);return m});