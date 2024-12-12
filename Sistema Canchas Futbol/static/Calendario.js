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