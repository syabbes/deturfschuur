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
    let x;
    if (firstMonthDay === 0)
    {
        x = 6;
    }
    else
    {
        x = firstMonthDay - (firstMonthDay - 1);
    }
    let firstDay = new Date(year, month, 1);
    firstDay.setDate(firstDay.getDate() - x);
    console.log(firstDay);

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
    console.log("length = " + calendar_dates.length);
    console.log(calendar_dates[0] + '-' + calendar_dates[41]);
    
    // loop over every table cell
    let calendar_table = document.getElementById("calendar-body");
    // itterator for the array
    let itterator = 0;
    console.log(calendar_table.rows.length);
    for (let i = 0; i < calendar_table.rows.length; i++)
    {
        let row = calendar_table.rows[i];
        for (let j = 0; j < row.cells.length; j++)
        {
            console.log(row.cells.length);
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
            else if (calendar_dates[itterator].getMonth() !== month)
            {
                row.cells[j].classList.add("deactivated");
            }
            // move itterator to next date
            itterator++;
        }
    }
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