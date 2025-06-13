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
    get_appointments(year, month);
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
function get_appointments(y, m)
{
    $.ajax({
        url: 'app_month',
        type: 'POST',
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