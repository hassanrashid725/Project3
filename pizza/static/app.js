//cart
let cart=[];
let selectedSizes=[];
let selectedToppings=[];
let buttonsDOM = [];
var productsGlobal,categoriesGlobal,totalAmount,cartPrices=[],extraPrice=[],extraCounter=0;
//getting the products
class Products {
  async getProducts(){
    var t="a";

    $.ajax(
        {
            type:"GET",
            url: "/getmenu",
            async:false,
            data:{
              post_id: t
            },
            success: function(data)
            {
               let products = JSON.parse(data);
               products = products.map(item =>{
               const {category,itemName,priceSmall,priceLarge} = item.fields;
               const {pk} = item;
               return {pk,category,itemName,priceLarge,priceSmall};
              });
               productsGlobal = products;
            }
         }) //ajax

  } //getProducts end

  async getcategories(){
    var t="a";

    $.ajax(
        {
            type:"GET",
            url: "/getcategories",
            async:false,
            data:{
              post_id: t
            },
            success: function(data)
            {
               let categories = JSON.parse(data);
               categories = categories.map(item =>{
               const {categoryName} = item.fields;
               const {pk} = item;
               return {pk,categoryName};
              });
               categoriesGlobal = categories;
            }
         }) //ajax

  } //getProducts end

} //class Products end


//displaying products
class UI {
  getAddtoCartButtons(){
    const buttons = [...document.querySelectorAll(".toppings-selection-btn")];
    buttonsDOM = buttons;
    buttons.forEach(button =>{
      let id = button.dataset.item;
      button.addEventListener("click", event => {
      let cartItem = Storage.getProduct(id);
      let category = Storage.getcategory(cartItem);
      cartItem.category = category.categoryName;
      cart = [...cart, cartItem];
      Storage.saveCart(cart);
      this.setCartValues(cart,id);
      this.addCartItem(cartItem,null);
      // this.showCart();
      });
    });
  }

  setCartValues(cart,id){
    if(id != null)
    {
      let str1a = "#size_";
      let size_id = str1a.concat(id);
      let selected_size = $(size_id).val();
      let str1b = "#toppings_";
      let toppings_id = str1b.concat(id);
      let selected_toppings = $(toppings_id).val();
      var n;
      if (selected_toppings != undefined)
      {
        for(var m=0;m<selected_toppings.length;m++)
        {
          if(selected_toppings[m].includes("+"))
          {
              n = selected_toppings[m].indexOf("+");
              n--;
              selected_toppings[m] = selected_toppings[m].slice(0, n);
          }
        }
      }
      selectedToppings.push(selected_toppings);
      selectedSizes.push(selected_size);
      localStorage.setItem("sizes",JSON.stringify(selectedSizes));
      localStorage.setItem("toppings",JSON.stringify(selectedToppings));

    }
      let sizes = JSON.parse(localStorage.getItem("sizes"));
      let toppings = JSON.parse(localStorage.getItem("toppings"));
      let price;

    let tempTotal = 0;
    let itemsTotal = 0;
    var k=0;
    extraPrice=[];
    cartPrices=[];
    for(var j=0;j<sizes.length;j++)
    {     var extraAddOn=0;

          while(sizes[j] == "Deleted")
          {
            j++;
          }
          if(j == sizes.length)
          {
            break;
          }
          if(sizes[j] == "small")
          {
             price = cart[k].priceSmall;
          }
          else {
             price = cart[k].priceLarge;
          }
          if (cart[k].category == "Subs")
          {
            $.ajax(
                {
                    type:"GET",
                    url: "/getsubsextraprices",
                    async:false,
                    data:{
                      post_id: "t"
                    },
                    success: function(data)
                    {
                       let subsExtraPrices = JSON.parse(data);
                       subsExtraPrices = subsExtraPrices.map(item =>{
                       const {name,price} = item.fields;
                       return {name,price};
                      });
                      for(var m=0;m<toppings[j].length;m++)
                      {
                        for(var n=0;n<subsExtraPrices.length;n++)
                        {
                          if(toppings[j][m]==subsExtraPrices[n].name)
                          {
                            price=parseFloat(price) + parseFloat(subsExtraPrices[n].price);
                            extraAddOn = extraAddOn + parseFloat(subsExtraPrices[n].price);
                            console.log(price);
                          }
                        }
                      }
                      extraPrice.push(extraAddOn);
                    }

                 }) //ajax

          }
        k++;
        cartPrices.push(price);
        tempTotal += parseFloat(price);
        itemsTotal += 1;
    }

    totalAmount = tempTotal.toFixed([2]);

    if(totalAmount == undefined ||  totalAmount<=0)
    {
      document.querySelector("#checkout-btn").onclick=function() {
          alert("Cart is empty.");
      }
      document.querySelector("#checkout-btn").removeEventListener("click",this.checkoutCart);
    }
    else {
      document.querySelector("#checkout-btn").onclick=function() {
          location.href='/checkout/';
      }
      document.querySelector("#checkout-btn").addEventListener("click",this.checkoutCart);
    }
    document.querySelector(".cart-items").innerText = itemsTotal;
    document.querySelector(".cart-total").innerText = tempTotal.toFixed([2]);
  }

  addCartItem(item,index){
    let sizes = JSON.parse(localStorage.getItem("sizes"));
    let toppings = JSON.parse(localStorage.getItem("toppings"));
    let price;
    const div = document.createElement('div');
    div.classList.add('cart-item');
    if(index == null)
    {
      if(sizes[sizes.length-1] == "small")
      {
        price = item.priceSmall;
      }
      else {
        price = item.priceLarge;
      }
      if(item.category=="Subs" && toppings[toppings.length-1].length>0)
      {
        console.log(extraPrice[extraPrice.length-1]);
        price=parseFloat(price)+extraPrice[extraPrice.length-1];
        price=price.toFixed([2]);
      }
      div.innerHTML=`<img src="static/pizza-logo.jpg" alt="pizza">
                  <div>
                    <h4>${item.category}</h4>
                    <h4>${item.itemName}</h4>
                    <h4 id=cartToppings${toppings.length-1}>${toppings[toppings.length-1]}</h4>
                    <h4 id=cartSize${sizes.length-1}>${sizes[sizes.length-1]}</h4>
                    <h5>$${price}</h5>
                    <span class="remove-item" data-infoId=${toppings.length-1} data-id=${item.pk}
                    >Remove</span>
                  </div>`;

      document.querySelector(".cart-content").appendChild(div);

      if(toppings[toppings.length-1] == null || toppings[toppings.length-1].length < 1)
      {
        document.getElementById(`cartToppings${toppings.length-1}`).outerHTML = "";
      }
      if(sizes[sizes.length-1] == null || sizes[sizes.length-1].length < 1)
      {
        document.getElementById(`cartSize${sizes.length-1}`).outerHTML = "";
      }


    }

    else {

      if(sizes[index] == "small")
      {
        price = item.priceSmall;
      }
      else {
        price = item.priceLarge;
      }

      if(item.category=="Subs")
      {
        if(toppings[index].length>0)
        {
          console.log(extraPrice[extraCounter]);
          price=parseFloat(price)+extraPrice[extraCounter];
          price=price.toFixed([2]);
        }
        extraCounter++;
      }

      div.innerHTML=`<img src="static/pizza-logo.jpg" alt="pizza">
                  <div>
                    <h4>${item.category}</h4>
                    <h4>${item.itemName}</h4>
                    <h4 id=cartToppings${index}>${toppings[index]}</h4>
                    <h4 id=cartSize${index}>${sizes[index]}</h4>
                    <h5>$${price}</h5>
                    <span class="remove-item" data-infoId=${index} data-id=${item.pk}
                    >Remove</span>
                  </div>`;

      document.querySelector(".cart-content").appendChild(div);

      if(toppings[index] == null || toppings[index].length < 1)
      {
        document.getElementById(`cartToppings${index}`).outerHTML = "";
      }
      if(sizes[index] == null || sizes[index].length < 1)
      {
        document.getElementById(`cartSize${index}`).outerHTML = "";
      }

    }
  }

  showCart(){
    document.querySelector(".cart-overlay").classList.add('transparentBcg');
    document.querySelector(".cart").classList.add('showCart');

  }

  hideCart(){
    document.querySelector(".cart-overlay").classList.remove('transparentBcg');
    document.querySelector(".cart").classList.remove('showCart');
  }

  showSidebar(){
    document.querySelector(".sidebar-overlay").classList.add('transparentBcg');
    document.querySelector(".sidebar").classList.add('showSidebar');

    $(document).click(function(e) {
    	if ($(e.target).is('.sidebar-overlay')) {
        document.querySelector(".sidebar-overlay").classList.remove('transparentBcg');
        document.querySelector(".sidebar").classList.remove('showSidebar');
        }
    });

    document.querySelectorAll('.sidebar-options').forEach(a => {
      a.onclick =  function() {
        document.querySelector(".sidebar-overlay").classList.remove('transparentBcg');
        document.querySelector(".sidebar").classList.remove('showSidebar');
      };
    });
  }

  hideSidebar(){
    document.querySelector(".sidebar-overlay").classList.remove('transparentBcg');
    document.querySelector(".sidebar").classList.remove('showSidebar');
  }


  checkoutCart(){
    var csrftoken = getCookie('csrftoken');
    let toppings = JSON.parse(localStorage.getItem("toppings"));
    let sizes = JSON.parse(localStorage.getItem("sizes"));
    for (var m=0;m<toppings.length;m++)
    {
      if(toppings[m]=="Deleted")
      {
        toppings.splice(m,1);
        sizes.splice(m,1);
        m--;
      }
    }
    var n=0;
    var t=2*toppings.length;
    for(var m=0;m<t;m++)
    {
      toppings.splice(m,0,sizes[n]);
      m++;
      n++;
    }
    console.log(cartPrices);
    cart = [...cart, cartPrices, totalAmount, toppings];
    console.log(cart);
          $.ajax({
                  type:'POST',
                  headers: { "X-CSRFToken": csrftoken },
                  url:'/checkout/',
                  data:{
                      'arr': JSON.stringify(cart),
                  },
                   success:function(data){
                     if(data.result == "SUCCESS")
                     {
                       cart=[];
                       selectedSizes=[];
                       selectedToppings=[];
                       Storage.saveCart(cart);
                       localStorage.setItem("sizes",JSON.stringify(selectedSizes));
                       localStorage.setItem("toppings",JSON.stringify(selectedToppings));
                     }
                   },
                  error : function(xhr,errmsg,err) {
                  console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
              }
              });

  }

  setupAPP(){
    cart = Storage.getCart();
    if (cart.length > 0)
    { Storage.getSelectedChoices();
      this.setCartValues(cart,null);
      this.populateCart(cart);
    }

    document.querySelector(".cart-btn").addEventListener("click",this.showCart);
    document.querySelector(".close-cart").addEventListener("click",this.hideCart);
    document.querySelector("#sidebar-btn").addEventListener("click",this.showSidebar);
    document.querySelector(".close-sidebar").addEventListener("click",this.hideSidebar);


    if(totalAmount == undefined ||  totalAmount<=0)
    {
      document.querySelector("#checkout-btn").onclick=function() {
          alert("Cart is empty.");
      }
    }
    else {
      document.querySelector("#checkout-btn").onclick=function() {
          location.href='/checkout/';
      }
      document.querySelector("#checkout-btn").addEventListener("click",this.checkoutCart);
    }
    // document.querySelector("#checkout-btn").removeEventListener("click",this.checkoutCart);


  }

  populateCart(cart){
  var k=0;
  let sizes = JSON.parse(localStorage.getItem("sizes"));
    for(var j=0;j<sizes.length;j++)
    {
      while(sizes[j] == "Deleted")
      {
        j++;
      }
      if(j == sizes.length)
      {
        break;
      }
      this.addCartItem(cart[k],j);
      k++;
    }
  }

  cartLogic(){
    document.querySelector(".cart-content").addEventListener('click', event =>{
      if (event.target.classList.contains("remove-item"))
      {
        document.querySelector(".cart-content").removeChild(event.target.parentElement.parentElement);
        selectedToppings.splice(event.target.dataset.infoid, 1, "Deleted");
        selectedSizes.splice(event.target.dataset.infoid, 1, "Deleted");
        localStorage.setItem("sizes",JSON.stringify(selectedSizes));
        localStorage.setItem("toppings",JSON.stringify(selectedToppings));
        this.removeItem(event.target.dataset.id);
      }
    });
  }

  removeItem(id){
    for(var j=0;j<cart.length;j++)
    {
      if(cart[j].pk == id)
      {
        cart.splice(j,1);
        break;
      }
    }

    this.setCartValues(cart);
    Storage.saveCart(cart);
  }

} // class UI end

//local products
class Storage {
  static saveProducts(products){
    localStorage.setItem('products',JSON.stringify(products));
  }

  static savecategories(categories){
    localStorage.setItem('categories',JSON.stringify(categories));
  }

  static getProduct(id){
    let products = JSON.parse(localStorage.getItem("products"));
    return products.find(product => product.pk == id);
  }

  static getcategory(item){
    let categories = JSON.parse(localStorage.getItem("categories"));
    return categories.find(category => category.pk == item.category);
  }

  static saveCart(cart){
    localStorage.setItem('cart',JSON.stringify(cart));
  }

  static getCart(){
    return localStorage.getItem('cart')?JSON.parse(localStorage.getItem('cart')):[];
  }

  static getSelectedChoices(){
    selectedToppings = JSON.parse(localStorage.getItem("toppings"));
    selectedSizes = JSON.parse(localStorage.getItem("sizes"));
  }

}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// document.addEventListener("click", event => {
//   alert("A");
// });



document.addEventListener("DOMContentLoaded",()=>{
  const ui = new UI();
  const products = new Products();

  ui.setupAPP();
  products.getcategories().then(() =>{
    products.getProducts().then(() =>{
      Storage.saveProducts(productsGlobal);
      Storage.savecategories(categoriesGlobal);
      ui.getAddtoCartButtons();
      ui.cartLogic();
    });
  });


  document.querySelectorAll('.bag-btn').forEach(button => {
    button.onclick =  function() {
      var buttons = document.getElementsByClassName('toppings-selection-hidden');

      var i = button.dataset.id;
      i=parseInt(i);
      i--;
      buttons[i].style.visibility = "visible";
      for(var j=0; j< buttons.length; j++)
      {
          if (j!=i)
          {
          buttons[j].style.visibility = "hidden";
          }
      }

    };
  });



});
