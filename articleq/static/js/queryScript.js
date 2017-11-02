DIR = 0
INV = 1

rel = {
    "write": ["written", "written by"],
    "classify as": ["classified as", "that classified"],
    "mention": ["that mentions", "mentioned by"],
    "mention many time": ["that mentions (many times)", "mentioned (many times) by"],
    "classify by": ["classified by", "that classified"],
    "issue by": ["issued by", "that issued"],
    "tag": ["were tagged as", "that tagged"],
    "review as": ["reviewed as", "of"],
    "issue in": ["issued in", "issued in"],
    "locate in": ["located in", "located in"]
}

rel_node = {
    "write": ["person", "document"],
    "written by": ["document", "person"],
    "classified as": ["document", "classification"], 
    "that classified": ["classification", "document"],
    "that mentions": ["document", ["person", "location", "organization", "money", "percentage", "date", "time"]], 
    "mentioned by": [["person", "location", "organization", "money", "percentage", "date", "time"], "document"],
    "that mentions (many times)": ["document", "context"], 
    "mentioned (many times) by": ["context", "document"],
    "classified by": ["document", "person"], 
    "that classified": ["person", "document"],
    "issued by": ["document", "organization"], 
    "that issued": ["organization", "document"],
    "were tagged as": ["document", "tag"], 
    "that tagged": ["tag", "document"],
    "reviewed as": ["document", "sensitive"], 
    "of": ["sensitive", "document"]
    // "issue in" and "locate in" => too new
}

rel_db_name = {
    "write": "WRITES",
    "written by": "WRITES",
    "classified as": "IS CLASSIFIED AS", 
    "that classified": "IS CLASSIFIED AS",
    "that mentions": "MENTIONS", 
    "mentioned by": "MENTIONS",
    "mentions (many times)": "MENTIONS MANY TIMES", 
    "mentioned (many times) by": "MENTIONS MANY TIMES",
    "classified by": "IS CLASSIFIED BY", 
    "that classified": "IS CLASSIFIED BY",
    "issued by": "IS ISSUED BY", 
    "that issued": "IS ISSUED BY",
    "were tagged as": "TAGS", 
    "that tagged": "TAGS",
    "reviewed as": "IS REVIEWED AS", 
    "of": "IS REVIEWED AS",
    // new relationship
    "located in": "IS LOCATED IN",
    "issued in": "IS ISSUED IN"
}

label_db_name = {
    "document": "DOC",
    "sensitivity": "SENSITIVITY", 
    "person": "PERSON", 
    "location": "LOCATION", 
    "organization": "ORGANIZATION",
    "classification": "CLASSIFICATION", 
    "tag": "TAG", 
    "context": "CONTEXT", 
    "money": "MONEY", 
    "pecentage": "PERCENTAGE", 
    "date": "DATE", 
    "time": "TIME"
}

ql = {
    "open": ["show", "find"],
    "label": ["document", "sensitivity", "person", "location", "organization", "classification", "tag", "context", "money", "pecentage", "date", "time"],
    "property": {
        "document": ["id", "title", "created date", "released date", "subject", "words", "paragraphs", "REF", "doctype"],
        "sensitivity": ["value"],
        "person": ["name", "position"],
        "location": ["name", "latitude", "longtitude"],
        "organization": ["name", "latitude", "longtitude"],
        "classification": ["classified type"],
        "tag": ["name"],
        "context": ["words"], 
        "money": ["money"], 
        "percentage": ["percent"], 
        "date": ["date"], 
        "time": ["time"]   
    },
    "graph_keyword": ["the scatter of", "the number of", "the trend of", "the percentage of"],
    "determiner": ["each"],
    "rel_list": {
        "document": [rel["write"][INV], rel["classify as"][DIR], rel["mention"][DIR], rel["mention many time"][DIR], rel["classify by"][DIR], rel["issue by"][DIR], rel["tag"][DIR], rel["review as"][DIR], rel["issue in"][DIR]],
        "sensitivity": [rel["review as"][INV]],
        "person": [rel["write"][DIR], rel["mention"][INV], rel["classify by"][INV]],
        "location": [rel["mention"][INV], rel["locate in"][INV], rel["locate in"][DIR]],
        "organization": [rel["mention"][INV], rel["issue by"][INV]],
        "classification": [rel["classify as"][INV]],
        "tag": [rel["tag"][INV]],
        "context": [rel["mention many time"][INV]], 
        "money": [rel["mention"][INV]], 
        "percentage": [rel["mention"][INV]], 
        "date": [rel["mention"][INV]], 
        "time": [rel["mention"][INV]] 
    }, 
}

s = 0
t = 0
type = {
    text: 0,
    graph: 1,
    changeType: function(word) {
        if (word == ql["open"][0])
            return this.graph
        if (word == ql["open"][1])
            return this.text
        return -1
    }
}

termCount = 0
current_list = []

input = new Awesomplete('input[id="query"]', {
    list: ql["open"],
    maxItems: 30,
    minChars: 0,
	data: function (item, input) {
		return item;
    },
    // item: function (suggestion, input) {
    //     if ()
    // },
    filter: function(text, input) {
        inputSplit = input.split(" ")
        inputLast = inputSplit[inputSplit.length - 1].toLowerCase()
        return text.indexOf(inputLast) === 0;
    },
    replace: function (text) {
        inputArray = this.input.value.split(" ")
        inputArray[inputArray.length - 1] = text
        this.input.value = inputArray.join(" ") + " "
        checkValid()
    }
});

countTerm = function(termCount, n, text) {
    // handle undefined
    return termCount == n || (termCount == n && text.slice(-1) == " ")
}

contain = function(t, list) {
    // list contains t
    return list.indexOf(t) >= 0
}

setInitialSuggestion = function(text, textCount) {
    if (textCount == 0 || !contain(text, ql["open"])) {
        input._list = ql["open"]
    } else {
        input._list = []
    }
}

validQuery = [{state: "open"}, {state: "graph_keyword"}, {state: "label"}, 
                {state: "relationship"}, {state: "determiner"}, {state: "label"}]

valid = false
states = []
  
doValid = function(v) {
    if (v) {
        valid = true
        changeTextFieldColorToGreen()
        input._list = []
        input.evaluate()
        jsonDOM.value = statesJSON
    }
    else {
        valid = false
        changeTextFieldColorToBlack()
        jsonDOM.value = ""
    }
}

checkValid = function() {
    statesJSON = JSON.stringify(states, null, 0)
    if (states.length != validQuery.length) {
        doValid(false)
        return;
    } else {
        for (i = 0; i < validQuery.length; i++) {
            if (validQuery[i].state != states[i].state) {
                doValid(false)
                return;
            }
        }
        // valid
        doValid(true)
    }
}

update = function(e) {
    nodeList = []
    stepList = []

    text = inputDOM.value
    textArray = text.split(" ")
    textCount = textArray.length

    states = []
    phrase = ""

    if (e.keyCode == '38' || e.keyCode == '40') {
        return;
    }

    // set initial suggestion for first text
    setInitialSuggestion(text, textCount)
    for (i = 0; i < textCount; i++) {
        phrase += textArray[i]
        console.log("phrase: " + phrase + "|")
        console.log("states: " + JSON.stringify(states, null, 4))
        // console.log("states: ")
        if (states.length == 0) {
            if (contain(phrase, ql["open"])) {
                // change type of query
                t = type.changeType(phrase)
                // change suggestions
                if (t == type.text) {
                    input._list = ql["label"]
                    input.evaluate()
                    states.push({state: "open", phrase: phrase})
                    phrase = "";
                }
                else if (t == type.graph) {
                    input._list = ql["graph_keyword"]
                    input.evaluate()
                    states.push({state: "open", phrase: phrase})
                    phrase = "";
                }
            }
        }
        else {
            // after open --> check 'state' instead
            current_state = states[states.length - 1]
            previous_state = states[states.length - 2]
            // console.log("in state.length !0: ", input._list)
            if (current_state.phrase == "find") {
                // possible next state: label

            }
            if (states[0].phrase == "show") {
                // possible next state: graph_keyword
                if (contain(phrase, ql["graph_keyword"])) {
                    input._list = ql["label"]
                    input.evaluate()
                    states.push({state: "graph_keyword", phrase: phrase})
                    phrase = ""
                } 
                if (current_state.state == "graph_keyword") {
                    // possible next state: label
                    if (contain(phrase, ql["label"])) {
                        input._list = ql["rel_list"][phrase]
                        input.evaluate()
                        states.push({state: "label", phrase: phrase, db_name: label_db_name[phrase]})
                        phrase = ""
                    }
                } else if (current_state.state == "label") {
                    // possible next state: 
                    if (previous_state.state == "determiner") {
                        // last phrase
                        input._list = []
                        input.evaluate()
                        phrase = ""
                    } else {
                        // first label case
                        if (contain(phrase, ql["rel_list"][current_state.phrase])) {
                            input._list = ql["determiner"] // each
                            input.evaluate()
                            states.push({state: "relationship", phrase: phrase, db_name: rel_db_name[phrase]})
                            phrase = "";
                        }
                    }
                    
                } else if (current_state.state == "relationship") {
                    // possible next state: 
                    console.log("rel_node: " + rel_node[current_state.phrase][1])
                    if (contain(phrase, ql["determiner"])) {
                        console.log("possible label: ")
                        nodes = rel_node[current_state.phrase][1]
                        if (!Array.isArray(nodes)) {
                            input._list = [nodes] // the end of relationship
                        }
                        else {
                            input._list = nodes
                        }
                        input.evaluate()
                        states.push({state: "determiner", phrase: phrase, possible_label: nodes})
                        phrase = "";
                    }
                } else if (current_state.state == "determiner") {
                    // possible next state: 
                    console.log("possible_label: " + current_state.possible_label)
                    console.log("phrase: " + phrase)
                    isContain = false
                    if (Array.isArray(current_state.possible_label)) {
                        isContain = contain(phrase, current_state.possible_label)
                    } else {
                        isContain = contain(phrase, [current_state.possible_label])
                    }
                    if (isContain) {
                        states.push({state: "label", phrase: phrase, db_name: label_db_name[phrase]})
                        console.log(JSON.stringify(states, null, 4))
                        phrase = "";
                    }
                }
            }
        }
        if (phrase != "") // after reset the phrase, no need to add a space
            phrase += " "
    }

    console.log("states: " + JSON.stringify(states, null, 4))

    checkValid()
}

inputDOM = document.getElementById("query")
inputDOM.addEventListener("keyup", update, false)
inputDOM.onmousedown = function() {
    if (!valid) // don't show suggestion if query's already valid
        input.open()
};
jsonDOM = document.getElementById("json")
awesomplete = document.getElementsByClassName("awesomplete")[0]
// console.log(awesomplete.style)
awesomplete.style.display = "block"
changeTextFieldColorToGreen = function() {
    inputDOM.style.color = 'green'
}
changeTextFieldColorToBlack = function() {
    inputDOM.style.color = 'black'
}