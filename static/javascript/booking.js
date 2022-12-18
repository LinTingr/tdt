fetch("/api/user/auth").then(function(response){
    return response.json()
}).then(function(data){
    if(data.data == null){
        window.location.href = "http://127.0.0.1:3000/"
    }else{
        console.log(data.data.name)
        document.querySelector(".no_booking").style.display = "none"
        const username = document.querySelector(".username")
        username.textContent = data.data.name
        const contactNameInput = document.querySelector(".contact_name_input")
        const contactEmailInput = document.querySelector(".contact_email_input")
        contactNameInput.setAttribute("value", data.data.name) 
        contactEmailInput.setAttribute("value", data.data.email) 
        fetch("/api/booking").then(function(response){
            return response.json()
        }).then(function(data){
            if(data.data){
                document.querySelector(".footer").style.height = "104px"
                const attraction = data.data.attraction
                const datadate = data.data
                const img = document.querySelector(".book_img")
                const bookname = document.querySelector(".bookname")
                const inforBookdate = document.querySelector(".infor_bookdate")
                const inforBooktime = document.querySelector(".infor_booktime")
                const inforBookcost = document.querySelector(".infor_bookcost")
                const inforBooklocal = document.querySelector(".infor_booklocal")
                const AllPrice = document.querySelector(".All_price")
                img.setAttribute("src", attraction.image)
                bookname.textContent = "台北一日遊 :" + attraction.name
                inforBookdate.textContent = datadate.date
                inforBooktime.textContent = datadate.time
                inforBookcost.textContent = "總價 : 新台幣 " + datadate.price + " 元"
                inforBooklocal.textContent = attraction.address
                AllPrice.textContent = datadate.price 
            }
            if(data.data == null){
                const section = document.querySelector(".section")
                const contactForm = document.querySelector(".contact_form")
                const paymentForm = document.querySelector(".payment_form")
                const confirm = document.querySelector(".confirm")
                section.style.display="none"
                contactForm.style.display="none"
                paymentForm.style.display="none"
                confirm.style.display="none"
                const hr = document.querySelectorAll(".booking_hr")
                hr.forEach(ele =>{
                    ele.style.display="none"
                })
                document.querySelector(".no_booking").style.display = "block"
                
            }
        })
    }
})

const deleteBooking = document.querySelector(".delete")
deleteBooking.addEventListener("click", ()=>{
    fetch("/api/booking",{
        method : "DELETE"
    }).then(function(response){
        return response.json()
    }).then((data)=>{
        if(data.ok){
            location.reload()
        }
    })
})