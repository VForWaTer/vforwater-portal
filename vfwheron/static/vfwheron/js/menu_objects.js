function menu_builder() {
    // var newMenu = JSON.parse(document.getElementById('data_style').value);
    console.log('test');
    // var Menuitem = {name:'Hallo', total_choices: 4,};
    // var Menuitem = {name:'Fred', total_choices: 5,};
    // console.log(Menuitem)
    // console.log(jsonMenu)
    var jsMenu = JSON.parse(jsonMenu)
    // console.log(jsMenu)
    // console.log(jsonMenu.getKey())
    // Object.keys(obj).map(e => console.log(`key=${e}  value=${obj[e]}`));
    Object.keys(jsMenu).forEach(function(key,value) {
        console.log(jsMenu.valueOf(key))
        console.log(value.valueOf(key))

    })

}

function child_builder(child) {

}

function Menuitem(name, total_choices, type, child) {
    this.name = name;
    this.total_choices = total_choices;
    this.choices = total_choices;
    this.chosen = 0;
    // this.child = child_builder(child)

}

function Childitem(name, total_choices, type, child) {
    this.name = name
    this.type = type || 'default'
    this.total_choices = total_choices;
    this.choices = total_choices;
    this.chosen = 0;

}