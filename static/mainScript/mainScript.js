function getTime() {

    try {
        let currentTime = new Date(), // for now
            hours = currentTime.getHours(),
            minutes = currentTime.getMinutes();

        if (minutes < 10) {
            minutes = "0" + minutes;
        }

        let suffix = "AM";
        if (hours >= 12) {
            suffix = "PM";
            hours = hours - 12;
        }
        if (hours == 0) {
            hours = 12;
        }

        return hours + ":" + minutes + ":" + suffix;
    } catch (err) {
        console.log("Error occurred while executing getTime().\t" + err);
    }

}

function getDate() {

    try {
        let date = new Date(),
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

        return days[date.getDay()] + ' ' + months[date.getMonth()] + ' ' + date.getDate() + ' ' + date.getFullYear();
    } catch (err) {
        console.log("Error occurred while executing getDate().\t" + err);
    }

}


