let instructions_1 = [

    ["jasmin", "tulip"],

    ["lily", "tulip"],

    ["tulip", "tulip"],

    ["rose", "rose"],

    ["violet", "rose"],

    ["sunflower", "violet"],

    ["daisy", "violet"],

    ["iris", "violet"]

];
let treasure_rooms_1 = ["violet", "rose"];

function treasureRoom() {


    let findRooms = instructions_1.flat().filter((a, b, c) => c.indexOf(a) == b);
    let rp = [];
    let roomPointerCol = {};
    for (let index = 0; index < findRooms.length; index++) {
        const element = findRooms[index];
        let findPointers = instructions_1.filter(x => (x[1] == element && x[0] != element) || (x[1] == element && x[0] == element));
        if (findPointers.length >= 2) {
            roomPointerCol[element] = findPointers.map(x => x[0])
        };

    }



    for (let tr = 0; tr < treasure_rooms_1.length; tr++) {
        for (let item in roomPointerCol) {
            let findPOint = instructions_1.filter(x => x[0] == item && x[1] == treasure_rooms_1[tr]);
            if (findPOint.length > 0)
                rp.push(item);
        }



    }
    console.log(rp)
}

// let findPointedRooms = findRooms.filter( x => instructions_1.filter(a => a[0] == x || a[1] == x).length >= 2);

// for (let index = 0; index < treasure_rooms_1.length; index++) {
//     const element = array[index];

// }

//reasureRoom()

function tr() {
    let result = [];
    let incomingMap = {};

    for (let [src, dest] of instructions_1) {
        if (!incomingMap[dest]) incomingMap[dest] = [];
        incomingMap[dest].push(src);
    }

    for (let [src, dest] of instructions_1) {
        // Check if this src room has 2 or more incoming connections
        if (incomingMap[src] && incomingMap[src].length >= 2) {
            // Check if this room's instruction points to a treasure room
            if (treasure_rooms_1.includes(dest)) {
                result.push(src);
            }
        }
    }
    console.log(result)
}
// treasureRoom();
// tr();


// Dairy Product Problem

function ShoppingList() {
    let products = [
        ["Cheese", "Dairy"],
        ["Carrots", "Produce"],
        ["Potatoes", "Produce"],
        ["Canned Tuna", "Pantry"],
        ["Romaine Lettuce", "Produce"],
        ["Chocolate Milk", "Dairy"],
        ["Flour", "Pantry"],
        ["Iceberg Lettuce", "Produce"],
        ["Coffee", "Pantry"],
        ["Pasta", "Pantry"],
        ["Milk", "Dairy"],
        ["Blueberries", "Produce"],
        ["Pasta Sauce", "Pantry"]
    ]

    let list1 = ["Blueberries", "Carrots", "Romaine Lettuce", "Iceberg Lettuce"];

    let depWithProducts = {};
    let visitDep = [];
    let c = list1.length;
    for (let [product, dep] of products) {
        if (!depWithProducts[dep]) depWithProducts[dep] = [];
        depWithProducts[dep].push(product);
        let findProduct = list1.filter(x => x == product);
        if (findProduct.length > 0)
            visitDep.push(dep);


    }
    console.log(visitDep.filter((a, b, c) => c.indexOf(a) == b).length)
}
//ShoppingList();

function RobotNames() {
    let all_parts = [
        "Rosie_claw",
        "Rosie_sensors",
        "Dustie_case",
        "Optimus_sensors",
        "Rust_sensors",
        "Rosie_case",
        "Rust_case",
        "Optimus_speaker",
        "Rosie_wheels",
        "Rosie_speaker",
        "Dustie_case",
        "Dustie_arms",
        "Rust_claw",
        "Dustie_case",
        "Dustie_speaker",
        "Optimus_case",
        "Optimus_wheels",
        "Rust_legs",
        "Optimus_sensors"];

    let required_parts_1 = "sensors,case,screws".split(',');
    //[ ["Optimis","sensors"] ]
    let robots = {};
    let robotNames = [];
    let splitArray = all_parts.map(x => x.split('_'));
    for (let [r, p] of splitArray) {
        if (!robots[r]) robots[r] = [];
        robots[r].push(p);
    }
    for (const element in robots) {
        let findParts = required_parts_1.filter((a, b, c) => {
            debugger
            robots[element].find(x => x == a)
        });
        if (findParts.length == required_parts_1.length)
            robotNames.push(element)
    }
    console.log(robotNames);

}
 RobotNames()

//Game Obstacles

function Game() {
    let Obstacles = [9, 4, 2];
    let instruction = 'RJJRRRJ'.split('');
    //[R,R,R,J,J,R,R,R]
    let start = 0;
    let lastAction = '';

    for (let ins = 0; ins < instruction.length; ins++) {

        lastAction = instruction[ins - 1] == 'J' ? lastAction : instruction[ins - 1];
        if (instruction[ins] === 'R') {
            start++;
        }
        else if (instruction[ins] === 'L') {
            start--;
        }
        else if (instruction[ins] === 'J') {
            if (lastAction == 'R')
                start = start + 2;
            else if (lastAction == 'L')
                start = start - 2;
        }
        if (Obstacles.includes(start))
            return console.log(start === 10);
    }
    console.log(start === 10);


}
Game();

function ludoo() {
    let teleporters1 = ["6,18", "36,26", "41,21", "49,55", "54,52",
        "71,58", "74,77", "50,45", "80,73", "92,85"].map(x => x.split(','));
    // 0 , 1 , 2, 3, 4, 5

    let rollingDies = 47;
    let startsFrom = 45;
    let totalSquares = 50;
    let squarPos = [];
    for (let index = 0; index < rollingDies; index++) {

        let dies_pos = startsFrom + (index + 1);
        if (dies_pos >= totalSquares)
            dies_pos = totalSquares;
        let findTeleporetrPoint = teleporters1.find(x => x[0] == dies_pos);
        if (findTeleporetrPoint) {
            let findTelePos = findTeleporetrPoint[1];
            if (findTelePos >= totalSquares)
                findTelePos = totalSquares;
            squarPos.push(findTelePos);
        }
        else
            squarPos.push(dies_pos);



    }
    console.log(squarPos.filter((a, b, c) => c.indexOf(a) == b))
}




function concatWords() {
    let words = ["The", "age", "group", "work", "life", "adventure", "time", "menu", "ram", "market", "car", "power", "society"];

    let lenght = 13;
    let collect = [];
    let concat = '';
    let pushPrevWord = [];
    for (let index = 0; index < words.length; index++) {
        const element = words[index];
        pushPrevWord.push(element);
        concat = pushPrevWord.join('-');
        if (concat.length == 13) {
            collect.push(concat);
            concat = '';
            pushPrevWord = [];

        }
        if (concat.length > 13) {
            pushPrevWord.pop();
            concat = pushPrevWord.join('-');
            collect.push(concat);
            concat = '';
            pushPrevWord = [];
            index--;

        }
    }

    console.log(JSON.stringify(collect))
}
//concatWords();


///Pair for songs

function pairOfSongs() {
    let songList = [
        ["Stairway to Heaven", "8:05"], ["Immigrant Song", "2:27"],
        ["Rock and Roll", "3:41"], ["Communication Breakdown", "2:29"],
        ["Good Times Bad Times", "2:48"], ["Black Dog", "4:55"],
        ["The Crunge", "3:18"], ["Achilles Last Stand", "10:26"],
        ["The Ocean", "4:31"], ["Hot Dog", "3:19"],
    ];
    let col = [];

    songList = songList.map(x => [x[0], (x[1].split(':').map(a => parseFloat(a)))])
    let lenght = 7;
    for (let index = 0; index < songList.length; index++) {
        const element = songList[index];
        let calcP = (element[1][0] * 60) + element[1][1];
        for (let indexI = 1; indexI < songList.length; indexI++) {
            const elementNext = songList[indexI];
            let calc = (elementNext[1][0] * 60) + elementNext[1][1];
            if (((calcP + calc) / 60) == lenght)
                col.push(element[0], elementNext[0])
        }

    }
    console.log(JSON.stringify(col));
}
//pairOfSongs()

function FindScrambled() {
    let word = ["baby", "referee", "cat", "dada", "dog", "bird", "ax", "baz"];
    let note = 'breadmaking'.split('').map((a, b, c) => ({ [a]: c.filter(x => a == x).length }));


    for (let index of word) {
        const element = index.split('');
        let wordFinal = '';

        for (let e = 0; e < element.length; e++) {
            const singWord = element[e];
            let findWordLenght = element.filter(x => x == singWord).length;
            let worldLenghtFromNote = note.find(x => x[singWord]) ? note.find(x => x[singWord])[singWord] : 0;


            if (worldLenghtFromNote >= findWordLenght) {

                wordFinal = wordFinal + singWord;
            }
            if (wordFinal == index && wordFinal.length == index.length) {
                return console.log(index)
            }



        }

    }
    if (wordFinal == '')
        return console.log('-')
}
FindScrambled();


let words1 = [ "The", "day", "began", "as", "still", "as", "the",
          "night", "abruptly", "lighted", "with", "brilliant",
          "flame" ];
          
function wordWrap(length){
  let pushWraps = [];
    let tempWord= '';
    for (var i = 0; i < words1.length; i++) {
      let _thisWord = words1[i];
      if(_thisWord.length > length)
        continue;
      if(!tempWord) tempWord =  _thisWord;
     else tempWord = tempWord + '-' +_thisWord;
      if(tempWord.length == length){
        pushWraps.push(tempWord);
        tempWord='';
      }
     else  if(tempWord.length > length){
        let newAr = tempWord.split('-');
         newAr.pop();
        pushWraps.push(newAr.join('-'));
        tempWord='';
        i--
      }  
      else if(words1.length - 1 == i && _thisWord.length <= length) 
      pushWraps.push(tempWord);
        
    }
    console.log(pushWraps)
}
wordWrap(13);


let  events = [
    ["CONNECT","Alice","Bob"],
    ["DISCONNECT","Bob","Alice"],
    ["CONNECT","Alice","Charlie"],
    ["CONNECT","Dennis","Bob"],
    ["CONNECT","Pam","Dennis"],
    ["DISCONNECT","Pam","Dennis"],
    ["CONNECT","Pam","Dennis"],
    ["CONNECT","Edward","Bob"],
    ["CONNECT","Dennis","Charlie"],
    ["CONNECT","Alice","Nicole"],
    ["CONNECT","Pam","Edward"],
    ["DISCONNECT","Dennis","Charlie"],
    ["CONNECT","Dennis","Edward"],
    ["CONNECT","Charlie","Bob"]
]
;
          
function connections(length){
    
    let user = [[],[]];
   
    let MapCOnnections = {};
    for(let [eventName,leftUser, rightUser] of events){
       if(! MapCOnnections[leftUser])  MapCOnnections[leftUser] =[];
       if(! MapCOnnections[rightUser])  MapCOnnections[rightUser] =[];
       
       if(eventName == 'CONNECT'){
           MapCOnnections[leftUser].push(rightUser);
            MapCOnnections[rightUser].push(leftUser);
       }
       else  if(eventName == 'DISCONNECT'){
         let findIndexLeft = MapCOnnections[rightUser].findIndex(x => x == leftUser);
           let findIndexRight = MapCOnnections[leftUser].findIndex(x => x == rightUser);
         MapCOnnections[rightUser].splice(findIndexLeft,1);
          MapCOnnections[leftUser].splice(findIndexRight,1);
       }
       
        
       
    }
     console.log(MapCOnnections)
    for (let item in MapCOnnections){
       let getConnectionCount = MapCOnnections[item].length;
       if(getConnectionCount >= length)
        user[1].push(item);
        else if(getConnectionCount < length)
        user[0].push(item);
      
    }
    console.log(user)
}
connections(2);