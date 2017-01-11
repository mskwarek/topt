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
								$scope.somethingWrong = "Nie mozna wyznacyzm modu";
								$scope.result = "Nie udało się";
								return;
							}
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
                 	return $http.get('/ajax/fiberMode/getMatrix/?data_m='+document.getElementById('data_m').value+'&data_p='+document.getElementById('data_p').value+'&data_lam='+document.getElementById('data_lam').value+'&data_a='+document.getElementById('data_a').value+'&data_n='+document.getElementById('data_n').value+'&data_nc='+document.getElementById('data_nc').value+'& ').success(callback);
                 }
             });
