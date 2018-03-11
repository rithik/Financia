/**
 * Theme: Minton Admin Template
 * Author: Coderthemes
 * Module/App: Flot-Chart
 */

! function($) {
    "use strict";

    var FlotChart = function() {
        this.$body = $("body")
        this.$realData = []
    };

    //creates plot graph
    FlotChart.prototype.createPlotGraph = function(selector, data1, data2, labels, colors, borderColor, bgColor) {
        //shows tooltip
        function showTooltip(x, y, contents) {
            $('<div id="tooltip" class="tooltipflot">' + contents + '</div>').css({
                position : 'absolute',
                top : y + 5,
                left : x + 5
            }).appendTo("body").fadeIn(200);
        }


        $.plot($(selector), [{
            data : data1,
            label : labels[0],
            color : colors[0]
        }, {
            data : data2,
            label : labels[1],
            color : colors[1]
        }], {
            series : {
                lines : {
                    show : true,
                    fill : true,
                    lineWidth : 1,
                    fillColor : {
                        colors : [{
                            opacity : 0.5
                        }, {
                            opacity : 0.5
                        }]
                    }
                },
                points : {
                    show : false
                },
                shadowSize : 0
            },

            grid : {
                hoverable : true,
                clickable : true,
                borderColor : borderColor,
                borderWidth : 0,
                labelMargin : 10
            },
            legend : {
                position : "ne",
                margin : [0, -24],
                noColumns : 0,
                labelBoxBorderColor : null,
                labelFormatter : function(label, series) {
                    // just add some space to labes
                    return '' + label + '&nbsp;&nbsp;';
                },
                width : 30,
                height : 2
            },
            yaxis : {
                tickColor : 'transparent',
                tickLength: 0,
                font : {
                    color : '#bdbdbd'
                }
            },
            xaxis : {
                tickColor : '#transparent',
                tickLength: 0,
                font : {
                    color : '#bdbdbd'
                }
            },
            tooltip : true,
            tooltipOpts : {
                content : '%s: Value of %x is %y',
                shifts : {
                    x : -60,
                    y : 25
                },
                defaultTheme : false
            }
        });
    },
        //end plot graph

        //creates Pie Chart
        FlotChart.prototype.createPieGraph = function(selector, labels, datas, colors) {
            var data = [{
                label : labels[0],
                data : datas[0]
            }, {
                label : labels[1],
                data : datas[1]
            }, {
                label : labels[2],
                data : datas[2]
            }];
            var options = {
                series : {
                    pie : {
                        show : true
                    }
                },
                legend : {
                    show : false
                },
                grid : {
                    hoverable : true,
                    clickable : true
                },
                colors : colors,
                tooltip : true,
                tooltipOpts : {
                    content : "%s, %p.0%"
                }
            };

            $.plot($(selector), data, options);
        },

        //returns some random data
        FlotChart.prototype.randomData = function() {
            var totalPoints = 300;
            if (this.$realData.length > 0)
                this.$realData = this.$realData.slice(1);

            // Do a random walk
            while (this.$realData.length < totalPoints) {

                var prev = this.$realData.length > 0 ? this.$realData[this.$realData.length - 1] : 50,
                    y = prev + Math.random() * 10 - 5;

                if (y < 0) {
                    y = 0;
                } else if (y > 100) {
                    y = 100;
                }

                this.$realData.push(y);
            }

            // Zip the generated y values with the x values
            var res = [];
            for (var i = 0; i < this.$realData.length; ++i) {
                res.push([i, this.$realData[i]])
            }

            return res;
        }, FlotChart.prototype.createRealTimeGraph = function(selector, data, colors) {
        var plot = $.plot(selector, [data], {
            colors : colors,
            series : {
                grow : {
                    active : false
                }, //disable auto grow
                shadowSize : 0, // drawing is faster without shadows
                lines : {
                    show : true,
                    fill : true,
                    lineWidth : 2,
                    steps : false
                }
            },
            grid : {
                show : true,
                aboveData : false,
                color : '#36404a',
                labelMargin : 15,
                axisMargin : 0,
                borderWidth : 0,
                borderColor : null,
                minBorderMargin : 5,
                clickable : true,
                hoverable : true,
                autoHighlight : false,
                mouseActiveRadius : 20
            },
            tooltip : true, //activate tooltip
            tooltipOpts : {
                content : "Value is : %y.0" + "%",
                shifts : {
                    x : -30,
                    y : -50
                }
            },
            yaxis : {
                min : 0,
                max : 100,
                tickColor : '#transparent',
                tickLength: 0
            },
            xaxis : {
                show : false
            }
        });

        return plot;
    },
        //creates Pie Chart
        FlotChart.prototype.createDonutGraph = function(selector, labels, datas, colors) {
            var data = [{
                label : labels[0],
                data : datas[0]
            }, {
                label : labels[1],
                data : datas[1]
            }, {
                label : labels[2],
                data : datas[2]
            }, {
                label : labels[3],
                data : datas[3]
            }];
            var options = {
                series : {
                    pie : {
                        show : true,
                        innerRadius : 0.5
                    }
                },
                legend : {
                    show : true,
                    labelFormatter : function(label, series) {
                        return '<div style="font-size:14px;">&nbsp;' + label + '</div>'
                    },
                    labelBoxBorderColor : null,
                    margin : 50,
                    width : 20,
                    padding : 1
                },
                grid : {
                    hoverable : true,
                    clickable : true
                },
                colors : colors,
                tooltip : true,
                tooltipOpts : {
                    content : "%s, %p.0%"
                }
            };

            $.plot($(selector), data, options);
        },
        //creates Combine Chart
        FlotChart.prototype.createCombineGraph = function(selector, ticks, labels, datas) {

            var data = [{
                label : labels[0],
                data : datas[0],
                lines : {
                    show : true,
                    fill : true
                },
                points : {
                    show : true
                }
            }, {
                label : labels[1],
                data : datas[1],
                lines : {
                    show : true
                },
                points : {
                    show : true
                }
            }, {
                label : labels[2],
                data : datas[2],
                bars : {
                    show : true
                }
            }];
            var options = {
                series : {
                    shadowSize : 0
                },
                grid : {
                    hoverable : true,
                    clickable : true,
                    tickColor : "transparent",
                    borderWidth : 0
                },
                colors : ["#3bafda", "#f76397", "#34d3eb"],
                tooltip : true,
                tooltipOpts : {
                    defaultTheme : false
                },
                legend : {
                    position : "ne",
                    margin : [0, -24],
                    noColumns : 0,
                    labelBoxBorderColor : null,
                    labelFormatter : function(label, series) {
                        // just add some space to labes
                        return '' + label + '&nbsp;&nbsp;';
                    },
                    width : 30,
                    height : 2
                },
                yaxis : {
                    tickColor : '#f5f5f5',
                    tickLength: 0,
                    font : {
                        color : '#bdbdbd'
                    }
                },
                xaxis : {
                    ticks: ticks,
                    tickColor : '#f5f5f5',
                    tickLength: 0,
                    font : {
                        color : '#bdbdbd'
                    }
                }
            };

            $.plot($(selector), data, options);
        },

        //initializing various charts and components
        FlotChart.prototype.init = function() {

            //Pie graph data
            var pielabels = ["Series 1", "Series 2", "Series 3"];
            var datas = [20, 30, 15];
            var colors = ["#3bafda", "#26c6da", "#80deea"];
            this.createPieGraph("#sparkline3", pielabels, datas, colors);

            


           
        },

        //init flotchart
        $.FlotChart = new FlotChart, $.FlotChart.Constructor =
        FlotChart

}(window.jQuery),

//initializing flotchart
    function($) {
        "use strict";
        $.FlotChart.init()
    }(window.jQuery);

$(document).ready(function() {



    //------------- Ordered bars chart -------------//
    
});
