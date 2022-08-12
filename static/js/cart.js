var updateBtns = document.getElementsByClassName('update-cart') // Store all html elements with update-cart class.

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){  // Give each element the ability to check for clicks and on click perform funtion.
        var productId = this.dataset.product // Store product that was clicked on.
        var action = this.dataset.action // Store action that was clicked on.
        console.log('productId: ', productId, 'action: ', action)
        console.log('User: ', user)
        if( user == 'AnonymousUser'){ // Check if user is not logged in.
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

// Create cart for users not logged in and store in cookie.
function addCookieItem(productId, action){
    console.log("User not logged in.")

    // Add to cart functionality
    if(action == "add"){
        if(cart[productId] == undefined){
            cart[productId] = {"quantity":1}
        } else {
            cart[productId]["quantity"] = cart[productId]["quantity"] + 1
        }
    }

    // Remove from cart functionality
    if(action == "remove"){
        cart[productId]["quantity"] = cart[productId]["quantity"] - 1

        if(cart[productId]["quantity"] <= 0){
            delete cart[productId]
            console.log("Item removed.")
        }
    }

    console.log("Cart: ", cart)
    //Update cookie
    document.cookie = "cart = " + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    console.log('User is logged in. Data sent.')
    var url = '/update_item/' // Store where data is sent. Data is sent to update_item.
    fetch(url, { // Send data to url
        method: 'POST',
        headers: {'Content-Type':'application/json', 'X-CSRFToken':csrftoken, },
        body: JSON.stringify({'productId':productId, 'action':action, })
    })
    .then((response) => { // Receive response from url and convert to json value.
        return response.json()
    })
    .then((data) => {
        console.log('data: ', data)
        location.reload() // Reload page.
    })
}