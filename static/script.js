function logout()
{
    // do nothing yet
    alert("Doet nog niks");
}

function generate_calendar(year, month)
{
    // first day of the month
    let firstMonthDay = new Date(year, month, 1).getDay();
    // get the monday before the month
    // get the number of days to substract to get to monday
    x = firstMonthDay - (firstMonthDay - 1);
    firstDay = new Date(year, month, 1);
    firstDay.setDate(firstDay.getDate() - x);
    console.log(firstDay);
}

function load_calendar()
{
    if (document.getElementById("calendar-container"))
    {
        console.log("loading calendar...")
        // get current month and year
        let date = new Date();
        let month = date.getMonth();
        let year = date.getFullYear();
        // call other function to generate the calendar
        generate_calendar(year, month);

        console.log(month + "-" + year);
    }
}

console.log("test");
document.addEventListener("DOMContentLoaded", load_calendar);