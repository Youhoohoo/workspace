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
define("esri/layers/LabelLayer","dojo/_base/declare dojo/_base/lang dojo/_base/connect dojo/has dojox/gfx/_base esri/kernel esri/lang esri/SpatialReference esri/graphic esri/layers/GraphicsLayer esri/layers/LabelClass esri/renderers/SimpleRenderer esri/geometry/Geometry esri/geometry/Extent esri/geometry/Point esri/geometry/Polyline esri/geometry/Polygon esri/symbols/TextSymbol esri/symbols/SimpleLineSymbol".split(" "),function(y,F,J,K,A,L,M,S,N,O,G,H,T,I,P,U,Q,R,V){y=y(O,{declaredClass:"esri.layers.LabelLayer",
constructor:function(){this._featureLayers=[];this._zone=[];this._mainStore=[];this._PI=Math.PI;this._PI2=Math.PI/2;this._extent;this._y1=this._x1=this._y0=this._x0=this._ymax=this._ymin=this._xmax=this._xmin=0;this._scale=1},_refresh:function(){this._zone=[];this._mainStore=[];this._extent=this._map.extent;this._xmin=this._extent.xmin;this._xmax=this._extent.xmax;this._ymin=this._extent.ymin;this._ymax=this._extent.ymax;this._scale=(this._xmax-this._xmin)/this._map.width;var a,b;for(a=0;a<this._featureLayers.length;a++){var c=
this._featureLayers[a],f=c.featureLayer,e=c.renderer,h=c.labelRenderer;if(f.visibleAtMapScale){var d=c.textExpression,g=f.graphics;for(b=0;b<g.length;b++){var k=g[b],s=f._map._convertGeometry(this._extent,k.geometry);if(this._extent.intersects(s)){var l=M.substitute(k.attributes,d);if(null!=l&&""!=F.trim(l)&&null!=h){var c=h.getSymbol(k),q=c.angle;c.setText(l);var m=c.getWidth()/2,c=c.getHeight()/2,n=0,p=0;if(null!=e){var r=e.getSymbol(k);if(null!=r)if("simplemarkersymbol"==r.type)n=p=A.normalizedLength(r.size)/
2;else if("picturemarkersymbol"==r.type)n=A.normalizedLength(r.width)/2,p=A.normalizedLength(r.height)/2;else if("simplelinesymbol"==r.type||"cartographiclinesymbol"==r.type)p=A.normalizedLength(r.width)/2}this._mainStore.push({fNumber:a,labelWidth:m,labelHeight:c,symbolWidth:n,symbolHeight:p,graphic:k,geometry:s,text:l,angle:q})}}}}}this.process();this.clear();for(a=0;a<this._zone.length;a++)f=this._zone[a],h=this._featureLayers[f.fNumber].labelRenderer,c=h.getSymbol(f.graphic),"polyline"==f.graphic.geometry.type&&
c.setAngle(f.angle*(180/this._PI)),c.setText(f.text),h=f.x,e=f.y,c instanceof R&&(b=c.getHeight(),Math.cos(f.angle),f=Math.sin(f.angle),h-=0.25*b*this._scale*f,e-=0.33*b*this._scale),h=new N(new P(h,e,this._extent.spatialReference)),h.setSymbol(c),this.add(h)},addFeatureLayer:function(a,b,c,f){var e=null,h=null,d=null,g=a.labelingInfo;if(null!=g)for(i=0;i<g.length;i++){var k=g[i];if(null!=k){e=new H(k.symbol);h=this._convertLabelExpression(k.labelExpression);d=this._convertOptions(k);break}}b instanceof
G&&(e=new H(b.symbol),h=this._convertLabelExpression(b.labelExpression),d=this._convertOptions(b));null!=b&&!(b instanceof G)&&(e=b);null!=c&&(h=c);null!=f&&(d=f);this._featureLayers.push({featureLayer:a,labelRenderer:e,textExpression:h,options:d});J.connect(a,"onUpdateEnd",this,"_refresh")},_convertLabelExpression:function(a){return"$"+a.replace(RegExp("\\[","g"),"{").replace(RegExp("\\]","g"),"}")},_convertOptions:function(a){a=a.labelPlacement;var b=!0;"always-horizontal"==a&&(b=!1);return{pointPriorities:"above-center"==
a?"AboveCenter":"above-left"==a?"AboveLeft":"above-right"==a?"AboveRight":"below-center"==a?"BelowCenter":"below-left"==a?"BelowLeft":"below-right"==a?"BelowRight":"center-center"==a?"CenterCenter":"center-left"==a?"CenterLeft":"center-right"==a?"CenterRight":"AboveRight",lineLabelPlacement:"above-start"==a||"below-start"==a||"center-start"==a?"PlaceAtStart":"above-end"==a||"below-end"==a||"center-end"==a?"PlaceAtEnd":"PlaceAtCenter",lineLabelPosition:"above-after"==a||"above-along"==a||"above-before"==
a||"above-start"==a||"above-end"==a?"Above":"below-after"==a||"below-along"==a||"below-before"==a||"below-start"==a||"below-end"==a?"Below":"center-after"==a||"center-along"==a||"center-before"==a||"center-start"==a||"center-end"==a?"OnLine":"Above",labelRotation:b,howManyLabels:"OneLabel"}},getFeatureLayer:function(a){return this._featureLayers[a]},process:function(){var a;for(a=this._mainStore.length-1;0<=a;a--){var b=this._mainStore[a],c=Math.min(b.labelWidth,b.labelHeight),f=b.labelWidth+0*c,
c=b.labelHeight+0*c,e=this._featureLayers[b.fNumber].options,h=null!=e&&void 0!=e.lineLabelPlacement?e.lineLabelPlacement:"PlaceAtCenter",d=null!=e&&void 0!=e.lineLabelPosition?e.lineLabelPosition:"Above",g=null!=e&&void 0!=e.pointPriorities?e.pointPriorities:"AboveRight",k=[2,2,1,3,0,2,3,3,2];"AboveLeft"==g?k=[1,2,2,2,0,3,2,3,3]:"AboveCenter"==g?k=[2,1,2,2,0,2,3,3,3]:"AboveRight"==g?k=[2,2,1,3,0,2,3,3,2]:"CenterLeft"==g?k=[2,2,3,1,0,3,2,2,3]:"CenterCenter"==g?k=[0,0,0,0,1,0,0,0,0]:"CenterRight"==
g?k=[3,2,2,3,0,1,3,2,2]:"BelowLeft"==g?k=[2,3,3,2,0,3,1,2,2]:"BelowCenter"==g?k=[3,3,3,2,0,2,2,1,2]:"BelowRight"==g&&(k=[3,3,2,3,0,2,2,2,1]);g=e&&void 0!=e.labelRotation?e.labelRotation:!0;e=b.angle*(this._PI/180);if("point"==b.geometry.type)this.generatePointPositions(b.fNumber,b.graphic,b.geometry,b.text,e,f,c,b.symbolWidth,b.symbolHeight,k);else if("multipoint"==b.geometry.type){h=b.geometry;for(d=0;d<h.points.length;d++)this.generatePointPositions(b.fNumber,b.graphic,h.points[d],b.text,e,f,c,
b.symbolWidth,b.symbolHeight,k)}else"polyline"==b.geometry.type?this.generateLinePositions(b.fNumber,b.graphic,b.geometry,b.text,f,c,2*b.symbolHeight+c,h,d,g):"polygon"==b.geometry.type&&this.generatePolygonPositions(b.fNumber,b.graphic,b.geometry,b.text,e,f,c)}},combineLines:function(a,b){return a},combinePolygons:function(a,b){},generatePointPositions:function(a,b,c,f,e,h,d,g,k,s){var l=c.x;c=c.y;g=(g+h)*this._scale;k=(k+d)*this._scale;var q,m;for(q=1;3>=q;q++)for(m=1;9>=m;m++)if(s[m-1]==q)switch(m){case 1:if(this.findPlace(a,
b,f,l-g,c+k,e,h,d))return;break;case 2:if(this.findPlace(a,b,f,l,c+k,e,h,d))return;break;case 3:if(this.findPlace(a,b,f,l+g,c+k,e,h,d))return;break;case 4:if(this.findPlace(a,b,f,l-g,c,e,h,d))return;break;case 5:if(this.findPlace(a,b,f,l,c,e,h,d))return;break;case 6:if(this.findPlace(a,b,f,l+g,c,e,h,d))return;break;case 7:if(this.findPlace(a,b,f,l-g,c-k,e,h,d))return;break;case 8:if(this.findPlace(a,b,f,l,c-k,e,h,d))return;break;case 9:if(this.findPlace(a,b,f,l+g,c-k,e,h,d))return}},generateLinePositions:function(a,
b,c,f,e,h,d,g,k,s){var l=e*this._scale*e*this._scale,q,m,n;for(q=0;q<c.paths.length;q++){var p=c.paths[q],r=p.length,t=Math.floor((r-1)/2),u=0!=(r-1)%2?1:-1;"PlaceAtStart"==g&&(t=0,u=1);"PlaceAtEnd"==g&&(t=r-2,u=-1);for(;0<=t&&t<r-1;){for(m=t;m<r;m++){var v=p[t][0],w=p[t][1],x=p[m][0]-v,y=p[m][1]-w;if(x*x+y*y>l){for(var z=Math.atan2(y,x);z>this._PI2;)z-=this._PI;for(;z<-this._PI2;)z+=this._PI;var A=Math.sin(z),D=Math.cos(z),B=0,C=0;"Above"==k&&(B=d*A*this._scale,C=d*D*this._scale);"Below"==k&&(B=
-d*A*this._scale,C=-d*D*this._scale);if(1==m-t){if(this.clipLine(v,w,p[m][0],p[m][1])&&(v=this._x1-this._x0,n=this._y1-this._y0,v*v+n*n>l&&(m=Math.atan2(n,v),x=e/2+2*h,w=x*this._scale*Math.cos(m),x=x*this._scale*Math.sin(m),"PlaceAtStart"==g?(v=this._x0+w,n=this._y0+x):"PlaceAtEnd"==g?(v=this._x1-w,n=this._y1-x):(v=this._x0+v/2,n=this._y0+n/2),this.findPlace(a,b,f,v-B,n+C,s?-m:0,e,h))))return}else{var E=0;for(n=t;n<=m;n++)E=Math.max(E,Math.abs((p[n][1]-w)*D-(p[n][0]-v)*A));if(E<h&&this.findPlace(a,
b,f,v+x/2-B,w+y/2+C,s?-z:0,e,h))return}break}}t+=u}}},generatePolygonPositions:function(a,b,c,f,e,h,d){var g=this._featureLayers[a].options;if("ManyLabels"==(null!=g?g.howManyLabels:"OneLabel"))for(g=0;g<c.rings.length;g++){var k=this.findCentroid(c.rings[g],this._xmin,this._ymin,this._xmax,this._ymax);this.findPlace(a,b,f,k[0],k[1],e,h,d)}else for(var k=this.findCentroidForFeature(c,this._xmin,this._ymin,this._xmax,this._ymax),s=k[1],l=0,g=0;10>g;g++){l+=d/4;k=this.findCentroidForFeature(c,this._xmin,
s+(l-d/4),this._xmax,s+(l+d/4));if(this.findPlace(a,b,f,k[0],k[1],e,h,d))break;k=this.findCentroidForFeature(c,this._xmin,s-(l+d/4),this._xmax,s-(l-d/4));if(this.findPlace(a,b,f,k[0],k[1],e,h,d))break}},findCentroid:function(a,b,c,f,e){var h=a.length,d=[0,0],g=0,k=a[0][0],s=a[0][1];k>f&&(k=f);k<b&&(k=b);s>e&&(s=e);s<c&&(s=c);for(var l=1;l<h-1;l++){var q=a[l][0],m=a[l][1],n=a[l+1][0],p=a[l+1][1];q>f&&(q=f);q<b&&(q=b);m>e&&(m=e);m<c&&(m=c);n>f&&(n=f);n<b&&(n=b);p>e&&(p=e);p<c&&(p=c);var r=(q-k)*(p-
s)-(n-k)*(m-s);d[0]+=r*(k+q+n);d[1]+=r*(s+m+p);g+=r}d[0]/=3*g;d[1]/=3*g;if(isNaN(d[0])||isNaN(d[1]))return d;c=[];this.fillBuffer(a,c,d);d[0]=this.sortBuffer(c,d[0],b,f);return d},findCentroidForFeature:function(a,b,c,f,e){for(var h=0,d=[0,0],g=0;g<a.rings.length;g++){var k=a.rings[g],s=k.length,l=k[0][0],q=k[0][1];l>f&&(l=f);l<b&&(l=b);q>e&&(q=e);q<c&&(q=c);for(var m=1;m<s-1;m++){var n=k[m][0],p=k[m][1],r=k[m+1][0],t=k[m+1][1];n>f&&(n=f);n<b&&(n=b);p>e&&(p=e);p<c&&(p=c);r>f&&(r=f);r<b&&(r=b);t>e&&
(t=e);t<c&&(t=c);var u=(n-l)*(t-q)-(r-l)*(p-q);d[0]+=u*(l+n+r);d[1]+=u*(q+p+t);h+=u}}d[0]/=3*h;d[1]/=3*h;if(isNaN(d[0])||isNaN(d[1]))return d;c=[];for(m=0;m<a.rings.length;m++)this.fillBuffer(a.rings[m],c,d);d[0]=this.sortBuffer(c,d[0],b,f);return d},fillBuffer:function(a,b,c){for(var f=a.length-1,e=a[0][1]>=a[f][1]?1:-1,h=0;h<=f;h++){var d=h,g=h+1;h==f&&(g=0);var k=a[d][0],d=a[d][1],s=a[g][0],g=a[g][1],l=g>=d?1:-1;if(d<=c[1]&&c[1]<=g||g<=c[1]&&c[1]<=d)c[1]!=d&&c[1]!=g?(b.push((c[1]-d)*(s-k)/(g-d)+
k),e=l):c[1]==d&&c[1]!=g?(e!=l&&b.push(k),e=l):c[1]!=d&&c[1]==g?(b.push(s),e=l):c[1]==d&&c[1]==g&&(1==e&&b.push(k),b.push(s),e=l)}},sortBuffer:function(a,b,c,f){var e=a.length;a.sort();if(0<e){for(var h=0,d=b=0;d<e-1;d+=2){var g=Math.abs(a[d+1]-a[d]);!(a[d]<=c&&a[d+1]<=c)&&(!(a[d]>=f&&a[d+1]>=f)&&g>h)&&(h=g,b=d)}e=a[b];a=a[b+1];e>f&&(e=f);e<c&&(e=c);a>f&&(a=f);a<c&&(a=c);b=(e+a)/2}return b},findPlace:function(a,b,c,f,e,h,d,g){if(isNaN(f)||isNaN(e)||f<this._xmin||f>this._xmax||e<this._ymin||e>this._ymax)return!1;
for(var k=new I(-d*this._scale,-g*this._scale,d*this._scale,g*this._scale,null),s=0;s<this._zone.length;s++){var l=this._zone[s],q=l.angle,m=l.width*this._scale,n=l.height*this._scale,p=l.x-f,r=l.y-e;if(0==h&&0==q){if(l=new I(p-m,r-n,p+m,r+n,null),k.intersects(l))return!1}else{var t=0,u=1;0!=h&&(t=Math.sin(h),u=Math.cos(h));var l=p*u-r*t,p=p*t+r*u,q=q-h,t=Math.sin(q),u=Math.cos(q),v=-m*u- -n*t,r=-m*t+-n*u,q=+m*u- -n*t,w=+m*t+-n*u,m=l+v,n=p-r,t=l+q,u=p-w,v=l-v,r=p+r,l=l-q,p=p+w,q=new Q;q.addRing([[m,
n],[t,u],[v,r],[l,p],[m,n]]);if(k.intersects(q))return!1}}for(;h>this._PI2;)h-=this._PI;for(;h<-this._PI2;)h+=this._PI;this._zone.push({fNumber:a,graphic:b,text:c,angle:h,x:f,y:e,width:d,height:g});return!0},clipLine:function(a,b,c,f){for(var e=this.code(a,b),h=this.code(c,f);0!=e||0!=h;){if(0!=(e&h))return!1;var d=c-a,g=f-b;0!=e?(a<this._xmin?(b+=g*(this._xmin-a)/d,a=this._xmin):a>this._xmax?(b+=g*(this._xmax-a)/d,a=this._xmax):b<this._ymin?(a+=d*(this._ymin-b)/g,b=this._ymin):b>this._ymax&&(a+=
d*(this._ymax-b)/g,b=this._ymax),e=this.code(a,b)):(c<this._xmin?(f+=g*(this._xmin-c)/d,c=this._xmin):c>this._xmax?(f+=g*(this._xmax-c)/d,c=this._xmax):f<this._ymin?(c+=d*(this._ymin-f)/g,f=this._ymin):f>this._ymax&&(c+=d*(this._ymax-f)/g,f=this._ymax),h=this.code(c,f))}this._x0=a;this._y0=b;this._x1=c;this._y1=f;return!0},code:function(a,b){return(a<this._xmin?1:0)<<3|(a>this._xmax?1:0)<<2|(b<this._ymin?1:0)<<1|(b>this._ymax?1:0)}});K("extend-esri")&&F.setObject("layers.LabelLayer",y,L);return y});