let pizzas = [];
let indexPizzaSeleccionado;
function addPizza(){
    // Obtener valores del formulario usando ID
    let nombreCompleto = document.querySelector('#nombreCompleto').value;
    let direccion = document.querySelector('#direccion').value;
    let telefono = document.querySelector('#telefono').value;
    let tamanio = document.querySelector('input[name="tamanio"]:checked').value;
    let ingredientesSeleccionados = document.querySelectorAll('input[name="ingredientes"]:checked');
    

    let cantidadIngredientes = ingredientesSeleccionados.length;
    let valoresIngredientes = [];
    ingredientesSeleccionados.forEach(ingrediente => {
        valoresIngredientes.push(ingrediente.value);
    });
    let numeropizza = document.querySelector('#numeropizza').value;
    let ingredientesComoString = valoresIngredientes.join(', ');
    let pizza={};
    subtotal= parseInt(tamanio)+(parseInt(cantidadIngredientes)*10)
    if (tamanio == '40'){
        tamanio= 'Chica'

    }else if(tamanio == '80'){
        tamanio= 'Mediana'
    }else if(tamanio == '120'){
        tamanio= 'Grande'
    }
    console.log(nombreCompleto, direccion, telefono, tamanio,ingredientesSeleccionados,valoresIngredientes,ingredientesComoString, cantidadIngredientes, numeropizza,subtotal); 
    pizza.tamanio=tamanio
     pizza.ingredientes=ingredientesComoString;
     pizza.numPizza=numeropizza;
     pizza.subtotal=subtotal;
     pizzas.push(pizza);

     cargarTabla();
}

function cargarTabla(){
    let cuerpoE="";
    pizzas.forEach(function (pizza){
        let registroE =  
                '<tr onclick="selectPizza('+ pizzas.indexOf(pizza) +');">'+
                '<td>' + pizza.tamanio + '</td>' +
                '<td>' + pizza.ingredientes + 
                '<td>' + pizza.numPizza + '</td>' +
                '<td>' + pizza.subtotal + '</td></tr>' ; 
        cuerpoE += registroE;
    });
    console.log(cuerpoE);
    document.getElementById("tblPizza").innerHTML =cuerpoE;

}

function limpiar(){
    document.querySelector('#nombreCompleto').value='';
    document.querySelector('#direccion').value='';
    document.querySelector('#telefono').value='';
    document.querySelector('#numeropizza').value='';


}

function selectPizza(index){
    if (pizzas[index].tamanio == 'Chica'){
        t='40'

    } else if (pizzas[index].tamanio == 'Mediana'){
        t='80'

    }else if (pizzas[index].tamanio == 'Grande'){
        t='120'

    }
    document.querySelector('input[name="tamanio"]:checked').value = t;

    let ingredientesSeleccionados = document.querySelectorAll('input[name="ingredientes"]');
    ingredientesSeleccionados.forEach(checkbox => {
        checkbox.checked = pizzas[index].ingredientes.includes(checkbox.value);
    });

    document.querySelector('#numeropizza').value = pizzas[index].numPizza;
    indexPizzaSeleccionado = index;
    console.log(indexPizzaSeleccionado);
}
function eliminar(){
    pizzas.splice(indexPizzaSeleccionado);   
    cargarTabla();   

}


function modificar(){
      // Obtener valores del formulario usando ID
      let nombreCompleto = document.querySelector('#nombreCompleto').value;
      let direccion = document.querySelector('#direccion').value;
      let telefono = document.querySelector('#telefono').value;
      let tamanio = document.querySelector('input[name="tamanio"]:checked').value;
      let ingredientesSeleccionados = document.querySelectorAll('input[name="ingredientes"]:checked');
      
  
      let cantidadIngredientes = ingredientesSeleccionados.length;
      let valoresIngredientes = [];
      ingredientesSeleccionados.forEach(ingrediente => {
          valoresIngredientes.push(ingrediente.value);
      });
      let numeropizza = document.querySelector('#numeropizza').value;
      let ingredientesComoString = valoresIngredientes.join(', ');

      subtotal= parseInt(tamanio)+(parseInt(cantidadIngredientes)*10)
      if (tamanio == '40'){
          tamanio= 'Chica'
  
      }else if(tamanio == '80'){
          tamanio= 'Mediana'
      }else if(tamanio == '120'){
          tamanio= 'Grande'
      }
      console.log(nombreCompleto, direccion, telefono, tamanio,ingredientesSeleccionados,valoresIngredientes,ingredientesComoString, cantidadIngredientes, numeropizza,subtotal);

      pizzas[indexPizzaSeleccionado].tamanio=tamanio
       pizzas[indexPizzaSeleccionado].ingredientes=ingredientesComoString;
       pizzas[indexPizzaSeleccionado].numPizza=numeropizza;
       pizzas[indexPizzaSeleccionado].subtotal=subtotal;
       cargarTabla();


}


function terminar() {
    let total=0
    for (let i = 0; i < pizzas.length; i++) {
       n= parseInt(pizzas[i].numPizza)
       s= parseInt(pizzas[i].subtotal)
        total=total+(n*s) //60

      }
      console.log(total)
    var resultado = window.confirm("El costo total es de:"+total+"¿Deseas continuar?");
    
    if (resultado) {

        
        enviarDatos(total);
    } else {
        var boton = document.getElementById("Actualizar");
        boton.disabled = false;
    }
}


function enviarDatos(total) {
  
        let nombreCompleto = document.querySelector('#nombreCompleto').value;
        let direccion = document.querySelector('#direccion').value;
        let telefono = document.querySelector('#telefono').value;
    
        // Crear un objeto que contenga la información del formulario y el arreglo de pizzas
        let data = {
            nombreCompleto: nombreCompleto,
            telefono: telefono,
            direccion: direccion,
            total:total,
            pizzas: pizzas
        };
    
        // Instancia de AJAX
        var xhr = new XMLHttpRequest();
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        alert("Guardado exitoso");
                    } else {
                        document.getElementById("error-message").innerText = response.message;
                    }
                } else {
                    alert("Error en la solicitud AJAX");
                }
            }
        };
    
        xhr.open("POST", "/vista", true);
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send(JSON.stringify(data));
    }
    
