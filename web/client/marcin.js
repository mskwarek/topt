angular.module('fiber', ['myAppControllers', 'myAppServices'] );

function linspace(a,b,n) {
    if(typeof n === "undefined") n = Math.max(Math.round(b-a)+1,1);
    if(n<2) { return n===1?[a]:[]; }
    var i,ret = Array(n);
    n--;
    for(i=n;i>=0;i--) { ret[i] = (i*b+(n-i)*a)/n; }
    return ret;
}

angular.module('myAppControllers', [])
	.controller('codeController',
				['$scope',
				 'srvInfo',
				 function ($scope, srvInfo) {
					$scope.myFunction = function(data){
						srvInfo.getMatrix(
						function(data) {
							// document.getElementById('myDiv').value = data['matrix'];
							x_base = linspace(-2, 2, 150);
							x = [];
							for (var i=0;i<data['matrix'].length;i++ ) { 
								x_row = [];
								for(var j=0;j<data['matrix'][i].length;j++) { 
									x_row.push(x_base);
								}
								x.push(x_row);
							}
							y=[];
							for (var i=0;i<data['matrix'].length;i++ ) { 
								y_row = [];
								for(var j=0;j<data['matrix'][i].length;j++) { 
									y_row.push(x_base);
								}
								y.push(y_row);
							}
							var data_z1 = {z: data['matrix'], type: 'surface'};
							var data_z2 = {z: x, showscale: false, opacity:0.9, type: 'surface'};
							var data_z3 = {z: y, showscale: false, opacity:0.9, type: 'surface'};
							// Plotting the surfaces..
							Plotly.newPlot('myDiv', [data_z1, data_z2, data_z3]);
						});	
						document.getElementById('text_to_code').style='background-color:white;';
						document.getElementById('text_error').style='display:none;';	
					}
				 }]);


angular.module('myAppServices', [])
    .service('srvInfo',
             function($http) {
                 this.Decode = function(callback) {
                     return $http.get('/ajax/AtBashCoderPython/Decode/?text='+document.getElementById('text_to_decode').value+'& ').success(callback);
                 };
                 this.Code = function(callback) {
                     return $http.get('/ajax/AtBashCoderPython/Code/?text='+document.getElementById('text_to_code').value+'& ').success(callback);
                 };
                 this.getMatrix = function(callback){
                 	return $http.get('/ajax/fiberMode/getMatrix/?data_m='+document.getElementById('text_to_code').value+'&data_p='+document.getElementById('text_to_decode').value+'& ').success(callback);
                 }
             });
