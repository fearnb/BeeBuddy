let session = false;
let bees = [];
let scrapped = 0;

document.getElementById('session').style.display = "none";

document.getElementById('start').onclick = start;
document.getElementById('end').onclick = start;
document.getElementById('record').onclick = recordBee;

function start(){
    if(session == false){
        session = true;
        document.getElementById('start').style.display = "none";
        document.getElementById('session').style.display = "block";
        document.getElementById("beeCount").innerHTML = bees.length;
        document.getElementById("beeScrapped").innerHTML = scrapped;
        document.getElementById("beeGood").innerHTML = bees.length - scrapped;

    }else{
        session = false;
        document.getElementById('start').style.display = "block";
        document.getElementById('session').style.display = "none";

    }
}

function recordBee(){
    if (session == false){
        console.log("wtf")
    }else{
        let start = new Date().getTime()
        let startDate = new Date()
        // let end = start + 5000
        let end = start + 2*60000
        let endDate = new Date(end);
        let bee = {
            "id" : bees.length,
            "recordStart" : start,
            "recordStartDate" : startDate,
            "recordEnd" : end,
            "recordEndDate" : endDate,
            "hops" : []
        }

        document.getElementById('beeCounter').style.display = "block";
        document.getElementById('record').style.display = "none"; //hide record button
        document.getElementById('end').style.display = "none";
        document.getElementById('loggers').style.display = "block";

        long = () =>{
            bee['hops'].push({type : 'l',
                              time : new Date()})
        }

        short = () =>{
            bee['hops'].push({type : 's',
                              time : new Date()})
        }

        scrap = () => {
            bee['hops'].push('scrapped');
            end = new Date().getTime();
            endDate = new Date();
            bee['recordEnd'] = end;
            bee['recordEndDate'] = endDate;
            countDownDate = bee['recordEnd'];
            scrapped++;
            document.getElementById("beeCount").innerHTML = bees.length;
            document.getElementById("beeScrapped").innerHTML = scrapped;
            document.getElementById("beeGood").innerHTML = bees.length - scrapped;
        }

        document.getElementById('longLogger').onclick = long;
        document.getElementById('shortLogger').onclick = short;
        document.getElementById('scrap').onclick = scrap;

        // Set the date we're counting down to
        var countDownDate = bee['recordEnd'];

        // Update the count down every 1 second
        var x = setInterval(function() {

         // Get today's date and time
         var now = new Date().getTime();

         // Find the distance between now and the count down date
         var distance = countDownDate - now;

         // Time calculations for minutes and seconds
         var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
         var seconds = Math.floor((distance % (1000 * 60)) / 1000);

          // Display the result in the element with id="timer"
          document.getElementById("timer").innerHTML =  minutes + "m " + seconds + "s ";

          // If the count down is finished, end the session
          if (distance <= 0) {
           clearInterval(x);
           bees.push(bee)
           document.getElementById("beeCount").innerHTML = bees.length;
           document.getElementById("beeScrapped").innerHTML = scrapped;
           document.getElementById("beeGood").innerHTML = bees.length - scrapped;
           document.getElementById('beeCounter').style.display = "none";
           document.getElementById('record').style.display = "block";
           document.getElementById('end').style.display = "block";
           document.getElementById('loggers').style.display = "none";
          }
        }, 1000);
    }

}

function sendMail() {
    beeString = JSON.stringify(bees)
    goodBees = bees.length - scrapped
    var link = "mailto:fearnbishop@gmail.com"
             + "?subject=" + encodeURIComponent("This is extremely stupid")
             + "&body=" + encodeURIComponent("good bees: " + goodBees + "\n" + beeString)
    ;
    
    window.location.href = link;
    bees = []
    scrapped = 0;
}