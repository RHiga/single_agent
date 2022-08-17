Vue.config.debug = true;
var app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        row: 9,
        column: 6,
        moveProb: 0.9,
        grid: [],
        selectedIndex: null,
        simulation: false,
        log: [],
        logIndex: 0,
        initagent: 5
    },
    created: function(){
        this.draw();
        this.selectedIndex = [0, 2];
        this.setTreasure();
        this.selectedIndex = [0, 3];
        this.setDanger();
        this.selectedIndex = [0, 4];
        this.setDanger();
        this.selectedIndex = [0, 1];
        this.setBlock();
        this.selectedIndex = [1, 1];
        this.setBlock();
        this.selectedIndex = [2, 1];
        this.setBlock();
        this.selectedIndex = [3, 1];
        this.setBlock();
        this.selectedIndex = [2, 3];
        this.setBlock();
        this.selectedIndex = [3, 3];
        this.setBlock();
        this.selectedIndex = [0, 5];
        this.setBlock();
        this.selectedIndex = [1, 5];
        this.setBlock();
        this.selectedIndex = [2, 5];
        this.setBlock();
        this.selectedIndex = [3, 5];
        this.setBlock();
        this.selectedIndex = [5, 0];
        this.setBlock();
        this.selectedIndex = [6, 0];
        this.setBlock()
        this.selectedIndex = [7, 0];
        this.setBlock();
        this.selectedIndex = [5, 2];
        this.setBlock();
        this.selectedIndex = [6, 2];
        this.setBlock()
        this.selectedIndex = [7, 2];
        this.setBlock();
        this.selectedIndex = [5, 4];
        this.setBlock();
        this.selectedIndex = [6, 4];
        this.setBlock()
        this.selectedIndex = [7, 4];
        this.setBlock();
    },
    computed: {
        targetGrid: function () {
            if(!this.simulation){
                return this.grid;
            }else{
                return this.log[this.logIndex];
            }
        },
        hasLog: function(){
            if(this.log.length > 0){
                return true;
            }else{
                return false;
            }
        }
    },
    methods: {
        init: function(){
            this.selectedIndex = null;
            this.simulation = false;
            this.logIndex = 0;
            this.log = [];
        },
        draw: function(){
            this.init();
            this.makeGrid();
        },
        makeGrid: function(){
            this.grid = [];
            var size = this.row * this.column;
            for(var i = 0; i < size; i++){
                var rowIndex = Math.floor(i / this.column);
                var columnIndex = i % this.column;
                if(columnIndex == 0){
                    this.grid.push([]);
                }
                var cellAttribute = 0;
                this.grid[rowIndex].push(cellAttribute);
            }
        },
        getCellAttribute: function(row, column){
            var attribute = this.grid[row][column];
            switch(attribute){
                case 1:
                    return "treasure"
                case -1:
                    return "danger"
                case 9:
                    return "block"
            }
            if(this.selectedIndex != null && (this.selectedIndex[0] == row && this.selectedIndex[1] == column)){
                return "active"
            }
            if(row == (this.grid.length - 1) && column == this.initagent){
                return "agent"
            }
            if(this.simulation){
                var value = this.log[this.logIndex][row][column];
                if(value >= 0.8){
                    return "v5"
                }else if(value >= 0.6){
                    return "v4"
                }else if(value >= 0.3){
                    return "v3"
                }else if(value >= 0.1){
                    return "v2"
                }else{
                    return "v1"
                }
            }
        },
        plan: function(planType){
            var data = {
                "plan": planType,
                "prob": this.moveProb,
                "grid": this.grid,
                "initagent": this.initagent
            }
            var self = this;
            fetch("/plan", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }).then(function(resp){
                return resp.json()
            }).then(function(resp){
                self.log = resp["log"];
                self.play();
            })
        },
        play: function(){
            this.logIndex = 0;
            this.simulation = true;
            var self = this;
            var timer = setInterval(function(){
                if(self.logIndex < self.log.length - 1){
                    self.logIndex += 1;
                }else{
                    clearInterval(timer);
                }
            }, 1000);
        },
        stop: function(){
            this.init();
        },
        value: function(row, column){
            var attribute = this.grid[row][column];
            if(attribute != 0 || (row == (this.grid.length -1) && column == this.initagent)){
                return "";
            }
            var value = this.log[this.logIndex][row][column];
            var value = Math.floor(value * 1000) / 1000;
            return value;
        },
        selectCell: function(row, column){
            // [row, 0] is Agent point
            if(!(row == (this.grid.length - 1) && column == this.initagent)){
                this.selectedIndex = [row, column];
            }
        },
        setTreasure: function(){
            this.setAttribute(1);
        },
        setDanger: function(){
            this.setAttribute(-1);
        },
        setBlock: function(){
            this.setAttribute(9);
        },
        clearAttribute: function(row, column){
            if(this.simulation){
                this.init();
            }
            this.selectedIndex = [row, column];
            this.setAttribute(0);
        },
        setAttribute: function(attribute){
            var index = this.selectedIndex;
            if(this.selectedIndex != null){
                this.grid[index[0]][index[1]] = attribute;
                this.selectedIndex = null;
            }
        }
    }
})
