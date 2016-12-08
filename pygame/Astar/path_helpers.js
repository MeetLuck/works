// =============================================================================
//  Generic helpers.
// =============================================================================

// Returns the index of a node in the list.
var getNodeIndex = function(node, list) {
    for (i in list) {
        if (node == list[i]) {
            return i;
        }
    }
    return -1;
}


// Determines whether a node is on the list.
var findNode = function(node, list) {
    return getNodeIndex(node, list) >= 0;
}


// Removes a node from a list.
var removeNode = function(node, list) {
    var idx = getNodeIndex(node, list);
    if (idx >= 0) {
        list.splice(idx, 1);
    }
}


// Writes the contents of a list of nodes in a readable way.
var listNodes = function(id, list) {
    var par = document.getElementById(id);

    var text = id + " = [";

    for (var i = 0; i < list.length; i++) {
        text += list[i].label;
        if (i < list.length - 1 ) {
            text += ", ";
        }
    }

    text += "]";
    par.textContent = text;
}




// =============================================================================
//  Renders the graph and the state of the search.
// =============================================================================
var render = function(search, canvas) {
    var canvas = document.getElementById("demo");
    canvas.width = canvas.width;

    ctx = canvas.getContext("2d");

    var node_w = Math.floor(canvas.width / search.graph.cols);
    var node_h = Math.floor(canvas.height / search.graph.rows);

    ctx.font = "12px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (var r = 0; r < search.graph.rows; r++) {
        for (var c = 0; c < search.graph.cols; c++) {
            var node = search.graph.nodes[r*search.graph.cols + c];
            var x = c*node_w;
            var y = r*node_h;

            ctx.beginPath();
            ctx.rect(x + .5, y + .5, node_w, node_h);

            // Color the nodes according to their type.
            var fillStyle = "";
            if (node.adjacent.length == 0) {
                fillStyle = "lightgray";
            } else if (findNode(node, search.path)) {
                fillStyle = "#A0A0FF";
            } else if (findNode(node, search.reachable)) {
                fillStyle = "#80FF80";
            } else if (findNode(node, search.explored)) {
                fillStyle = "#FF8080";
            } else if (node == search.goal_node) {
                fillStyle = "#FFFF00";
            }

            if (fillStyle) {
                ctx.fillStyle = fillStyle;
                ctx.fill();
            }

            ctx.stroke();
            ctx.closePath();

            ctx.fillStyle = "black";
            ctx.fillText(node.label, x + node_w/2, y + node_h/2);
        }
    }

    // Draw "previous" arrows on top of the graph.
    for (var r = 0; r < search.graph.rows; r++) {
        for (var c = 0; c < search.graph.cols; c++) {
            var node = search.graph.nodes[r*search.graph.cols + c];
            if (node.previous) {
                var pidx = getNodeIndex(node.previous, search.graph.nodes);
                var pr = Math.floor(pidx / search.graph.cols);
                var pc = pidx % search.graph.cols;

                var mx = (c + pc + 1) * node_w / 2;
                var my = (r + pr + 1) * node_h / 2;
                
                var aw = 4;
                var angle = 0;
                if (c == pc) {
                    angle = (r < pr) ? Math.PI/2 : -Math.PI/2;
                } else {
                    angle = (c < pc) ? 0 :  Math.PI;
                }

                ctx.save();
                ctx.beginPath();
                ctx.translate(mx, my);
                ctx.rotate(angle);
                ctx.moveTo(aw, 0);
                ctx.lineTo(-aw, -aw);
                ctx.lineTo(-aw, aw);
                ctx.closePath();
                ctx.restore();
                ctx.fill();
            }
        }
    }

    listNodes("reachable", search.reachable);
    listNodes("explored", search.explored);

    var path_p = document.getElementById("path");
    if (search.path.length) {
        listNodes("path", search.path);
        path.textContent += " found in " + search.iterations + " iterations.";
    } else {
        path.textContent = "";
    }
}


// =============================================================================
//  Graph.
// =============================================================================

// A Node in the graph.
// Edges are represented implicitly with the "adjacent" list.
var Node = function() {
    this.adjacent = [];
    this.previous = undefined;
    this.label = "";
}


Node.prototype.clear = function() {
    this.previous = undefined;
    this.cost = Infinity;
}


// The Graph.
// Build the Graph from an ASCII description.
var Graph = function(grid) {
    this.rows = grid.length;
    this.cols = grid[0].length;

    // Create some labels.
    var labels = [];
    var first = ["", "A", "B", "C"];
    for (var i in first) {
        var prefix = first[i];
        for (var j = 65; j < 91; j++) {
            labels.push(prefix + String.fromCharCode(j));
        }
    }


    // Create one node per square in the grid.
    this.nodes = []
    for (var i = 0; i < this.rows*this.cols; i++) {
        var node = new Node();
        node.label = labels[i];
        this.nodes.push(node);
    }
   
    // Add edges to adjacent nodes.
    for (var r = 0; r < this.rows; r++) {
        for (var c = 0; c < this.cols; c++) {
            var node = this.nodes[this.cols*r + c];

            // Ignore blocked squares.
            if (grid[r][c] == '*') {
                continue;
            }

            // Figure out the adjacent nodes.
            if (r > 0 && grid[r-1][c] == ' ') {  // Up
                node.adjacent.push(this.nodes[this.cols*(r-1) + c]);
            }
            if (r < this.rows-1 && grid[r+1][c] == ' ') {  // Down
                node.adjacent.push(this.nodes[this.cols*(r+1) + c]);
            }
            if (c > 0 && grid[r][c-1] == ' ') {  // Left
                node.adjacent.push(this.nodes[this.cols*r + c - 1]);
            }
            if (c < this.cols-1 && grid[r][c+1] == ' ') {  // Right
                node.adjacent.push(this.nodes[this.cols*r + c + 1]);
            }
        }
    }
}


// Find a node given its label.
Graph.prototype.findNodeByLabel = function(label) {
    for (var i in this.nodes) {
        if (this.nodes[i].label == label) {
            return this.nodes[i];
        }
    }
}


// =============================================================================
//  Search.
// =============================================================================

// The state of the search.
// For the purposes of the demo, we want to run step by step, so instead of
// implementing the search as a function with a loop, we keep the state in
// a class and we have a method that executes a single iteration of the loop.
var Search = function(graph, start, goal) {
    this.graph = graph;
    this.reachable = [];
    this.explored = [];
    this.path = [];
    this.start_label = start;
    this.goal_label = goal;
}


Search.prototype.reset = function() {
    this.reachable = [this.graph.findNodeByLabel(this.start_label)];
    this.goal_node = this.graph.findNodeByLabel(this.goal_label);
    this.explored = [];
    this.path = [];
    this.iterations = 0;

    for (var i in this.graph.nodes) {
        this.graph.nodes[i].clear();
    }

    this.reachable[0].cost = 0;

    render(this);
}


Search.prototype.step = function() {
    // Is the search already done?
    if (this.path.length > 0) {
        return;
    }

    // If there are no more nodes to consider, we're done.
    if (this.reachable.length == 0) {
        this.finished = true;
        return;
    }

    this.iterations++;

    // Choose a node to examine next.
    var node = this.chooseNode();

    // Are we done yet?
    if (node == this.goal_node) {
        // Reconstruct the path.
        while (node) {
            this.path.unshift(node);
            node = node.previous;
        }
        render(this);
        return;
    }

    // Don't repeat ourselves.
    removeNode(node, this.reachable);
    this.explored.push(node);

    // Where can we get from here?
    for (var i in node.adjacent) {
        this.addAdjacent(node, node.adjacent[i]);
    }
    
    render(this);
}


// =============================================================================
//  Support methods to run the search as an animation.
// =============================================================================
var runSearchInterval;
var runSearch = function() {
    if (search.path.length > 0) {
        search.reset();
    }

    stopRunSearch();
    runSearchInterval = setInterval(stepSearch, stepDelay);
}

var stepSearch = function() {
    search.step();
    if (search.path.length > 0) {
        stopRunSearch();
    }
}

var stopRunSearch = function() {
    clearInterval(runSearchInterval);
    runSearchInterval = undefined;
}

