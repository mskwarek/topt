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
							if(angular.isUndefined(data['matrix']) || data['matrix'] === null ){
								document.getElementById('result_label').value =  "Nie mozna wyznaczyć modu";
								Plotly.deleteTraces('myDiv', 0);
								return;
							}
							document.getElementById('result_label').value =  "";
							// console.log(data['matrix']);
							// document.getElementById('myDiv').value = data['matrix'];
							$scope.somethingRight = "Obliczono";
							result = 1;
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
					}
				 }]);


angular.module('myAppServices', [])
    .service('srvInfo',
             function($http) {
                 this.getMatrix = function(callback){
					document.getElementById('result_label').value =  "";
								
                 	return $http.get('/ajax/fiberMode/getMatrix/?data_m='+document.getElementById('M').value+'&data_p='+document.getElementById('P').value+'&data_lam='+document.getElementById('Lambda').value+'&data_a='+document.getElementById('a').value+'&data_n='+document.getElementById('N').value+'&data_nc='+document.getElementById('Nc').value+'& ').success(callback);
                 }
             });
