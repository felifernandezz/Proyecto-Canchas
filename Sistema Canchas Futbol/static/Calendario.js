let monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

let currentDate = new Date();
let currentDay = currentDate.getDate();
let monthNumber = currentDate.getMonth();
let currentYear = currentDate.getFullYear()

let dates = document.getElementById('dates');
let month = document.getElementById('month');
let year = document.getElementById('year');

let prevMonthDOM = document.getElementById('prev-month');
let nextMonthDOM = document.getElementById('next-month');

month.textContent = monthNames[monthNumber];
year.textContent = currentYear.toString();

prevMonthDOM.addEventListener('click', ()=>lastMonth());
nextMonthDOM.addEventListener('click', ()=>nextMonth());

writeMonth(monthNumber);

function writeMonth(month){
    dates.innerHTML = '';
    for(let i = startDay(); i>0;i--){
        dates.innerHTML += `<div class="calendar__date calendar__item calendar__last-days">${getTotalDays(monthNumber-1)-(i-1)}</div>`;
    }


    for(let i=1; i<=getTotalDays(month); i++){
        if(i===currentDay){
            dates.innerHTML += `<div class="calendar__date calendar__item calendar__today">${i}</div>`;
        }else{
            dates.innerHTML += `<div class="calendar__date calendar__item">${i}</div>`;         
        }
    }
}

function getTotalDays(month){
    if(month === -1) month = 11;

    if (month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 9 || month == 11){
        return 31;;
    } else if (month == 3 || month == 5 || month == 8 || month == 10){
        return 30;
    } else {
        return isLeap() ? 29:28;
    }
}

function isLeap(){
    return ((currentYear%100 !==0) && (currentYear % 4 === 0) || (currentYear % 400 === 0));
}

function startDay(){
    let start = new Date(currentYear, monthNumber, 1); 
    return ((start.getDay()-1) === -1) ? 6 : start.getDay()-1;
}

function lastMonth(){
    if(monthNumber !== 0){
        monthNumber--;
    }else{
        monthNumber=11;
        currentYear--;
    }
    setNewDate();
}

function nextMonth(){
    if(monthNumber !== 11){
        monthNumber++;
    }else{
        monthNumber=0;
        currentYear++;
    }
    setNewDate();
}

function setNewDate(){
    currentDate.setFullYear(currentYear,monthNumber,currentDay);
    month.textContent = monthNames[monthNumber];
    year.textContent = currentYear.toString(); 
    writeMonth(monthNumber);
}

//popup funct

document.querySelectorAll('.calendar__date').forEach(day => {
    day.addEventListener('click', () => openPopup(day.textContent));
  });

  async function openPopup(day) {
    const popup = document.getElementById('popup');
    const timeSlots = document.getElementById('time-slots');
    timeSlots.innerHTML = ''; // Limpia los horarios previos

    // ID de la cancha (puedes adaptarlo según tu lógica)
    const canchaId = 1; // Ejemplo: id fijo o dinámico
    const fecha = `${new Date().getFullYear()}-${(new Date().getMonth() + 1).toString().padStart(2, '0')}-${day.padStart(2, '0')}`;

    // Obtén los horarios disponibles desde la API
    const horarios = await obtenerHorariosDisponibles(canchaId, fecha);

    if (horarios.length === 0) {
        timeSlots.innerHTML = '<p>No hay horarios disponibles para esta fecha.</p>';
    } else {
        horarios.forEach(horario => {
            const timeButton = document.createElement('button');
            timeButton.textContent = `${horario.hora_inicio} - ${horario.hora_fin}`;
            timeButton.addEventListener('click', () => {
                alert(`Reserva confirmada para el día ${day} a las ${horario.hora_inicio}`);
                closePopup();
            });
            timeSlots.appendChild(timeButton);
        });
    }
    popup.classList.remove('hidden');
}

function closePopup(){
    const popup = document.getElementById('popup');
    popup.classList.add('hidden');
}


async function obtenerHorariosDisponibles(cancha_id, fetchCanchas) {
    try {
        const response = await fetch(`http://tu-servidor.com/horarios-disponibles?cancha_id=${canchaId}&fecha=${fecha}`);
        if (!response.ok){
            throw new Error('Erro al obtener los horarios disponibles');
        }
        const horarios = await response.json();
        return horarios;
    } catch (error){
        console.error(error);
        return[];
    }
}

function cargarHorarios(fechaSeleccionada){
    //llama a la api del servidor flask
    fetch(`/api/horarios/${fechaSeleccionada}`)
        .then(response => {
            if (!response.ok){
                throw new Error('Error al obtener los horarios');
            }
            return response.json();
        })
        .then(data => {
            const timeSlots = document.getElementById('time-slots'); //contenedor de horarios
            timeSlots.innerHTML = ''; //limpia los horarios anteriores
        
            //agrega cada horario disponible como un boton
            data.forEach(hora => {
                const btn = document.createElement('button');
                btn.textContent = hora;
                btn.classList.add('time-button');
                timeSlots.appendChild(btn);
            });
        })
        .catch(error => console.error('Error:', error));
}

//evento para llamar a la funcion cunado se seleeccione una fecha
const calendarDates = document.querySelectorAll('.calendar__dates div');
calendarDates.forEach(date => {
    date.addEventListener('click', () => {
        const fechaSeleccionada = date.dateset.date;
        cargarHorarios(fechaSeleccionada);
    });
});

const courtButtons = document.querySelectorAll('.court-button');
courtButtons.forEach(button => {
    button.addEventListener('click', () => {
        courtButtons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    })
})

const today = new Date()
const dates = document.querySelectorAll('.calendar__dates div');

dates.forEach(Date => {
    const selectedDate = new Date(data.dataset.date);
    if(selectedDate < today){
        date.classList.add('disabled');
    }
})

fetch(`api/horarios/${fechaSeleccionada}`)
    .then(response => response.json())
    .then(data => {
        const timeSlots = document.getElementById('time-slots');
        timeSlots.innerHTML = '';
        data.forEach(hora => {
            timeSlots.innerHTML += `<button>${hora}</button>`;
        });
    });


// Validación del formulario de cliente
const form = document.querySelector('.client-data'); // Selecciona el formulario

if (form) { // Asegúrate de que el formulario exista
    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Previene el envío por defecto

        // Captura los valores de los campos
        const nombre = form.querySelector('input[name="nombre"]').value.trim();
        const apellido = form.querySelector('input[name="apellido"]').value.trim();
        const telefono = form.querySelector('input[name="telefono"]').value.trim();

        // Expresión regular para validar el teléfono (10 dígitos)
        const telefonoRegex = /^\d{10}$/;

        // Validación de los campos
        if (nombre === '') {
            alert('Por favor, ingresa tu nombre.');
        } else if (apellido === '') {
            alert('Por favor, ingresa tu apellido.');
        } else if (!telefonoRegex.test(telefono)) {
            alert('Por favor, ingresa un número de teléfono válido (10 dígitos).');
        } else {
            // Si todo está correcto, envía el formulario
            alert('Formulario enviado correctamente. ¡Gracias por tu reserva!');
            form.submit(); // Envía el formulario
        }
    });
}
