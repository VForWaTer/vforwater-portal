/* Hierarchical Order of data
array
  - iarray
    - varray
  - timeseries
    - vtimeseries
 ndarray
  - raster
    - vraster
  - 2darray
  - idataframe
    - vdataframe
  - time-dataframe
    - vtime-dataframe
 html
  - plot
*/

class array {
  constructor(name) {
    this.dataname = name;
  }
  present() {
    return 'I am ' + this.dataname;
  }
}
class iarray extends array {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class varray extends iarray {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class timeseries extends array {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class vtimeseries extends timeseries {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}

class ndarray {
    constructor(name) {
        this.dataname = name;
    }
    present() {
        return 'I am ' + this.dataname;
    }
}
class raster extends ndarray {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class vraster extends raster {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class _2darray extends ndarray {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class idataframe extends ndarray {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class vdataframe extends idataframe {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class time_dataframe extends ndarray {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
class vtime_dataframe extends time_dataframe {
  constructor(name) {
    super(name);
  }
  show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}

class _html {
    constructor(name) {
        this.dataname = name;
    }
    present() {
        return 'I am ' + this.dataname;
    }
}
class plot extends _html {
    constructor(name) {
    super(name);
  }
    show() {
    return this.present() + ', more specific a ' + this.dataname;
  }
}
