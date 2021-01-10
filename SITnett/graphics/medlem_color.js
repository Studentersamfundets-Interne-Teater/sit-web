const memberCard = document.getElementsByClassName('card');

for (i=0; i<memberCard.length; i++){
    let memberType = memberCard[i].getElementsByClassName('card-container');
    if (memberType[0].innerHTML.includes('Kulisse')){
        memberCard[i].setAttribute("style", "background-color:#DED5CE;");
    } else if (memberType[0].innerHTML.includes('Kostyme')){
        memberCard[i].setAttribute("style", "background-color:#97B5C3;");
    } else {
        memberCard[i].setAttribute("style", "background-color:#F99FA3;");
    }
};