/** this is an unused example yet **/

// {% comment %}   $(window).load(function () {
//
//      var canvas = new draw2d.Canvas("dropdiv");
//
//      var figure1 = new draw2d.shape.basic.Oval();
//      var figure2 = new draw2d.shape.basic.Rectangle();
//      canvas.add(figure1,100,100);
//      canvas.add(figure2,120,150);
//  });{% endcomment %}

let canvas = new draw2d.Canvas("dropdiv");

// var rect2 = new draw2d.shape.basic.Rectangle({
//     x: 100,
//     y: 10,
//     bgColor: "#f0f000",
//     alpha: 0.7,
//     width: 100,
//     height: 60,
//     radius: 10
// });

let start = new draw2d.shape.node.Start({x:80, y:150});

start.add(new draw2d.shape.basic.Label({text:"Test Label"}), new draw2d.layout.locator.Locator());
let Button = "Button"

let dataRect = new draw2d.shape.basic.Rectangle({
    width: 120,
    height: 30,
    radius: 5,
    bgColor: "#D9EFFD",
    stroke: 0
})
dataRect.add(
    new draw2d.shape.basic.Label({
        text:Button,
        stroke:0,
        fontSize:15,
        x:5,
        y:2
    }),
    new draw2d.layout.locator.Locator());
// dataRect.attr({"cssClass": "red_border_figure"})
let port;
port = dataRect.createPort(
    "output",
    new draw2d.layout.locator.XYRelPortLocator(100, 50),
    // {
    // radius:20,
    // "cssClass": "red_border_figure"
    // }
);
port.setCssClass("red_border_figure")
// port.setBackgroundColor("#f0f000");
// port = draw2d.figure.Port(
//     "output",
//     new draw2d.layout.locator.XYRelPortLocator(100, 50),
//     {fill: "#f0f000",
//     radius:20,
//     "cssClass": "red_border_figure"
//     })
console.log('dataRect: ', dataRect.outputPorts)
// dataRect.Port.setClass("red_border_figure")
// canvas.add(figure2, 120, 150);
// canvas.add(rect2);
canvas.add(dataRect);
