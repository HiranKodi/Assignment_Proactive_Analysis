function Product(name, price){
    this.name = name;
    this.price = price;

    this.getDetails = function(){
        console.log(`Product name: ${this.name} \nPrice: ${this.price}\n`);
    }
}

function updatePrice(item, newPrice){
    let newItem = Object.assign({}, item);
    newItem.price = newPrice;
    return newItem;
}

let product1 = new Product('milk', 1.50);
product1.getDetails();

let product2 = updatePrice(product1, 1.75);
product2.getDetails();

