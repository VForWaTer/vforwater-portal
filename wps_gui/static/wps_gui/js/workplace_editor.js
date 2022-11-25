/** this is an unused example yet **/

let canvas = new draw2d.Canvas("dropdiv");

let start = new draw2d.shape.node.Start({x:80, y:150});

start.add(new draw2d.shape.basic.Label({text:"Test Label"}), new draw2d.layout.locator.Locator());
let Button = "Button"

let dataRect = new vfw.draw2d.Rectangle({
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
let port;
port = dataRect.createPort(
    "output",
    new draw2d.layout.locator.XYRelPortLocator(100, 50),
);
port.setCssClass("red_border_figure")
canvas.add(dataRect);
