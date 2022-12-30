fetch("api/user/auth").then(function(response){
    return response.json()
}).then(function(data){
    console.log(data);
    const memberName = document.querySelector(".memberName");
    memberName.textContent = data.data.name;
})
fetch("api/member").then(function(response){
    return response.json();
}).then((data)=>{
    // console.log(data.data);
    // let Frame = ()
    let historyOrder = document.querySelector(".historyOrder")
    // console.log(historyOrder)   
    let datas = data.data
    for(let i = 0 ; i < data.data.length; i++){

        let one = datas[i].images.split(", ", 1)
        // console.log(one)
        historyOrder.innerHTML += ('<div class="historyOrderFrame">'+
        '<div class="orderImage">'+
        '<img src = "'+one[0] +'">'+'</div>'+
        '<div class="orderFrame">'+
            '<div class="orderItem"><div>訂單編號 : </div><div class="number">'+data.data[i].number+'</div></div>'+
            '<div class="orderItem"><div>日期 : </div><div class="date">'+data.data[i].date+'</div></div>'+
            '<div class="orderItem"><div>時間 : </div><div class="time">'+data.data[i].time+'</div></div>'+
            '<div class="orderItem"><div>金額 : </div><div class="price">'+data.data[i].price+'</div></div>'+
        '</div>'+'</div>')
    //     let number =document.querySelector(".number")
    //     let date = document.querySelector(".date")
    //     let time = document.querySelector(".time")
    //     let price = document.querySelector(".price")
    //     number.textContent = data.data[i].number;
    //     date.textContent = data.data[i].date;
    //     time.textContent = data.data[i].time;
    //     price.textContent = data.data[i].price;
    }
})

let historyItem = document.querySelectorAll(".historyitem")
console.log(historyItem)
historyItem.forEach(function(ele){
    console.log(ele)
    ele.addEventListener("click", ()=>{
        console.log(ele.className)
        ele.className = "historyitem borderbottom"
    })
});