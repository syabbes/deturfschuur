function logout()
{
    // do nothing yet
    alert("Doet nog niks");
}

function generate_calendar(year, month)
{
    // array of months
    let months = ["Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli", "Augustus", "Sebtember", "Oktober", "November", "December"];
    // first day of the month
    let firstMonthDay = new Date(year, month, 1).getDay();
    // get the monday before the month
    // get the number of days to substract to get to monday
    let x;
    if (firstMonthDay === 0)
    {
        x = 6;
    }
    else
    {
        x = firstMonthDay - 1;
    }
    let firstDay = new Date(year, month, 1);
    firstDay.setDate(firstDay.getDate() - x);

    // calculate the next 42 days and add them in array
    // first day = firstDay
    const calendar_dates = [firstDay];
    // 41 days left to be calculated
    for (let i = 1; i < 42; i++)
    {
        // day to be added is the i'th date after the first one
        let newDate = new Date(firstDay);
        newDate.setDate(firstDay.getDate() + i);
        // add the day to the array
        calendar_dates.push(newDate);
    }
    
    // add month and year to calendar title
    let month_title = new Date(year, month);

    calendar_month = document.getElementById("calendar-month");
    calendar_month.innerText = months[month_title.getMonth()] + " " + month_title.getFullYear();
    // add month and year as attribute
    calendar_month.setAttribute("data-month", month_title.getMonth());
    calendar_month.setAttribute("data-year", month_title.getFullYear());
    // loop over every table cell
    let calendar_table = document.getElementById("calendar-body");
    // itterator for the array
    let itterator = 0;
    for (let i = 0; i < calendar_table.rows.length; i++)
    {
        let row = calendar_table.rows[i];
        for (let j = 0; j < row.cells.length; j++)
        {
            // remove classes from previous month if needed
            row.cells[j].classList.remove("deactivated");
            row.cells[j].classList.remove("today");
            // inner text of cell = the day of the month
            row.cells[j].innerText = calendar_dates[itterator].getDate();
            // add the date as attribute
            row.cells[j].setAttribute("data-date", calendar_dates[itterator].toDateString());

            // check if date is today
            const today = new Date();
            if (calendar_dates[itterator].toDateString() === today.toDateString())
            {
                // add class today
                row.cells[j].classList.add("today");
            }
            // check if date is in targeted month
            else if (calendar_dates[itterator].getMonth() !== month_title.getMonth())
            {
                row.cells[j].classList.add("deactivated");
            }
            // move itterator to next date
            itterator++;
        }
    }
    // At the end, call the get_appointments function
    get_appointments(month_title.getFullYear(), month_title.getMonth());
}

function load_calendar()
{
    if (document.getElementById("calendar-container"))
    {
        // get current month and year
        let date = new Date();
        let month = date.getMonth();
        let year = date.getFullYear();
        // call other function to generate the calendar
        generate_calendar(year, month);
    }
}

function next_month()
{
    let current_month = document.getElementById("calendar-month");
    generate_calendar(Number(current_month.getAttribute("data-year")), Number(current_month.getAttribute("data-month")) + 1);
}

function previous_month()
{
    let current_month = document.getElementById("calendar-month");
    generate_calendar(Number(current_month.getAttribute("data-year")), Number(current_month.getAttribute("data-month")) - 1);
}

document.addEventListener("DOMContentLoaded", load_calendar);

// eventlistener for the calendar
var modal = document.getElementById("modal");
var calendar = document.getElementById("calendar-body");
calendar.addEventListener("click", function(event){
    modal.style.display = "block";
    clicked_day = event.target;
    setbegintime();
    setendtime();
    // Remove all appointments
    let apps = document.getElementById("appointments")
    while (apps.hasChildNodes())
    {
        apps.removeChild(apps.children[0]);
    }
    get_appointments_day(clicked_day.dataset.date);
})

// eventlistener for close button of modal
document.getElementById("close-modal").addEventListener("click", function(){
    modal.style.display = "none";
});

// functions for setting a default time for the appointment
function setbegintime()
{
    let datetime_begin = document.getElementById("begin")
    let begindate = new Date(clicked_day.getAttribute("data-date"));
    begindate.setMinutes(begindate.getMinutes() - begindate.getTimezoneOffset());
    datetime_begin.value = begindate.toISOString().slice(0,16);
}
function setendtime()
{
    let datetime_einde = document.getElementById("einde")
    let enddate = new Date(clicked_day.getAttribute("data-date"));
    enddate.setHours(enddate.getHours() + 1);
    enddate.setMinutes(enddate.getMinutes() - enddate.getTimezoneOffset());
    datetime_einde.value = enddate.toISOString().slice(0,16);
}
// Function for getting the appointments in the calendar
var progress = null;
function get_appointments(y, m)
{
    if (progress)
    {
        progress.abort();
    }
    progress = $.ajax({
        url: 'app_month',
        type: 'GET',
        data: {month: (m + 1), year: y},
        success: function(response){
            // Fill the calendar wih the appointments
            // Loop over every appointment
            for (let i = 0; i < response.length; i++)
            {
                // Turn dates to Datestring for comparing
                beginday = new Date(response[i].begin).toDateString();
                endday = new Date(response[i].eind).toDateString();
                // Since appointments cant be longer than 1 day, just check if the begin and enddate is the same
                // If end and begindate are the same, search for the associated day in the calendar
                if (beginday == endday)
                {
                    // Add marker
                    add_marker(beginday);
                }
                else
                {
                    add_marker(beginday);
                    add_marker(endday);
                }
            }
            progress = null
        }
    })
}
// Define datetime format
const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
};
const datetime_format = new Intl.DateTimeFormat("nl-NL", options);
var list_of_appointments = {};
function get_appointments_day(day)
{
    $.ajax({
        url: 'app_day',
        type: 'GET',
        data: {day: day},
        success: function(response){
            // Store the response in global var
            list_of_appointments = response;
            // Get the div in which the appointments need to come
            appointment_div = document.getElementById("appointments");
            // loop over every appointment
            for (let i = 0; i < response.length; i++)
            {
                // Add appointment to the modal
                let app_div = document.createElement("div");
                app_div.setAttribute("data-id", response[i].afspraak_id);
                app_div.classList.add("app_div")
                let title = document.createElement("p");
                title.classList.add("rem-title", "app-title");
                title.innerText = response[i].titel;

                let time = document.createElement("p");
                time.classList.add("crimson-pro-regular", "app-time");
                let starttime = new Date(response[i].begin);
                let endtime = new Date(response[i].eind);
                // Check if begin and endtime are on the same day
                if (endtime.toDateString() == starttime.toDateString())
                {
                    // Show only hours and minutes
                    var string = (starttime.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'})) + " - " + (endtime.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'}));
                }
                else
                {
                    // Show full datetime in nl format
                    var string = (datetime_format.format(starttime)) + " - " + (datetime_format.format(endtime))
                }
                time.innerText = string

                // Add time and title to the div
                app_div.appendChild(title)
                app_div.appendChild(time)
                // Add div to the div for the appointments
                appointment_div.appendChild(app_div)
            }
        }
    })
}
function add_marker(date)
{
    // Check if there's already a marker
    string = `[data-date="${date}"]`;
    let cell = document.querySelector(string);
    if (cell == null)
    {
        return;
    }
    let m = cell.getElementsByTagName("p");
    if (m.length == 0)
    {
        // Add a new marker
        cell.insertAdjacentHTML("afterbegin",
        '<p class="app-marker top-0 end-0 text-align-center crimson-pro-regular rounded-circle">1</p>');
    }
    else
    {
        number = Number(m[0].innerText) + 1;
        m[0].innerText = number;
    }
}

// Eventlistener for the list of appointments
let list_apps = document.getElementById("appointments");
var div_popup = document.getElementById("update-appointment-popup")
let app_modal = document.getElementById("app-modal");
var is_delete;
var flag;
list_apps.addEventListener("click", function(event){
    let app_div = event.target.closest(".app_div");
    // Check if there is indeed an appointment
    if (!app_div)
    {
        return;
    }
    // Load the modal for the appointment
    load_app_info(app_div.getAttribute("data-id"));
});

// Eventlistener for all of the buttons of appointment modal
app_modal.addEventListener("click", function(event){
    let info_form = document.getElementById("info-form");
    inputs_info_form = info_form.elements;
    // Check if popup message is visible
    if (div_popup.classList.contains("show"))
    {
        div_popup.classList.remove("show");
    }
    // Else check which button is pressed
    else if (event.target.id == "close-app-modal")
    {
        app_modal.style.display = "none";
    }
    else if (event.target.id == "btn-update")
    {
        is_delete = false;
        div_popup.classList.add("show");
        console.log(is_delete);
    }
    else if (event.target.id == "btn-delete")
    {
        is_delete = true;
        div_popup.classList.add("show");
        console.log(is_delete);
    }

    if (event.target.id == "btn-all")
    {
        // Check status of is_delete
        if (is_delete === true)
        {
            flag = 2;
        }
        else
        {
            flag = 0;
        }
        // Update invisible input field
        inputs_info_form["updatedelete-flag"].value = flag;
        console.log(flag);
        info_form.submit();
    }
    else if (event.target.id == "btn-single")
    {
        if (is_delete === true)
        {
            flag = 3;
        }
        else
        {
            flag = 1;
        }
        // Update invisible input field
        inputs_info_form["updatedelete-flag"].value = flag;
        console.log(flag);
        info_form.submit();
    }
    // Also dont forget to add invisible input field which contains information about what should be updated/deleted (all/single) and (delete/update)
});

function load_app_info(app_id)
{
    console.log(app_id);
    console.log(list_of_appointments);
    // Get the form with its elements
    var form = document.getElementById("info-form");
    form_inputs = form.elements;
    // Loop over all the appointments and look for the appointment with the right id
    for (let i = 0; i < list_of_appointments.length; i++)
    {
        if (list_of_appointments[i].afspraak_id == app_id)
        {
            // Update the input fields with the data of json[i]
            form_inputs["app-titel"].value = list_of_appointments[i].titel;
            form_inputs["app-prijs"].value = list_of_appointments[i].prijs.toFixed(2);
            form_inputs["app-omschrijving"].value = list_of_appointments[i].omschrijving_prijs;
            form_inputs["app-extra"].value = list_of_appointments[i].extra.toFixed(2);
            form_inputs["app-omschrijving_extra"].value = list_of_appointments[i].omschrijving_extra;
            form_inputs["app-info"].value = list_of_appointments[i].info;
            // Convert times to datetime-local
            let app_begin = new Date(list_of_appointments[i].begin);
            app_begin.setMinutes(app_begin.getMinutes() - app_begin.getTimezoneOffset());
            let app_eind = new Date(list_of_appointments[i].eind);
            app_eind.setMinutes(app_eind.getMinutes() - app_eind.getTimezoneOffset());
            // Update time input fields
            form_inputs["app-begin"].value = app_begin.toISOString().slice(0,16);
            form_inputs["app-eind"].value = app_eind.toISOString().slice(0,16);
            // Update hidden field with id
            form_inputs["id"].value = app_id;
            // Update the p tag with the person
            // the right p tag is the third child of the form
            let achternaam = list_of_appointments[i].achternaam
            if (achternaam != null)
            {
                let c_achternaam = achternaam.charAt(0).toUpperCase() + achternaam.slice(1);
                form.children[2].innerText = (list_of_appointments[i].voorletter.toUpperCase() + " " + c_achternaam + " (id: " + String(list_of_appointments[i].adres_id) + ")");
            }
            else
            {
                form.children[2].innerText = ""
            }
            // No need to finish the loop since the right id has already been found
            break;
        }
    }
    // Show the modal
    app_modal.style.display = "block";
}